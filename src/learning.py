"""Self-healing corrections layer — logs drafts, detects edits, retrieves relevant patterns."""

import difflib
import sqlite3
import time
from pathlib import Path
from typing import Optional

from src.gmail_client import get_message, list_sent_messages, add_label, remove_label

_ROOT = Path(__file__).parent.parent
DB_PATH = _ROOT / "data" / "corrections.db"


# ---------------------------------------------------------------------------
# DB bootstrap
# ---------------------------------------------------------------------------

def _get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    _bootstrap(conn)
    return conn


def _bootstrap(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS drafts (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id    TEXT NOT NULL,
            thread_id     TEXT NOT NULL,
            category      TEXT NOT NULL,
            priority      TEXT NOT NULL,
            generated_body TEXT NOT NULL,
            logged_at     REAL NOT NULL,
            checked       INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS corrections (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            draft_id      INTEGER REFERENCES drafts(id),
            category      TEXT NOT NULL,
            generated_body TEXT NOT NULL,
            sent_body     TEXT NOT NULL,
            diff_summary  TEXT NOT NULL,
            keywords      TEXT NOT NULL,
            created_at    REAL NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_drafts_thread ON drafts(thread_id);
        CREATE INDEX IF NOT EXISTS idx_corrections_category ON corrections(category);
    """)
    conn.commit()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def log_draft(
    message_id: str,
    thread_id: str,
    category: str,
    priority: str,
    generated_body: str,
) -> int:
    """Persist a generated draft. Returns the new draft row ID."""
    with _get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO drafts (message_id, thread_id, category, priority, generated_body, logged_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (message_id, thread_id, category, priority, generated_body, time.time()),
        )
        return cur.lastrowid


def check_for_sent_edits() -> list[dict]:
    """
    Compare unchecked logged drafts against Gmail Sent.
    If Sean edited the draft before sending, store a correction.
    Returns list of new correction dicts.
    """
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM drafts WHERE checked = 0 ORDER BY logged_at DESC LIMIT 50"
    ).fetchall()
    if not rows:
        conn.close()
        return []

    # Build thread_id → draft mapping
    thread_map = {r["thread_id"]: dict(r) for r in rows}

    # Fetch recent sent messages (metadata only, then full body on match)
    sent = list_sent_messages(max_results=100)
    new_corrections = []

    for sent_meta in sent:
        msg = get_message(sent_meta["id"])
        if "error" in msg:
            continue
        thread_id = msg.get("thread_id", "")
        if thread_id not in thread_map:
            continue

        draft = thread_map[thread_id]
        sent_body = (msg.get("body") or msg.get("snippet", "")).strip()
        generated_body = draft["generated_body"].strip()

        # Mark checked regardless of whether they match
        conn.execute("UPDATE drafts SET checked = 1 WHERE id = ?", (draft["id"],))
        conn.commit()

        # Re-label: move from action/xxx to done/xxx on the original email
        _move_to_done(draft["message_id"], draft["category"])

        if _bodies_match(generated_body, sent_body):
            continue  # Sean sent as-is — no correction needed

        diff_summary = _summarise_diff(generated_body, sent_body)
        keywords = _extract_keywords(generated_body + " " + sent_body)

        conn.execute(
            """INSERT INTO corrections
               (draft_id, category, generated_body, sent_body, diff_summary, keywords, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                draft["id"],
                draft["category"],
                generated_body,
                sent_body,
                diff_summary,
                keywords,
                time.time(),
            ),
        )
        conn.commit()
        new_corrections.append({
            "category": draft["category"],
            "diff_summary": diff_summary,
            "generated_body": generated_body,
            "sent_body": sent_body,
        })

    conn.close()
    return new_corrections


def retrieve_relevant_corrections(message_text: str, category: str, k: int = 3) -> list[dict]:
    """
    Return up to k corrections for this category ranked by keyword overlap with message_text.
    """
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM corrections WHERE category = ? ORDER BY created_at DESC LIMIT 100",
        (category,),
    ).fetchall()
    conn.close()

    if not rows:
        return []

    msg_words = set(_tokenise(message_text))
    scored = []
    for r in rows:
        kw_words = set(r["keywords"].split())
        overlap = len(msg_words & kw_words)
        scored.append((overlap, dict(r)))

    scored.sort(key=lambda x: -x[0])
    return [item for _, item in scored[:k]]


def get_all_corrections() -> list[dict]:
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM corrections ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def seed_manual_correction(category: str, before: str, after: str, summary: str) -> int:
    """Manually seed a correction (for demo / pre-training)."""
    if category not in ("pilates", "norton_and_quay", "personal"):
        raise ValueError(f"Unknown category: {category}")
    keywords = _extract_keywords(before + " " + after)
    with _get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO corrections
               (draft_id, category, generated_body, sent_body, diff_summary, keywords, created_at)
               VALUES (NULL, ?, ?, ?, ?, ?, ?)""",
            (category, before, after, summary, keywords, time.time()),
        )
        return cur.lastrowid


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _bodies_match(a: str, b: str) -> bool:
    """True if sent body is close enough to generated that no edit happened."""
    if not a or not b:
        return False
    ratio = difflib.SequenceMatcher(None, a, b).ratio()
    return ratio > 0.92


def _summarise_diff(before: str, after: str) -> str:
    """One-line English summary of the key change."""
    before_lines = before.splitlines()
    after_lines = after.splitlines()
    diff = list(difflib.unified_diff(before_lines, after_lines, lineterm="", n=0))

    removed = [l[1:].strip() for l in diff if l.startswith("-") and not l.startswith("---")]
    added = [l[1:].strip() for l in diff if l.startswith("+") and not l.startswith("+++")]

    removed_str = "; ".join(removed[:3])[:120]
    added_str = "; ".join(added[:3])[:120]

    if removed_str and added_str:
        return f'Replaced "{removed_str}" → "{added_str}"'
    elif added_str:
        return f'Added: "{added_str}"'
    elif removed_str:
        return f'Removed: "{removed_str}"'
    else:
        return "Minor formatting change"


def _tokenise(text: str) -> list[str]:
    import re
    words = re.findall(r"[a-zA-Z]{3,}", text.lower())
    stopwords = {
        "the", "and", "for", "are", "this", "that", "with", "have",
        "from", "your", "our", "will", "just", "been", "was", "not",
        "you", "they", "but", "its", "can", "all", "has", "more",
    }
    return [w for w in words if w not in stopwords]


ACTION_LABELS = {
    "pilates": "action/pilates",
    "norton_and_quay": "action/nq",
    "personal": "action/personal",
}
DONE_LABELS = {
    "pilates": "done/pilates",
    "norton_and_quay": "done/nq",
    "personal": "done/personal",
}


def _move_to_done(message_id: str, category: str) -> None:
    """Remove action/xxx label and add done/xxx on the original email."""
    try:
        action_lbl = ACTION_LABELS.get(category)
        done_lbl = DONE_LABELS.get(category)
        if action_lbl and done_lbl:
            remove_label(message_id, action_lbl)
            add_label(message_id, done_lbl)
    except Exception:
        pass


def _extract_keywords(text: str) -> str:
    words = _tokenise(text)
    # Deduplicate while preserving rough order
    seen: set = set()
    unique = []
    for w in words:
        if w not in seen:
            seen.add(w)
            unique.append(w)
    return " ".join(unique[:60])

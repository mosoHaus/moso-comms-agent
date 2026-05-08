"""Safety guardrails: sender allowlist, content blocklist, decisions log."""

import json
import re
import time
from pathlib import Path

from src.gmail_client import list_sent_messages

_ROOT = Path(__file__).parent.parent
ALLOWLIST_PATH = _ROOT / "data" / "sender_allowlist.json"
DECISIONS_LOG = _ROOT / "data" / "decisions.jsonl"
KILL_SWITCH = _ROOT / "data" / "KILL_SWITCH"

# Hard-coded content patterns that should NEVER be auto-archived
SAFE_PATTERNS = [
    r"\binvoice\b",
    r"\bpayment\b",
    r"\brefund\b",
    r"\bcontract\b",
    r"\bagreement\b",
    r"\blegal\b",
    r"\burgent\b",
    r"\bpassword\b",
    r"\bverif",
    r"\bsecurity alert\b",
    r"\byour account\b",
    r"\baction required\b",
]

_SAFE_RE = re.compile("|".join(SAFE_PATTERNS), re.IGNORECASE)


def is_kill_switch_active() -> bool:
    return KILL_SWITCH.exists()


def build_sender_allowlist() -> int:
    """Scan sent mail, extract domains, persist to data/sender_allowlist.json. Returns domain count."""
    sent = list_sent_messages(max_results=300)
    domains: set = set()
    for msg in sent:
        to_addr = msg.get("to", "")
        for part in to_addr.split(","):
            part = part.strip()
            email = _extract_email(part)
            if "@" in email:
                domain = email.split("@", 1)[1].lower()
                if domain:
                    domains.add(domain)

    existing: set = set()
    if ALLOWLIST_PATH.exists():
        try:
            existing = set(json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8")))
        except Exception:
            pass

    merged = sorted(existing | domains)
    ALLOWLIST_PATH.write_text(json.dumps(merged, indent=2), encoding="utf-8")
    return len(merged)


def _load_allowlist() -> set:
    if not ALLOWLIST_PATH.exists():
        return set()
    try:
        return set(json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8")))
    except Exception:
        return set()


def check_safe_to_archive(message: dict) -> tuple[bool, str]:
    """
    Returns (is_safe, reason).
    If is_safe is False, the message should NOT be archived.
    """
    if is_kill_switch_active():
        return False, "Kill switch active — no archiving"

    sender = message.get("from", "")
    subject = message.get("subject", "")
    snippet = message.get("snippet", "")
    body = message.get("body", "") or snippet

    # Blocklist check on content
    combined = f"{subject} {snippet} {body}"
    if _SAFE_RE.search(combined):
        return False, f"Content matches safety pattern in subject/body"

    # Allowlist check — if sender domain is in allowlist, don't auto-archive
    sender_email = _extract_email(sender)
    if "@" in sender_email:
        domain = sender_email.split("@", 1)[1].lower()
        allowlist = _load_allowlist()
        if domain in allowlist:
            return False, f"Sender domain {domain!r} is in sent-mail allowlist"

    return True, "OK"


def log_decision(
    message_id: str,
    subject: str,
    sender: str,
    category: str,
    priority: str,
    action: str,
    rationale: str,
) -> None:
    """Append one decision record to decisions.jsonl."""
    DECISIONS_LOG.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": time.time(),
        "message_id": message_id,
        "subject": subject,
        "sender": sender,
        "category": category,
        "priority": priority,
        "action": action,
        "rationale": rationale,
    }
    with DECISIONS_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def _extract_email(from_str: str) -> str:
    if "<" in from_str and ">" in from_str:
        return from_str[from_str.index("<") + 1 : from_str.index(">")]
    return from_str.strip()

"""Core triage agent — classifies and acts on unread emails using Claude tool use."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root — works regardless of working directory
_PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(_PROJECT_ROOT / ".env")

import anthropic
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from src.gmail_client import list_recent_messages
from src.tools import TOOLS, handle_tool, reset_archive_count
from src.learning import log_draft, retrieve_relevant_corrections

MODEL = "claude-sonnet-4-6"
_PROJECT_ROOT = Path(__file__).parent.parent
VOICE_PROFILE_PATH = _PROJECT_ROOT / "data" / "voice_profile.md"
SENT_SAMPLES_PATH = _PROJECT_ROOT / "data" / "sent_samples.md"

CATEGORY_COLORS = {
    "pilates": "green",
    "norton_and_quay": "blue",
    "personal": "yellow",
    "marketing": "dim",
    "calendar": "cyan",
    "escalate": "red",
}

VOICE_REGISTERS = {
    "pilates": (
        "Warm, casual, peer-to-peer. Like texting a friend who does Pilates with you. "
        "Use :) smileys. Short sentences. Relaxed energy."
    ),
    "norton_and_quay": (
        "Professional but not stiff. Bizdev tone. Friendly and direct. "
        "Lead with something personal, then get to the point. Clear call to action."
    ),
    "personal": (
        "Most casual. Full Sean voice. Genuine and warm. "
        "Ask about them. End with an open invitation."
    ),
}


def _load_file(path: Path, label: str) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def _parse_sent_samples(content: str) -> dict:
    """Extract per-register samples from sent_samples.md."""
    sections = {}
    current = None
    lines = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("## Pilates samples"):
            if current and lines:
                sections[current] = "\n".join(lines).strip()
            current = "pilates"
            lines = []
        elif stripped.startswith("## Norton & Quay samples"):
            if current and lines:
                sections[current] = "\n".join(lines).strip()
            current = "norton_and_quay"
            lines = []
        elif stripped.startswith("## Personal samples"):
            if current and lines:
                sections[current] = "\n".join(lines).strip()
            current = "personal"
            lines = []
        elif current is not None:
            lines.append(line)
    if current and lines:
        sections[current] = "\n".join(lines).strip()
    return sections


def _build_system_prompt(voice_profile: str, samples: dict, corrections: dict) -> str:
    # Pull the Quick Reference Card section from voice profile if present
    qr_section = ""
    if "QUICK REFERENCE CARD" in voice_profile:
        start = voice_profile.index("QUICK REFERENCE CARD")
        qr_section = voice_profile[start:start + 3000]
    elif voice_profile:
        qr_section = voice_profile[:3000]

    parts = ["""You are an autonomous email triage agent for Sean Teh (sean@moso.haus).

## YOUR JOB
For each email: read it, classify it, then either draft a reply in Sean's voice or archive it.

## FIVE CATEGORIES

**PILATES** — moso.haus reformer Pilates students, class inquiries, instructor admin.
**NORTON_AND_QUAY** — accountants / their networks responding to Sean's outreach for Norton & Quay tax law firm. Bizdev contacts.
**PERSONAL** — friends, family, genuine contacts, startup/event world, services Sean uses. Anything real that isn't Pilates or N&Q.
**MARKETING** — newsletters, promos, platform notifications, AI updates, Substacks, automated emails, cold outreach with no personal connection. AUTO-ARCHIVE THESE.
**CALENDAR** — meeting invitations, event invites, calendar requests (Zoom/Meet links, .ics attachments, "let's catch up" scheduling emails, RSVP confirmations). Sean needs to accept/decline these himself — do NOT draft a reply UNLESS the email explicitly mentions a scheduling conflict or asks Sean to suggest alternative times, in which case draft a short conflict/reschedule email.
**ESCALATE** — genuinely ambiguous. No draft, just label.

## PRIORITY (for non-marketing)
- **HIGH** — direct reach-out, time-sensitive, specific question to Sean, reply expected within 24h
- **MEDIUM** — reply expected this week
- **LOW** — nice to reply, not urgent

## WORKFLOW (follow exactly)
1. Call `read_message(message_id)` to read the full email
2. Call `classify_and_act(...)` exactly once with your decision

## WHEN TO DRAFT vs NOT
Only include `draft_body` if a reply is genuinely expected. Skip it if the email is:
- A one-way notification or update (class schedule, booking confirmation, receipt)
- An FYI with no question or request directed at Sean
- A thread where Sean already replied last and no new question was asked
- An automated message that happens to be categorised as pilates/personal/nq
- Sean is CC'd (not in the To: field directly) — CC means FYI, not action required

If no reply is needed, omit `draft_body` entirely — the email will be labelled for awareness only.

## SEAN'S VOICE — HARD RULES
NEVER use: em dashes, "truly humbled", "I am privileged to", "the conversations we shared", "In today's fast-paced world", "incredibly", performative gratitude, AI-sounding openers.
ALWAYS: lead with warmth, use :) smileys in Pilates/Personal, sign off "Cheers, Sean" (professional) or "Cheerio" (casual).
Short punchy sentences. 2-3 sentence paragraphs. No walls of text.

"""]

    # Voice register examples per category
    if samples:
        parts.append("## VOICE SAMPLES (match these exactly)\n")
        for cat, sample in samples.items():
            if sample:
                label = cat.replace("_", " ").title()
                parts.append(f"### {label}:\n{sample}\n")

    # Quick reference card
    if qr_section:
        parts.append(f"\n## SEAN'S VOICE QUICK REFERENCE\n{qr_section}\n")

    # Learned corrections
    if corrections:
        parts.append("\n## LEARNED CORRECTIONS (apply these patterns to matching category)\n")
        for cat, items in corrections.items():
            if items:
                parts.append(f"\n### {cat}:\n")
                for c in items[:3]:
                    parts.append(f"- {c.get('diff_summary', '')}\n")
                    before = c.get("generated_body", "")
                    after = c.get("sent_body", "")
                    if before and after:
                        parts.append(f"  Before: {before[:150]}\n  After: {after[:150]}\n")

    return "".join(parts)


def run_once(console: Console):
    demo_mode = os.environ.get("AGENT_DEMO_MODE") == "true"
    reset_archive_count()

    # Auto-learn: detect any drafts Sean edited before sending
    try:
        from src.learning import check_for_sent_edits
        new_corrections = check_for_sent_edits()
        if new_corrections:
            console.print(f"[cyan]Learned {len(new_corrections)} new correction(s) from your edits:[/cyan]")
            for c in new_corrections:
                console.print(f"  [dim]{c['category']}:[/dim] {c['diff_summary']}")
            console.print()
    except Exception:
        pass

    # Stale nudge: warn about action/ emails with no reply after 24h
    try:
        import sqlite3, time as _time
        from pathlib import Path as _Path
        _db = _Path(__file__).parent.parent / "data" / "corrections.db"
        if _db.exists():
            _conn = sqlite3.connect(str(_db))
            _cutoff = _time.time() - 86400
            _stale = _conn.execute(
                "SELECT category, message_id FROM drafts WHERE checked=0 AND logged_at < ?",
                (_cutoff,)
            ).fetchall()
            _conn.close()
            if _stale:
                console.print(f"[yellow bold]Stale drafts ({len(_stale)}) — no reply detected after 24h:[/yellow bold]")
                for _cat, _mid in _stale:
                    console.print(f"  [yellow]· {_cat}[/yellow] message_id={_mid[:16]}…")
                console.print()
    except Exception:
        pass

    client = anthropic.Anthropic()

    voice_profile = _load_file(VOICE_PROFILE_PATH, "voice_profile")
    samples_raw = _load_file(SENT_SAMPLES_PATH, "sent_samples")
    samples = _parse_sent_samples(samples_raw)

    if not voice_profile:
        console.print("[yellow]Warning: data/voice_profile.md not found. Using generic voice.[/yellow]")
    if not samples:
        console.print("[yellow]Warning: data/sent_samples.md not found. Drafts may not match your voice.[/yellow]")

    with console.status("[bold green]Fetching unread messages..."):
        messages = list_recent_messages(
            query="in:inbox -label:moso/processed newer_than:1d",
            max_results=20,
        )

    if not messages:
        console.print("[dim]No unread messages to process.[/dim]")
        return

    console.print(f"\n[bold]Processing {len(messages)} message(s)...[/bold]\n")

    summary: dict = {
        "pilates": 0, "norton_and_quay": 0, "personal": 0,
        "marketing": 0, "calendar": 0, "escalate": 0, "error": 0,
    }

    for i, msg in enumerate(messages, 1):
        msg_id = msg["id"]
        subject = msg.get("subject", "(no subject)")
        sender = msg.get("from", "")
        snippet = msg.get("snippet", "")

        safe_subject = subject[:60].encode("ascii", errors="replace").decode("ascii")
        safe_sender = sender[:40].encode("ascii", errors="replace").decode("ascii")
        console.print(f"[dim][{i}/{len(messages)}][/dim] [bold]{safe_subject}[/bold] [dim]— {safe_sender}[/dim]")

        try:
            # Load relevant corrections for this message
            corrections_by_cat: dict = {}
            for cat in ["pilates", "norton_and_quay", "personal"]:
                items = retrieve_relevant_corrections(snippet, cat, k=2)
                if items:
                    corrections_by_cat[cat] = items

            if corrections_by_cat and demo_mode:
                for cat, items in corrections_by_cat.items():
                    console.print(f"  [cyan]Applying {len(items)} correction(s) from past {cat} edits[/cyan]")
                    for c in items:
                        console.print(f"    [dim]{c.get('diff_summary', '')}[/dim]")

            system_prompt = _build_system_prompt(voice_profile, samples, corrections_by_cat)

            user_content = (
                f"Process this email.\n"
                f"message_id: {msg_id}\n"
                f"From: {sender}\n"
                f"Subject: {subject}\n"
                f"Snippet: {snippet}\n\n"
                f"Call read_message first, then classify_and_act."
            )

            history = [{"role": "user", "content": user_content}]
            category = None
            priority = None
            draft_body = None
            rationale = ""
            final_text = ""

            # Tool-use loop
            while True:
                response = client.messages.create(
                    model=MODEL,
                    max_tokens=2048,
                    system=system_prompt,
                    tools=TOOLS,
                    messages=history,
                )

                tool_uses = [b for b in response.content if b.type == "tool_use"]
                text_blocks = [b for b in response.content if b.type == "text"]

                if text_blocks:
                    final_text = text_blocks[-1].text

                if not tool_uses or response.stop_reason == "end_turn":
                    break

                tool_results = []
                for tu in tool_uses:
                    if demo_mode:
                        safe_input = {k: v for k, v in tu.input.items() if k != "draft_body"}
                        console.print(f"  [dim]→ {tu.name}({safe_input})[/dim]")

                    result = handle_tool(tu.name, tu.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tu.id,
                        "content": result,
                    })

                    if tu.name == "classify_and_act":
                        category = tu.input.get("category")
                        priority = tu.input.get("priority")
                        draft_body = tu.input.get("draft_body")
                        rationale = tu.input.get("rationale", "")

                history.append({"role": "assistant", "content": response.content})
                history.append({"role": "user", "content": tool_results})

            # Log draft for self-healing
            if category and category not in ("marketing", "escalate") and draft_body:
                try:
                    log_draft(
                        message_id=msg_id,
                        thread_id=msg.get("thread_id", ""),
                        category=category,
                        priority=priority or "low",
                        generated_body=draft_body,
                    )
                except Exception:
                    pass

            # Display result
            color = CATEGORY_COLORS.get(category, "white")
            if category == "marketing":
                action_str = "labelled: marketing"
            elif category == "escalate":
                action_str = "labelled: review"
            elif category == "calendar":
                action_str = "labelled: calendar/conflict — draft created" if draft_body else "labelled: calendar (accept/decline)"
            elif draft_body:
                action_str = f"draft created — {(priority or '').lower()} → action/{category.replace('norton_and_quay', 'nq')}"
            else:
                action_str = f"no reply needed → {category.replace('norton_and_quay', 'nq')}"

            panel_text = f"[bold {color}]{(category or 'unknown').upper()}[/bold {color}]  {action_str}"
            if rationale:
                panel_text += f"\n[dim]{rationale}[/dim]"

            console.print(Panel(panel_text, expand=False))
            console.print()

            if category:
                summary[category] = summary.get(category, 0) + 1

        except Exception as e:
            console.print(f"  [red]Error processing message: {e}[/red]")
            if demo_mode:
                import traceback
                console.print(f"  [dim]{traceback.format_exc()}[/dim]")
            summary["error"] += 1

    # Summary table
    table = Table(title="Run complete", box=box.SIMPLE, header_style="bold magenta")
    table.add_column("Category")
    table.add_column("Count", justify="right")
    for cat, count in summary.items():
        if count > 0:
            color = CATEGORY_COLORS.get(cat, "white")
            table.add_row(f"[{color}]{cat}[/{color}]", str(count))
    console.print(table)

"""Tool definitions and server-side logic for the triage agent."""

import os
from typing import Optional

from src.gmail_client import (
    get_message as gmail_get_message,
    get_thread_messages,
    create_draft,
    add_label,
    remove_label,
    archive_message,
    star_message,
)
from src.safety import check_safe_to_archive, is_kill_switch_active, log_decision

ARCHIVE_ENABLED = os.environ.get("AGENT_ARCHIVE_ENABLED", "true").lower() != "false"
_archive_count = 0
ARCHIVE_CAP = 30

# Label scheme — clean, no AGENT/ prefix
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
PROCESSED_LABEL = "moso/processed"

TOOLS = [
    {
        "name": "read_message",
        "description": (
            "Read the full body of a Gmail message. "
            "Always call this first to understand the email before classifying."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "message_id": {
                    "type": "string",
                    "description": "The Gmail message ID",
                }
            },
            "required": ["message_id"],
        },
    },
    {
        "name": "classify_and_act",
        "description": (
            "Classify the email and take the appropriate action. "
            "For marketing: labels (stays in inbox). "
            "For pilates/norton_and_quay/personal: creates a draft reply and labels. "
            "For escalate: labels only, no draft."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "message_id": {
                    "type": "string",
                    "description": "The Gmail message ID",
                },
                "category": {
                    "type": "string",
                    "enum": ["pilates", "norton_and_quay", "personal", "marketing", "escalate"],
                    "description": "Email category",
                },
                "priority": {
                    "type": "string",
                    "enum": ["high", "medium", "low", "none"],
                    "description": "Priority. Use 'none' only for marketing or escalate.",
                },
                "rationale": {
                    "type": "string",
                    "description": "1-2 sentences explaining the classification decision.",
                },
                "draft_body": {
                    "type": "string",
                    "description": (
                        "Reply body to draft. Required for pilates, norton_and_quay, personal. "
                        "Omit for marketing and escalate."
                    ),
                },
            },
            "required": ["message_id", "category", "priority", "rationale"],
        },
    },
]


def reset_archive_count():
    global _archive_count
    _archive_count = 0


def handle_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "read_message":
        return _read_message(**tool_input)
    elif tool_name == "classify_and_act":
        return _classify_and_act(**tool_input)
    return f"Unknown tool: {tool_name}"


def _read_message(message_id: str) -> str:
    msg = gmail_get_message(message_id)
    if "error" in msg:
        return f"Error reading message: {msg['error']}"

    thread_id = msg.get("thread_id", "")
    thread_msgs = get_thread_messages(thread_id) if thread_id else []

    # Build thread context (all messages except the last, which is shown as THIS EMAIL)
    if len(thread_msgs) > 1:
        history_parts = [f"=== THREAD HISTORY ({len(thread_msgs)} messages) ===\n"]
        for i, m in enumerate(thread_msgs[:-1], 1):
            sender = m["from"][:50]
            date = m["date"][:10] if m["date"] else ""
            body_preview = (m["body"] or m["snippet"] or "")[:800].strip()
            history_parts.append(f"[{i}] From: {sender} | {date}\n{body_preview}\n")
        history_parts.append("=== THIS EMAIL ===")
        thread_context = "\n".join(history_parts) + "\n"
    else:
        thread_context = ""

    return (
        f"{thread_context}"
        f"From: {msg['from']}\n"
        f"To: {msg['to']}\n"
        f"Subject: {msg['subject']}\n"
        f"Date: {msg['date']}\n"
        f"---\n"
        f"{msg['body'] or msg['snippet']}"
    )


def _classify_and_act(
    message_id: str,
    category: str,
    priority: str,
    rationale: str,
    draft_body: Optional[str] = None,
) -> str:
    global _archive_count
    results = []

    if is_kill_switch_active():
        return "KILL SWITCH ACTIVE — no actions taken. Delete data/KILL_SWITCH to resume."

    try:
        msg = gmail_get_message(message_id)
        thread_id = msg.get("thread_id")
        sender = msg.get("from", "")
        subject = msg.get("subject", "")

        action = "unknown"

        if category == "marketing":
            safe, reason = check_safe_to_archive(msg)
            if not safe:
                add_label(message_id, "review")
                add_label(message_id, PROCESSED_LABEL)
                action = "escalated_by_safety"
                log_decision(message_id, subject, sender, category, priority, action,
                             f"Safety override: {reason}")
                return f"Safety check blocked marketing classification: {reason} | Escalated instead."

            add_label(message_id, "marketing")
            action = "labelled_marketing"
            results.append("Labelled: marketing")

        elif category == "escalate":
            add_label(message_id, "review")
            action = "escalated"
            results.append("Labelled: review")

        else:
            if draft_body:
                # Reply warranted — create draft and put in action/
                if priority == "none":
                    priority = "low"

                to_addr = _extract_email(sender)
                draft_subject = subject if subject.lower().startswith("re:") else f"Re: {subject}"

                draft_id = create_draft(
                    to=to_addr,
                    subject=draft_subject,
                    body=draft_body,
                    thread_id=thread_id,
                )
                results.append(f"Draft created (ID: {draft_id})")

                action_label = ACTION_LABELS.get(category, f"action/{category}")
                add_label(message_id, action_label)
                results.append(f"Labelled: {action_label}")

                if priority == "high":
                    star_message(message_id)
                    results.append("Starred (high priority)")

                action = "draft_created"
            else:
                # No reply needed — label for awareness only, no action/ prefix
                info_label = category.replace("norton_and_quay", "nq")
                add_label(message_id, info_label)
                results.append(f"Labelled: {info_label} (no reply needed)")
                action = "categorised_no_reply"

        add_label(message_id, PROCESSED_LABEL)
        results.append(f"Labelled: {PROCESSED_LABEL}")

        log_decision(message_id, subject, sender, category, priority, action, rationale)

        return " | ".join(results) + f"\nRationale: {rationale}"

    except Exception as e:
        return f"Error in classify_and_act: {e}"


def _extract_email(from_str: str) -> str:
    if "<" in from_str and ">" in from_str:
        return from_str[from_str.index("<") + 1 : from_str.index(">")]
    return from_str.strip()

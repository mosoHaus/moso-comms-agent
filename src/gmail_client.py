"""Gmail API client with OAuth 2.0 (gmail.modify scope)."""

import base64
import os
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")
from email.mime.text import MIMEText
from email.utils import parsedate_to_datetime
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
_ROOT = Path(__file__).parent.parent
CREDENTIALS_FILE = str(_ROOT / "credentials.json")
TOKEN_FILE = str(_ROOT / "token.json")

_service = None


def get_credentials() -> Credentials:
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"credentials.json not found in project root.\n"
                    "Download OAuth Desktop credentials from Google Cloud Console\n"
                    "and save as credentials.json."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return creds


def get_service():
    global _service
    if _service is None:
        _service = build("gmail", "v1", credentials=get_credentials())
    return _service


def list_recent_messages(query: str = "is:unread", max_results: int = 10) -> list[dict]:
    """Return list of message dicts: {id, from, subject, snippet, body, date, thread_id}."""
    service = get_service()
    result = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results,
    ).execute()
    messages = result.get("messages", [])
    return [_get_message_detail(service, m["id"]) for m in messages if m]


def get_message(message_id: str) -> dict:
    """Return full message dict for a single message ID."""
    return _get_message_detail(get_service(), message_id)


def _get_message_detail(service, message_id: str) -> dict:
    try:
        msg = service.users().messages().get(
            userId="me",
            id=message_id,
            format="full",
        ).execute()
    except HttpError as e:
        return {"id": message_id, "error": str(e)}

    headers = {h["name"].lower(): h["value"] for h in msg.get("payload", {}).get("headers", [])}

    date = None
    date_str = headers.get("date", "")
    if date_str:
        try:
            date = parsedate_to_datetime(date_str).isoformat()
        except Exception:
            date = date_str

    body = _extract_body(msg.get("payload", {}))

    return {
        "id": message_id,
        "thread_id": msg.get("threadId", ""),
        "from": headers.get("from", ""),
        "to": headers.get("to", ""),
        "subject": headers.get("subject", "(no subject)"),
        "date": date or "",
        "snippet": msg.get("snippet", ""),
        "body": body[:4000] if body else msg.get("snippet", ""),
        "label_ids": msg.get("labelIds", []),
    }


def _extract_body(payload: dict) -> str:
    if payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="ignore")
    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain":
            if part.get("body", {}).get("data"):
                return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
        nested = _extract_body(part)
        if nested:
            return nested
    return ""


def create_draft(to: str, subject: str, body: str, thread_id: Optional[str] = None) -> str:
    """Create a Gmail draft. Returns the draft ID."""
    service = get_service()
    mime = MIMEText(body, "plain", "utf-8")
    mime["to"] = to
    mime["subject"] = subject
    raw = base64.urlsafe_b64encode(mime.as_bytes()).decode()

    draft_body: dict = {"message": {"raw": raw}}
    if thread_id:
        draft_body["message"]["threadId"] = thread_id

    draft = service.users().drafts().create(userId="me", body=draft_body).execute()
    return draft["id"]


def _get_or_create_label(service, label_name: str) -> str:
    """Return label ID, creating the label if it doesn't exist."""
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    for lbl in labels:
        if lbl["name"] == label_name:
            return lbl["id"]

    new_label = service.users().labels().create(
        userId="me",
        body={
            "name": label_name,
            "labelListVisibility": "labelShow",
            "messageListVisibility": "show",
        },
    ).execute()
    return new_label["id"]


def add_label(message_id: str, label_name: str) -> None:
    service = get_service()
    label_id = _get_or_create_label(service, label_name)
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"addLabelIds": [label_id]},
    ).execute()


def remove_label(message_id: str, label_name: str) -> None:
    service = get_service()
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    label_id = next((l["id"] for l in labels if l["name"] == label_name), None)
    if label_id:
        service.users().messages().modify(
            userId="me",
            id=message_id,
            body={"removeLabelIds": [label_id]},
        ).execute()


def archive_message(message_id: str) -> None:
    """Remove INBOX label, effectively archiving the message."""
    service = get_service()
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"removeLabelIds": ["INBOX"]},
    ).execute()


def get_thread_messages(thread_id: str, max_messages: int = 6) -> list[dict]:
    """Return all messages in a thread (oldest first, capped), each as a message dict."""
    service = get_service()
    try:
        thread = service.users().threads().get(
            userId="me", id=thread_id, format="full"
        ).execute()
    except HttpError as e:
        return []
    msgs = thread.get("messages", [])[-max_messages:]
    return [_get_message_detail_from_raw(m) for m in msgs]


def _get_message_detail_from_raw(msg: dict) -> dict:
    """Parse a raw Gmail message object (already fetched) into our standard dict."""
    headers = {h["name"].lower(): h["value"] for h in msg.get("payload", {}).get("headers", [])}
    date_str = headers.get("date", "")
    date = date_str
    if date_str:
        try:
            from email.utils import parsedate_to_datetime as _p
            date = _p(date_str).isoformat()
        except Exception:
            pass
    body = _extract_body(msg.get("payload", {}))
    return {
        "id": msg.get("id", ""),
        "thread_id": msg.get("threadId", ""),
        "from": headers.get("from", ""),
        "to": headers.get("to", ""),
        "subject": headers.get("subject", "(no subject)"),
        "date": date,
        "snippet": msg.get("snippet", ""),
        "body": body[:2000] if body else msg.get("snippet", ""),
        "label_ids": msg.get("labelIds", []),
    }


def star_message(message_id: str) -> None:
    """Add Gmail STARRED label to a message."""
    service = get_service()
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"addLabelIds": ["STARRED"]},
    ).execute()


def list_sent_messages(max_results: int = 200) -> list[dict]:
    """Return sent messages for allowlist building."""
    service = get_service()
    result = service.users().messages().list(
        userId="me",
        q="in:sent",
        maxResults=max_results,
    ).execute()
    messages = result.get("messages", [])
    out = []
    for m in messages:
        try:
            msg = service.users().messages().get(
                userId="me", id=m["id"], format="metadata",
                metadataHeaders=["To", "From"],
            ).execute()
            headers = {h["name"].lower(): h["value"] for h in msg.get("payload", {}).get("headers", [])}
            out.append({"id": m["id"], "to": headers.get("to", ""), "from": headers.get("from", "")})
        except HttpError:
            continue
    return out

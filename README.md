# moso comms agent

Autonomous Gmail triage and drafting agent for sean@moso.haus. Built for the [Hourglass AI Agent Challenge](https://challenge.thehourglass.ai/).

Polls Gmail every 3 minutes, reads each new email with full thread context, classifies it into one of four contexts (Pilates / Norton & Quay / Personal / Marketing), drafts a reply in the right voice register, and learns from every edit you make before sending.

---

## Architecture

```
Gmail inbox (polling every 3 min)
    │
    ▼
 auto-learn: diff sent mail vs logged drafts → corrections.db
 stale nudge: warn if action/ email unreplied after 24h
    │
    ▼
src/agent.py ──► Claude claude-sonnet-4-6 (tool use loop)
    │               ├── read_message()
    │               │       └── full thread history (up to 6 messages)
    │               └── classify_and_act()
    │                       ├── marketing  ──► label: marketing
    │                       ├── pilates    ──► draft + label: action/pilates [★ if HIGH]
    │                       ├── nq         ──► draft + label: action/nq      [★ if HIGH]
    │                       ├── personal   ──► draft + label: action/personal [★ if HIGH]
    │                       └── escalate   ──► label: review (no draft)
    │
    ▼
src/learning.py ── SQLite (data/corrections.db)
    ├── log_draft()              — record every generated draft
    ├── check_for_sent_edits()  — diff agent draft vs what you actually sent
    │       └── on match: move action/xxx → done/xxx automatically
    └── retrieve_relevant_corrections() — keyword search, injected into system prompt

src/safety.py
    ├── sender allowlist  — domains from your sent mail, never auto-archived
    ├── content blocklist — invoice/payment/contract/legal blocks marketing label
    ├── decisions.jsonl   — every action logged with rationale
    └── KILL_SWITCH file  — drop data/KILL_SWITCH to freeze all agent actions
```

---

## Gmail label scheme

```
action/
  nq          ← draft waiting, needs review & send   ★ starred if HIGH
  personal    ←
  pilates     ←
done/
  nq          ← replied and sent (moved here automatically)
  personal    ←
  pilates     ←
marketing     ← stays in inbox for your review
moso/
  processed   ← internal tracking
review        ← escalated, needs your judgement
```

---

## The four categories

| Category | What lives here | Voice |
|---|---|---|
| **Pilates** | moso.haus students, class inquiries, instructor admin | Warm, casual, peer-to-peer. Smileys :) |
| **Norton & Quay** | Accountants responding to Sean's bizdev outreach | Professional but direct. Lead personal, clear CTA. |
| **Personal** | Friends, family, startup world, services | Most casual. Full Sean voice. Ask about them. |
| **Marketing** | Newsletters, promos, platform notifications, cold outreach | Labelled only. No draft. |

## Priority rubric

- **High** — direct reach-out, time-sensitive, named question, reply expected within 24h → auto-starred
- **Medium** — reply expected this week
- **Low** — nice to reply, not urgent

---

## Self-healing loop

1. Agent drafts a reply → logged to `corrections.db`
2. You edit the draft in Gmail → send it
3. Next agent cycle (3 min later) detects the diff → logs correction
4. Original email moves from `action/xxx` → `done/xxx` automatically
5. Next batch of emails gets the correction injected into the system prompt as a few-shot example

You never run anything manually — the loop is fully automatic.

---

## Safety guardrails

Before labelling any email as marketing:
1. **Sender allowlist** — if the sender's domain appears in emails you've previously sent, blocked (likely a real contact)
2. **Content blocklist** — invoice / payment / contract / legal / urgent patterns block marketing classification
3. **Kill switch** — `python -m src.main kill-switch on` freezes all agent actions instantly
4. **Audit log** — every decision logged to `data/decisions.jsonl` with rationale

---

## Setup

**Prerequisites:** Python 3.11+, a GCP project with Gmail API enabled.

### 1. Clone and install

```bash
git clone https://github.com/seanaayy/moso-comms-agent
cd moso-comms-agent
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux
pip install -e .
```

### 2. OAuth credentials

In Google Cloud Console:
- APIs & Services → OAuth consent screen → External → Testing
- Add scope: `https://www.googleapis.com/auth/gmail.modify`
- Add your email as a test user
- Credentials → Create Credentials → Desktop app → Download JSON → save as `credentials.json`

### 3. Environment

```bash
cp .env.example .env
# Add ANTHROPIC_API_KEY to .env
```

### 4. Voice profile and sent samples

```
data/voice_profile.md      — paste your voice/tone profile here
data/sent_samples.md       — paste real sent emails here, under three headers:
                             ## Pilates samples
                             ## Norton & Quay samples
                             ## Personal samples
```

Both files are gitignored.

### 5. Build sender allowlist

```bash
python -m src.main refresh-allowlist
```

---

## Usage

```bash
# Verify Gmail auth + list inbox
python -m src.main inspect

# Process inbox once then exit
python -m src.main run --once

# Poll every 3 minutes (leave running)
python -m src.main run --watch

# View all learned corrections
python -m src.main corrections

# Seed a manual correction for demo/testing
python -m src.main seed-correction --category pilates --before "..." --after "..." --summary "..."

# Rebuild sender allowlist
python -m src.main refresh-allowlist

# Kill switch
python -m src.main kill-switch on
python -m src.main kill-switch off
python -m src.main kill-switch status

# Verbose demo mode
python -m src.main demo
```

---

## Demo

<!-- Add 2-minute demo video link here -->

---

## Stack

- Python 3.11
- [anthropic](https://pypi.org/project/anthropic/) — Claude claude-sonnet-4-6 with tool use
- [google-api-python-client](https://pypi.org/project/google-api-python-client/) — Gmail API
- [rich](https://pypi.org/project/rich/) — terminal UI
- SQLite — correction store (`data/corrections.db`)
- `data/decisions.jsonl` — audit log

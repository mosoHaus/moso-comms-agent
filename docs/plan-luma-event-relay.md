# Plan: Luma Event Relay

*Volunteers submit events through a form; Claude validates and posts them to Luma. Sean reviews and publishes. Nobody but Sean ever touches the Luma account.*

Blueprint produced 2026-08-15 on branch `claude/luma-event-form-5ewjuo`. This is a plan, not an implementation — nothing has been built yet.

---

## Verdict from the interrogation

**The idea holds up, and a build (or a small spend) is genuinely required.** Three findings that settle it:

1. **Luma's permission model cannot solve this natively.** Event hosts are binary: a **Manager** gets full backend access — including ticket sales and revenue for the event — while a **Non-Manager host** is just displayed on the page with *no* backend access. The only other role is check-in staff (door scanning only). There is no "can edit content, can't see money" role, at event or calendar level. So "just give volunteers restricted access" is not an option; a relay layer between volunteers and Luma is the correct shape.

2. **Every official automation path is behind Luma Plus ($59/mo billed annually, $69 monthly).** The public API, webhooks, and Zapier all require Plus on the calendar. There is even an off-the-shelf **Luma MCP server for Claude Code** (`adelaidasofia/luma-mcp` — create/update events, ticket types, draft+confirm on every write) — but it authenticates with an official API key, so it needs Plus too.

3. **The no-pay path exists: browser automation.** Claude driving the Luma web app with Sean's logged-in session (Playwright + Chromium, both already available in the Claude environment). Workable and $0/mo, but it's the fragile part of the system — see Risks.

**The fork nobody asked about but matters most:** Luma Plus also drops the platform fee on paid tickets to **0%** (the free tier charges a platform fee on paid tickets — ~5% at last check; confirm the current rate on the Luma pricing page or your payment tab). At 5%, Plus breaks even at roughly **$1,180/month in gross ticket sales**. AsiaX Circle sells paid tickets at every event. If monthly ticket volume is near or above that line, Plus is free-to-negative cost **and** replaces the entire fragile automation layer with a supported API + a ready-made MCP server. Check the number before building Path A below.

---

## Problem

Volunteers organize events but can't post them to Luma, because any Luma access that allows editing also exposes revenue, payouts, and sales data. Sean is therefore the data-entry bottleneck for every event: title, description, times, location, ticket tiers, images, invites.

## Goal

A volunteer fills in one form and, within a day (later: within the hour), a correctly-built Luma event exists — private, awaiting Sean's ~30-second review-and-publish. Sean's role shrinks from "does all the data entry" to "approves." Volunteers never see anything financial beyond the public ticket prices they themselves set.

## Scope

**In scope (v1):**
- Intake form + submissions database (event title, description, date, start/end time, timezone, location, ticket tiers with prices/quantities/sales windows, capacity, cover image, collaborator names, submitter identity)
- Validation + "needs info" bounce-back to the submitter
- Automated creation of the event on Luma **with Private visibility** (link-only, not listed on the calendar)
- Write-back of the Luma URL + a screenshot to the submission row; notification to Sean for review
- Sean flips the event to Public manually (or tells Claude to)

**Out of scope (v1, explicitly):**
- Editing already-posted events via the form (phase 2)
- Guest-list email uploads / CSV invites (phase 2 — note free-tier weekly invite limits)
- Auto-publishing without Sean's review (phase 3, once trust is earned)
- Adding collaborators as event *Managers* (would expose financials to them — only Sean does that, by hand). Adding them as Non-Manager hosts is safe (no backend access) and can be automated.

## Architecture

```
Volunteer                     Claude                          Sean
   │                            │                              │
   ▼                            │                              │
Notion form (public link, ──►  Submissions DB (Notion)         │
no account needed,             Status: New                     │
file upload for cover art)      │                              │
                                ▼                              │
                        Validate submission                    │
                        (required fields, date sanity,         │
                         price sanity, tz)                     │
                          │           │                        │
                    incomplete      valid                      │
                          │           │                        │
                          ▼           ▼                        │
                   "Needs info"   Post to Luma ──────────►  Review private
                   notify         (Playwright OR Plus API)  event link,
                   submitter      visibility = PRIVATE      flip to Public
                                  write back URL+screenshot    │
                                  Status: Posted ──────────────┘
                                                     Status: Published
```

**Why Notion for the form:** Notion forms share via public link, respondents need no Notion account, and file-upload questions are supported (cover image). Submissions land in a database Claude already reaches through the Notion connector, alongside the existing AXC CRM. Google Forms → Sheet is the fallback (note: Google Forms requires respondents to sign in to Google when a file-upload question is present — a real point against it here).

**The poster — two interchangeable implementations:**

| | Path A: browser automation | Path B: Luma Plus API |
|---|---|---|
| Cost | $0/mo | $59/mo annual — offset by 0% platform fee |
| Mechanism | Playwright drives lu.ma with a stored session cookie | Official API; `luma-mcp` server is off-the-shelf |
| Robustness | Breaks when Luma changes its UI | Stable, supported, rate-limited (200 req/min) |
| Standing | Unofficial (own account, human-reviewed, low volume) | Fully sanctioned |

The form, database, validation, review gate, and notifications are **identical under both paths**. Build the relay so the poster is swappable: start on Path A if current ticket volume is well under break-even; flip to Path B the moment volume clears ~$1.2k/mo or Path A breaks twice in a month.

**Path A auth (the clever-but-fragile bit):** store Sean's Luma session cookie as an environment secret. When it expires, the agent self-heals: it starts an email-code login on lu.ma, reads the verification code from sean@moso.haus via the Gmail connector, completes login, and stores the fresh cookie. Sean does nothing. (This works precisely because Claude already has Gmail access — same account the code is sent to.)

**Where the poster runs — decision needed:**
- **Cloud (recommended):** a scheduled Claude routine checks the DB and posts. ⚠️ The current Claude cloud environment's network policy **blocks luma.com** — Sean must add `lu.ma` / `luma.com` / `api.luma.com` (plus any asset-upload domains discovered on first run) to the environment's domain allowlist first. No laptop dependency after that.
- **Local:** run it on the Windows machine that already runs `moso-comms-agent` on Task Scheduler, as a new module with a persistent logged-in Chromium profile (auth problem disappears entirely). Downside: posts only happen when that machine is on.

## Approach — build order

1. **(30 min, useful immediately)** Create the "Event Submissions" Notion database + public form. Fields: submission type (New event); title; description; date; start & end time; timezone (default to home city); location (+ "hide until registration" flag); up to three ticket tiers (name, price, quantity, sales start/end — covers early bird + GA + one more); total capacity; cover image upload; collaborators (names + emails, "will be listed as hosts"); submitter name + email; notes. Agent-managed fields: Status (New / Needs info / Posted / Published / Rejected), Luma URL, Agent log. Share the form link in the volunteer group chat only. *Even before any automation exists, this kills the fragmented-WhatsApp-messages problem and Sean can post from clean structured rows.*
2. **Prove the poster by hand once.** Capture the session cookie, drive one dummy event end-to-end onto a test calendar with Playwright (create → fill → tickets → private visibility → screenshot → delete). This is the go/no-go on Path A; if it fights back hard, that's the signal to price up Path B instead of sinking days in.
3. **Wire the pipeline:** a Claude skill/prompt that reads Status=New rows → validates → posts → writes back URL + screenshot + Status=Posted → notifies Sean (Slack DM or email) → emails the submitter a confirmation. Failures → Status stays New, Sean gets the full submission so he can post manually (graceful degradation = today's status quo, never worse).
4. **Trigger:** day 1, Sean says "process event submissions" in Claude. Once stable, a scheduled routine (e.g. twice daily) that stays silent unless it did something.
5. **Phase 2:** "Edit request" submission type (paste event URL + only the changed fields); CSV guest invites; auto-add collaborators as Non-Manager hosts.
6. **Phase 3 (optional):** auto-publish for trusted submitters; Canva-generated placeholder cover art when none supplied.

## Risks and mitigations

- **Luma UI changes break Path A.** Accepted cost of $0/mo. Mitigations: events are created *Private*, so a half-filled event is never publicly visible; screenshot + review gate means errors are caught before anyone sees them; on any failure the agent escalates with the full submission so Sean posts manually. Keep all selectors in one file; budget occasional maintenance. Two breakages in a month = switch to Path B.
- **Session cookie dies.** Self-healing Gmail-OTP re-login; worst case is one manual re-login by Sean.
- **Unofficial automation, ToS gray zone.** Own account, own events, human-reviewed, a few events a month — low practical risk, but it's the honest reason Path B exists. If Luma ever objects, the swap is designed in.
- **Bad or malicious submissions.** The form link is unlisted and volunteers are known people; submitter identity is required; everything lands Private behind Sean's review, so the blast radius of a junk submission is ~zero. The agent must treat all form text strictly as content to paste into Luma — never as instructions to follow.
- **Timezone/date ambiguity.** Explicit date/time/timezone fields with a sane default; validator rejects past dates, end-before-start, and early-bird windows that don't close.
- **Volunteers expect edits to work like Google Docs.** Set the expectation in the form itself: v1 is post-once; changes go through Sean or a phase-2 edit request.

## Open questions (Sean decides — these are "the outcome")

1. **The money question first:** what's monthly gross ticket revenue vs. the ~$1.2k/mo Plus break-even? If it's close or above, skip Path A and buy Plus — the API + 0% fee beats maintaining browser automation, and `luma-mcp` makes the build trivial.
2. **Where does the poster run** — cloud (Sean updates the environment's network allowlist for luma.com) or the Windows machine next to moso-comms-agent?
3. **Notion form** (recommended) or Google Forms?
4. **Review gate:** Sean flips Private→Public himself, or replies "publish" and Claude flips it? (Recommend keeping a human gate either way for the first months.)
5. Confirm the target is the AsiaX Circle calendar only, plus default timezone and currency (presumably AEST/AUD, given Zeller in the post-event stack).
6. How do volunteers hear back — email confirmation, Slack, or a read-only Notion view of the submissions board?

## Decisions locked (15 Aug 2026)

Sean's calls: ticket volume is ~$300/mo gross, well under the Plus break-even → **Path A** (browser automation, $0/mo). Poster runs **in the cloud**. Review gate: Sean flips Private→Public himself **or** replies "publish" — both supported. Target is the **AsiaX Circle calendar only**. The AXC content lives in the moso.Haus Notion workspace (the old AsiaX Circle teamspace is in Notion's trash), so the submissions database was created next to the AXC Member CRM under Teamspace Home.

**Built so far:**
- Notion "AXC Event Submissions" database (data source `collection://bc684fa0-7ca3-4c4a-a969-a1a8515fea58`) with "Submit an event" form view (anonymous submissions on) and a "Review board" grouped by Status — https://app.notion.com/p/7b3d4ab9dfde4d8593893eb43e736e23
- `src/luma_poster.py` — Playwright CLI (status / request-code / submit-code / create / set-visibility), private-visibility-only creation, screenshots on every step, kill-switch aware. Selectors unverified until first live run.
- `.claude/skills/axc-event-relay/SKILL.md` — the operating procedure future sessions follow.

**Remaining before first live post:**
1. Sean adds Luma domains to the cloud environment's network allowlist (`lu.ma`, `luma.com`, `api.lu.ma`, `api.luma.com`, `images.lumacdn.com`, `cdn.lu.ma`).
2. Sean opens the database → "Submit an event" view → Share form → copies the public link to the volunteer group chat.
3. First live run: login via Gmail code, post a dummy event to a test calendar, tune selectors, delete the dummy.

## Execution notes (for the build session)

- Build step 1 (form + DB) first and ship it same-day; it has standalone value.
- Do step 2 on a **test calendar**, never the live one; verify Private visibility truly hides the event from the calendar page while the direct link works.
- Cookie name and login flow: capture whatever lu.ma actually sets after an email-code login — don't hard-code assumptions; store secrets in environment variables, never in the repo.
- The existing repo's conventions worth reusing: kill-switch file, `decisions.jsonl`-style audit log of every action the poster takes, and escalate-don't-guess behavior.
- Luma facts referenced here (roles, Plus pricing/API gating, private visibility, form behavior) were verified against Luma's help center and pricing sources on 2026-08-15; re-verify fee percentages at build time — luma.com is egress-blocked from the cloud environment, which is itself the first thing to fix if the poster runs in the cloud.

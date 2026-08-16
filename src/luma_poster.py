"""Luma poster — drives lu.ma in a real browser to create AXC events from submission specs.

No Luma API on the free plan, so this automates the web app with Playwright.
Auth is a two-phase email-code login (Claude reads the code from Sean's Gmail
and passes it back in), persisted in a local browser profile between commands.

Selectors were written blind against Luma's known UI and are UNVERIFIED until
the first live run — luma.com is unreachable from the dev environment where
this was authored. Run `status` first, then tune SELECTORS/flows as needed.
Locators prefer roles/placeholders/text over CSS so minor redesigns survive.

Commands (all print a JSON result line to stdout):
    python -m src.luma_poster status
    python -m src.luma_poster request-code --email sean@moso.haus
    python -m src.luma_poster submit-code --code 123456
    python -m src.luma_poster create --spec data/luma_events/<row>.json
    python -m src.luma_poster set-visibility --url https://lu.ma/xyz --visibility public

Event spec JSON:
    {
      "title": "...",
      "description": "plain text or simple markdown",
      "start": "2026-09-12T18:30:00",          # local wall time
      "end": "2026-09-12T21:30:00",
      "timezone": "Australia/Melbourne",
      "venue_name": "...", "address": "...", "hide_address": false,
      "calendar": "AsiaX Circle",
      "capacity": 80,                            # optional
      "cover_image": "data/luma_events/cover.png",  # optional local path
      "tickets": [
        {"name": "Early Bird", "price_aud": 25, "quantity": 20, "sales_end": "2026-09-01T23:59:00"},
        {"name": "General Admission", "price_aud": 35, "quantity": null, "sales_end": null}
      ]
    }
"""

import json
import os
import sys
import time
from pathlib import Path

import click

_PROJECT_ROOT = Path(__file__).parent.parent
BROWSER_DIR = _PROJECT_ROOT / "data" / "luma_browser"
SHOTS_DIR = _PROJECT_ROOT / "data" / "luma_shots"
KILL_SWITCH = _PROJECT_ROOT / "data" / "KILL_SWITCH"

LUMA_HOME = "https://lu.ma/home"
LUMA_SIGNIN = "https://lu.ma/signin"
LUMA_CREATE = "https://lu.ma/create"

SELECTORS = {
    # Central place to patch when Luma ships UI changes.
    "signin_email": 'input[type="email"]',
    "signin_code": 'input[autocomplete="one-time-code"], input[name="code"]',
    "create_title": 'textarea[placeholder*="Event Name"], input[placeholder*="Event Name"]',
    "description_editor": '[contenteditable="true"]',
}


def _shot(page, label: str) -> str:
    SHOTS_DIR.mkdir(parents=True, exist_ok=True)
    path = SHOTS_DIR / f"{time.strftime('%Y%m%d-%H%M%S')}-{label}.png"
    try:
        page.screenshot(path=str(path), full_page=True)
    except Exception:
        return ""
    return str(path)


def _result(ok: bool, **fields):
    print(json.dumps({"ok": ok, **fields}))
    sys.exit(0 if ok else 1)


def _chromium_path() -> str | None:
    """Find a preinstalled Chromium so we never trigger `playwright install`.

    Cloud images ship a pinned build that often doesn't match the pip
    playwright version's expected revision. LUMA_CHROMIUM overrides.
    """
    explicit = os.environ.get("LUMA_CHROMIUM")
    if explicit and Path(explicit).exists():
        return explicit
    root = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"))
    candidates = sorted(root.glob("chromium*/chrome-linux/chrome"), reverse=True)
    return str(candidates[0]) if candidates else None


def _launch(p, headed: bool = False):
    BROWSER_DIR.mkdir(parents=True, exist_ok=True)
    args = ["--no-sandbox"]

    # Sandboxed/cloud egress proxies re-terminate TLS, and some can't parse
    # Chromium's TLS 1.3 ClientHello — every navigation dies with
    # ERR_CONNECTION_RESET while curl works fine. Capping at TLS 1.2 fixes it
    # without weakening verification (certs are still fully validated).
    if os.environ.get("LUMA_TLS12", "1") == "1":
        args.append("--ssl-version-max=tls1.2")

    kwargs = {
        "headless": not headed and os.environ.get("LUMA_HEADED") != "1",
        "viewport": {"width": 1440, "height": 1000},
        "args": args,
    }
    chromium = _chromium_path()
    if chromium:
        kwargs["executable_path"] = chromium

    # Chromium doesn't read HTTPS_PROXY from the environment the way curl does.
    # In sandboxed/cloud runs all egress goes through a local policy proxy, so
    # pass it explicitly or every navigation fails with ERR_CONNECTION_RESET.
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxy:
        kwargs["proxy"] = {"server": proxy}

    return p.chromium.launch_persistent_context(str(BROWSER_DIR), **kwargs)


def _is_logged_in(page) -> bool:
    page.goto(LUMA_HOME, wait_until="domcontentloaded")
    page.wait_for_timeout(2500)
    # Signed-out lu.ma/home redirects to a marketing page with a Sign In button.
    return "signin" not in page.url and page.get_by_role(
        "link", name="Sign In"
    ).count() == 0


def _require_no_kill_switch():
    if KILL_SWITCH.exists():
        _result(False, error="KILL_SWITCH present — refusing to act")


@click.group()
def cli():
    pass


@cli.command()
def status():
    """Report whether the stored browser profile is signed in to Luma."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx = _launch(p)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            logged_in = _is_logged_in(page)
            shot = _shot(page, "status")
            _result(True, logged_in=logged_in, url=page.url, screenshot=shot)
        except Exception as e:
            _result(False, error=str(e), screenshot=_shot(page, "status-error"))
        finally:
            ctx.close()


@cli.command("request-code")
@click.option("--email", required=True)
def request_code(email: str):
    """Phase 1 of login: submit the email so Luma sends a sign-in code."""
    _require_no_kill_switch()
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx = _launch(p)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            page.goto(LUMA_SIGNIN, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)
            page.locator(SELECTORS["signin_email"]).first.fill(email)
            cont = page.get_by_role("button", name="Continue with Email")
            if cont.count():
                cont.first.click()
            else:
                page.keyboard.press("Enter")
            page.wait_for_timeout(5000)
            _result(True, note="code requested — read it from Gmail, then run submit-code",
                    screenshot=_shot(page, "request-code"))
        except Exception as e:
            _result(False, error=str(e), screenshot=_shot(page, "request-code-error"))
        finally:
            ctx.close()


@cli.command("submit-code")
@click.option("--code", required=True)
def submit_code(code: str):
    """Phase 2 of login: enter the emailed code on the page left by request-code."""
    _require_no_kill_switch()
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx = _launch(p)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            # The profile persists the signin page state; if not, redo phase 1 first.
            if "signin" not in page.url:
                page.goto(LUMA_SIGNIN, wait_until="domcontentloaded")
                page.wait_for_timeout(1500)
            field = page.locator(SELECTORS["signin_code"]).first
            if field.count() == 0:
                _result(False, error="no code field visible — run request-code again",
                        screenshot=_shot(page, "submit-code-error"))
            field.fill(code)
            page.keyboard.press("Enter")
            page.wait_for_timeout(4000)
            _result(True, logged_in=_is_logged_in(page), screenshot=_shot(page, "submit-code"))
        except Exception as e:
            _result(False, error=str(e), screenshot=_shot(page, "submit-code-error"))
        finally:
            ctx.close()


def _fill_datetime(page, which: str, iso_local: str):
    # Luma's start/end pickers open from buttons labelled with the current value.
    # Typing into the revealed date and time inputs is more reliable than clicking
    # calendar cells. Tune on first live run.
    date_part, time_part = iso_local.split("T")
    trigger = page.get_by_text("Start" if which == "start" else "End", exact=False).first
    trigger.click()
    page.wait_for_timeout(500)
    inputs = page.locator('input[type="text"]:visible')
    # Heuristic: the picker exposes a date input then a time input.
    inputs.nth(0).fill(date_part)
    inputs.nth(1).fill(time_part[:5])
    page.keyboard.press("Enter")
    page.wait_for_timeout(500)


def _add_ticket(page, ticket: dict):
    page.get_by_text("New Ticket Type", exact=False).first.click()
    page.wait_for_timeout(600)
    dialog = page.locator('[role="dialog"]').last
    dialog.get_by_placeholder("Name").first.fill(ticket["name"])
    price = ticket.get("price_aud") or 0
    if price > 0:
        dialog.get_by_text("Paid", exact=False).first.click()
        dialog.get_by_placeholder("0.00").first.fill(f"{price:.2f}")
    if ticket.get("quantity"):
        dialog.get_by_text("Restrict Capacity", exact=False).first.click()
        dialog.locator('input[type="number"]').last.fill(str(int(ticket["quantity"])))
    if ticket.get("sales_end"):
        dialog.get_by_text("Sales End", exact=False).first.click()
        date_part, time_part = ticket["sales_end"].split("T")
        vis = dialog.locator('input[type="text"]:visible')
        vis.nth(0).fill(date_part)
        vis.nth(1).fill(time_part[:5])
    dialog.get_by_role("button", name="Create").first.click()
    page.wait_for_timeout(800)


@cli.command()
@click.option("--spec", "spec_path", required=True, type=click.Path(exists=True))
def create(spec_path: str):
    """Create the event from a spec JSON — always with Private visibility."""
    _require_no_kill_switch()
    from playwright.sync_api import sync_playwright

    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    with sync_playwright() as p:
        ctx = _launch(p)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            if not _is_logged_in(page):
                _result(False, error="not logged in — run request-code / submit-code first")

            page.goto(LUMA_CREATE, wait_until="domcontentloaded")
            page.wait_for_timeout(2500)

            # Calendar picker sits top-left; visibility (Public/Private) top-right.
            page.get_by_text("Personal Calendar", exact=False).first.click()
            page.get_by_text(spec.get("calendar", "AsiaX Circle"), exact=False).first.click()
            page.wait_for_timeout(400)
            page.get_by_text("Public", exact=True).first.click()
            page.get_by_text("Private", exact=False).first.click()
            page.wait_for_timeout(400)

            page.locator(SELECTORS["create_title"]).first.fill(spec["title"])
            _fill_datetime(page, "start", spec["start"])
            _fill_datetime(page, "end", spec["end"])

            page.get_by_text("Add Event Location", exact=False).first.click()
            page.wait_for_timeout(500)
            loc_box = page.locator('input:visible').last
            loc_box.fill(spec.get("address") or spec.get("venue_name", ""))
            page.wait_for_timeout(1500)
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)

            page.get_by_text("Add Description", exact=False).first.click()
            page.wait_for_timeout(500)
            editor = page.locator(SELECTORS["description_editor"]).last
            editor.click()
            editor.type(spec["description"], delay=1)
            done = page.get_by_role("button", name="Done")
            if done.count():
                done.first.click()

            page.get_by_role("button", name="Create Event").first.click()
            page.wait_for_url("**/lu.ma/**", timeout=20000)
            page.wait_for_timeout(2500)
            event_url = page.url.split("?")[0]

            # Post-create: tickets, capacity and address-hiding live in Manage.
            for ticket in spec.get("tickets", []):
                _add_ticket(page, ticket)
            if spec.get("capacity"):
                cap = page.get_by_text("Capacity", exact=False)
                if cap.count():
                    cap.first.click()
                    page.locator('input[type="number"]:visible').first.fill(str(int(spec["capacity"])))
                    page.get_by_role("button", name="Set Limit").first.click()

            _result(True, event_url=event_url, screenshot=_shot(page, "created"))
        except Exception as e:
            _result(False, error=str(e), screenshot=_shot(page, "create-error"))
        finally:
            ctx.close()


@cli.command("set-visibility")
@click.option("--url", required=True)
@click.option("--visibility", type=click.Choice(["public", "private"]), required=True)
def set_visibility(url: str, visibility: str):
    """Flip an existing event between Private and Public (the publish step)."""
    _require_no_kill_switch()
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx = _launch(p)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            if not _is_logged_in(page):
                _result(False, error="not logged in — run request-code / submit-code first")
            page.goto(url.rstrip("/"), wait_until="domcontentloaded")
            page.wait_for_timeout(2000)
            page.get_by_text("Manage", exact=False).first.click()
            page.wait_for_timeout(2000)
            current = "Private" if visibility == "public" else "Public"
            page.get_by_text(current, exact=True).first.click()
            page.get_by_text(visibility.capitalize(), exact=False).first.click()
            page.wait_for_timeout(1000)
            _result(True, visibility=visibility, screenshot=_shot(page, "visibility"))
        except Exception as e:
            _result(False, error=str(e), screenshot=_shot(page, "visibility-error"))
        finally:
            ctx.close()


if __name__ == "__main__":
    cli()

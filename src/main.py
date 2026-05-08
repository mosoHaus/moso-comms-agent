"""moso comms agent — CLI entry point."""

import os
import sys
from pathlib import Path

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich import box

# Load .env from project root regardless of working directory
_PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(_PROJECT_ROOT / ".env")
console = Console()

BANNER = """[bold cyan]
  moso comms agent
  autonomous Gmail triage for sean@moso.haus
[/bold cyan]"""


@click.group()
def cli():
    """moso comms agent — autonomous Gmail triage and drafting."""


@cli.command()
@click.option("--max", "max_results", default=10, show_default=True, help="Number of messages to fetch")
@click.option("--query", default="in:inbox", show_default=True, help="Gmail search query")
def inspect(max_results: int, query: str):
    """List recent messages from Gmail."""
    console.print(BANNER)
    console.print(f"[dim]Fetching up to {max_results} messages: [italic]{query}[/italic][/dim]\n")

    from src.gmail_client import list_recent_messages

    with console.status("[bold green]Connecting to Gmail…"):
        messages = list_recent_messages(query=query, max_results=max_results)

    if not messages:
        console.print("[yellow]No messages found.[/yellow]")
        return

    table = Table(
        show_header=True,
        header_style="bold magenta",
        box=box.ROUNDED,
        expand=True,
        show_lines=True,
    )
    table.add_column("#", style="dim", width=3, no_wrap=True)
    table.add_column("From", min_width=20, max_width=35)
    table.add_column("Subject", min_width=25, max_width=45)
    table.add_column("Date", width=20, no_wrap=True)
    table.add_column("Snippet", min_width=30)

    for i, msg in enumerate(messages, 1):
        if "error" in msg:
            table.add_row(str(i), "[red]error[/red]", msg.get("error", ""), "", "")
            continue
        table.add_row(
            str(i),
            _truncate(msg.get("from", ""), 33),
            _truncate(msg.get("subject", ""), 43),
            _truncate(msg.get("date", ""), 18),
            _truncate(msg.get("snippet", ""), 80),
        )

    console.print(table)
    console.print(f"\n[dim]Total: {len(messages)} message(s)[/dim]")


@cli.command("run")
@click.option("--once", is_flag=True, default=False, help="Process current unread then exit")
@click.option("--watch", is_flag=True, default=False, help="Poll every 3 minutes continuously")
def run_agent(once: bool, watch: bool):
    """Run the triage agent (once or in polling loop)."""
    if not once and not watch:
        console.print("[yellow]Specify --once or --watch[/yellow]")
        raise SystemExit(1)

    from src.agent import run_once

    console.print(BANNER)

    if once:
        run_once(console)
    else:
        import time
        interval = 180
        console.print(f"[dim]Watching inbox every {interval}s. Press Ctrl+C to stop.[/dim]\n")
        while True:
            run_once(console)
            console.print(f"\n[dim]Sleeping {interval}s…[/dim]")
            time.sleep(interval)


@cli.command()
def learn():
    """Check Gmail for sent edits to drafts and log corrections."""
    from src.learning import check_for_sent_edits
    console.print(BANNER)
    with console.status("[bold green]Scanning sent mail for corrections…"):
        new_corrections = check_for_sent_edits()
    if new_corrections:
        console.print(f"[green]Logged {len(new_corrections)} new correction(s).[/green]")
        for c in new_corrections:
            console.print(f"  [cyan]{c['category']}[/cyan]: {c['diff_summary']}")
    else:
        console.print("[dim]No new corrections found.[/dim]")


@cli.command()
def corrections():
    """Display all logged corrections grouped by category."""
    import time as _time
    from src.learning import get_all_corrections
    console.print(BANNER)
    rows = get_all_corrections()
    if not rows:
        console.print("[dim]No corrections logged yet. Run 'learn' after sending edited drafts.[/dim]")
        return
    by_cat: dict = {}
    for r in rows:
        by_cat.setdefault(r["category"], []).append(r)
    for cat, items in by_cat.items():
        console.print(f"\n[bold cyan]{cat.upper()}[/bold cyan] — {len(items)} correction(s)")
        for item in items:
            ts = _time.strftime("%Y-%m-%d %H:%M", _time.localtime(item["created_at"]))
            console.print(f"  [dim]{ts}[/dim]  {item['diff_summary']}")
            console.print(f"    [dim]Before:[/dim] {item['generated_body'][:80].strip()!r}")
            console.print(f"    [dim]After: [/dim] {item['sent_body'][:80].strip()!r}")


@cli.command("seed-correction")
@click.option("--category", required=True, type=click.Choice(["pilates", "norton_and_quay", "personal"]))
@click.option("--before", required=True, help="Generated draft body")
@click.option("--after", required=True, help="Sent (edited) body")
@click.option("--summary", required=True, help="One-sentence description of the change")
def seed_correction(category: str, before: str, after: str, summary: str):
    """Manually seed a correction for demo/testing."""
    from src.learning import seed_manual_correction
    cid = seed_manual_correction(category, before, after, summary)
    console.print(f"[green]Seeded correction #{cid} for category '{category}'[/green]")
    console.print(f"  Summary: {summary}")


@cli.command("refresh-allowlist")
def refresh_allowlist():
    """Rebuild sender allowlist from sent mail."""
    from src.safety import build_sender_allowlist
    with console.status("[bold green]Scanning sent mail…"):
        count = build_sender_allowlist()
    console.print(f"[green]Allowlist updated: {count} domain(s) saved to data/sender_allowlist.json[/green]")


@cli.command("kill-switch")
@click.argument("action", type=click.Choice(["on", "off", "status"]))
def kill_switch(action: str):
    """Toggle the kill switch (on/off/status). 'on' stops all agent actions."""
    from pathlib import Path
    from src.safety import KILL_SWITCH
    if action == "on":
        KILL_SWITCH.parent.mkdir(parents=True, exist_ok=True)
        KILL_SWITCH.touch()
        console.print("[bold red]Kill switch ACTIVATED — agent will take no actions.[/bold red]")
    elif action == "off":
        if KILL_SWITCH.exists():
            KILL_SWITCH.unlink()
        console.print("[green]Kill switch deactivated — agent is active.[/green]")
    else:
        state = "ON" if KILL_SWITCH.exists() else "OFF"
        color = "red" if KILL_SWITCH.exists() else "green"
        console.print(f"Kill switch is [{color}]{state}[/{color}]")


@cli.command()
def demo():
    """Run agent in verbose demo mode — designed for screen recording."""
    from src.agent import run_once
    console.print(BANNER)
    console.print("[bold yellow]DEMO MODE — verbose logging enabled[/bold yellow]\n")
    os.environ["AGENT_DEMO_MODE"] = "true"
    run_once(console)


def _truncate(s: str, n: int) -> str:
    return s if len(s) <= n else s[: n - 1] + "…"


def main():
    cli()


if __name__ == "__main__":
    main()

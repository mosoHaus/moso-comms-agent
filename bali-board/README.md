# bali-board

Shared trip board for the Bali group trip, 27–30 August 2026. Fifteen people,
one link, everyone edits the same thing.

Live at **https://bali-board.vercel.app** (Vercel project `bali-board`).

## What it is

A single static page plus one serverless function. No framework, no build step.

```
index.html        the whole front end — markup, styles, and app JS inline
api/board.js      GET returns the board state, POST applies ops and returns the new state
backup/           point-in-time snapshots of the live state
```

Maps are Leaflet from unpkg, tiles from OpenStreetMap. Addresses typed into a
schedule row are geocoded server-side via Nominatim, so a pin appears without
anyone having to look up coordinates.

## Where the data lives

**Not in this repo.** State is a single JSON blob in Upstash Redis under the key
`bali:state`, reached through the Vercel Redis integration.

That separation is the important bit: **deploying new code does not touch
anyone's entries.** Votes, flight times, tasks, notes and schedule rows all
survive a deploy untouched. What a deploy *can* break is the reader — if
`api/board.js` or its env vars go missing, the data is still in Redis but the
page has no way to reach it.

The function looks for the first pair it finds of:

| URL | Token |
|---|---|
| `KV_REST_API_URL` | `KV_REST_API_TOKEN` |
| `kv_KV_REST_API_URL` | `kv_KV_REST_API_TOKEN` |
| `UPSTASH_REDIS_REST_URL` | `UPSTASH_REDIS_REST_TOKEN` |
| `REDIS_REST_API_URL` | `REDIS_REST_API_TOKEN` |

With neither set the API returns `503 {"error":"nostore"}` and the page shows a
"SETUP NEEDED" banner rather than silently looking empty.

## State shape

```jsonc
{
  "legs":   { "<name>": { "arrFl", "arrT", "depFl", "depT", "note" } },
  "votes":  { "<optId>": ["<name>", ...] },
  "tasks":  [ { "id", "label", "hint", "done", "owners": [], "notes": [] } ],
  "opts":   [ { "id", "label", "day", "when", "note", "loc", "lat", "lng", "url", "by" } ],
  "sched":  [ { "id", "day", "time", "dur", "type", "everyone", "activity",
                "loc", "cost", "note", "lat", "lng", "url", "by" } ],
  "base":   { "label", "loc", "lat", "lng", "url" },
  "meta":   { "<key>": "<value>" },
  "rev":    0
}
```

`clean()` runs on every read and write, so older stored shapes are migrated
forward on the fly — single `owner` strings become `owners` arrays, ideas with
only a free-text `when` get a `day` inferred from it, junk coordinates are
nulled out. Old shapes never need a migration script.

Roster and the four valid days are hardcoded in `api/board.js`. Anything a
client sends that isn't on the roster is dropped, so a stale tab can't invent
people.

## Backups

`backup/` holds snapshots pulled from `GET /api/board`. Take one before any
change that touches the storage key, the state shape, or the env vars:

```sh
curl -s https://bali-board.vercel.app/api/board > backup/board-data-$(date +%Y%m%d-%H%M).json
```

`board-data-rev415.json` is the state as of 22 Aug 2026 — 13 of 15 manifests
filled, 16 ideas, 12 tasks, 16 schedule rows, contributions from all 15 people.

## Deploying

Vercel builds from this directory. No framework preset, no build command —
`index.html` is served static and `api/board.js` becomes a Node function.

Because state lives outside the deployment, rollbacks are safe: reverting to an
earlier deployment restores old *code* against current *data*.

## Conventions

The front end is deliberately one file with no dependencies to install. Keep it
that way — it's a four-day trip board, not a product. Server-side, every string
that reaches storage goes through `str()` with a length cap, and every
coordinate through `okCoords()`.

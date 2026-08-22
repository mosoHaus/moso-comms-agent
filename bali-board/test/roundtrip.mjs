// Verifies the reconstructed api/board.js preserves the live board state.
// Strips the Redis import (no network), exposes clean()/apply(), then round-trips
// the real rev415 snapshot and diffs every field anyone contributed.
import fs from "node:fs";
import path from "node:path";
import os from "node:os";

const DIR = path.resolve(new URL("..", import.meta.url).pathname);
const src = fs.readFileSync(path.join(DIR, "api/board.js"), "utf8")
  .replace(/^import \{ Redis \} from "@upstash\/redis";$/m, "const Redis = class {};")
  + "\nexport { clean, apply, blank };\n";

const tmp = path.join(os.tmpdir(), "_board_test.mjs");
fs.writeFileSync(tmp, src);
const { clean, apply } = await import(tmp);

const live = JSON.parse(fs.readFileSync(path.join(DIR, "backup/board-data-rev415.json"), "utf8"));

let fail = 0;
const ok = (label, cond, detail = "") => {
  console.log(`${cond ? "  ok  " : "FAIL  "}${label}${detail ? "  " + detail : ""}`);
  if (!cond) fail++;
};

// --- 1. clean() must not drop anything anyone entered ------------------------
const out = clean(JSON.parse(JSON.stringify(live)));

console.log("\n== manifests (flight times people typed in) ==");
for (const [name, legIn] of Object.entries(live.legs)) {
  const legOut = out.legs[name];
  const same = JSON.stringify(legIn) === JSON.stringify(legOut);
  ok(name.padEnd(10), same, same ? "" : JSON.stringify(legOut));
}
ok("count".padEnd(10), Object.keys(out.legs).length === Object.keys(live.legs).length,
  `${Object.keys(out.legs).length}/${Object.keys(live.legs).length}`);

console.log("\n== votes (every single vote cast) ==");
const vIn = Object.entries(live.votes).flatMap(([k, v]) => v.map((n) => `${k}:${n}`)).sort();
const vOut = Object.entries(out.votes).flatMap(([k, v]) => v.map((n) => `${k}:${n}`)).sort();
ok("total votes", vIn.length === vOut.length, `${vOut.length}/${vIn.length}`);
ok("identical set", JSON.stringify(vIn) === JSON.stringify(vOut),
  vIn.filter((x) => !vOut.includes(x)).join(", ") || "");

console.log("\n== tasks ==");
ok("count", out.tasks.length === live.tasks.length, `${out.tasks.length}/${live.tasks.length}`);
for (const t of live.tasks) {
  const o = out.tasks.find((x) => x.id === t.id);
  const same = o && o.label === t.label && o.done === t.done
    && JSON.stringify(o.owners || []) === JSON.stringify(t.owners || [])
    && JSON.stringify(o.notes || []) === JSON.stringify(t.notes || []);
  ok(t.label.slice(0, 44).padEnd(46), !!same);
}

console.log("\n== ideas ==");
ok("count", out.opts.length === live.opts.length, `${out.opts.length}/${live.opts.length}`);
for (const o of live.opts) {
  const n = out.opts.find((x) => x.id === o.id);
  const same = n && n.label === o.label && n.day === o.day && n.when === o.when && n.note === o.note && n.by === o.by;
  ok(o.label.slice(0, 44).padEnd(46), !!same, same ? "" : JSON.stringify(n));
}

console.log("\n== schedule ==");
ok("count", out.sched.length === live.sched.length, `${out.sched.length}/${live.sched.length}`);
for (const s of live.sched) {
  const n = out.sched.find((x) => x.id === s.id);
  const same = n && n.activity === s.activity && n.day === s.day && n.time === s.time
    && n.note === s.note && n.everyone === s.everyone && n.lat === s.lat && n.lng === s.lng && n.url === s.url;
  ok(`${s.day} ${s.activity}`.slice(0, 44).padEnd(46), !!same, same ? "" : JSON.stringify(n));
}

console.log("\n== base + meta + rev ==");
ok("villa loc", out.base.loc === live.base.loc, out.base.loc);
ok("rev preserved", out.rev === live.rev, String(out.rev));

// --- 2. idempotency: clean(clean(x)) === clean(x) ----------------------------
console.log("\n== idempotency ==");
const twice = clean(JSON.parse(JSON.stringify(out)));
ok("clean() is stable", JSON.stringify(twice) === JSON.stringify(out));

// --- 3. ops still work on real data -----------------------------------------
console.log("\n== ops against live data ==");
let s = clean(JSON.parse(JSON.stringify(live)));
const before = s.tasks.length;
s = apply(s, { op: "addTask", label: "Book 2 Hiace vans", hint: "Thu airport, Sat pickleball, Sun departures" });
ok("addTask appends", s.tasks.length === before + 1);
ok("rev increments", s.rev === live.rev + 1, String(s.rev));
const added = s.tasks[s.tasks.length - 1];
s = apply(s, { op: "toggleOwner", id: added.id, who: "Sean" });
ok("toggleOwner on roster", JSON.stringify(s.tasks.at(-1).owners) === '["Sean"]');
s = apply(s, { op: "toggleOwner", id: added.id, who: "Mallory" });
ok("non-roster rejected", JSON.stringify(s.tasks.at(-1).owners) === '["Sean"]');
s = apply(s, { op: "toggleVote", opt: "beach", who: "Sean" });
ok("toggleVote adds", s.votes.beach.includes("Sean"));
s = apply(s, { op: "toggleVote", opt: "beach", who: "Sean" });
ok("toggleVote removes", !s.votes.beach.includes("Sean"));
// everyone else's votes on that option untouched
ok("others' votes intact",
  JSON.stringify(s.votes.beach) === JSON.stringify(live.votes.beach),
  JSON.stringify(s.votes.beach));

console.log("\n" + (fail === 0 ? "ALL CHECKS PASSED — no data loss" : `${fail} CHECK(S) FAILED`));
process.exit(fail === 0 ? 0 : 1);

import { Redis } from "@upstash/redis";

const KEY = "bali:state";

const ROSTER = ["Amanda", "Hansel", "Cheryl", "Sean", "Matt", "Di", "Janelle", "Chan", "Darren", "Amy", "Ryan", "Sherilyn", "Jim", "Jason", "Kenny"];

const DAYS = ["27", "28", "29", "30"];

// Kinds of itinerary row. The client owns the emoji and colour for each.
const TYPES = ["arrive", "depart", "travel", "food", "seafood", "drinks", "snack", "activity", "beach", "spa", "hotel", "free"];

// Identifies us to Nominatim, whose usage policy requires it.
const UA = "bali-board/1.0 (https://bali-board.vercel.app)";

const SEED_TASKS = [
  { id: "t1", label: "Book Naughty Nuri's for 15, Fri 6pm", hint: "Which branch? Peak season, likely needs a deposit", done: false, owners: [], notes: [] },
  { id: "t2", label: "Book pickleball courts, Sat 9–11am", hint: "Enough courts for 15", done: false, owners: [], notes: [] },
  { id: "t3", label: "Book Milk & Madu for 15, Sat lunch", hint: "Straight after pickleball", done: false, owners: [], notes: [] },
  { id: "t4", label: "Lock Thursday group dinner venue", hint: "Arrival night, keep it near the villa", done: false, owners: [], notes: [] },
  { id: "t5", label: "Sort Saturday villa dinner order-in", hint: "Plus a cake for the August babies", done: false, owners: [], notes: [] },
  { id: "t6", label: "Sort the massages, Thu and Fri", hint: "Both TBC. Vote tells you the numbers", done: false, owners: [], notes: [] },
  { id: "t7", label: "Chase the last flight times", hint: "The blanks are visible in the manifest", done: false, owners: [], notes: [] },
  { id: "t8", label: "Collect dietaries + allergies", hint: "Before anything gets booked", done: false, owners: [], notes: [] },
  { id: "t9", label: "Confirm villa check-in / checkout", hint: "Matters for Thu and Sun", done: false, owners: [], notes: [] },
  { id: "t10", label: "Set up Splitwise", hint: "Before anyone pays for anything", done: false, owners: [], notes: [] },
];

const SEED_OPTS = [
  { id: "atv", label: "ATV", day: "28", when: "FRI 8–3", note: "An hour plus each way to Ubud. Book ahead." },
  { id: "surf", label: "Surfing", day: "28", when: "FRI 8–3", note: "Better earlier. Enough instructors for mixed ability." },
  { id: "hyrox", label: "Hyrox / S&C class", day: "28", when: "FRI 8–3", note: "Book a slot or you won't all get in." },
  { id: "facial", label: "Facial / spa", day: "28", when: "FRI 8–3", note: "Easy to book. Quiet rather than social." },
  { id: "run", label: "Run club", day: "28", when: "FRI EARLY", note: "Bali run clubs go 6–7am for the heat." },
  { id: "cafe", label: "Cafe hopping + shopping", day: "28", when: "FRI 8–3", note: "Low effort, easy to join late." },
  { id: "babi", label: "Babi guling lunch", day: "28", when: "FRI LUNCH", note: "Small groups, optional together." },
  { id: "mthu", label: "Massage after dinner", day: "27", when: "THU PM", note: "TBC. Needs numbers before anyone books." },
  { id: "mfri", label: "Massage after dinner", day: "28", when: "FRI PM", note: "Optional. Same deal, needs numbers." },
  { id: "beach", label: "Beach club", day: "29", when: "SAT PM", note: "Optional hang between lunch and dinner." },
  { id: "kc", label: "KC Bali", day: "30", when: "SUN", note: "Check it against your flight time." },
];

// The villa. Coordinates resolved from "Gang Daksina, Kerobokan Kelod" — the
// gang itself, not the building, so it points at the right lane. Swap in a
// Google Maps link for the exact gate when there is one.
const VILLA = "Gg. Daksina, Kerobokan Kelod, Kec. Kuta Utara, Badung, Bali";
const VILLA_LAT = -8.6735952;
const VILLA_LNG = 115.1492701;

// Ported from the schedule that used to be hardcoded in index.html.
// Only DPS carries coordinates — everything else is still an open decision,
// so a pin would be a guess. People add locations as they book them.
const SEED_SCHED = [
  { id: "s01", day: "27", time: "ALL DAY", dur: "", type: "arrive", everyone: false, activity: "Arrivals, staggered", loc: "Ngurah Rai International Airport (DPS)", lat: -8.7482, lng: 115.1675, cost: "", note: "Own transfer from DPS. Check the villa check-in time." },
  { id: "s02", day: "27", time: "EVENING", dur: "", type: "food", everyone: true, activity: "Group dinner", loc: "", cost: "", note: "Venue not locked yet." },
  { id: "s03", day: "27", time: "AFTER", dur: "", type: "spa", everyone: false, activity: "Massage", loc: "", cost: "", note: "TBC. Vote below if you're in." },
  { id: "s04", day: "27", time: "OTHERWISE", dur: "", type: "hotel", everyone: false, activity: "Hang at the villa", loc: VILLA, lat: VILLA_LAT, lng: VILLA_LNG, cost: "", note: "Home base for all four nights." },

  { id: "s05", day: "28", time: "8–3", dur: "", type: "free", everyone: false, activity: "Own thing", loc: "", cost: "", note: "ATV, surf, facial, run, Hyrox, cafes, shopping. Vote below so people can join you." },
  { id: "s06", day: "28", time: "LUNCH", dur: "", type: "food", everyone: false, activity: "Babi guling, small groups", loc: "", cost: "", note: "Optional together." },
  { id: "s07", day: "28", time: "6:00 PM", dur: "", type: "food", everyone: true, activity: "Dinner at Naughty Nuri's", loc: "", cost: "", note: "6pm sharp. Branch and booking not confirmed yet." },
  { id: "s08", day: "28", time: "AFTER", dur: "", type: "spa", everyone: false, activity: "Massage", loc: "", cost: "", note: "Optional." },

  { id: "s09", day: "29", time: "9–11 AM", dur: "2h", type: "activity", everyone: true, activity: "Pickleball at PickleBali", loc: "PickleBali Clubs, Jl. Raya Padonan, Dalung, Kuta Utara", lat: -8.62266, lng: 115.16575, cost: "150–250k/court", note: "5.0★ (375). 3 courts — book 2–3 privately for 15. Vans leave 8:30am, it's 20–25 min. Add a coach (~300–400k/hr) for a beginner clinic alongside open play." },
  { id: "s10", day: "29", time: "LUNCH", dur: "", type: "food", everyone: true, activity: "Milk & Madu", loc: "", cost: "", note: "Which outlet not decided yet." },
  { id: "s11", day: "29", time: "AFTERNOON", dur: "", type: "beach", everyone: false, activity: "Beach club", loc: "", cost: "", note: "Optional hang." },
  { id: "s12", day: "29", time: "DINNER", dur: "", type: "food", everyone: true, activity: "Order in at the villa", loc: VILLA, lat: VILLA_LAT, lng: VILLA_LNG, cost: "", note: "August baby celebration. Nothing ordered yet." },

  { id: "s13", day: "30", time: "DAYTIME", dur: "", type: "activity", everyone: false, activity: "Split", loc: "", cost: "", note: "Some to KC Bali, some doing their own thing." },
  { id: "s14", day: "30", time: "ALL DAY", dur: "", type: "depart", everyone: false, activity: "Departures, staggered", loc: "Ngurah Rai International Airport (DPS)", lat: -8.7482, lng: 115.1675, cost: "", note: "Allow 3hrs at DPS on a Sunday." },
];

const str = (v, max = 400) => String(v == null ? "" : v).slice(0, max).trim();
const now = () => Date.now();
const uid = (p) => p + now().toString(36) + Math.random().toString(36).slice(2, 6);

// Null unless it's a real, usable coordinate. 0,0 is in the Atlantic, not Bali.
const num = (v) => {
  const n = typeof v === "number" ? v : parseFloat(v);
  return Number.isFinite(n) ? n : null;
};
const okCoords = (lat, lng) =>
  lat != null && lng != null && Math.abs(lat) <= 90 && Math.abs(lng) <= 180 && !(lat === 0 && lng === 0);

// Ideas used to carry only a free-text "when". Read a day out of it so older
// stored ideas land in the right day tab instead of falling into Any time.
const dayFromWhen = (w) => {
  const s = String(w == null ? "" : w).toUpperCase();
  if (/\bTHU/.test(s) || /\b27\b/.test(s)) return "27";
  if (/\bFRI/.test(s) || /\b28\b/.test(s)) return "28";
  if (/\bSAT/.test(s) || /\b29\b/.test(s)) return "29";
  if (/\bSUN/.test(s) || /\b30\b/.test(s)) return "30";
  return "";
};

// Tasks used to carry a single `owner` string; upgrade any still stored that way.
const fixTask = (t) => {
  const o = { ...t };
  o.owners = Array.isArray(o.owners)
    ? o.owners.filter((n) => ROSTER.includes(n))
    : typeof o.owner === "string" && ROSTER.includes(o.owner) ? [o.owner] : [];
  delete o.owner;
  if (!Array.isArray(o.notes)) o.notes = [];
  return o;
};

const fixOpt = (o) => {
  const day = str(o && o.day, 4);
  // Ideas added from the recommendations carry the place with them, so the
  // vote card can link straight out to it.
  const lat = num(o && o.lat), lng = num(o && o.lng);
  const pinned = okCoords(lat, lng);
  return {
    id: str(o && o.id, 40) || uid("o"),
    label: str(o && o.label, 80),
    day: DAYS.includes(day) ? day : dayFromWhen(o && o.when),
    when: str(o && o.when, 40),
    note: str(o && o.note, 200),
    loc: str(o && o.loc, 160),
    lat: pinned ? lat : null,
    lng: pinned ? lng : null,
    url: str(o && o.url, 400) || null,
    by: str(o && o.by, 40) || null,
  };
};

// Where the group is staying. Shown on every day's map so people can see
// where they're going relative to where they sleep.
const fixBase = (b) => {
  const lat = num(b && b.lat), lng = num(b && b.lng);
  const pinned = okCoords(lat, lng);
  return {
    label: str(b && b.label, 60) || "Villa",
    loc: str(b && b.loc, 160),
    lat: pinned ? lat : null,
    lng: pinned ? lng : null,
    url: str(b && b.url, 400) || null,
  };
};

const fixSched = (s) => {
  const lat = num(s && s.lat), lng = num(s && s.lng);
  const pinned = okCoords(lat, lng);
  const type = str(s && s.type, 16).toLowerCase();
  return {
    id: str(s && s.id, 40) || uid("s"),
    day: DAYS.includes(str(s && s.day, 4)) ? str(s.day, 4) : DAYS[0],
    time: str(s && s.time, 24),
    dur: str(s && s.dur, 16),
    type: TYPES.includes(type) ? type : "activity",
    everyone: !!(s && s.everyone),
    activity: str(s && s.activity, 120),
    loc: str(s && s.loc, 160),
    cost: str(s && s.cost, 40),
    note: str(s && s.note, 240),
    lat: pinned ? lat : null,
    lng: pinned ? lng : null,
    url: str(s && s.url, 400) || null,
    by: str(s && s.by, 40) || null,
  };
};

const blank = () => ({
  legs: {},
  votes: {},
  tasks: SEED_TASKS.map((t) => ({ ...t, owners: [], notes: [] })),
  opts: SEED_OPTS.map((o) => fixOpt(o)),
  sched: SEED_SCHED.map((s) => fixSched(s)),
  base: fixBase({ label: "Villa", loc: VILLA, lat: VILLA_LAT, lng: VILLA_LNG }),
  meta: {},
  rev: 0,
});

const clean = (s) => {
  const b = blank();
  if (!s || typeof s !== "object") return b;
  return {
    legs: s.legs && typeof s.legs === "object" ? s.legs : b.legs,
    votes: s.votes && typeof s.votes === "object" ? s.votes : b.votes,
    tasks: (Array.isArray(s.tasks) ? s.tasks : b.tasks).map(fixTask),
    opts: (Array.isArray(s.opts) ? s.opts : b.opts).map(fixOpt),
    sched: (Array.isArray(s.sched) ? s.sched : b.sched).map(fixSched),
    base: fixBase(s.base && typeof s.base === "object" ? s.base : b.base),
    meta: s.meta && typeof s.meta === "object" ? s.meta : b.meta,
    rev: typeof s.rev === "number" ? s.rev : 0,
  };
};

/* ---- turning what someone typed into a map pin ---------------------------- */

// "-8.65, 115.19" pasted straight in.
function parseCoords(text) {
  const m = String(text).match(/^\s*(-?\d{1,2}(?:\.\d+)?)\s*,\s*(-?\d{1,3}(?:\.\d+)?)\s*$/);
  if (!m) return null;
  const lat = +m[1], lng = +m[2];
  return okCoords(lat, lng) ? { lat, lng } : null;
}

// Google Maps URLs carry coordinates in a few different shapes.
function coordsFromUrl(u) {
  // !3d!4d is the actual place pin, so it wins over the map centre.
  let m = u.match(/!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)/);
  if (!m) m = u.match(/[?&](?:q|query|ll|daddr|center|sll)=(-?\d+\.\d+),\s*(-?\d+\.\d+)/);
  if (!m) m = u.match(/@(-?\d+\.\d+),(-?\d+\.\d+)/);
  if (!m) return null;
  const lat = +m[1], lng = +m[2];
  return okCoords(lat, lng) ? { lat, lng } : null;
}

// maps.app.goo.gl links hide the coordinates behind a redirect.
async function expand(u) {
  try {
    const r = await fetch(u, { redirect: "follow", headers: { "user-agent": UA }, signal: AbortSignal.timeout(5000) });
    return r.url || u;
  } catch {
    return u;
  }
}

// Indonesian addresses are written in abbreviations that Nominatim doesn't
// know. "Gg. Daksina, Kerobokan Kelod" finds nothing; "Gang Daksina" finds it.
const ABBR = [
  [/\bGg\.?(?=\s)/gi, "Gang"],
  [/\bJl\.?(?=\s)/gi, "Jalan"],
  [/\bJln\.?(?=\s)/gi, "Jalan"],
  [/\bKec\.?(?=\s)/gi, "Kecamatan"],
  [/\bKab\.?(?=\s)/gi, "Kabupaten"],
  [/\bKel\.?(?=\s)/gi, "Kelurahan"],
  [/\bBr\.?(?=\s)/gi, "Banjar"],
  [/\bPerum\.?(?=\s)/gi, "Perumahan"],
];
const expandAbbr = (s) => ABBR.reduce((a, [re, to]) => a.replace(re, to), String(s || ""));

async function geocodeOnce(q, ms) {
  const query = /bali|indonesia/i.test(q) ? q : q + ", Bali, Indonesia";
  const url =
    "https://nominatim.openstreetmap.org/search?format=jsonv2&limit=1&viewbox=114.40,-8.03,115.75,-8.95&q=" +
    encodeURIComponent(query);
  try {
    const r = await fetch(url, {
      headers: { "user-agent": UA, "accept-language": "en" },
      signal: AbortSignal.timeout(ms),
    });
    if (!r.ok) return null;
    const j = await r.json();
    if (!Array.isArray(j) || !j.length) return null;
    const lat = num(j[0].lat), lng = num(j[0].lon);
    return okCoords(lat, lng) ? { lat, lng } : null;
  } catch {
    return null;
  }
}

// A full postal address often fails as one string but resolves once the
// trailing district/regency/postcode noise is trimmed off. Try progressively
// shorter versions, under a total budget so a save never hangs.
async function geocode(q) {
  const base = expandAbbr(q).trim();
  const parts = base.split(",").map((p) => p.trim()).filter(Boolean);
  const tries = [base];
  if (parts.length > 3) tries.push(parts.slice(0, 3).join(", "));
  if (parts.length > 2) tries.push(parts.slice(0, 2).join(", "));

  const deadline = Date.now() + 7000;
  for (let i = 0; i < tries.length; i++) {
    if (Date.now() > deadline) break;
    // Nominatim's usage policy is one request a second.
    if (i) await new Promise((r) => setTimeout(r, 1100));
    const hit = await geocodeOnce(tries[i], i ? 3000 : 5000);
    if (hit) return hit;
  }
  return null;
}

// Never throws and never blocks a save — no pin is an acceptable outcome.
async function resolvePlace(loc) {
  const text = str(loc, 160);
  if (!text) return { lat: null, lng: null, url: null };

  const bare = parseCoords(text);
  if (bare) return { ...bare, url: null };

  if (/^https?:\/\//i.test(text)) {
    let hit = coordsFromUrl(text);
    if (!hit) hit = coordsFromUrl(await expand(text));
    if (hit) return { ...hit, url: text };
    // A link we can't read coordinates from still names the place in its path.
    const named = text.match(/\/place\/([^/@?]+)/);
    if (named) {
      const g = await geocode(decodeURIComponent(named[1]).replace(/\+/g, " "));
      if (g) return { ...g, url: text };
    }
    return { lat: null, lng: null, url: text };
  }

  const g = await geocode(text);
  return g ? { ...g, url: null } : { lat: null, lng: null, url: null };
}

/* ---- ops ------------------------------------------------------------------ */

function apply(s, op) {
  switch (op && op.op) {
    case "setLeg": {
      const name = str(op.name, 40);
      if (!ROSTER.includes(name)) break;
      s.legs[name] = {
        arrFl: str(op.arrFl, 20),
        arrT: str(op.arrT, 10),
        depFl: str(op.depFl, 20),
        depT: str(op.depT, 10),
        note: str(op.note, 120),
      };
      break;
    }
    case "toggleVote": {
      const who = str(op.who, 40);
      const opt = str(op.opt, 40);
      if (!who || !opt) break;
      const cur = s.votes[opt] || [];
      s.votes[opt] = cur.includes(who) ? cur.filter((n) => n !== who) : [...cur, who];
      break;
    }
    case "addOpt": {
      const label = str(op.label, 80);
      if (!Array.isArray(s.opts)) s.opts = [];
      if (!label || s.opts.length >= 60) break;
      s.opts.push(fixOpt({
        id: uid("o"), label, day: op.day, when: op.when, note: op.note, by: op.by,
        loc: op.loc, lat: op.lat, lng: op.lng, url: op.url,
      }));
      break;
    }
    case "editOpt": {
      const i = (s.opts || []).findIndex((x) => x.id === op.id);
      if (i < 0) break;
      const prev = s.opts[i];
      const label = str(op.label, 80);
      s.opts[i] = fixOpt({
        ...prev,
        label: label || prev.label,
        day: op.day == null ? prev.day : op.day,
        when: op.when,
        note: op.note,
      });
      break;
    }
    case "deleteOpt": {
      const id = str(op.id, 40);
      if (Array.isArray(s.opts)) s.opts = s.opts.filter((o) => o.id !== id);
      delete s.votes[id];
      break;
    }

    case "addSched": {
      const activity = str(op.activity, 120);
      if (!Array.isArray(s.sched)) s.sched = [];
      if (!activity || s.sched.length >= 120) break;
      s.sched.push(
        fixSched({
          id: uid("s"),
          day: op.day,
          time: op.time,
          dur: op.dur,
          type: op.type,
          everyone: op.everyone,
          activity,
          loc: op.loc,
          cost: op.cost,
          note: op.note,
          lat: op._lat,
          lng: op._lng,
          url: op._url,
          by: op.by,
        })
      );
      break;
    }
    case "editSched": {
      const i = (s.sched || []).findIndex((x) => x.id === op.id);
      if (i < 0) break;
      const prev = s.sched[i];
      const activity = str(op.activity, 120);
      s.sched[i] = fixSched({
        ...prev,
        day: op.day == null ? prev.day : op.day,
        time: op.time,
        dur: op.dur,
        type: op.type == null ? prev.type : op.type,
        everyone: op.everyone == null ? prev.everyone : op.everyone,
        activity: activity || prev.activity,
        loc: op.loc,
        cost: op.cost,
        note: op.note,
        // Only present when the handler re-resolved the location for us.
        lat: op._geo ? op._lat : prev.lat,
        lng: op._geo ? op._lng : prev.lng,
        url: op._geo ? op._url : prev.url,
      });
      break;
    }
    case "setBase": {
      const prev = s.base || {};
      s.base = fixBase({
        label: op.label == null ? prev.label : op.label,
        loc: op.loc,
        // Only present when the handler re-resolved the location for us.
        lat: op._geo ? op._lat : prev.lat,
        lng: op._geo ? op._lng : prev.lng,
        url: op._geo ? op._url : prev.url,
      });
      break;
    }
    case "toggleEveryone": {
      const t = (s.sched || []).find((x) => x.id === op.id);
      if (t) t.everyone = !t.everyone;
      break;
    }
    case "deleteSched": {
      const id = str(op.id, 40);
      if (Array.isArray(s.sched)) s.sched = s.sched.filter((x) => x.id !== id);
      break;
    }
    // Drag and drop sends the position the row should land at within its day.
    case "reorderSched": {
      const list = s.sched || [];
      const i = list.findIndex((x) => x.id === op.id);
      if (i < 0) break;
      const d = list[i].day;
      const [row] = list.splice(i, 1);
      // Where the day's remaining rows sit in the flat array.
      const spots = [];
      list.forEach((x, k) => { if (x.day === d) spots.push(k); });
      if (!spots.length) { list.splice(i, 0, row); break; }
      const to = Math.max(0, Math.min(spots.length, Number(op.toIndex) || 0));
      const at = to >= spots.length ? spots[spots.length - 1] + 1 : spots[to];
      list.splice(at, 0, row);
      break;
    }
    // Kept so a tab left open on the previous version still works.
    case "moveSched": {
      const list = s.sched || [];
      const i = list.findIndex((x) => x.id === op.id);
      if (i < 0) break;
      const dir = op.dir < 0 ? -1 : 1;
      let j = i + dir;
      while (j >= 0 && j < list.length && list[j].day !== list[i].day) j += dir;
      if (j < 0 || j >= list.length) break;
      const [row] = list.splice(i, 1);
      list.splice(j, 0, row);
      break;
    }

    case "addTask": {
      const label = str(op.label, 160);
      if (!label) break;
      s.tasks.push({ id: uid("u"), label, hint: str(op.hint, 160), done: false, owners: [], notes: [] });
      break;
    }
    case "editTask": {
      const t = s.tasks.find((x) => x.id === op.id);
      if (!t) break;
      const label = str(op.label, 160);
      if (label) t.label = label;
      t.hint = str(op.hint, 160);
      break;
    }
    case "deleteTask":
      s.tasks = s.tasks.filter((t) => t.id !== op.id);
      break;
    case "moveTask": {
      const i = s.tasks.findIndex((x) => x.id === op.id);
      const j = i + (op.dir < 0 ? -1 : 1);
      if (i < 0 || j < 0 || j >= s.tasks.length) break;
      s.tasks.splice(j, 0, s.tasks.splice(i, 1)[0]);
      break;
    }
    case "reorderTask": {
      const list = s.tasks || [];
      const i = list.findIndex((x) => x.id === op.id);
      if (i < 0) break;
      const [row] = list.splice(i, 1);
      const to = Math.max(0, Math.min(list.length, Number(op.toIndex) || 0));
      list.splice(to, 0, row);
      break;
    }
    case "toggleTask": {
      const t = s.tasks.find((x) => x.id === op.id);
      if (t) t.done = !t.done;
      break;
    }
    case "toggleOwner": {
      const t = s.tasks.find((x) => x.id === op.id);
      const who = str(op.who, 40);
      if (!t || !ROSTER.includes(who)) break;
      if (!Array.isArray(t.owners)) t.owners = [];
      t.owners = t.owners.includes(who) ? t.owners.filter((n) => n !== who) : [...t.owners, who];
      break;
    }
    case "clearOwners": {
      const t = s.tasks.find((x) => x.id === op.id);
      if (t) t.owners = [];
      break;
    }
    // Older single-assignee pages may still be open in someone's tab.
    case "setOwner":
    case "claimTask": {
      const t = s.tasks.find((x) => x.id === op.id);
      const who = str(op.who, 40);
      if (!t) break;
      t.owners = ROSTER.includes(who) ? [who] : [];
      break;
    }
    case "addNote": {
      const t = s.tasks.find((x) => x.id === op.id);
      const text = str(op.text, 600);
      if (!t || !text) break;
      if (!Array.isArray(t.notes)) t.notes = [];
      t.notes.push({ id: uid("n"), by: str(op.by, 40) || "someone", text, at: now() });
      if (t.notes.length > 60) t.notes = t.notes.slice(-60);
      break;
    }
    case "deleteNote": {
      const t = s.tasks.find((x) => x.id === op.id);
      if (t && Array.isArray(t.notes)) t.notes = t.notes.filter((n) => n.id !== op.noteId);
      break;
    }
    case "setMeta": {
      const k = str(op.key, 40);
      if (k) s.meta[k] = str(op.value, 400);
      break;
    }
    default:
      break;
  }
  s.rev = (s.rev || 0) + 1;
  return s;
}

// Geocoding is async and apply() is not, so locations get resolved up front
// and handed to apply() on the op. An unchanged location keeps its existing pin
// rather than being looked up again on every edit.
async function prepare(state, op) {
  if (!op || (op.op !== "addSched" && op.op !== "editSched" && op.op !== "setBase")) return;
  const loc = str(op.loc, 160);

  if (op.op === "editSched") {
    const prev = (state.sched || []).find((x) => x.id === op.id);
    if (prev && prev.loc === loc) return;
  }
  if (op.op === "setBase" && state.base && state.base.loc === loc) return;
  if (!loc) {
    op._geo = true;
    op._lat = op._lng = op._url = null;
    return;
  }

  // Adding straight from the recommendations list, where the coordinates are
  // already known and verified. No point asking the geocoder again.
  const givenLat = num(op.lat), givenLng = num(op.lng);
  if (okCoords(givenLat, givenLng)) {
    op._geo = true;
    op._lat = givenLat;
    op._lng = givenLng;
    op._url = str(op.url, 400) || null;
    return;
  }

  const hit = await resolvePlace(loc);
  op._geo = true;
  op._lat = hit.lat;
  op._lng = hit.lng;
  op._url = hit.url;
}

function getClient() {
  const url = process.env.KV_REST_API_URL || process.env.kv_KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL || process.env.REDIS_REST_API_URL;
  const token = process.env.KV_REST_API_TOKEN || process.env.kv_KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN || process.env.REDIS_REST_API_TOKEN;
  if (!url || !token) return null;
  return new Redis({ url, token });
}

export default async function handler(req, res) {
  res.setHeader("cache-control", "no-store");

  const redis = getClient();
  if (!redis) {
    return res.status(503).json({
      error: "nostore",
      message: "Storage not connected yet. In Vercel: Storage, create a Redis database, connect it to this project, then redeploy.",
    });
  }

  try {
    if (req.method === "GET") {
      const raw = await redis.get(KEY);
      return res.status(200).json(clean(typeof raw === "string" ? JSON.parse(raw) : raw));
    }

    if (req.method === "POST") {
      let body = req.body;
      if (typeof body === "string") body = JSON.parse(body);
      const ops = Array.isArray(body) ? body : [body];
      const raw = await redis.get(KEY);
      let state = clean(typeof raw === "string" ? JSON.parse(raw) : raw);
      for (const op of ops.slice(0, 20)) {
        await prepare(state, op);
        state = apply(state, op);
      }
      await redis.set(KEY, JSON.stringify(state));
      return res.status(200).json(state);
    }

    return res.status(405).json({ error: "method not allowed" });
  } catch (e) {
    return res.status(500).json({ error: "server", message: String(e && e.message ? e.message : e) });
  }
}

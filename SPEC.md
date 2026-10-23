# Geography Coverage Quiz: Build Spec

Mobile-first Muse app (fullstack, saves data). Clone of HugeQuiz World 50K+ City Coverage, plus Niko's additions. Research basis: ~/workspace/geography-quiz/rea/ (REA extraction of the original's code and data).

## Verified original behavior (from worldcoverage.js and worldcities.csv)

- Dataset: 10,276 cities, population >= 50,000 exactly, 175 countries, sorted by population desc. Columns: display name; country slug; match key A; match key B (alias); population; unique key; lat; lng; rank within country; global rank. No continent field in the original.
- Levels: beg 1000 km / 20 min; int 500 km / 45 min; adv 250 km / 90 min; exp 100 km / 180 min. Custom radius (Premium in original): any integer 50 to 2,500 km, 180 min, score not saved.
- Matching: checked live on every keystroke; exact match after normalization (strip all spaces, lowercase, NFD strip diacritics U+0300-U+036F, extra letter map for Polish/Turkish/Nordic characters, strip apostrophes/hyphens/commas/periods). Two accepted keys per city (name + alias, e.g. Mumbai/Bombay). No autocomplete, no prefix matching, no submit button.
- Coverage: distance via spherical computeDistanceBetween / 1000 km, dist <= radius. Correct guess draws one circle (white stroke 0.5, blue fill #0000FF 0.25) plus a cosmetic animated green ring. Every remaining city within radius is counted, marked, and removed from the pool. NO chaining: covered cities get no circles.
- Markers: pin color by population band (12 bands from 10M+ down to 50-75K). Title: "population (country)".
- HUD: cities gotten/total; countries completed X/175; Top 100/250/500/1000 bars; 12 population-range bars. "Countries Remaining" list appears when >= 160 countries completed. Timer starts on first keystroke after level chosen; pause freezes; typing "alldone" or End Quiz button (confirm) ends; onbeforeunload warning once totalCities >= 250.
- End: score = cities covered. Premium in original: 25 largest missed as large magenta markers labeled "Name (#globalrank)". Confetti at 100%.
- Map (original): Google Maps v3, HYBRID, center (30, 0), zoom 3, max zoom 8, streetView and mapType controls off, some labels hidden by styles. Not reusable in an artifact; see decisions.
- Dead in original: population-covered percent never updates (popgotten/totalpop never written). Ours implements it for real.

## Niko's decisions (2026-10-17)

1. Typing: NO dropdown, NO suggestions. Pure recall, exact typing like the original. ("that defeats the quiz part of the game")
2. Map: NO labels during play. ("it defeats the quiz part again") Names only on the end screen after the game. Platform constraint found during build (2026-10-17): Muse artifacts only allow the built-in map control (vector styles light/dark/grayscale); satellite imagery is unavailable. Niko's decision: built-in map, dark style, all place-name labels off during play, no satellite.
3. Population floor: selectable option (not locked at 50K). Options to offer: 15K, 25K, 50K (default, original), 100K, 250K, 500K, 1M. Below-50K data comes from GeoNames cities15000.
4. Misses: NO feedback. A miss is a miss: wrong or out-of-scope guesses simply do nothing, no rejection message, no miss penalty display. Out-of-scope guesses treated the same. Coverage in a scoped game only fills cities inside the scope (assumption flagged to Niko, unchallenged).
5. Chain mode: NO (Niko, 2026-10-17). Covered cities never blast. No chain variant.
6. Duplicate names multi-blast (Niko, 2026-10-17, stated as how the current game works): a guess fires EVERY remaining city whose match key (name or alias) equals the guess, each with its own circle and radius fill. Verified in the data: 277 duplicate-name groups at 50K+, e.g. Springfield x5 (MO, MA, IL, OR, OH; display names carry the state, match key is just "springfield"), San Fernando x7, Santa Rosa x6, Santa Cruz x6, San Jose x5. This supersedes the REA inference of first-match-by-rank; Niko's statement of current behavior governs.
7. Saving: YES. Fullstack private Muse app: best scores per scope+radius+floor combo, settings, and unfinished-game resume.
8. Covered cities can fire (Niko, 2026-10-17, diverges from the original): matching runs against the full in-scope pool. A city auto-covered by an earlier blast but never directly guessed still fires its own circle when typed (once). Score counts each covered city once. Re-typing an already-fired city does nothing.
9. Units: miles (Niko, 2026-10-17). Radius stops are logical round miles: 10, 25, 50, 100, 250, 500, 1000; slider snaps to them. Classic tiers: Beginner 500 mi/20 min, Intermediate 250/45, Advanced 100/90, Expert 50/180. Exact km conversions rejected by Niko.
10. Alternate spellings (Niko, 2026-10-17): English AND local names both match (Munich/München). Extra match keys harvested from GeoNames alternatenames with collision filtering; matching checks all keys.
11. Timer is a setup option (Niko, 2026-10-17): classic presets, custom minutes, or No Time Limit (completion mode, elapsed counts up). Reaching 100% of any scope auto-ends into a win state: success message, celebration, stats (time, blasts fired, population, best-combo check).

## Our additions over the original

- Scope narrowing: World / continent (Africa, Asia, Europe, North America, South America, Oceania) / single country (175). Pool, totals, country tracking all shrink to scope. Needs the country-to-continent join (dataset prep task).
- Custom blast radius: presets (classic four) plus slider/input, 25 to 2,500 km.
- Population covered percent, working.
- Settings: sound on/off, pins show/hide, circle persistence, km/mi units, timer mode (classic per level / untimed / custom minutes).

## Live reference: original hit rendering (observed 2026-10-17, Africa Coverage at 250 km, played in browser)

- Correct guess (Cairo): +105, Cities 105/1359. A radius circle draws centered on the city and PERSISTS for the whole game.
- Newest circle is saturated blue; older circles remain but fade to pale lavender/periwinkle. Circles accumulate.
- Every covered city gets a small yellow/gold teardrop pin (DOM alt/title "population (country)", hover tooltip). The directly guessed city gets NO distinct pin in the original (ours adds a distinct hit marker as a deliberate improvement).
- HUD: +N delta by the counter, progress percent bar, Population Range bars and Largest Cities bars fill live, Countries X/Y updates on completion. Timer on this sibling started at 45:00 for the 250 km level.
- Original map is satellite hybrid WITH labels (our build deliberately differs: Niko chose no labels).
- Quirk: END QUIZ clicks did not end the quiz in that session.
- YouTube gameplay videos were blocked in the browser environment (Error 153); thumbnails corroborate the yellow pins.
- Note: sibling quiz pins are uniform yellow/gold; the World quiz's own code (worldcoverage.js) specifies population-band pin colors. Our build follows the World code.

## Dataset (built 2026-10-17, see data/DATA.md)

## Dataset (current: GeoNames-only, swapped 2026-10-19)

- data/cities-final.json (build input): 34,112 cities, 210 countries, built
  purely from GeoNames (CC BY 4.0) by data/build_geonames_only.py plus the
  approved fixups in data/fixup_clean.py (16 same-place record merges by a
  0.065-degree same-footprint rule; Wien restored as Vienna's canonical
  keyB). Every row traces to a GeoNames id (cities-final.provenance.json).
  Floor counts: 15K 34,112; 25K 22,847; 50K 12,381; 100K 6,276; 250K 2,452;
  500K 1,210; 1M 573. US pools: 15K 3,408; 25K 2,081; 50K 976. Full audit:
  data/CLEAN-REBUILD-REPORT.md and data/FIXUP-REPORT.md.
- History: the original build spliced the reverse-engineered HugeQuiz 50K
  set (10,276) with a GeoNames 15-50K band (31,522 combined after the
  2026-10-18 dedupe correction). Niko's 2026-10-19 IP rule (no shipped
  product on a reverse-engineered proprietary dataset) retired it; the
  spliced files remain in data/ as build history (see data/DATA.md).
- Display names are GeoNames names (Czechia, Eswatini, North Macedonia,
  Cabo Verde, Ivory Coast, Köln). Russia maps to Europe per GeoNames;
  Cyprus Europe; Timor-Leste Oceania.

## Mobile design

- Map fills the screen; guess input fixed at the bottom (the original's own mobile pattern), large tap targets.
- Setup screen before the clock starts: scope, floor, radius, timer.
- Stats in a collapsible bottom sheet; end screen with missed markers and lists.
- QA: full mobile pass at phone viewport before delivery, per standing artifact rules.

## Current state (2026-10-19, at tag good-suggest-opacity-2026-10-19)

- Name: GeoQuiz (slug city-coverage-quiz unchanged; all saved data carried over).
- Map: Leaflet 1.9.4 + Esri World Imagery satellite, CARTO dark fallback.
  (A MapLibre globe build shipped 2026-10-19 and was reverted 2026-10-21:
  the map never loaded on Niko's phone, twice, and the sandbox cannot
  verify a painted frame for it. Globe is parked; see DECISIONS.)
  Borders
  from Natural Earth 10m for BOTH layers at 0.02° simplification: country
  lines weight 2 / opacity 0.55, state lines 0.8 / 0.3. In country games the
  national outline is the dissolved union of the state polygons (shared edge
  exact, measured deviation 0). Completed regions shade light green
  (admin_1 in country games, admin_0 in world/continent). A region or
  country with zero pool cities at the floor counts as complete from
  game start and shades grey instead (the out-of-scope grey, #8b9096 at
  0.22, following the borders toggle), never green (2026-10-22, Niko;
  supersedes both the from-start-green rule and the 2026-10-21 rule that
  zero-pool states shade only once the game is actually complete);
  out-of-scope countries shade grey at the same 0.22 opacity. Each admin_0
  feature shades at most once per game (feature-index dedupe, 2026-10-19):
  slugs that share one Natural Earth feature (France with Réunion,
  Martinique, French Guiana, Mayotte, Guadeloupe; Morocco with Western
  Sahara; Spain with Gibraltar) shade that feature together, never stacked.
  Slugs whose cities vote for no feature take the nearest feature within
  2.0 degrees of their city centroid (Gibraltar, Jersey, Kiribati, Tonga,
  Marshall Islands, St. Vincent and the Grenadines).
- Matching: live per keystroke against primary + alias + GeoNames alternate
  keys; duplicate names multi-blast; covered-but-unfired cities can fire.
- Spelling correction always on with guards (additions-only evaluation,
  finishing-distance prefix safeguard, length-difference cap, substring ban).
  Since 2026-10-19 a correction win SUGGESTS instead of firing: one
  "Did you mean X?" chip above the guess input; tapping it fires through the
  normal corrected-fire path, any input change dismisses it, and it never
  appears for exact matches. Every fired match shows a toast: city-only name
  + fired count ("✓ Springfield ×5"); corrected fires show the corrected
  spelling.
- Guess field: a contenteditable element, not a form control; during play the
  app mounts zero input/textarea/select elements. It renders as a centered
  floating pill (width min(80vw, 24rem)) in the HUD-pill material (translucent
  dark fill, backdrop blur, same border); typed text and the
  "Type a city..." placeholder are center-aligned.
- HUD: two rows, merging into one compact row while the keyboard is open;
  board sized from visualViewport; the input layer is a transparent overlay
  anchored to the board's bottom and the map fills the whole board behind it,
  so the pill, the match toast, and the suggestion chip float over the map in
  both keyboard states (no solid band; 2026-10-22 redesign matching Safari's
  floating pills). There is no End button in the input row: ending a game
  runs through the Pause sheet's "End quiz" action. Circles and pins
  non-interactive except hit markers (tap shows name popup).
- Region counter (HUD sub-line, keyboard-merged HUD, stats sheet, end
  summary): the denominator is every admin_1 region of the country (every
  country in scope for world/continent games; world = 210), and the numerator
  counts fully covered regions plus zero-pool regions, which count from game
  start (and shade grey, above). US exception: the District of Columbia is
  excluded from the counter entirely, so the US denominator is 50; DC cities
  stay in the pool, DC shades normally, and covering DC never moves the
  counter (2026-10-22, Niko: "50, 50 states"). Labels: "states" in country
  scope, "countries" in world/continent scope.
- Setup: scope (World / continent / country via a searchable picker, United
  States pinned first and preselected), population floor 15K-1M, radius in miles
  (10/25/50/100/250/500/1000), timer classic/custom/no-limit with a 100% win
  state; won games close and never offer resume.
- Versioning: see VERSIONING.md (commit per verified round, tag before risky
  changes, getstate snapshots at every tag).

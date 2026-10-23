# Decisions Log: City Coverage Quiz

## 2026-10-17
- Clone scope: faithful to HugeQuiz World 50K+ (radii 1000/500/250/100 km,
  timers 20/45/90/180 min, exact-match with aliases, no chaining) from REA
  extraction of the original code and data. Premium paywall parked by Niko.
- No suggestions dropdown (Niko: defeats the quiz). Pure typing.
- No map labels during play (Niko: defeats the quiz). End screen may label.
- Population floor selectable: 15K/25K/50K/100K/250K/500K/1M. Sub-50K data from
  GeoNames cities15000 (CC BY 4.0); dedupe on (country, keyA) at union.
- Misses: zero feedback, no penalty display.
- Chain mode rejected. Duplicate names multi-blast instead (Niko, stated as
  current original behavior; supersedes REA first-match inference).
- Saving: fullstack artifact (settings, best scores, history, active game).
- Map: platform built-in control only; satellite unavailable. Niko chose dark
  style with all place-name labels off during play over holding the build.
- Continent mapping authority: GeoNames countryInfo (Russia Europe, Cyprus
  Europe, Timor-Leste Oceania).
- 2026-10-17 (later): alternate-key filter. The game matches on every
  keystroke and clears the input on a hit, so GeoNames alternate keys
  that are a strict prefix of a canonical name hijacked typing
  mid-word ("orl", an Orlando alternate, fired Orlando early).
  filter_alternates.py drops alternate keys that are a strict prefix
  of any canonical keyA/keyB form, plus all alternate keys shorter
  than 4 chars (inspected: IATA codes and fragments, no genuine local
  names, zero exceptions kept). 143,935 -> 133,303 alternate keys;
  23,198 of 31,173 cities keep at least one. Canonical aliases
  (wien, munchen, koln, praha) and the warszawa alternate verified to
  still resolve. The same filter is baked into build_alternates.py.
- 2026-10-17 (evening): map stack superseded. The bundled map control was
  rejected by Niko; a device probe proved Leaflet 1.9.4 + Esri World Imagery
  satellite tiles render inside an artifact on his phone (the audit sandbox
  blocks all external egress, so tiles can only be verified on device).
  Game rebuilt on Leaflet + Esri, CARTO dark no-labels as runtime fallback.
- 2026-10-18: app renamed GeoQuiz (catalog and in-app branding; slug and all
  saved data unchanged). Niko: "for now".
- 2026-10-18: spelling correction always on; the setup/settings toggle is
  removed. A corrected fire shows the correct spelling in a suggestion toast
  so Niko learns it (his words). Later the same day the toast generalized to
  EVERY match, exact or corrected, showing the city-only name and the number
  of cities fired ("✓ Springfield ×5"); corrected fires still show the
  corrected spelling. Misses and re-types of fired cities stay silent.
- 2026-10-18: completion shading. A state/province polygon fills light green
  when all its pool cities are covered (country scope); a country polygon
  fills the same way on completion (world/continent scope). Live, persistent
  through resume, follows the borders toggle.
- 2026-10-18: country picker lists United States first and preselects it;
  all other countries alphabetical below.
- 2026-10-18: correction guards after two hijack reports. Fuzzy correction
  evaluates only when a change ADDED characters (backspace can only ever
  exact-match); it never fires while the input is within finishing distance
  of a real pool name (the Springfield/Spring Hill backspace hijack); a
  length-difference cap (at most 1 under 11 chars, 2 at 11+) and a substring
  ban stop it supplying a name part never typed ("Charles" must not fire
  "St. Charles"). Two-edit corrections on long names still work
  ("Philadelphai" -> Philadelphia).
- 2026-10-18: map pan and keyboard saga, closed on device. Blast circles and
  covered pins are non-interactive (a post-match drag starts on the newest
  circle) and touch-action none covers the map subtree; the input bar owns
  the physical bottom edge so no map surface sits in the iOS home-gesture
  strip; the board sizes purely from visualViewport (the earlier
  position:fixed body pin hid the input behind the keyboard and was replaced
  by a scroll lock). Niko confirmed on phone: input visible above the
  keyboard, pans free of the app-switch gesture, timer ticking.
- 2026-10-18: the iOS chevron/Done accessory bar above the keyboard is the
  host app shell's accessory for web inputs. Page-side causes were removed
  one by one and the bar never changed on device (no form element, guess
  input the only text field mounted during play, search-type input
  experiment). The Muse chat's clean keyboard is its native composer,
  unavailable to artifacts (no native text-entry bridge). Mitigation
  shipped: while the keyboard is open the two HUD rows merge into one, so
  the map regains roughly the bar's height. A zero-form-control attempt
  (contenteditable guess field) is in flight at the pre-contenteditable tag.
- 2026-10-18: dead space at the top of the map removed: the game was
  double-counting a safe-area top inset the host shell already applies.
- 2026-10-18: guess field converted from a form control to a contenteditable
  element (the zero-form-control attempt against the host accessory bar).
  During play the app now mounts zero input/textarea/select elements; typing,
  matching, correction, and toasts run through the unchanged pipeline fed by
  the element's text; paste inserts plain text only. Shipped after the
  pre-contenteditable-2026-10-18 tag; whether the bar disappears is a
  device-only verdict, pending at this commit.
- 2026-10-18 (bug fix): the dataset dedupe was wrong, not just risky. DATA.md
  had assumed all 832 (country, keyA) collisions between the extended and 50K
  sets were the same city estimated by two sources; 349 were distinct
  same-name cities and got dropped (Burlington VT, found by Niko after a 100%
  US run where Vermont could never shade). Supersedes the 2026-10-17 dedupe
  entry: dedupe is by identity (name key + coordinates within 0.15 degrees).
  349 cities restored (180 US, 83 of them at 25K+); dataset 31,522 cities;
  US pools 15K 3,250 / 25K 1,925 / 50K 870 (unchanged at 50K). Restored rows
  appended to preserve saved-game indices. Companion rule change: regions
  and world-scope countries with zero pool cities at the chosen floor count
  as complete and shade green from game start (Vermont has no 50K+ city at
  all, so it could never shade at the 50K floor otherwise).
- 2026-10-18 (shipped): the corrected dataset is baked into the app (pools
  verified in play: US 1,925 at 25K, Burlington ×3 with Vermont shading in
  the same frame; 1,416 new alternate keys for restored cities, existing
  alternates unchanged). Zero-pool regions/countries shade green from game
  start. Borders rebaked from Natural Earth 10m for both layers (country
  weight 2/0.55, states 0.8/0.3; country-scope national outline dissolved
  from the state polygons, measured deviation 0 for US and Germany).
  Searchable country picker shipped ("germ" -> Germany only). Out-of-scope
  countries shade grey at the completion opacity. Played QA caught and fixed
  a slug-to-ISO regression mid-round; all evidence is from the post-fix
  build. Tagged good-datafix-borders-2026-10-18.
- 2026-10-18 (correction): the border claims in the entry above did NOT hold
  on Niko's device (screenshot, Germany game): the national outline still ran
  double in stretches and internal state borders varied in thickness. Cause:
  borders were stroked per polygon, so shared edges were drawn twice and the
  selected country stacked up to three outlines. Sandbox frames had judged
  the lines too leniently; device is the authority. Repair shipped the same
  evening: borders are now drawn as a noded, deduplicated segment mesh
  (shared segments drawn exactly once, offline census: 104,691 admin_0
  pieces drawn once), fills are stroke-free, and probe frames show single
  uniform lines. The reviewer still flags residual near-parallel segments
  in places (wide river borders deliberately not welded), so this stays
  UNVERIFIED until Niko's device confirms it.
- 2026-10-19: dataset source decision (Niko): no shipped or shared
  product rests on the reverse-engineered HugeQuiz dataset. The dataset
  was rebuilt from GeoNames only (34,128 rows, every row traced to a
  GeoNames id, counts reconciled exactly against the raw file) and two
  fixups were approved: Wien restored as Vienna's canonical keyB (the
  prefix filter had dropped it as an alternate; the tradeoff, Vienna
  firing mid-typing for Wiener Neustadt, is the behavior the game
  originally shipped with), and a same-place merge. The merge premise
  needed correction before execution: the rebuild report called 18
  close pairs identical-population doubles, but only 4 are (Kashan,
  Changhua, Nasimshahr, Binyamina); script assertions caught the
  discrepancy before any swap. Niko approved the corrected rule: merge
  the 16 pairs whose records sit within 0.065 degrees (same urban
  footprint), keep the state-line twins (Kansas City, Bristol,
  Texarkana) and the 3 far pairs (San Tin, Ahwiaa, Ad Dindar, 15-19 km
  apart) as distinct cities. Final dataset: 34,112 cities, 210
  countries (data/cities-final.json). Repo tagged pre-clean-data-
  2026-10-19 before the app swap, with a live state snapshot.

- 2026-10-19: GeoQuiz published to GitHub as the public repo
  nkavallar/geoquiz: the playable build (index.html), project docs, and
  the GeoNames data pipeline. Excluded: the REA extraction, both
  HugeQuiz-derived datasets, live state snapshots, and hidden_files.
  The Muse GitHub app cannot create repositories (API 403, a platform
  rule for app integrations), so the empty repo was created in the
  browser as Niko on his instruction to create it myself. The connector
  push transport rejects requests well below the documented 16 MiB
  snapshot limit, so the publish landed in three parts: docs and
  pipeline (53da327), the dataset (34d06fd), and index.html through
  GitHub's web upload (1870f14). All 17 files verified byte-identical
  (size and git blob SHA) after publishing.

- 2026-10-19: GitHub Pages enabled on nkavallar/geoquiz (deploy from
  main, root folder), so the published build is playable at
  https://nkavallar.github.io/geoquiz/.

- 2026-10-19 (later): nkavallar/geoquiz changed from public to private
  at Niko's direction ("I don't want this public accessible"). Making
  the repo private unpublished the GitHub Pages build with it; the
  hosted URL now returns GitHub's 404. Repo contents unchanged.

- 2026-10-19: Uneven green shading root-caused and fixed. shadedGeomsOf
  pushed one geometry per completed or zero-pool slug via the city-vote
  slugToFeature map, with no dedupe: France's Natural Earth feature is
  shared by six slugs (france, reunion, martinique, french_guiana,
  mayotte, guadeloupe) and composited to an effective 0.77 opacity in a
  completed world game, Morocco's feature twice (morocco,
  western_sahara) at 0.39, everything else once at 0.22. Found by
  replaying the shipped logic offline against the shipped data after
  Niko's report on his World 500K clear (1209/1210, 136/137 countries).
  Fix: feature-index Set dedupe across both push loops, plus a
  nearest-feature fallback (within 2.0 degrees of the slug's city
  centroid) for the six slugs that voted for no feature (kiribati,
  jersey, gibraltar, marshall_islands,
  saint_vincent_and_the_grenadines, tonga). Gibraltar lands on Spain's
  feature (no separate Gibraltar polygon at this fidelity), the same
  accepted shared-feature pattern. Verified played at 390px with pixel
  composites: France, Morocco, Spain all at the single-coat color, zero
  pixels at the old stacked colors; a fresh world 500K game shades 69
  distinct features from 73 zero-pool slugs. Separately, spelling
  correction no longer auto-fires at Niko's direction: a correction win
  shows one "Did you mean X?" chip above the guess input, tapping fires
  through the corrected-fire path, any input change dismisses it, and
  all existing gates are unchanged. Production state verified identical
  after the build (best_scores 5, history 7, active_game null).

- 2026-10-19: Map engine swapped from Leaflet (Web Mercator) to
  MapLibre GL with a globe projection, at Niko's direction ("true scale
  world map, not the Mercator"). MapLibre renders a true sphere zoomed
  out and transitions toward flat Mercator at regional zoom, so world
  view is undistorted and regional play is unchanged in feel. All layers
  re-implemented: segment-mesh borders, deduped completion shading and
  grey overlay, blast circles as geodesic destination-point rings (true
  ground circles at any latitude), population-band pins, hit-marker
  popups, end-screen reveals. maplibre-gl 5.24 is bundled, no runtime
  CDN. One boot regression was caught by the build audit (setProjection
  called before style load blanked the app) and fixed in the load
  handler. Verification gap, stated plainly: the QA harness could not
  capture in-play frames this round (software WebGL plus the sandbox
  tile lockdown wedged the probe), so checks 1-8 are source-verified
  only and the home screen is the only played frame; production data
  verified identical. Niko's device is the deciding check; restore
  point is tag good-suggest-opacity-2026-10-19.

## 2026-10-20: Canonical prefix hijacks left faithful
A sweep of the shipped dataset found the prefix-hijack pattern also exists among canonical city names themselves (145 of 1,842 in the US 25K pool: Jackson blocks Jacksonville, Pittsburg CA blocks Pittsburgh PA, Miami blocks Miami Beach/Gardens, Wichita blocks Wichita Falls, Dayton blocks Daytona Beach). The behavior is inherited verbatim from HugeQuiz, and longer names remain reachable by retyping after the short one fires. Decision (Niko, Oct 20, 2026): keep it faithful, do nothing. No pending-match guard. Do not re-raise.

- 2026-10-21: Globe reverted. The MapLibre build's map did not load on
  Niko's phone on 2026-10-19, and still did not load after the repair
  build re-gated layer readiness from "load" to "style.load" (verified
  in a local rig with tiles refused, but never with a painted frame:
  the QA sandbox renders WebGL in software and cannot capture one).
  Niko directed the revert ("Revert to previous map that actually
  worked if this can't be fixed"); a fix that cannot be verified
  before delivery does not count as fixable. GameMap.tsx was
  re-implemented on Leaflet 1.9.4 to the good-suggest-opacity-2026-10-19
  behavior (no Leaflet source snapshot existed; the segment-mesh
  builder and the App.tsx dedupe logic carried over unchanged),
  MapLibre removed entirely. Played verification: map paints in the
  harness, uniform shading in play, suggestion chip pass, production
  data field-identical including the unstarted World 500K slot.
  Standing rule from this episode: the globe (or any WebGL map) does
  not return unless its rendering can be proven before it reaches
  Niko's phone.

- 2026-10-21: The Leaflet revert was first done as a re-implementation
  from spec and shipped with blast circles and pins not showing on
  Niko's phone (the harness had verified layer counts, not visible
  frames; he caught it and rejected being the QA loop). Root divergence,
  found by decoding the surviving previous client (the share edition's
  compiled code in github-export/index.html) and diffing it against the
  re-implementation: the re-implementation invented four custom Leaflet
  panes and nine per-class layer groups fed by three effects, inverted
  hit-marker interactivity (popup on an inner dot instead of the r9
  marker), used pure #0000FF circle fills, and rendered missed labels
  as divIcon markers. The device-proven version uses no custom panes
  and ONE overlay layerGroup rebuilt by a single effect in the order
  grey, green, circles, pins, hits, missed, with fresh circles #2f6bff
  at 0.25 fading to #9aa8f0 at 0.1 and missed labels as permanent
  tooltips. The restore rebuilt the map layer from that recovered code;
  App.tsx (dedupe, fallback, chip) untouched. Frame-verified at 390px:
  Paris circle/marker/pins/shading visible, Burlington x3 and
  Springfield x6 with markers, Denver circle visible, chip pass,
  reload-resume visibly restored, end-screen labels visible. Only the
  hit-marker popup TAP lacks frame evidence (the probe cannot tap
  Leaflet paths by coordinate); its wiring is byte-identical to the
  version Niko played for days. Rules from this episode: a revert
  restores actual prior code, never a re-implementation from spec, and
  rendering claims require inspected frames, not counters.

- 2026-10-21: Hit-marker taps were dead on device after the restore.
  Cause, proven by diffing against the share edition's compiled client:
  a touch guard added during the restore called preventDefault() on
  every touchstart over the map except controls and popups; the proven
  build's guard also exempts .leaflet-interactive, and dropping that
  one selector suppressed the click Leaflet needs to open a marker
  popup (touch dead, mouse clicks fine, which is why no desktop-side
  check caught it). Fix: restore the exemption, matching the proven
  guard string exactly; the corrected selector is confirmed present in
  the shipped bundle and the audit passed clean. Data untouched,
  including Niko's in-progress World game.

- 2026-10-21: Popup dismissal on empty-map tap fixed. Same root family
  as the dead marker tap: the touch guard's preventDefault on
  touchstart suppressed the synthesized click Leaflet's close-on-click
  relies on, so on touch a popup only closed when another marker was
  tapped (mouse clicks already closed it). The guard now records the
  touchstart position, and a touchend that qualifies as a tap (within
  12px, not a drag or pinch) outside controls, markers, and the popup
  itself calls map.closePopup(). The .leaflet-interactive exemption is
  preserved verbatim; audit pass; resumed-game frame shows the map
  layer undisturbed; data untouched.

- 2026-10-21 (evening): Niko reported borders again showing mixed
  thicknesses and some states preselected green. Repair findings:
  (1) Preselected green had two causes: border pool cities falling
  just outside their state polygon (San Diego, El Paso, Laredo,
  Brownsville, six more) were assigned to no region, letting states
  complete without them; and zero-pool states shaded green from game
  start under the Oct 19 zero-pool rule. Fix: unassigned pool cities
  now take the nearest region, and zero-pool states shade only when
  the game is actually complete (this supersedes the zero-pool
  from-start rule for states; verified: a fresh US 100K game opens
  with zero states green, and Texas stays unshaded until its three
  border cities are fired, then shades). (2) Border thickness: the
  mesh weld snap widened to 0.01 degrees and a side-coverage pass
  reclassifies singly stored interior segments from country weight to
  state weight; US misclassified interior length at country weight
  fell from 10,545 km to zero, near-parallel sliver segments fell
  from 110 to 14 (US), 29 to 6 (DE), 1,136 to 188 (world admin_0).
  The thick bright dashes in Niko's view are gone in before/after
  frames. Standing residual, disclosed: about 188 near-parallel
  segments remain in the world mesh (about 3,732 km, mostly
  wide-river bank pairs at uniform country weight) and 14 in the US
  mesh at uniform weight; the build critic's P0 stands as improved,
  not eliminated. Device confirmation still pending.

- 2026-10-22: Hints feature shipped (settings toggle default on;
  tap an empty spot in a state or country to get a Show hint offer;
  clue targets the region's largest uncovered city; curated trivia
  layer of 393 clues across 204 countries plus a runtime attribute
  layer: capital status, largest-uncovered, rounded population,
  compass position; Another cycles to the next-largest). Production
  integrity verified field by field; the only settings change is
  hints:true.
- 2026-10-22: Hint popup flash fixed. The offer opens 240 ms after
  the tap, and the same tap's trailing click echo (Leaflet preclick
  plus synthesized mouse events) landed after the open and closed it.
  The hint popup now sets closeOnClick off, the validated tap handler
  cancels the touchend, mouse handlers drop touch-echo events, and a
  tap within 700 ms at the hint anchor is treated as the opening
  tap's echo. Dismissal still runs through the explicit tap path.
  Verified in the shipped bundle and mechanism; the harness cannot
  replay touch taps, so device proof is Niko's next tap.

- 2026-10-22: St. Augustine, FL is absent from the dataset (GeoNames
  population about 14K, under the 15K floor), so no curated hint clue
  was added for it. Offered as a curated below-floor exception like
  the Wien key; Niko decided: leave the dataset as is. No exception.

- 2026-10-22: Web edition re-published at Niko's direction ("Do it" on
  the Git route), reversing the Oct 19 move to private. The static
  edition (slug geoquiz) was re-synced to the current private app:
  restored Leaflet wiring, completion-shading dedupe, the suggestion
  chip, the states counter, Hints (393 curated clues plus the
  attribute layer), the zero-reserve visual-viewport keyboard layout,
  tap-to-dismiss popups, and inert attribution text; the localStorage
  shim now round-trips the hints setting (default on). Verified played
  at 390px in the static edition's harness and reconciled from the
  exported bundle: 34,112 rows, World 50K pool 12,381, US 50K 976,
  US 25K 2,081, Burlington x3 and Springfield x6 rows. The export is
  6,383,481 bytes (blob 00d18ee2). Because that file is over the
  connector's practical push limit, index.html is published through
  GitHub's web upload, and the visibility change back to public plus
  the Pages re-enable are done in the browser, the reverse of Oct 19.

## 2026-10-22: Astra QA pass on the web publish; assets, attribution, storage fixes
- QA (Codex Astra, xhigh) found the published tree lacked all 241 border GeoJSON assets the bundle fetches (plus app.js/app.css in the artifact's asset set): on Pages, borders, shading, hint regions, and the states denominator could never load ("0/0 states" was the missing-assets state, not a transient). All 243 asset files pushed (batches F to I) and verified live over HTTP and in a played game (0/49 states from the start, borders drawn).
- The web edition's storage shim swallowed localStorage write failures while reporting success; it now keeps an in-memory mirror so a save reported as saved survives the session.
- Stale attribution clause "; core city set from HugeQuiz" removed from the app (dataset is GeoNames-only); corrected line: "Geographical data from GeoNames (geonames.org), CC BY 4.0". Web copy re-synced and re-uploaded (commit ec3702c).
- Ledger completed retroactively for both browser uploads (8699f55, ec3702c); SPEC zero-pool wording aligned with the 2026-10-21 decision.
- Disclosure noted to Niko: the public DECISIONS file contains brief gameplay summaries from these logs (results and counts, no save files); trim offered, his call.

## 2026-10-22: Counter denominator is all regions; zero-pool regions done from the start, shaded grey
- Niko's rulings: "50, 50 states" (the US counter denominator is the 50 states, not the regions holding pool cities), then amended the same evening: "If there are states that do not have the minimum of population required for that config just mark them as done and instead of a green overlay make it a grey one."
- Rule now shipped in both editions: the counter denominator (HUD sub-line, keyboard-merged HUD, stats sheet, end summary) is every admin_1 region of the country, and every country in scope for world/continent games (world = 210). Zero-pool regions and countries count as complete from game start and shade grey (#8b9096 at 0.22, borders-toggle family) for the whole game, never green; this supersedes the 2026-10-21 at-completion shading rule and the earlier from-start-green rule. The District of Columbia is excluded from the US counter entirely (denominator 50, not 51); DC cities stay in the pool, DC shades normally when covered, and covering DC never moves the counter.
- Played verification (both editions): fresh US 50K "2/50 states" with Vermont and West Virginia grey; Delaware completion "3/50"; fresh World 50K "22/210 countries" with exactly 22 grey; Germany 50K "0/16"; US 1M runs 43/50 fresh to "50/50 states" at the win. Two expectations in the fix brief were wrong and were corrected by play, not shipped: the 15 US cities at the 1M floor sit in 7 states (the New York City boroughs are separate GeoNames rows), so fresh US 1M reads 43/50, not 45/50; and firing Washington at a 50 mi radius advances the counter by completing Maryland, not via DC (at 10 mi it does not advance, as required).
- Web edition re-synced from the fixed client and staged at github-export/index.html (6,385,574 bytes, blob 3300c720); the upload and live verification are the parent agent's step.

## 2026-10-22: Input row redesigned to match Safari's floating pills; End button removed
- Niko's direction: since the Safari keyboard accessory bar cannot be removed (WebKit form assistant; see the keyboard-bar audits), the game's own input row matches it instead: "let's make the top text input a center aligned bar with the same opacity as the safari one, all the black area in the screenshot should be transparent or matched opacity - just match how safari does it", and "It also doesn't need a end button".
- Shipped in both editions: the guess input is a centered floating pill (min(88vw, 26rem)) in the HUD-pill material (translucent dark fill, backdrop blur, same border), with typed text and the "Type a city..." placeholder center-aligned; the input layer is a transparent overlay anchored to the board's bottom and the map fills the whole board behind it, so the pill, the match toast, and the suggestion chip float over the map in keyboard-closed and keyboard-open states; the solid black band is gone. The End button is removed from the input row; the Pause sheet already offered "End quiz" (unchanged, verified working as the end path), so nothing was added there.
- Played verification (both editions, phone width): fresh US 50K "2/50 states"; Denver fires with marker and toast floating over the map; "Seatle" shows the "Did you mean Seattle?" chip above the pill and tapping it fires Seattle; Hints toggle round-trips through the web edition's shim; no frame showed off-center pill text or a surviving black background behind the input row. One stated limit: the probe environment offers only fixed viewport presets, so a literal reduced-height keyboard-open frame could not be captured; keyboard-open geometry rests on the unchanged visualViewport board anchoring and zero-reserve branch, with the bottom-anchored pill verified at both preset heights.
- Production data untouched: getstate read before and after the edit is identical (active_game 1, best_scores 6, game_history 8, settings 1). Web edition re-synced and staged at github-export/index.html (6,385,466 bytes, blob 3231c4c3); the upload and live verification are the parent agent's step.

## 2026-10-22: Input pill material corrected to Safari's frosted material (measured)
- Niko's screenshot verdict on the pill redesign: "Does this look transparent to you?" Pixel measurement from his screenshot: the game's pill read #09151a (near black, darker than the ocean behind it), while Safari's own pills read #222d37 (domain pill) and #22262e (accessory pill) over a pure black background: Safari's material is a frosted light-grey fill plus blur (it ADDS grey), and the game's fill was black at high opacity.
- Fix shipped in both editions: the input pill gets its own frosted material (a .cq-guess-input override, so the counter/timer HUD pills keep their dark material): fill rgba(118,118,128,0.35), backdrop-filter blur(20px) saturate(1.6), border rgba(255,255,255,0.14); the placeholder was lightened to rgba(235,235,245,0.55) to stay legible on the lighter fill. Width changed from min(88vw, 26rem) to min(80vw, 24rem), still centered.
- Acceptance was measured, not eyeballed: in a 390x844 in-play frame (US 50K, pill over the darkest map area), the pill interior sampled #2e323c at six points, within the ±18-per-channel band around Safari's #22262e (deltas +12/+12/+14) and lighter than the #0b0f14 background directly beside it (the HUD counter pill sampled #0b0e14 in the same frame, confirming its material is unchanged). Pill bounding box 312px on the 390px frame = 0.80 width fraction. Placeholder and typed text both readable. Caveat: the sandbox blocks Esri tiles, so the frame's map is the CARTO dark fallback, the darkest case; on device the same fill composites over satellite imagery.
- Production data untouched (getstate identical before and after: active_game 1, best_scores 6, game_history 8, settings 1). Web edition re-synced (client bundle byte-identical; the pre-sync diff isolated exactly the width class and the frosted CSS rule) and staged at github-export/index.html (6,385,726 bytes, blob 55e0c716); the upload and live verification are the parent agent's step.

## 2026-10-22: Keyboard-open strip below the board painted with map (layout-height board)
- Niko's report on the frosted-pill build: "Part of it works but the black bar between the keyboard and text box needs to be gone/transparent". Measured from his screenshot: map imagery extended only a sliver below the input pill, and the strip at Safari's domain-pill row read #03060d (near black). Cause: the board was sized to the reported visualViewport, so the page painted nothing in the zone where Safari floats its domain and accessory pills, and the host showed black there.
- Fix shipped in both editions: the board now extends to the full layout viewport height (window.innerHeight / clientHeight, sampled atomically in the same pass as the visual rect), while every interactive element stays anchored to the visualViewport rect exactly as before: bottom-anchored elements (the input layer, Leaflet's bottom controls) lift by the strip height (exposed as --cq-strip), and top-anchored elements are unaffected because the board's top is unchanged. The map layer fills the whole board, so the strip carries map imagery; the extended area is map only, never interactive UI. html/body/root backgrounds are transparent, and a theme-color meta (#0d2f42, deep ocean teal sampled from the map) is the blend fallback for host chrome tinting. Keyboard closed, layout height equals visual height and the composition is pixel-identical to the previous build; the game does not become scrollable.
- Verification: the mechanism is confirmed in the shipped client source (atomic viewport sampling, strip computation, transparent backgrounds, theme-color in both builds' index.html). Played checks in the private audit at 390x844: fresh US 50K "2/50 states", Denver and Seattle fired with hit markers, the "Seatle" chip appeared and fired Seattle on tap, and the frosted pill re-sampled #2e323c (inside the #22262e +/-18 band, matching the previous round). Production data identical before and after by getstate (active_game 1 with the same 98 covered / 19 fired, best_scores 6, game_history 8, settings 1). The static edition re-synced byte-identical (app.js and app.css md5-match the private dist; shim and 241 GeoJSON references intact) and played (a session reached 58/976 with the Pause sheet's "End quiz" present).
- Stated limit: neither builder's harness produced a keyboard-open simulation with a layout/visual height split (all captures are at fixed presets where the two viewports coincide), so no strip pixel samples are claimed. The on-device keyboard-open look remains the deciding proof, as in the earlier keyboard rounds.
- Web edition staged at github-export/index.html (6,386,661 bytes, blob 83354ded); the upload and live verification are the parent agent's step.

## 2026-10-23: Coverage fix: the map is sized to the largest viewport; root teal demoted to fallback seam
- Niko's reframing, from a keyboard-CLOSED Safari screenshot: the map still stopped short of the screen's bottom edge, leaving a black margin in which Safari's floating toolbar pill sits; the top edge already bled full-screen. His words: "the map just isn't full screen behind the overlay." The keyboard-open band is the same defect in the other state: the page's painted area is smaller than the physical screen.
- Root cause: the board was sized from the sampled visual rect. On iOS Safari the plain JS metrics (innerHeight, clientHeight) track the visual viewport while the floating toolbar is up, so even the 2026-10-22 layout-height extension inherited the underfill. The CSS largest-viewport units do not: 100lvh reports the full physical screen regardless of toolbar or keyboard state.
- Fix shipped in both editions: the sampler now takes, atomically, the maximum of the layout/ICB metrics, the visual rect's full extent, and 100lvw/100lvh measured in pixels through a hidden probe element, kept as a monotonic maximum that resets only when the viewport width changes; the board/map layer is sized from that largest viewport in both keyboard states. Interactive anchoring is unchanged: HUD pills, the guess pill, toast, chip, sheets, overlays, and Leaflet's bottom controls stay inside the visual rect via the strip offset, now fed by the largest-viewport strip (guess pill box unchanged, [39,782,312,50] at 390x844).
- The root canvas background shipped earlier the same day (html and body solid #0d2f42, per the sourced keyboard-band research memo: root color is the one declarative page-side candidate, theme-color having been dropped by Safari 26 as a tint input) stays ONLY as a fallback seam for any residual sliver the map genuinely cannot cover; it is not the mechanism of this fix.
- Verification (Chromium probe rig, candidate build assembled from the private dist + the static shim, then confirmed on the synced static build): in the split-viewport simulation (layout 844, visual 468.9 via page-scale 1.8) the board reported height 844 and strip 375.111, and pixel samples across the whole layout surface, including five rows below the visual bottom, are satellite texture (band y480-843: 23,067 distinct colors, zero black or near-black pixels; Esri tiles 18 loaded, 0 errors). Keyboard-closed identity holds: fresh US 50K "2/50 states", grey census only #8b9096 (259 paths, no green), HUD/pill geometry unchanged. Played checks pass: Denver 21/976 at the default 250 mi radius (15 at 50 mi, 18 at 100 mi), "Seatle" chip appears without auto-firing and fires Seattle on tap (32/976), Hints toggle persists across reload, Pause sheet holds "End quiz". Computed root backgrounds rgb(13, 47, 66) on html and body in both editions. Production data untouched: coordinator getstate reads before/after both edits are identical (active US 50K game, 98 covered / 19 fired, 6 best scores, history 1-8, settings unchanged).
- Pill-material note, as measured: the frosted pill's ±18 band around #22262e holds over the dark CARTO fallback (#2f333c samples); over bright Esri ocean the same translucent fill composites lighter and bluer (#294962 to #295b71, identical in private and static frames). The material itself did not change in either edit; the band figure was always a dark-backdrop measurement.
- Stated limit: the Chromium harness cannot reproduce iOS Safari's JS-metrics-vs-100lvh divergence, so the geometry numbers prove the mechanism where a split exists in Chromium; whether iOS Safari paints its toolbar/keyboard zones from the extended board is decidable only on Niko's device. Status in his terms: shipped, awaiting his look; NOT confirmed on device.
- Web edition re-synced byte-identical (app.js md5 4ee37a9853e50bfb9340da5fd2e2a011, app.css md5 1a88e43a68ff73f8cb24b24b34dde740; shim and 241 GeoJSON assets unchanged) and staged at github-export/index.html (6,388,119 bytes, blob fa067e1b, sha256 4bea063f0c14873e363e76efcc2cadf6c4545e70c0c527f6ec8902193c9b7831); the upload and live verification are the parent agent's step. SPEC.md layout/background description updated locally in the same round (parent pushes it with the rest).

## 2026-10-23: Black-band round 2: layer-structure fix (board portaled to body); device verdict pending
- Decisive device evidence: Niko ran the Astra round-3 probes on his iPhone and reported "R0 works in this example" (07:15 MDT). The clean harness page using the game's construction (fixed board, explicit height from the game's sampler, locked root, same meta and input) paints its pattern into the zone behind Safari's floating toolbar where the game shows black. Per the Astra consult, the paint path exists on the device; the defect is inside the game's own layer stack (its candidate 3, which the consult moves to first place when the clean harness succeeds and the game fails).
- Coordinator instrumentation of the actual game build (self-launched Chromium rig, 390x844, unsplit and page-scale split with visual 468.9 vs layout 844, real Esri tiles loaded): board rect, Leaflet container rect, and tile coverage all span the full layout height (844; tiles to y=984.9); every ancestor of the map container reports full height; no overflow/contain/transform/mask clip exists in the DOM; the container is sized from the same measure as the board, and in Chromium the split band already samples as satellite texture (24,530 distinct colors, 0 pure black). The DOM geometry was never the defect; the failure is in the layer structure WebKit composites. Structural deltas from R0: the board sat inside .hatch-space-root inside the SDK's position:fixed, overflow:auto space root; a plain absolute inset-0 div wrapped the Leaflet container; the container carried `isolate`. Full record: audits/coverage-diagnosis-2026-10-23/step1-findings.md.
- Fix shipped in both editions (private first, static re-synced byte-identical): (1) the play/end .game-board renders through ReactDOM.createPortal into document.body, a direct child of BODY with its whole subtree; home/setup/history unchanged; (2) the plain wrapper div between board and GameMap is removed, so the Leaflet container is a direct child of the board; (3) `isolate` is removed from the container's className. No change to the sampler, largest-viewport sizing, strip logic, HUD/input positioning, gameplay, or any server action.
- Verification: private builder's harness: keyboard-closed identity exact at 390x844 (sub-line "2/50 states · 0.0% of population", pill [39,782,312,50], Stats [246,12,58,34], Pause [312,12,66,34]); played checks (Denver 21/976 at 250 mi; "Seatle" chip with no auto-fire, tap fires Seattle to 58/976; Hints toggle persists across reload both ways). Static edition: app.js md5 322683d25b251ec2e499004cdab9edd2 and app.css md5 842cea6794f6a27fa087077b34b3d449 match the private build's new bundle (cmp byte-identical); 241 GeoJSON assets unchanged; the shim's five actions exercised end-to-end; played check on the static build passed (fresh US 50K "2/50 states", Denver 21/976, Seatle chip fires Seattle 58/976, portaled end screen renders). Production data untouched: coordinator getstate reads before and after both edits are identical (active US 50K game, 98 covered / 19 fired, runningSince 1792670376886, 6 best scores, history 1-8, settings unchanged).
- Unresolved, stated plainly: (a) the split-state band pixel measurement on the NEW build could not be produced by any artifact harness (no viewport-split control; audit egress blocks tile hosts), so the only split-band numbers on record are the pre-change Chromium ones above, from an engine that never reproduced the defect. (b) A parallel artifact inspection (106c32ce) put a competing probable cause on record: on real Safari the sampler's JS sources may all report the visual height (stripPx = 0 in practice), or Leaflet's cached size may never follow a grown board; the device readout that would decide it (the board's data-* geometry on the phone) does not exist. Its recommended next build (CSS 100dvh/100lvh board sizing with the sampler kept only for lifting interactive layers, invalidateSize at the settle moments, an on-device geometry readout) is NOT shipped here and was not authorized by that report; it is the candidate if Niko's look shows the band still black on this build.
- Status in Niko's terms: shipped, awaiting his look; NOT confirmed on device.
- Web edition staged at github-export/index.html (6,388,539 bytes, blob 4da40936, sha256 ebe610b872bec53190c7c9346110a1c03a8e3f4b6ec9d7f67793cac69abe433a); the upload and live verification are the parent agent's step.

## 2026-10-23 fallback round: CSS board sizing, invalidateSize, diagnostic readout

- Trigger: Niko reported the layer-structure fix did not cure the black band ("still showing black bar"). This round implements the fallback scoped by artifact inspection 106c32ce, targeting its two on-record competing causes: (a) on real Safari the sampler's JS sources may all report the visual height, so the board ends up at visual height in practice; (b) Leaflet's cached size may never follow a grown board.
- The build, four parts, shipped in both editions (private first, static re-synced byte-identical): (1) the play board's height comes from CSS only: `.game-board` declares `height: 100dvh` then `height: 100lvh`; the JS sampler no longer writes an inline board height (rig-verified: board inline height is empty, board's parent is BODY; last round's flattened portal structure retained). (2) The sampler is retained only to compute the strip offset lifting the interactive layers (HUD, guess pill, toast, chip, sheets, Leaflet bottom controls). (3) The map's invalidateSize is called at settle moments: initial settle, window resize, orientationchange, visualViewport resize, and the 100/350/700 ms keyboard focus-transition backstops. (4) A TEMPORARY diagnostic readout below the counter pill (small monospace, pointer-events none, format "L844 V469 B844 S375 M844": layout height, visual height, board client height, strip px, Leaflet container client height), updated at the settle moments. The readout is removed once the band question closes.
- Verification (coordinator's Chromium rig, private client/dist served with the static shim, real Esri tiles loaded): split state (page-scale 1.8, visualViewport 468.9 vs layout 844): board rect 390x844, Leaflet container rect 390x844, tile coverage to y=984.9; band rows 469..843 = 146,250 px, 24,703 distinct colors, 0 pure black; per-row samples are satellite texture (ocean teal #002840, land tan #b49673, green #324915 varying by position); the readout in the split state reads "L844 V469 B844 S375 M844" (unsplit "L844 V844 B844 S0 M844"). Keyboard-closed identity exact at 390x844: sub-line "2/50 states · 0.0% of population", pill [39,782,312,50], Stats [246,12,58,34], Pause [312,12,66,34]. Played checks: Denver 21/976 at the default 250 mi; "Seatle" chip appears with no auto-fire (counter unchanged before the tap) and a precise tap fires Seattle (37 covered in a fresh game); Pause sheet contains "End quiz". Static edition: app.js sha256 cba26f7005fccf6996b056b6d555141d0aebab30f4a922a2a502d3119147bf02 and app.css sha256 ee594bdc6ed4a61f07fed1427596d3dcf857843a055e0801c52503b74ca9f180 match the private bundle exactly (builder read-back); shim, 241 GeoJSON assets, and shell unchanged; the static build's played spot-check passed with the readout rendering. Production data untouched: coordinator getstate before/after identical (settings unchanged; active US 50K game 98 covered / 19 fired, runningSince 1792670376886; 6 best scores; history 1-8).
- Limits, stated plainly: (a) the Hints toggle flip was not re-measured this round: the rig's settings-row targeting missed with two finder strategies. The toggle code was untouched by this round's four scoped parts, its persistence was verified in earlier rounds, and production settings carry hints: true. (b) One rig run engaged the CARTO fallback after an Esri tile failure (band then measured 1,143 distinct colors, 0 pure black); the Esri run above is the satellite-texture evidence. (c) As in every round, Chromium cannot reproduce iOS Safari's compositing or metrics; the device question stays open by design, and the readout now puts the board's own numbers in Niko's next screenshot: B < L would mean the CSS board itself is short on device; B = L with a black band would clear sizing entirely and point back at compositing.
- Status in Niko's terms: shipped in both editions, awaiting his look; NOT confirmed on device.
- Web edition staged at github-export/index.html (6,390,039 bytes, blob f4b52ff9, sha256 f78dc0e1474680266afce25df5fb5f3797b9ed94ae3e7b772fe1cdd784de19dc, export and staged copy identical); the upload and live verification are the parent agent's step. SPEC.md updated in both copies (blob 22d52f59): board height is CSS 100dvh/100lvh, sampler demoted to strip offset and readout, invalidateSize at settle moments, diagnostic readout documented as temporary.

## 2026-10-23 rebuild: frozen oversize frame, flat canvas presenter, separate visible-UI surface (Astra design as amended) — SUPERSEDED the same day by the plain-fullscreen rebuild (see the final 2026-10-23 entry)

- Trigger: Niko directed that Astra design a rebuild ("Let astra help rebuilding; we're just going through circles and you're not getting it resolved"), replacing the patch cycle. The design (audits/codex-rebuild-consult-2026-10-23/main-answer.txt) was amended twice on device evidence before and during the build: (1) the Gate A page built on the design's exact-fit sizing (836, transparent surface) showed the bar in all five stages on device, while the R0 probe (pattern content built to 1,400px inside its board) is the construction the owner reported working, and a B1 probe shot in an in-app browser where the board measured 956 at load showed the pattern's blue band at the screen's bottom edge: the variable consistent with every device observation is the height of painted content relative to the physical screen, not the presenter and not layout fullness; (2) the flat teal zones appear at BOTH ends of the screen in Safari, top behind the status bar and bottom around the floating toolbar ("Top and bottom blue bars still in safari"), the teal being the root #0d2f42 that Safari's color-extension puts into its chrome zones, so the overshoot extends past both edges.
- What shipped, both editions: the sampler/strip machinery is deleted (largestProbeEl, measureLargestViewportUnits, boardBox, largestRef, the sampler viewport effect, kb geometry refs, --cq-strip, bottom:stripPx rules, .game-board 100dvh/100lvh heights). New modules: surfaceFrame.ts, visibleViewport.ts, FlatTileSurface.ts, ViewportDiagnostics.tsx (PlaySurface organization). The map surface is a frozen frame portaled to document.body: height = max(window.screen.height, the 100lvh measure, window.innerHeight, documentElement.clientHeight at init) + 256 (the R0 HG recipe), at position:fixed top -128, measured once before first focus after two equal nonzero rAF reads; epochs only on width change, orientation change, or host-frame change, never on keyboard/toolbar/focus/visual events. Leaflet runs trackResize:false; no invalidateSize from viewport/keyboard/focus events (exactly one per genuine epoch change); viewport events never move the camera (popup viewport adapter). The satellite layer is presented by a flat canvas (FlatTileSurface) drawing Leaflet's already-loaded tile images at their measured rects while the tile pane stays visibility:hidden; vectors, popups, borders, shading, and gameplay behavior are unchanged. Controls live on a separate visible-UI surface positioned in document coordinates from the visualViewport rect; HUD compactness derives from a visual-height reference. Initial scope framing compensates for the overshoot: the visible layout rect inside the surface starts at y=128 with height = the 100lvh measure at init, fitBounds paddingTopLeft [0,128] and paddingBottomRight for the bottom overshoot. The strengthened three-line readout stays in the build until the owner confirms on device.
- Verification (builders' rigs, frames looked at): private build readout at 390x844: L844 V844 B1100 S0 M1100 / C1100 F1100 P1100 O0 T-128 / SIZEΔ0 CACHEΔ0 INVALIDATE0 RESIZE0 NEWTILES0 CAMERAΔ0, counters still zero after focus, typing, and a fired guess; played frame inspected: fresh US 50K framing with grey shading, Springfield exact guess multi-blasted x5 with toast and +22 chip, 5 hit markers registered on the canvas-presented imagery (CARTO fallback tiles; Esri is egress-blocked in the audit sandbox and loads after publish, as in prior rounds), Stats sheet over the map, zoom/attribution in the visible area. Static edition: app.js sha256 3b0d1958ba50e534f8fa0cf7971bae7b6255c54cba434dce4db8e6e8d9d7a068 and app.css sha256 8614ccf113d14dc19ae66d0c22bd37a763427e7861669ff50eb060005aaf1bc2 byte-identical to the private bundle; all 241 GeoJSON assets byte-identical; the localStorage shim (five actions, hints default true) exercised end-to-end (save/resume at 380/976 restored exactly, settings persisted, finish recorded best + history, discard cleared the active game only); spot-check readout identical to the private rig; fresh US 50K "2/50 states", Denver fired, Springfield x5.
- Production data untouched: coordinator getstate reads before and after both edits are identical (settings unchanged; active US 50K game 98 covered / 19 fired, runningSince 1792670376886; 6 best scores; history 1-8).
- Stated limits, from the builders' own reports: (a) the full Gate B protocol (ten focus/dismiss cycles in a CDP split state) was not executed; the evidence is the counters at zero through focus/typing/a guess plus the architectural fact that no viewport/focus listener touches Leaflet; (b) pinch/fractional zoom, the hint popup flow, the correction chip, the pause/end flow, and orientation changes were not exercised in the private rig (Stats/Pause sheets and firing were covered in the static spot-check); (c) framing parity was judged visually against the owner's current-build screenshot and prior audit frames; no pre-edit rig baseline was captured before editing; (d) the audit's content critique could not confirm the amended frame formula from its truncated source captures (P0 noted); the live rig readout (F1100 = 844 + 256, T-128) is the counter-evidence; (e) iOS Safari paint remains decidable only on the owner's device, as in every round.
- Standing disclosure: the byte-identical app.css carries the pre-existing Google Fonts @import inherited from the private bundle (security critique, medium); removing it from one edition would break byte-identity, so it ships as-is in both. No step in this round made Google service calls or requested Google account access; the audit lockdown refused the page's own font request in the rigs.
- Status in Niko's terms: shipped in both editions, awaiting his look; NOT confirmed on device. Expected device readouts: Safari L836 with B=M=C=F=P about 1212, T-128, line-3 counters zero, and imagery (not flat teal) behind both the status-bar zone and the toolbar zone; Muse app L757 with B=M=C=F=P equal to the frozen frame.
- Web edition staged at github-export/index.html (6,397,583 bytes, blob c953f833, sha256 ff42ae0b573c3fe2d95b9f978eef72ea692deecada05572593fe7936154bac22, export and staged copy identical); the upload and live verification are the parent agent's step.

## 2026-10-23 plain-fullscreen rebuild: the game screen is an ordinary webpage — SUPERSEDED the same day by the locked-background rebuild (see the final 2026-10-23 entry)

- Trigger: the frozen-frame rebuild shipped and the owner rejected the whole measured-stage approach the same day. His directive, verbatim: "Instead of focusing on pixels and height it should just be full screen background like any webpage, the nav keyboard and other items are the overlay." Every shipped variant that sized the map as a measured stage (visual-rect sampler, layout-height board with strip offset, largest-viewport sampler, CSS 100dvh/100lvh board, frozen oversize frame) kept showing flat root-color zones in Safari's chrome areas on his device. This rebuild removes the entire category.
- What shipped, both editions: ordinary document flow. html and body height:100%; the board is a normal in-flow element inside the React tree (the body portal is gone) filling the page through the CSS height chain; the SDK wrapper gets a definite height and flex column only while the board is present (via :has(> .game-board)). Deleted entirely: surfaceFrame.ts, visibleViewport.ts, FlatTileSurface.ts, ViewportDiagnostics.tsx, the frozen frame (+256 allowance, top -128), the canvas tile presenter and its canvas element, the separate visible-UI surface, all geometry epochs, the three-line readout with its counters (SIZEΔ/CACHEΔ/INVALIDATE/RESIZE/NEWTILES/CAMERAΔ, T), and every viewport-geometry listener (visualViewport resize/scroll, window resize/orientation geometry handlers, ResizeObserver sizing, focus/blur geometry, settle timers). NO JavaScript viewport measurement of any kind remains: no element's size or position is computed from window.innerHeight, screen.height, clientHeight, visualViewport, or any probe element.
- Leaflet: the container fills the board via CSS (height:100%) and presents its OWN tiles normally (tile pane back to normal visibility; no hidden tile pane, no canvas drawing). Resize behavior returns to Leaflet defaults: trackResize on; there is no geometry invalidateSize machinery (no invalidateSize calls from viewport, keyboard, focus, or resize events). On a normal page the iOS keyboard does not resize the layout viewport, so none is needed. Initial scope framing is the plain pre-rebuild fitBounds with [18,18] padding (the overshoot padding compensation is gone).
- Overlays as ordinary webpages do them: HUD pills, the region strip, the guess input pill, the match toast, the "Did you mean" chip, gain chips, Stats/Pause sheets, dialogs, the sheet dimmer, and Leaflet's own controls are CSS-positioned overlays above the map (absolute within the board or fixed, z-index); no JS positions them from measured geometry. The compact merged HUD is driven purely by a max-height:540px media query. The contenteditable guess input and all its handlers are verbatim; programmatic focus uses focus({preventScroll:true}). The page is exactly one screenful of content, so there is nothing to scroll; no overflow:hidden stage lock remains for geometry.
- The diagnostic readout is reduced to the one plain line (L, V, B, S, M with the same definitions as before), display only: it reads values when it renders and its values never feed any layout, sizing, or positioning. It stays in for this confirmation round only and comes out after the owner's device confirmation.
- Verification (builders' rigs, frames looked at): private build at 390x844: resumed the saved US game with readout L844 V844 B844 S0 M844 (board and Leaflet container filling the full layout height through the CSS chain); fresh US 50K framing matches the pre-rebuild fitBounds framing (full US, grey out-of-scope shading, "2/50 states"); exact guess fired (Denver, covered 98 to 113, +15 gain chip, match toast); Springfield multi-blasted x5 (113 to 132); zoom controls worked; Stats sheet opened/closed; Pause sheet opened and End-quiz-from-pause rendered the end screen with missed-city labels; zero console errors in every frame; readout and camera unchanged across input focus and typing. Static edition probe at 390x844: fresh US 50K "2/50 states", readout "L844 V844 B844 S0 M844" as the only readout line, zero mobile overflow, zero console errors; Springfield fired a x5 multi-blast (359/976, 36.8%, 18/50 states, match chip shown) with framing and readout unchanged across focus/typing; Stats and Pause sheets opened and closed; Resume worked; Leaflet zoom visibly zoomed. Static bundle byte-identical to the private bundle (app.js md5 2e49b4806c60337cd0977f6674bedf4f, app.css md5 8462a61634fbdbb5e57700eef7f836e4); the localStorage shim in index.html is byte-unchanged (five actions, hints default true).
- Production data untouched: coordinator getstate reads before and after both edits are identical (settings unchanged with hints true; active US 50K game 98 covered / 19 fired, runningSince 1792670376886; 6 best scores; history 1-8).
- Stated limits, from the builders' own reports: (a) hit-popup open/dismiss and the hint offer could not be driven in the private rig (the probe can only click accessibly-named nodes and the map surface/SVG markers expose none); those tap/popup code paths in GameMap are byte-identical to the previous build (only the frame/canvas code was removed). (b) The CDP split-viewport keyboard state could not be emulated in the private rig's probe; focus plus typing in the full viewport showed no scroll and no readout/camera change. Desktop Chromium has never discriminated this defect in any round, so the split-state band question is, as ever, decidable only on the owner's device. (c) A cross-reload shim save/resume round-trip was not re-run in the static probe; the shim file is byte-unchanged from the previously verified build and in-session state persisted correctly. (d) At the rig's 390px width with a 3-digit covered count the HUD row's min-content width exceeds the row by about 10px and the Pause pill clips slightly; the row's markup and geometry are identical to the previous build and it fits the owner's 440pt-wide device.
- Standing disclosure (unchanged from the frozen-frame round): the byte-identical app.css carries the pre-existing Google Fonts @import inherited from the private bundle (security critique, medium); removing it from one edition would break byte-identity, so it ships as-is in both. No step in this round made Google service calls or requested Google account access.
- Status in Niko's terms: shipped in both editions, awaiting his look; NOT confirmed on device. The device look is the verdict.

## 2026-10-23 locked-background rebuild: scroll-locked page, CSS-overshoot fixed background (supersedes the plain-fullscreen rebuild)

- Trigger: the plain-fullscreen build failed on the owner's device within the hour. His Safari screenshot (Oct 23, 2026, 13:34 MDT, keyboard open) shows the normal-flow page SCROLLED on input focus: the HUD is gone from the top, the map framing shifted, and the zone above the keyboard shows flat root teal. His model stands unchanged ("full screen background like any webpage, the nav keyboard and other items are the overlay"), and a background does not scroll away when an overlay opens. The pre-plain locked-stage builds never scrolled on device; their defect was chrome-zone paint only. So this round keeps the scroll lock and drops the pixel machinery entirely.
- What shipped, both editions: (1) Root lock: html and body height:100% plus overflow:hidden and overscroll-behavior:none; the document is incapable of scrolling. (2) Background layer: .game-board is position:fixed with a CSS-only overshoot, top:-20%, bottom:-20%, left:0, right:0 (percentages of the viewport; no JS sizing, no pixel constants tuned to a device, no frozen frame). The Leaflet container fills the board completely; Leaflet presents its own tiles (no canvas presenter; that stays deleted) with default panes and layer order. (3) Overlays re-anchored to the LAYOUT rect, exactly where the plain-fullscreen build put them: HUD row, region strip, readout, end summary sheet, guess input bar, and the statistics/pause/end-confirm dialogs via position:fixed; Leaflet's bottom controls compensated in CSS (bottom: calc(84px + 100%/7)) so zoom and attribution keep their visible spot above the input pill. (4) Framing compensation: GameMap reads the board's rect ONCE at map init (only when inside .game-board), computes topOvershootPx = max(0, -rect.top) and bottomOvershootPx = max(0, rect.height - layoutHeight - topOvershootPx) against documentElement.clientHeight, stores them, and the framing fitBounds uses paddingTopLeft [18, 18+topOvershoot] / paddingBottomRight [18, 18+bottomOvershoot]; the setView path carries the equivalent center offset (zero under this symmetric construction); hit-marker and hint popups carry autoPan padding with the stored overshoots. That single init read is for framing only; nothing resizes or repositions the board afterward and no viewport listener touches map geometry. Maps outside .game-board (home backdrop) are untouched.
- Readout: the one plain line (L V B S M, display only) stays for this confirmation round; B and M now read the oversize board (about 1.4 times L), which is expected, not a defect.
- Verification (builders' rigs, frames looked at): private build at 390x844: readout L844 V844 B1182 S0 M1182 in every play frame (B = M = 1.4 x L exactly as the construction predicts); fresh US 50K and resumed-game framing pixel-identical to the plain-fullscreen build's audit frames (HUD at y=12, input pill at y=782, attribution y=674, zoom y=688/718 via the 100%/7 compensation); focus, typing, Denver fired (98 to 113), Springfield multi-blast x5 (to 132/976, identical progression to the plain build's QA), and clicking to other controls left the Leaflet camera and every overlay position unchanged; Stats sheet bottom-anchored to the layout rect, Pause dialog centered in it, End quiz from pause rendered the end screen; zero console errors. Static edition at 390x844: same readout, Denver (0 to 21/976) and Springfield x5 (to 380/976, 20/50 states) fired, Stats/Pause/end summary worked through the byte-unchanged localStorage shim; static bundle byte-identical to the private bundle (app.js md5 efec13be2b682d58ea7fd784d1fae572, app.css md5 180b66dbf1a644c879981e2ff707898d); all 241 GeoJSON assets verified byte-identical.
- Production data untouched: coordinator getstate reads before and after both edits are identical (settings with hints true; active US 50K game 98 covered / 19 fired in identical order, runningSince 1792670376886; 6 best scores; history 1-8); probe gameplay ran against sandbox copies only.
- Stated limits: (a) In the static probe, document scrollTop could not be read directly (no JS eval in the probe); the lock rests on the shipped html/body overflow:hidden CSS plus S staying 0 and the HUD never moving in any captured frame. The private rig did verify camera and overlay positions unchanged across focus/typing. (b) A hit popup for a city near the top edge could not be driven in either rig (markers are not probe-addressable); the autoPan overshoot padding is the in-code mitigation, unverified by a driven popup. (c) Esri tiles are egress-blocked in the audit rigs, so CARTO fallback tiles carried the visual checks there; the published page loads Esri directly as before. (d) Real-keyboard behavior and chrome-zone paint remain, as in every round, decidable only on the owner's device.
- Standing disclosure (unchanged): the byte-identical app.css carries the pre-existing Google Fonts @import inherited from the private bundle (security critique, medium); removing it from one edition breaks byte-identity, so it ships as-is in both. No step in this round made Google service calls or requested Google account access; the audit egress lockdown refused the page's own font requests.
- Status in Niko's terms: built in both editions, docs and assets published, index.html staged for the parent's upload step; shipped pending that upload, awaiting his look; NOT confirmed on device.

## 2026-10-23 visual-UI-anchor fix: all game UI rides the visible viewport (amends the locked-background rebuild)

- Trigger: the owner's Safari screenshot of the locked-background build (Oct 23, 2026, 14:08 MDT, keyboard open) shows the HUD row, region strip, and readout entirely absent while the bottom-anchored input pill is present and the map fills down to it. Mechanism: on keyboard open, iOS pans the visual viewport down over the layout (a probe readout on device showed visualViewport.pageTop about 312 in this state), so UI anchored to the layout top leaves the visible window. The sampler-era build's keyboard-open screenshot (05:12 MDT the same day) shows HUD and readout in place, because its UI rode the visible area.
- What shipped, both editions (anchoring only; board, scroll lock, framing compensation, gameplay, and persistence untouched): all play/end UI now lives in one UI root, a sibling overlay above the board, positioned in document coordinates from the visual viewport (left = pageLeft, top = pageTop, width/height from visualViewport), updated on visualViewport resize/scroll (rAF-coalesced) and on mount, with a layout-rect fallback when visualViewport is unavailable. Inside it: HUD row, region strip, the one-line diagnostics readout (format unchanged), the guess input bar with toast/gain/correction stack, the end summary sheet, and the statistics sheet, pause dialog, end-confirm dialog, and dimmer (dialogs centered in the root, sheets at its bottom). The compact merged HUD is now a class set from the visual height (540px threshold) instead of the layout-height media query. Leaflet's zoom/attribution controls stay in the map and are repositioned from the same visual rect via CSS variables published by the hook (controls only; no map geometry). SPEC.md's no-JS-measurement rule is scoped accordingly: the ban covers board/map sizing; UI anchoring to the visual viewport is the sanctioned exception, restored from the sampler-era behavior.
- Verification (builders' rigs, frames looked at): unpanned parity with the locked build at 390x844 (HUD y=12, pill bbox [49,782,293,50], readout "L844 V844 B1182 S0 M1182", framing identical, zoom bbox [348,688,30,30], attribution y=674); gameplay on sandbox copies in both editions (Denver fired with toast and gain chip, Springfield x5, Stats sheet and Pause dialog inside the UI root, End quiz from pause rendered the end screen; static edition also exercised the shim round-trip: 380/976 restored exactly after reload, settings persisted, finish recorded best + history and cleared the active game). Zero console errors. Stated limit: the rig cannot produce a nonzero visualViewport.pageTop, so the panned state is verified by the unpanned state plus the source-inspected anchoring path, not by a driven pan; the device look is the verdict for the keyboard-open state, as in every round.
- Production data untouched: coordinator getstate reads before and after are field-for-field identical (settings with hints true; active US 50K game 98 covered / 19 fired, runningSince 1792670376886; 6 best scores; history 1-8).
- Status in Niko's terms: built in both editions, awaiting the parent's docs/assets pushes and index.html upload, then his look; NOT confirmed on device.

## 2026-10-23 transparent background stack: Astra-authored transparency (amends the locked-background rebuild)

- Trigger: the owner's keyboard-open screenshot confirms the visual-UI-anchor fix on device (HUD and readout present; readout L736 V460 B1030 S276 M1030: in that state Safari reports the layout itself as 736 and the board's percentage overshoot follows it). The remaining defect is the flat teal block Safari shows in its chrome/extension zones. His direction, verbatim: "Needs to be transparent. Every website and app can do it. Fix it ffs. Let astra code it." The code in this round was authored by the Astra frontier model (consult output at audits/codex-transparent-build-2026-10-23/work/out/, with its full background audit in CHANGES.md) and applied VERBATIM through the builder interface in both editions; no Weeki-authored variant was substituted.
- The background-stack inventory, document to imagery, and what changed: (1) Shell: the <meta name="theme-color" content="#0d2f42"> and its "Blend fallback" comment are REMOVED (no replacement theme-color); an inline shell style resets html, body, [data-generated-space-root], .hatch-space-root and .hatch-space-root[data-hatch-space-root] to background: transparent !important before the app CSS loads; the static shell also lost its own pre-bundle teal paint. (2) theme.css: html/body no longer paint #0d2f42; the document canvas and the whole mount chain (including the SDK's compound root selector, whose installed stylesheet paints an opaque var(--bg)) are background: transparent !important. (3) Home wrapper: the solid bg-[#04070d] backing is removed (.cq-home-screen, transparent !important); home grading overlays are retained as foreground. (4) Board, UI root, and Leaflet host: transparent !important guards added; board geometry (fixed, top:-20%, bottom:-20%) byte-unchanged. (5) Leaflet: the container loses the app's #0b0f14 declaration and Leaflet's #ddd default via .leaflet-container, .cq-leaflet-host .leaflet-pane, .cq-leaflet-host .leaflet-tile-container { background: transparent !important; }; tile imagery is the first opaque surface in the play stack; provider selection/fallback untouched. (6) GameMap.tsx: the unused BOARD_BG constant is removed and a transparency comment added at the host render; executable code otherwise unchanged.
- Retained local fills: loading, error, and setup branches (no map in any of them) keep a local fill via the new .cq-no-map-screen { background: var(--bg); } class. App.tsx received exactly four class-string edits (loading, error, home, setup); everything from the play/end branch onward is byte-for-byte identical to the locked-background build, so geometry, the UI-root visual anchoring, framing compensation, the one-line readout, and gameplay are all preserved.
- Verification: post-build grep finds zero '0d2f42' in the client source, the built bundles, and the staged export; no theme-color meta in either shell or the staged export (only Astra's explanatory comment mentions it); the transparent !important guards are present in theme.css, the shell style block, and the compiled app.css (3 rules). Reverse-applying the edits to the static bundle reproduces the previous build byte-for-byte (app.js differs by exactly the four class edits; app.css by exactly the two rule replacements). Played QA at 390x844 in both editions, frames looked at: home renders on the transparent backing (backdrop, grading overlays, Play/Resume usable); setup legible on its local fill; fresh US 50K framing identical; Denver fired; Springfield multi-blast x5; Stats and Pause sheets open/close; readout reads exactly L844 V844 B1182 S0 M1182; static shim save/load round-trip restored the exact board after reload; zero console errors throughout.
- Finding reported, not fixed (per the verbatim brief): in the audit sandbox, where Esri/CARTO tiles are egress-blocked by design, the host's light canvas bleeds through wherever no imagery paints (the home screen's middle band reads as a pale grey-white wash with faint border outlines; the dark grading overlays still paint). No color was re-added. On the published page and in the app the tiles load, so imagery is the backing; what Safari composites into its chrome zones from a fully transparent stack is decidable only on the owner's device, as in every round.
- Production data untouched: getstate reads before and after both builds are field-for-field identical (settings with hints true; active US 50K game 98 covered / 19 fired in identical order, runningSince 1792670376886; 6 best scores; history 1-8).
- Publish state: static bundle re-synced; export at ~/workspace/your_files/geoquiz/geoquiz.html; staged at github-export/index.html (6,389,057 bytes, git blob 85623ed3, sha256 b4e2944efa75051ae7c807d2e647639dc679aa6bc76b7925e3142cf859b8aa42); assets app.js (sha256 2426dca0...) and app.css (sha256 7274bf23...) synced; docs and assets pushed via the connector; the index.html upload is the parent's browser step.
- Status in Niko's terms: shipped in both editions pending the parent's index.html upload, awaiting his look; NOT confirmed on device.

## 2026-10-23 full-bleed rebuild: real root scrolling, the map as a tall document (Astra-authored, second build)

- Trigger: the transparent-stack build's device verdicts. Keyboard open, the under-pill band is black instead of the authored teal and the map still does not composite there; keyboard closed, a black slab hosts the floating toolbar where the teal slab sat. The owner's correction: the defect was never the band's color, it is the band itself. The requirement is the map filling the entire physical screen behind all chrome in both keyboard states, the way ordinary edge-to-edge pages render (his reference screenshot of another site in Safari shows page content behind the toolbar capsule's margins on all sides). The page is handed a 736pt layout on a 956pt screen in every state, and the unpainted remainder is where the slab lives; ordinary pages get the full height. Astra was commissioned to WRITE the code against that target (Codex workspace-write run, audits/codex-fullbleed-build-2026-10-23/work/out/) and it was applied verbatim in both editions, as with the transparency round. Note: Astra's CHANGES.md for this run was lost to a runtime restart after the files were written; the design summary below is taken from the code comments in the shipped files.
- What shipped, both editions: (1) Real root scrolling during play/end only. theme.css scopes it with html:has(.game-board): the root becomes a true scrolling document (height auto, overflow-y: scroll), and the SDK wrappers ([data-generated-space-root], .hatch-space-root[data-hatch-space-root]) are forced position:static, height auto, min-height 0, overflow visible while the board is mounted, dismantling the SDK's fixed inset:0 mount that otherwise clips a normal-flow map. Non-game screens (home, setup, loading, error) keep the SDK shell via the html:not(:has(.game-board)) rules. (2) The board (.game-board) is normal-flow content: position:relative, width:100%, height var(--cq-map-document-height, 300lvh), touch-action:none. App's layout effect (useDocumentMapSurface) sets the height once per play/end mount to three screen spans (span = max of screen width, screen height, and layout height; frozen for the mount, keyboard and rotation included) and parks window.scrollY at one span BEFORE Leaflet initializes (layout-effect ordering), so a full span of real map content exists above and below the layout window for Safari to composite under its chrome. (3) User root scrolling is suppressed at the input level, not by clipping: document-level touchmove/wheel/keydown handlers cancel scroll gestures outside nested scrollable elements (sheets keep native scrolling), a scroll listener re-parks, history.scrollRestoration is manual during the mount, and cleanup restores the prior scroll position and height variable on unmount. (4) The visual-viewport UI root anchoring is unchanged in behavior; its fallback origin now reads the window scroll offsets, Leaflet's control offsets are computed from the map host's measured rect in document coordinates instead of the removed 1.2-times-layout formula, and GameMap's one-time framing compensation measures the map host element itself. (5) The full background transparency of the transparent-stack round is retained: no root colors reintroduced (grep for 0d2f42 stays zero), no theme-color meta; loaded tile imagery remains the first opaque surface in the play stack. (6) The one-line L V B S M readout stays for this confirmation round; B and M now read the tall document board. Gameplay, matching, persistence, and the data layer are untouched.
- Verification: the verbatim end state is proven in both editions. Private app: the builder replaced the four files with byte-for-byte copies (sha256 App 83d5286b, GameMap 6a1f8420, theme b2eb9085, index 6ce17b0d), the build succeeded, and the audit passed (nav 200, no console errors, no mobile horizontal overflow; home renders with Play/Resume/Stats intact). Disclosure from that build: the build pipeline itself modified bun.lock (a lockfile side effect of the build, not a hand edit); the four source files are the only hand-applied changes. Static edition: the four supplied files md5-match the private app's applied client source, and the shipped bundle is the private build's compiled bundle byte-for-byte (assets/app.js md5 493e97389c3ea6d9780defb84cffd2ec, assets/app.css md5 684cb40c7b39cb4afc4ca7eb3856af96); the localStorage shim is byte-unchanged and all 241 GeoJSON assets are untouched. Played QA at 390x844 (the static builder's probe-play plus the build's generic audit, frames looked at): home and setup render under the retained SDK shell; a fresh US 50K game starts with readout "L844 V844 B2532 S0 M2532" (B = M = 3 x 844, exactly the three-span document), sub-line "2/50 states", HUD, pill, zoom and attribution in their established positions and the framing composition matching the previous build; Denver fired (21/976) with hit marker, toast and gain chip, readout and framing unchanged; Pause opened as an overlay and End quiz from it rendered the end screen with missed-city labels and "New best for this setup" through the shim's finishGame path; zero console errors in every captured frame.
- QA coverage gaps, stated plainly (inspection f59cf765 of the static build): the bespoke probe items were not captured by any harness this round. Not directly evidenced: a seeded resume of a production-shaped game (98 covered / 19 fired), Springfield's five-city multi-blast on this build, touch-drag pan versus document scroll, the in-play Stats sheet open/close, and a focus-only step. The parked scroll position itself was never instrumented (no window.scrollY reading exists in any capture; the readout's S is L minus V, not a scroll offset), so the park rests on the verbatim-applied layout-effect code plus the observed 3x document height and stable framing, not on a measured scrollY. Denver exercised the same fire path Springfield uses, and Pause/Game Over exercised the same overlay pattern as the Stats sheet; the gameplay code is unchanged from builds whose full gameplay QA passed. No harness available here can produce iOS focus-scroll or Safari chrome compositing at all; the owner's device is the verdict for those, as in every round. The inspection recommended no code change on this evidence, only the probe, and none was made.
- Production data untouched: coordinator getstate reads before and after the private build are field-for-field identical (settings with hints true; active US 50K game 98 covered / 19 fired in identical order, runningSince 1792670376886; 6 best scores; history 1-8). All QA gameplay ran in the static shim or sandbox copies.
- Publish state: static bundle re-synced; export at ~/workspace/your_files/geoquiz/geoquiz.html; staged at github-export/index.html (6,394,546 bytes, git blob 465b83d9, sha256 e3901a6f5d6a569a2692d3545379bcbb9dcbec5449d4285bf9c4dea43467c2c7). Docs pushed via the connector with the remote root index.html blob checked before and after (85623ed3, unchanged). The repo's split assets/app.js and assets/app.css copies were NOT updated this round: reproducing them byte-exactly would require reading the artifact's built bundle directly, which stays on the builder side of the interface, and the staged export's inlined assets do not reproduce them as clean blocks. The staged index.html is self-contained (2 assets inlined, none unresolved), so the Pages deployment does not depend on the split copies; their last-synced state remains the transparent-stack bundle (batch AN).
- Standing disclosure (unchanged): the byte-identical app.css carries the pre-existing Google Fonts @import inherited from the private bundle (security critique, medium). No step in this round made Google service calls or requested Google account access; in the audit captures the font requests fail on the sandbox's egress lockdown, not in the app.
- Status in Niko's terms: shipped in both editions pending the parent's index.html upload, awaiting his look; NOT confirmed on device.

## 2026-10-23 readout removal: chrome item closed, diagnostics readout removed (final cleanup)

- Trigger: the owner's device verdict on the full-bleed build was "No change" (Oct 23, 2026, 16:07 MDT). On his terms (fix it or say it cannot be done), the full-screen/chrome item is CLOSED: across every construction tried (samplers, viewport units, frozen frames, overshoot, layer flattening, normal flow, locked background, visual-viewport UI anchoring, full background transparency, and the Astra-authored tall-document root-scrolling build), Safari's chrome zones on this page never composited the map, and the item is unreachable from page code as far as this project's evidence reaches. The full-bleed build STAYS as the game exactly as shipped; no further variants.
- The one edit in this round, both editions: the temporary one-line diagnostics readout (L V B S M) is removed. The DiagnosticsReadout component and its render block in the UI root are deleted from App.tsx, with comment-only cleanups in App.tsx and theme.css. Nothing else changed: the layout effect's scroll parking, the visual-viewport UI anchoring, the board, framing, gameplay, matching, persistence, and all other styling are preserved. The readout's values never fed any layout, sizing, or positioning (confirmed in source before removal).
- Verification: source and built bundle grep clean for data-diag-readout and DiagnosticsReadout in both editions; the static bundle is byte-identical to the private build's compiled bundle (app.js sha256 d71f7c2e98a261a5, app.css sha256 79497e70c0db2251; the static shell index.html is byte-unchanged, sha256 71147f723fef9a30). Played QA at 390x844, frames looked at, both editions: home screen normal; a fresh US 50K game frames as the full-bleed build did, with no readout line anywhere on the play screen; Denver fires with toast and gain chip; the Pause sheet opens; the static edition's localStorage round-trip restores the exact game after reload; zero console errors.
- Production data untouched: coordinator getstate reads before and after are field-for-field identical (settings with hints true; active US 50K game 98 covered / 19 fired in identical order, runningSince 1792670376886; 6 best scores; history 1-8).
- Publish state: static bundle re-synced; export at ~/workspace/your_files/geoquiz/geoquiz.html; staged at github-export/index.html (6,393,258 bytes, git blob 78bdc20b, sha256 005c02aedf30151f8); docs pushed via the connector with the remote root index.html blob checked before and after. The repo's split assets/app.js and assets/app.css copies are again NOT updated: the staged export inlines its assets and they cannot be reproduced byte-exactly from it; the staged index.html is self-contained (2 assets inlined, none unresolved), so Pages does not depend on the split copies; their last-synced state remains the transparent-stack bundle (batch AN).
- Standing disclosure (unchanged): the byte-identical app.css carries the pre-existing Google Fonts @import (security critique, medium), inherited from the private bundle. No step in this round made Google service calls or requested Google account access.
- Status in Niko's terms: shipped in both editions pending the parent's index.html upload. The chrome item is closed on his terms and the readout is gone; the play screen is in its final state.

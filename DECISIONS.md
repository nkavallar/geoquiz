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

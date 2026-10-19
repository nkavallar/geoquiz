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

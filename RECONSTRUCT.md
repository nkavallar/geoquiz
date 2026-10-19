# City Coverage Quiz: Reconstruct Notes

## What it is
Private Muse fullstack artifact, slug `city-coverage-quiz`, name "City Coverage Quiz".
Mobile-first clone of HugeQuiz World 50K+ City Coverage with player additions:
scope narrowing (World / continent / country), selectable population floor,
custom blast radius, saved scores/settings/history/resume.

## Sources of truth in this repo
- SPEC.md: full game spec, verified original behavior, all player decisions (dated).
- data/DATA.md: dataset sources, continent mapping calls, verification counts.
- data/build_data.py: rerunnable dataset build (GeoNames inputs in /tmp/geoquiz/).
- data/cities-compact.json: the exact dataset shipped to the builder
  (31,522 cities, 209 countries; dedupe on identity: (country, keyA) plus
  coordinates within 0.15 degrees; corrected 2026-10-18 by
  data/rebuild_compact.py, which restored 349 distinct cities the original
  name-only rule had dropped; restored rows are appended after the original
  31,173 so saved-game indices stay stable).
- data/cities-50k.json / cities-extended.json / continent-map.json: full datasets.

## Rebuild procedure
1. Recreate the dataset: python3 data/build_data.py (needs GeoNames cities15000.zip
   and countryInfo.txt from download.geonames.org, plus rea/worldcities.csv from
   https://hugequiz.com/html5/data/worldcities.csv), then regenerate
   cities-compact.json per SPEC.md dedupe rule (identity: name key plus
   coordinates), then run data/rebuild_compact.py if starting from the
   pre-fix compact file. Verify floor totals:
   15K 31,522 / 25K 20,344 / 50K 10,276 / 100K 5,360 / 250K 2,266 / 500K 1,097 / 1M 479.
2. Create a fullstack web artifact named "City Coverage Quiz" with the brief in
   SPEC.md (matching normalization, duplicate multi-blast, no chaining, silent
   misses, no labels during play, dark built-in map style; platform has no
   satellite imagery). Saved state: settings, best_scores (per scope+floor+radius),
   game_history, active_game.
3. QA at phone viewport: full game loop, resume after reload, end screen.

## Changelog
- 2026-10-17: initial build. Dataset built and verified; build completed and
  audit-verified (pool counts 10,276 world / 670 China at 50K; Beijing +27;
  resume restored 41/670). Sandbox audit could not render the basemap host;
  live map render to be confirmed on device.
- 2026-10-17 (evening): rebuilt on Leaflet + Esri World Imagery (device probe
  proof), CARTO fallback; covered-but-unfired cities fire; miles with logical
  stops, slider later removed; timer modes incl. no-limit completion mode and
  the 100% win state; GeoNames alternate spellings with prefix/short-key
  filters (the "orl" fix); borders overlay; home screen redesign approved.
- 2026-10-18: renamed GeoQuiz; spelling correction always on with the
  correct-spelling toast, generalized to a match toast with fired counts;
  completion shading (green regions); country picker USA first; correction
  guards (additions-only, prefix safeguard, length cap, substring ban);
  pan/keyboard fixes device-confirmed; top dead space removed; keyboard-open
  HUD merge. Repo brought current and tagged pre-contenteditable-2026-10-18
  with a live getstate snapshot (snapshots/) before the contenteditable
  guess-field experiment.
- 2026-10-18: contenteditable guess field shipped (zero form controls on the
  play screen; DOM audit clean; played regression green incl. a caught and
  fixed clear-on-fire regression). Accessory-bar outcome pending Niko's
  on-device verdict.
- 2026-10-18: dataset dedupe bug fixed. 349 distinct cities restored
  (31,522 total; US 25K pool 1,842 -> 1,925) after Niko found Burlington VT
  missing and Vermont unable to shade. Repo tagged pre-datafix-2026-10-18
  before the fix, with a live state snapshot.
- 2026-10-18: corrected dataset baked into the app and verified in play;
  zero-pool shading, matched-fidelity NE 10m borders with dissolved country
  outlines, border weight hierarchy, searchable country picker, and the
  grey out-of-scope overlay all shipped in the same round. Tagged
  good-datafix-borders-2026-10-18 with a live state snapshot.
- 2026-10-18: device check disproved that round's border claims (mixed
  outlines, uneven state lines). Borders rebuilt as a deduplicated segment
  mesh with stroke-free fills; pending Niko's device verdict before any new
  tag.
- 2026-10-19: dataset swapped to GeoNames-only (34,112 cities,
  data/cities-final.json; 16 same-place merges, Wien canonical exception,
  12 country slugs renamed with a stored-value remap). Attribution added:
  GeoNames CC BY 4.0. The spliced HugeQuiz-based dataset is retired from
  the app and kept in the repo as build history only.

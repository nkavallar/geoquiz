# GeoQuiz

Name a city. Blast the map. Cover the world.

A mobile-first geography quiz: type a city name and it blasts a radius
circle on a satellite map. Every city inside the circle counts as covered.
Narrow the game to the world, a continent, or a single country, pick a
population floor and a blast radius, and try to reach 100% coverage.

Play it by opening `index.html` (the whole game is one self-contained
file), or on GitHub Pages if enabled for this repo.

## How to play

- Setup: scope (World / continent / single country, searchable picker),
  population floor (15K to 1M), blast radius in miles
  (10 / 25 / 50 / 100 / 250 / 500 / 1000), and a timer (classic presets,
  custom minutes, or no time limit).
- Type a city name. Exact matches fire on the keystroke; duplicate names
  fire every city with that name at once. English and local spellings
  both work (Munich and München). A near-miss never fires on its own: it
  offers a "Did you mean X?" chip, and the city fires only when you tap
  the chip. Misses give no feedback: a miss is a miss.
- Covered regions shade green as you complete them; countries outside
  your scope sit under a grey overlay. In a single-country game the
  score line tracks completed states (for the US, "0/49 states" at the
  50K floor); world and continent games track countries. Reaching 100%
  ends the game in a win state.
- Hints (on by default, toggle in Settings): tap an empty spot inside a
  state or country and the game offers "Show hint". The clue describes
  the largest city you are still missing there without naming it;
  "Another" cycles to the next one. Famous places get a trivia clue
  ("Oldest city in America"); the rest are built from the data (capital
  status, size, position in the region).
- Settings, best scores, history, and an in-progress game save in your
  browser (localStorage). Nothing leaves the device.

## Data and attribution

- City dataset: built entirely from GeoNames. Geographical data from
  GeoNames (geonames.org), CC BY 4.0. 34,112 cities at the 15K floor,
  210 countries; see `data/` for the build pipeline and audit reports.
- Borders: Natural Earth (public domain), rendered as a deduplicated
  segment mesh so shared borders are drawn exactly once.
- Map tiles: Esri World Imagery (Esri, Maxar, Earthstar Geographics),
  with a CARTO dark no-labels fallback.

## Repository layout

- `index.html`: the game (self-contained build).
- `SPEC.md`: the living product spec. `DECISIONS.md`: dated decision
  log. `RECONSTRUCT.md`: rebuild manual. `VERSIONING.md`: the version
  and backup protocol.
- `data/`: the dataset pipeline (`build_geonames_only.py` builds
  `cities-clean.json` from GeoNames downloads staged in `/tmp/geoquiz/`;
  `fixup_clean.py` applies the approved merge and key fixups to produce
  `cities-final.json`, the file the game bakes in), with
  `CLEAN-REBUILD-REPORT.md` and `FIXUP-REPORT.md` as the audit trail.

## Development process

Changes land as commits; non-trivial changes go through a branch and a
pull request, and the git history is the tracking record (the same
process as the cave-map-restorer project). Dataset changes must keep
the provenance rule: every row traces to a GeoNames id, counts
reconciled against the source file before anything ships.

## License

Code: MIT (see `LICENSE`). City data: GeoNames, CC BY 4.0, attribution
above. This project began as a personal prototype inspired by coverage
quiz games; its shipped dataset and code are original work on open
data.

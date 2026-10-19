# Quiz Dataset: Sources, Mapping, Verification

**Superseded 2026-10-19.** The app now runs on a GeoNames-only dataset
(`cities-final.json`, 34,112 cities) built by `build_geonames_only.py`
plus the approved fixups in `fixup_clean.py`; see
`CLEAN-REBUILD-REPORT.md` and `FIXUP-REPORT.md` for the current source
of truth. This document describes the original spliced dataset (HugeQuiz
50K set + GeoNames band) and is kept as build history.

Built 2026-10-17 by `build_data.py` (kept alongside the outputs; raw stats in
`build_stats.json`). All counts below were verified against the written JSON
files in a separate pass after the build.

## Files

| File | Contents |
|---|---|
| `continent-map.json` | All 175 country slugs from the HugeQuiz CSV, each with `countryName`, `continent`, `iso` |
| `cities-50k.json` | 10,276 cities, population >= 50,000 (the original game's set) |
| `cities-extended.json` | 21,729 cities, population 15,000-49,999 (GeoNames), for sub-50K floors |
| `build_data.py` | The build script (rerunnable; GeoNames inputs expected in `/tmp/geoquiz/`) |

City record shape (both city files):
`{name, country (slug), countryName, continent, keyA, keyB, population, lat, lng, rankCountry, rankGlobal}`

## Sources

- **HugeQuiz `worldcities.csv`**, as extracted from hugequiz.com by REA reverse
  engineering (`~/workspace/geography-quiz/rea/worldcities.csv`). 10,276 rows,
  semicolon-delimited, no header: display name; country slug; match key A;
  match key B (alias); population; unique key; lat; lng; rank in country;
  global rank. This is HugeQuiz's own data; used here as the reference dataset
  for a personal clone of the game.
- **GeoNames** (`cities15000.txt` and `countryInfo.txt`, downloaded
  2026-10-17 from download.geonames.org). GeoNames data is licensed under the
  Creative Commons Attribution 4.0 License (CC BY 4.0).
  Attribution: "Geographical data from GeoNames (geonames.org), CC BY 4.0."

## Country-to-continent mapping

Authority: the continent code in GeoNames `countryInfo.txt`
(AF/ AS/ EU/ NA/ SA/ OC translated to Africa/ Asia/ Europe/ North America/
South America/ Oceania). Display names (`countryName`) are also the
countryInfo names.

The CSV slug is not an ISO code, so slugs were matched to countries by
normalized name (lowercase, non-alphanumerics stripped). 166 of 175 slugs
matched automatically. The other 9 needed an explicit alias because GeoNames
uses a different country name than the slug; each was resolved by hand:

| Slug | Resolved to | Why it did not auto-match |
|---|---|---|
| `congo` | CG, Republic of the Congo | GeoNames has no plain "Congo"; CD matched directly as "Democratic Republic of the Congo" |
| `cote_divoire` | CI, Ivory Coast | GeoNames name is "Ivory Coast" |
| `czech_republic` | CZ, Czechia | GeoNames name is "Czechia" |
| `macedonia` | MK, North Macedonia | GeoNames name is "North Macedonia" |
| `swaziland` | SZ, Eswatini | GeoNames name is "Eswatini" |
| `cape_verde` | CV, Cabo Verde | GeoNames name is "Cabo Verde" |
| `east_timor` | TL, Timor Leste | GeoNames name is "Timor Leste" |
| `palestine` | PS, Palestinian Territory | GeoNames name is "Palestinian Territory" |
| `netherlands` | NL, The Netherlands | GeoNames name has the leading "The" |

Display-name consequence: for those countries the app will show the modern
GeoNames name (Czechia, Eswatini, North Macedonia, Cabo Verde, Ivory Coast),
not the older name embedded in the HugeQuiz slug.

### Transcontinental / judgment calls (GeoNames value used in every case)

| Country | GeoNames continent | Note |
|---|---|---|
| Russia | **Europe** | GeoNames countryInfo assigns RU to EU despite most of its land area being in Asia |
| Turkey | Asia | |
| Egypt | Africa | Includes the Sinai (Asia) geographically; country-level value is AF |
| Kazakhstan | Asia | |
| Cyprus | **Europe** | GeoNames says EU (the UN geoscheme would say Asia) |
| Georgia, Armenia, Azerbaijan | Asia | |
| Panama | North America | |
| Indonesia | Asia | Country-level AS even though some islands sit in Oceania |
| Timor-Leste | **Oceania** | GeoNames assigns TL to OC |
| Spain, France, United Kingdom | Europe | Country-level EU; overseas territories are not separate rows in the 50K set |

Kosovo is present in countryInfo as XK, continent EU, and matched the
`kosovo` slug directly; no special handling was needed.

## Verification: cities-50k.json

- Row count: **10,276** (the raw CSV's last line has no trailing newline, so
  `wc -l` shows 10,275; parsed row count is 10,276).
- Minimum population: **exactly 50,000**. Maximum: 21,909,814 (Shanghai).
- Distinct countries: **175**. All rows have parseable coordinates, all within
  valid lat/lng ranges, none at 0,0.
- Rows are population-descending and the file's `rankGlobal` is sequential
  1..10,276 in row order (both checked).
- Per-continent counts (sum = 10,276, reconciles exactly):
  Asia 4,736; Europe 1,717; North America 1,356; Africa 1,340;
  South America 1,073; Oceania 54.
- `keyA == keyB` for 8,907 rows (no distinct alias); 1,369 rows carry a real
  alias in keyB.

### Top 20 countries (50K set)

| Country | Continent | Cities |
|---|---|---|
| India | Asia | 1,047 |
| United States | North America | 870 |
| China | Asia | 670 |
| Philippines | Asia | 590 |
| Brazil | South America | 559 |
| Japan | Asia | 482 |
| Russia | Europe | 314 |
| Pakistan | Asia | 249 |
| Mexico | North America | 216 |
| United Kingdom | Europe | 205 |
| Germany | Europe | 195 |
| Turkey | Asia | 185 |
| Iran | Asia | 185 |
| Spain | Europe | 153 |
| Egypt | Africa | 143 |
| Nepal | Asia | 142 |
| Italy | Europe | 138 |
| Argentina | South America | 132 |
| Nigeria | Africa | 131 |
| France | Europe | 131 |

## Cities-extended.json (GeoNames, 15K-49,999)

From `cities15000.txt` (34,166 rows, all feature class P by construction of
that file), keeping population 15,000 <= p <= 49,999: **21,729 rows**.
12,437 class-P rows fell outside the range (cities >= 50K, plus small
capitals below 15K that GeoNames includes in the file).

- Name = GeoNames `name`; country slug reuses the 50K-set slug for countries
  present there, otherwise derived from the countryInfo name (lowercase,
  spaces to underscores). `countryName` and `continent` come from
  countryInfo via the ISO country code.
- `keyA` = normalized asciiname (lowercase, spaces removed).
  `keyB` = normalized name if different from keyA, else the same value.
  4,707 rows have a distinct keyB.
- `rankCountry` / `rankGlobal` computed within the extended set,
  population descending, ties broken by name then GeoNames id; verified
  sequential (global 1..21,729; per-country 1..n).
- Observed population range: 15,001 to 49,993 (no source rows sit exactly on
  15,000 or 49,999/50,000 boundaries in this band).
- Per-continent counts: Asia 6,979; Europe 5,920; North America 3,603;
  Africa 2,434; South America 2,438; Oceania 355. Sum = 21,729.
- 205 distinct countries: the 175-set minus Barbados, Maldives,
  Sao Tome and Principe, and Eswatini (no GeoNames cities in the band), plus
  34 territories/small states absent from the 50K set (Andorra, Puerto Rico,
  Hong Kong, Malta, Monaco, Guam, etc.). A World-scope game at the 15K or
  25K floor therefore spans 209 distinct country values across both files.

## Floor counts (combined dataset: 50K set + extended set)

Total playable cities at each selectable floor, World scope:

| Floor | Cities |
|---|---|
| 15K | 32,005 |
| 25K | 20,742 |
| 50K | 10,276 |
| 100K | 5,360 |
| 250K | 2,266 |
| 500K | 1,097 |
| 1M | 479 |

Per continent at the 50K floor (= the original game's set):

| Continent | Cities at 50K |
|---|---|
| Africa | 1,340 |
| Asia | 4,736 |
| Europe | 1,717 |
| North America | 1,356 |
| Oceania | 54 |
| South America | 1,073 |
| **Total** | **10,276** |

(For reference, per-continent counts at every floor are in `build_stats.json`
under `floor_counts_by_continent_all`.)

## Data quality issues

1. **Cross-dataset name collisions at sub-50K floors (CORRECTED
   2026-10-18).** Population ranges do not overlap by construction (extended
   is strictly < 50,000, the 50K set is >= 50,000), so there is no overlap
   *by population*. But the two sources estimate populations independently,
   and **832 extended rows share (country, keyA) with a 50K-set city**. The
   original build assumed all 832 were the same real-world city estimated
   differently (true for e.g. Peine, Germany at 49,953 and Pordenone, Italy
   at 49,878) and dropped the extended copy on the name match alone. That
   assumption was wrong for 349 of the 832: same name, DIFFERENT city
   (Burlington VT vs Burlington NC; Charleston WV vs Charleston SC). Those
   349 distinct cities were missing from the game (found by Niko via
   Burlington VT, 2026-10-18). Corrected rule, applied by
   `rebuild_compact.py`: a row is a duplicate only when coordinates also
   agree within 0.15 degrees (483 of the 832 are same-place pairs and stay
   dropped). Restored dataset: 31,522 cities; US pools 15K 3,250 / 25K 1,925.
2. **Duplicate match keys are inherent to the source data.** In the 50K set,
   277 keyA values occur more than once globally (same-named cities in
   different countries; the original game resolves a typed name against the
   pool globally, so this mirrors original behavior). 0 duplicate unique keys
   (column 5). In the extended set, 432 (country, keyA) pairs are duplicated
   (same-named cities within one country).
3. **Populations are not comparable across the two files.** HugeQuiz's
   figures and GeoNames' figures come from different vintages/sources. Within
   one game this only matters at the seam described in issue 1.
4. No missing coordinates, no unparseable populations, and no unknown country
   codes were found in either file after filtering.

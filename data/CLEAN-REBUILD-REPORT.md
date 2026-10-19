# Clean Rebuild Report: GeoNames-Only Dataset

Built 2026-10-19 by `data/build_geonames_only.py`. Purpose: eliminate every
trace of HugeQuiz-derived data from the GeoQuiz dataset. The old
`cities-compact.json` spliced two sources: the entire 50K+ set (10,276 rows)
came from a reverse-engineered HugeQuiz CSV (names, keys, populations,
coordinates, ranks), and only the 15K-49,999 band was GeoNames. The clean
dataset below is one source end to end.

Nothing existing was overwritten. The swap into the app happens in a later
step after review.

## Inputs (fresh downloads, 2026-10-19, download.geonames.org)

- `cities15000.txt` (34,173 rows) and `countryInfo.txt`, staged in
  `/tmp/geoquiz/` per `build_data.py`'s convention.
- GeoNames data is CC BY 4.0. Attribution: "Geographical data from
  GeoNames (geonames.org), CC BY 4.0."
- `build_alternates.py` harvests alternate names from the alternatenames
  column embedded in `cities15000.txt` (not the separate alternateNamesV2
  file), so that is what this build uses too.

## Outputs

| File | Contents |
|---|---|
| `cities-clean.json` | `{countries: {slug: [countryName, continent]}, cities: [[name, slug, keyA, keyB, population, lat, lng, alternates], ...]}`, 34,128 rows sorted population-descending. The 8th element is the `\|`-joined alternate-key string, the exact shape the app build carries (the repo's `cities-compact.json` has 7 elements; the app-side `cities.json` produced from it by `build_alternates.py` has 8, with alternates in slot 8). |
| `continent-map-clean.json` | `{slug: {countryName, continent, iso}}`, same shape as `continent-map.json`, 210 countries (every country with at least one kept city), rebuilt purely from `countryInfo.txt`. |
| `cities-clean.provenance.json` | `[geonameid, ...]` parallel to the cities rows, so every output row traces to a GeoNames id. |

## Verification gates

### Provenance: PASS

- `build_geonames_only.py` contains no reference to the REA extraction or
  the old 50K file (grep for `worldcities`, `cities-50k`, `rea/`: no
  matches). Its only inputs are the two GeoNames files.
- Independent join of all 34,128 output rows against `cities15000.txt`
  via the provenance sidecar: 34,128 / 34,128 rows trace to a GeoNames id
  with name, population, and coordinates agreeing exactly. 0 mismatches.
  Provenance ids are all unique.

### Reconciliation: PASS, delta 0

Independent recount of the raw file (separate code from the builder):

| | Rows |
|---|---|
| Raw lines in `cities15000.txt` | 34,173 |
| Feature class not P | 0 (the file is class P by construction) |
| Unparseable population | 0 |
| Population < 15,000 (small capitals GeoNames includes in the file) | 45 |
| Unknown country code / non-mapped continent | 0 |
| Unparseable coordinates | 0 |
| Duplicate GeoNames ids | 0 |
| **Class-P rows with population >= 15,000** | **34,128** |
| **Rows in `cities-clean.json`** | **34,128** |

Every raw row is accounted for; nothing was dropped silently. Minimum
population in the output is 15,001 (no source row sits exactly on 15,000).

### Schema check: PASS

Top-level keys identical to `cities-compact.json` (`countries`, `cities`);
country values are `[str, str]` in both. Every clean row's first seven
fields have types identical to compact rows (`str, str, str, str, int,
float, float`); the 8th field (alternates) is a string on every row,
mirroring the app build. All coordinates in range, none at 0,0, rows
verified population-descending.

### Floor counts: old (spliced) vs clean

World:

| Floor | Old | Clean |
|---|---|---|
| 15K | 31,522 | 34,128 |
| 25K | 20,344 | 22,861 |
| 50K | 10,276 | 12,393 |
| 100K | 5,360 | 6,285 |
| 250K | 2,266 | 2,454 |
| 500K | 1,097 | 1,210 |
| 1M | 479 | 573 |

United States:

| Floor | Old | Clean |
|---|---|---|
| 15K | 3,250 | 3,408 |
| 25K | 1,925 | 2,081 |
| 50K | 870 | 976 |
| 100K | 352 | 356 |
| 250K | 93 | 94 |
| 500K | 39 | 42 |
| 1M | 12 | 15 |

The clean set is larger at every floor. That is expected and is the point
of the swap: the old 50K line was HugeQuiz's list (10,276 places they
chose to include), while GeoNames counts 12,393 places at 50K+ under its
own population estimates, which also run larger for many cities (Shanghai
24,874,500 here vs 21,909,814 in the HugeQuiz data; neither is wrong,
they are different sources and vintages, and now there is only one).

Per-continent counts, clean set at the 15K floor (sum = 34,128, exact):
Asia 12,590; Europe 8,164; North America 5,182; Africa 4,047;
South America 3,719; Oceania 426. Countries covered: 210.

### Spot checks: PASS

- **Burlington, VT** is its own row: population 42,452, GeoNames id
  5234372, 44.47588 / -73.21207. All five US Burlingtons are present
  (NC is now 52,472 in GeoNames, over the 50K line).
- **Charleston, WV** is its own row: 46,838, id 4801859.
- **Springfield, US at the 25K floor: 6 cities** (170,188; 154,341;
  114,394; 60,870; 59,680; 30,484), the same six the corrected spliced
  set produces, including Springfield, VA.
- **Shanghai is the top row**: 24,874,500, id 1796236.
- **Denver**: present, 729,019, id 5419384.

### Duplicate audit: PASS with itemized exceptions

Dedupe is on GeoNames id only, never on name. Grouping the clean set by
(country, match-normalized keyA): 884 groups covering 2,010 rows share a
key within one country (same-named distinct cities, the multi-blast
design). All group members have distinct GeoNames ids.

21 pairs inside those groups sit within 0.15 degrees on both axes and
were inspected individually against their GeoNames rows:

- Clearly separate municipalities (3 pairs): Kansas City, MO (475,378)
  vs Kansas City, KS (152,933); Bristol, TN (26,666) vs Bristol, VA
  (17,141); Texarkana, TX (37,280) vs Texarkana, AR (30,353).
  State-line twin cities, different admin_1, both real.
- GeoNames' own same-place double entries (18 pairs): the same place
  carried twice under variant romanizations, spellings, or as a section
  (PPLX) entry, e.g. Kashan / Kāshān (identical population 304,487),
  Chang-hua / Changhua (226,564), Nasimshahr / Nasīm Shahr (200,393),
  Ezhou, Xilinhot, Phu Quoc, La Ceiba, Lat Krabang, Kot Kapura, Banga,
  Ābyek, Panauti, Barbigha, Benito Juárez, Ahwiaa, Cañete, Ad Dindar,
  San Tin. Kept deliberately: they are distinct GeoNames records, the
  dedupe rule is id-only, and in play a typed name fires both, the same
  way the game already treats duplicate names. Flagged here so the
  swap review can decide if a coordinate-based merge pass is wanted;
  none was applied in this build.

  **Correction (2026-10-19):** the paragraph above mischaracterizes
  these pairs. Only 4 of the 18 have identical populations (Kashan,
  Changhua, Nasimshahr, and Binyamina-Giv'at Ada, the last missed by
  this audit's key grouping). The rest are city vs core/section records
  with different populations at small coordinate offsets, and 3 of the
  21 close pairs (San Tin, Ahwiaa, Ad Dindar) are 15-19 km apart and
  are distinct settlements, not doubles. The merge pass Niko approved
  (16 pairs by a 0.065-degree same-footprint rule, twins and far pairs
  excluded) is specified and logged in `FIXUP-REPORT.md`; the corrected
  audit trail lives there and in `fixup_clean.py`.

## Alternate keys

Same pipeline as the current dataset (`build_alternates.py` harvest
rules, then `filter_alternates.py` filters), with one simplification:
clean rows are GeoNames rows, so matching is by id exactly, with none of
the old name/coordinate matching losses.

- Harvested: 153,872 keys for 26,513 cities.
- Filters dropped 7,421 keys that are a strict prefix of a canonical
  name and 4,091 keys shorter than 4 characters.
- Final: **142,360 alternate keys on 25,607 cities** (old app build:
  134,719 keys on 23,473 cities). Canonical keyA/keyB were never
  filtered. 7,103 rows carry a keyB distinct from keyA.

Acceptance spellings re-checked against the clean data: Warszawa
(Warsaw) OK; München (Munich, via alternates) OK; Praha (Prague, via
alternates) OK; Köln OK (see below); Orlando, Tallahassee, West Palm
Beach OK. Regression keys `orl` and `mun` appear as alternates on no
city.

## Judgment calls and consequences to know before the swap

1. **"Wien" no longer resolves to Vienna.** In the old dataset, `wien`
   was Vienna's canonical keyB, a HugeQuiz alias, and canonical keys are
   exempt from the alternate filters by design. In the clean data,
   GeoNames names the city "Vienna" (keyA/keyB `vienna`) and "Wien" is
   only an alternate name. As an alternate it hits filter rule 1: `wien`
   is a strict prefix of the canonical key `wienerneustadt` (Wiener
   Neustadt), so it is dropped. Keeping it would make typing "Wiener
   Neustadt" fire Vienna at the fourth keystroke and clear the input,
   the exact hijack the filter exists to prevent. This is the specified
   pipeline working as designed; the old exemption existed only because
   the alias came from HugeQuiz. If Wien matters, the options are a
   curated canonical-alias exception (reintroduces the hijack tradeoff)
   or leaving it. Not decided here.
2. **Cologne's display name is now "Köln".** GeoNames' name field for
   the city is Köln (asciiname Koeln), so the row is
   `Köln / koeln / köln / 1,024,621`. Köln, Koln, Koeln, and Cologne all
   resolve. Display names across the dataset are GeoNames names now,
   which also means some cities display in local form where GeoNames
   prefers it.
3. **Country slugs are re-derived from countryInfo names**, since the
   old slugs were HugeQuiz strings. 12 renames, all the same country:
   `bosniaandherzegovina` -> `bosnia_and_herzegovina`,
   `cape_verde` -> `cabo_verde`, `congo` -> `republic_of_the_congo`,
   `cote_divoire` -> `ivory_coast`, `czech_republic` -> `czechia`,
   `east_timor` -> `timor_leste`, `guinea_bissau` -> `guineabissau`,
   `macedonia` -> `north_macedonia`, `netherlands` -> `the_netherlands`,
   `palestine` -> `palestinian_territory`, `swaziland` -> `eswatini`,
   `unitedkingdom` -> `united_kingdom`. Display names were already the
   GeoNames names (Czechia, Eswatini, North Macedonia, Cabo Verde,
   Ivory Coast, Timor Leste, etc.) and are unchanged. Saved settings
   that store a country slug (last scope) will need remapping at swap
   time for these 12.
4. **One genuinely new country: Antigua and Barbuda** (210 countries vs
   209 in the spliced set). Saint John's is 51,737 in current GeoNames,
   and the old set had no Antigua and Barbuda rows at any floor: the
   >= 50K band came only from HugeQuiz's list, which omits it, and the
   old GeoNames band stopped at 49,999.
5. **Row order changed** to purely population-descending (ties by name,
   then GeoNames id). Permitted per the task brief: no saved game in
   progress depends on row indices (the only active slot is an
   unstarted game with empty arrays).
6. Continent assignments are countryInfo's, unchanged from before:
   Russia Europe, Cyprus Europe, Timor-Leste Oceania.

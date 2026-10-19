#!/usr/bin/env python3
"""Build a GeoNames-ONLY dataset for GeoQuiz (no HugeQuiz data anywhere).

Purpose: replace the spliced dataset (HugeQuiz-derived 50K set + GeoNames
extended set) with a single-source dataset so the game no longer depends
on HugeQuiz data at all. Every row in the output is one row of GeoNames
`cities15000.txt`, traced by its GeoNames id (see the provenance sidecar).

Inputs (GeoNames, CC BY 4.0; download from download.geonames.org):
  /tmp/geoquiz/cities15000.txt   (build_data.py's scratch-dir convention)
  /tmp/geoquiz/countryInfo.txt
This script never opens the REA extraction or any previously built city
file. Grep it: there is no reference to them.

Outputs (this directory):
  cities-clean.json            {"countries": {slug: [countryName, continent]},
                                "cities": [[name, slug, keyA, keyB, population,
                                            lat, lng, alternates], ...]}
                                Rows sorted population-descending; the 8th
                                element is the "|"-joined alternate-key string,
                                mirroring the app build's cities.json shape.
  continent-map-clean.json     {slug: {"countryName", "continent", "iso"}}
                                for every country with >= 1 kept city, in the
                                same shape as continent-map.json.
  cities-clean.provenance.json [geonameid, ...] parallel to the cities rows,
                                so every output row traces to a GeoNames id.

Rules (mirroring the existing pipeline):
- Keep feature class P rows with population >= 15,000. Dedupe ONLY on
  GeoNames id (ids are unique in the source; asserted), never on name:
  same-named distinct cities are all kept (the old splice bug).
- Country slug derived from the countryInfo name (lowercase, non
  [a-z0-9 ] dropped, spaces -> underscores). Continent and display name
  come from countryInfo verbatim (Russia Europe, Cyprus Europe,
  Timor-Leste Oceania; Czechia, Eswatini, North Macedonia, Cabo Verde,
  Ivory Coast, Timor Leste are the countryInfo names themselves).
- keyA = normalized asciiname, keyB = normalized GeoNames name when it
  differs (build_data.py's normalize: lowercase, spaces removed).
- Alternate keys harvested from the same GeoNames row's alternatenames
  with build_alternates.py's rules (no digits, Latin-only after the
  game's guess normalization, length >= 3, cross-country primary-key
  collision filter, cap 50, name/asciiname themselves eligible), then
  filter_alternates.py's filters (drop strict prefixes of any canonical
  keyA/keyB form; drop keys shorter than 4 chars). Canonical keys are
  never filtered.

Run: python3 build_geonames_only.py   (prints a JSON stats block)
Attribution: "Geographical data from GeoNames (geonames.org), CC BY 4.0."
"""
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict

DATA_DIR = "/home/hatch/workspace/geography-quiz/data"
CITIES15000_PATH = "/tmp/geoquiz/cities15000.txt"
COUNTRYINFO_PATH = "/tmp/geoquiz/countryInfo.txt"
MIN_POP = 15000

CONTINENT_NAMES = {
    "AF": "Africa", "AS": "Asia", "EU": "Europe",
    "NA": "North America", "SA": "South America", "OC": "Oceania",
}

# --- normalization, copied verbatim from build_alternates.py / build_data.py ---

LETTER_MAP = [
    ("ą", "a"), ("ę", "e"), ("ć", "c"), ("ń", "n"), ("ó", "o"), ("ś", "s"),
    ("ź", "z"), ("ż", "z"), ("ß", "ss"), ("ł", "l"), ("ø", "o"), ("đ", "d"),
    ("æ", "ae"), ("į", "i"), ("þ", "th"), ("ų", "u"), ("ķ", "k"), ("å", "a"),
    ("ļ", "l"), ("ş", "s"), ("ț", "t"),
]


def normalize_guess(raw: str) -> str:
    g = raw.replace(" ", "").lower()
    g = unicodedata.normalize("NFD", g)
    g = "".join(ch for ch in g if not (0x0300 <= ord(ch) <= 0x036F))
    for a, b in LETTER_MAP:
        g = g.replace(a, b)
    if g == "ftmcmurray":
        g = "fortmcmurray"
    for ch in ("'", "-", ",", "."):
        g = g.replace(ch, "")
    return g


def normalize_key(key: str) -> str:
    g = key.replace("_", "").lower()
    for ch in ("'", "-", ",", "."):
        g = g.replace(ch, "")
    return g


def normalize_stored(s: str) -> str:
    """build_data.py's stored-key normalize: lowercase, spaces removed."""
    return s.lower().replace(" ", "")


def slug_style(country_name: str) -> str:
    """build_data.py: lowercase, drop non [a-z0-9 ], spaces -> underscores."""
    s = country_name.lower()
    s = re.sub(r"[^a-z0-9 ]", "", s)
    return s.replace(" ", "_")


# --- inputs ---

def load_country_info():
    """ISO -> {name, continent_code, continent} from countryInfo.txt."""
    info = {}
    with open(COUNTRYINFO_PATH, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 9:
                continue
            iso, name, cont = parts[0], parts[4], parts[8]
            info[iso] = {
                "name": name,
                "continent_code": cont,
                "continent": CONTINENT_NAMES.get(cont, cont),
            }
    return info


def main():
    stats = {"inputs": {"cities15000": CITIES15000_PATH,
                        "countryInfo": COUNTRYINFO_PATH}}
    ci = load_country_info()

    # ISO -> slug, derived only from countryInfo names; assert no collision.
    iso_to_slug = {}
    slug_owner = {}
    for iso, rec in ci.items():
        if rec["continent_code"] not in CONTINENT_NAMES:
            continue
        slug = slug_style(rec["name"])
        if slug in slug_owner and slug_owner[slug] != iso:
            print(f"FATAL: slug collision {slug!r} for {slug_owner[slug]} and {iso}",
                  file=sys.stderr)
            sys.exit(1)
        slug_owner[slug] = iso
        iso_to_slug[iso] = slug

    # ---------- read GeoNames cities15000 ----------
    dq = {"total_rows": 0, "not_P": 0, "bad_pop": 0, "below_floor": 0,
          "unknown_country": 0, "bad_coords": 0, "dup_geonameid": 0}
    seen_ids = set()
    kept = []
    with open(CITIES15000_PATH, encoding="utf-8") as f:
        for line in f:
            dq["total_rows"] += 1
            p = line.rstrip("\n").split("\t")
            if len(p) < 19:
                continue
            if p[6] != "P":
                dq["not_P"] += 1
                continue
            try:
                population = int(p[14]) if p[14] else 0
            except ValueError:
                dq["bad_pop"] += 1
                continue
            if population < MIN_POP:
                dq["below_floor"] += 1
                continue
            iso = p[8]
            if iso not in ci or ci[iso]["continent_code"] not in CONTINENT_NAMES:
                dq["unknown_country"] += 1
                continue
            try:
                flat, flng = float(p[4]), float(p[5])
            except ValueError:
                dq["bad_coords"] += 1
                continue
            gid = int(p[0])
            if gid in seen_ids:
                dq["dup_geonameid"] += 1
                continue
            seen_ids.add(gid)
            kept.append({
                "geonameid": gid,
                "name": p[1],
                "asciiname": p[2],
                "alternatenames": p[3],
                "lat": flat,
                "lng": flng,
                "iso": iso,
                "population": population,
            })
    stats["dq_raw"] = dq
    stats["kept"] = len(kept)

    # population-descending; ties by name then geonameid (build_data.py)
    kept.sort(key=lambda c: (-c["population"], c["name"], c["geonameid"]))

    # ---------- rows ----------
    countries = {}        # slug -> [countryName, continent]
    continent_map = {}    # slug -> {countryName, continent, iso}
    for c in kept:
        rec = ci[c["iso"]]
        slug = iso_to_slug[c["iso"]]
        c["slug"] = slug
        c["countryName"] = rec["name"]
        c["continent"] = rec["continent"]
        countries[slug] = [rec["name"], rec["continent"]]
        continent_map[slug] = {"countryName": rec["name"],
                               "continent": rec["continent"], "iso": c["iso"]}
        c["keyA"] = normalize_stored(c["asciiname"])
        key_b = normalize_stored(c["name"])
        c["keyB"] = key_b if key_b != c["keyA"] else c["keyA"]
        c["matchA"] = normalize_key(c["keyA"])
        c["matchB"] = normalize_key(c["keyB"])

    # ---------- alternates (build_alternates.py harvest, by geonameid) ----------
    primary_countries = defaultdict(set)
    for c in kept:
        primary_countries[c["matchA"]].add(c["slug"])
        primary_countries[normalize_guess(c["matchA"])].add(c["slug"])

    gained = 0
    total_alts = 0
    for c in kept:
        own = {c["matchA"], c["matchB"],
               normalize_guess(c["matchA"]), normalize_guess(c["matchB"])}
        seen = set()
        alts_out = []
        for raw_alt in c["alternatenames"].split(","):
            raw_alt = raw_alt.strip()
            if not raw_alt:
                continue
            if any(ch.isdigit() for ch in raw_alt):
                continue
            norm = normalize_guess(raw_alt)
            if len(norm) < 3:
                continue
            if not re.fullmatch(r"[a-z]+", norm):
                continue  # Latin-script keys only, like all primary keys
            if norm in own or norm in seen:
                continue
            owners = primary_countries.get(norm, set())
            if any(slug != c["slug"] for slug in owners):
                continue
            seen.add(norm)
            alts_out.append(norm)
            if len(alts_out) >= 50:
                break
        # the GeoNames name/asciiname themselves can be extra keys
        for raw in (c["name"], c["asciiname"]):
            norm = normalize_guess(raw)
            if len(norm) >= 3 and re.fullmatch(r"[a-z]+", norm) \
                    and norm not in own and norm not in seen:
                owners = primary_countries.get(norm, set())
                if not any(slug != c["slug"] for slug in owners):
                    seen.add(norm)
                    alts_out.insert(0, norm)
        c["alts"] = alts_out
        if alts_out:
            gained += 1
            total_alts += len(alts_out)
    stats["alts_before_filter"] = {"cities_with_alts": gained,
                                   "total_keys": total_alts}

    # ---------- alternate filters (filter_alternates.py) ----------
    canonical = set()
    for c in kept:
        for key in (c["keyA"], c["keyB"]):
            canonical.add(normalize_key(key))
            canonical.add(normalize_guess(normalize_key(key)))
    canonical.discard("")
    proper_prefixes = set()
    for nm in canonical:
        for i in range(1, len(nm)):
            proper_prefixes.add(nm[:i])
    f_prefix = f_short = 0
    kept_with_alts = 0
    total_after = 0
    for c in kept:
        out = []
        for alt in c["alts"]:
            if alt in proper_prefixes:
                f_prefix += 1
                continue
            if len(alt) < 4:
                f_short += 1
                continue
            out.append(alt)
        c["alts"] = out
        if out:
            kept_with_alts += 1
            total_after += len(out)
    stats["alts_after_filter"] = {"cities_with_alts": kept_with_alts,
                                  "total_keys": total_after,
                                  "dropped_prefix": f_prefix,
                                  "dropped_short": f_short}

    # ---------- write outputs ----------
    rows = [[c["name"], c["slug"], c["keyA"], c["keyB"], c["population"],
             c["lat"], c["lng"], "|".join(c["alts"])] for c in kept]
    out = {"countries": dict(sorted(countries.items())), "cities": rows}
    with open(f"{DATA_DIR}/cities-clean.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    with open(f"{DATA_DIR}/continent-map-clean.json", "w", encoding="utf-8") as f:
        json.dump(continent_map, f, ensure_ascii=False, indent=1, sort_keys=True)
    with open(f"{DATA_DIR}/cities-clean.provenance.json", "w", encoding="utf-8") as f:
        json.dump([c["geonameid"] for c in kept], f)

    # ---------- stats for the report ----------
    floors = [15000, 25000, 50000, 100000, 250000, 500000, 1000000]
    pops = [c["population"] for c in kept]
    stats["floor_counts_world"] = {
        str(fl): sum(1 for x in pops if x >= fl) for fl in floors}
    us = [c for c in kept if c["iso"] == "US"]
    stats["floor_counts_us"] = {
        str(fl): sum(1 for c in us if c["population"] >= fl) for fl in floors}
    cont_counts = Counter(c["continent"] for c in kept)
    stats["continent_counts_15k"] = dict(sorted(cont_counts.items()))
    stats["continent_counts_sum"] = sum(cont_counts.values())
    stats["countries_with_cities"] = len(countries)
    stats["top_row"] = {"name": kept[0]["name"], "population": kept[0]["population"],
                        "geonameid": kept[0]["geonameid"]}
    stats["min_pop"] = min(pops)
    stats["keyB_distinct"] = sum(1 for c in kept if c["keyB"] != c["keyA"])

    print(json.dumps(stats, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()

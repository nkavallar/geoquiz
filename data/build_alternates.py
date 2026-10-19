#!/usr/bin/env python3
"""Harvest GeoNames alternatenames for every city in the app dataset.

Matching: GeoNames row -> dataset city by (country + name/asciiname),
coordinate-nearest when several candidates; fallback: nearest GeoNames
row in the same country within 0.15 degrees.
Alternates are normalized with the game's exact guess normalization,
filtered per spec, and stored as an 8th row element: a "|"-joined string
of normalized alternate keys (Latin-script only, since match keys are
Latin; capped at 20 per city).
"""
import json, re, sys, unicodedata
from collections import defaultdict

CITIES_JSON = "/home/hatch/workspace/ts-spaces/city-coverage-quiz/client/src/data/cities.json"
GN = "/tmp/geoquiz2/cities15000.txt"
CI = "/tmp/geoquiz2/countryInfo.txt"
CONTINENT_MAP = "/home/hatch/workspace/geography-quiz/data/continent-map.json"

LETTER_MAP = [
    ("ą","a"),("ę","e"),("ć","c"),("ń","n"),("ó","o"),("ś","s"),
    ("ź","z"),("ż","z"),("ß","ss"),("ł","l"),("ø","o"),("đ","d"),
    ("æ","ae"),("į","i"),("þ","th"),("ų","u"),("ķ","k"),("å","a"),
    ("ļ","l"),("ş","s"),("ț","t"),
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

def norm_name_loose(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())

# ---- country slug -> ISO ----
def load_iso_by_slug(countries):
    info = {}
    with open(CI, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 9:
                continue
            info[norm_name_loose(parts[4])] = parts[0]
    iso_by_slug = {}
    for slug, (name, _cont) in countries.items():
        iso = info.get(norm_name_loose(name))
        if iso:
            iso_by_slug[slug] = iso
    # continent-map covers slugs whose display name may differ
    try:
        cm = json.load(open(CONTINENT_MAP))
        for slug, rec in cm.items():
            if slug in countries and slug not in iso_by_slug and rec.get("iso"):
                iso_by_slug[slug] = rec["iso"]
    except Exception as e:
        print("continent-map load failed", e, file=sys.stderr)
    return iso_by_slug

def main():
    data = json.load(open(CITIES_JSON, encoding="utf-8"))
    countries = data["countries"]
    cities = data["cities"]
    iso_by_slug = load_iso_by_slug(countries)
    missing = [s for s in countries if s not in iso_by_slug]
    print(f"slugs without ISO: {len(missing)} {missing[:10]}")

    # dataset city records
    recs = []
    for idx, row in enumerate(cities):
        name, slug, keyA, keyB, pop, lat, lng = row[:7]
        recs.append({
            "idx": idx, "name": name, "slug": slug,
            "iso": iso_by_slug.get(slug),
            "matchA": normalize_key(keyA), "matchB": normalize_key(keyB),
            "nameNorm": normalize_guess(name),
            "keyAGuess": normalize_guess(normalize_key(keyA)),
            "keyBGuess": normalize_guess(normalize_key(keyB)),
            "pop": pop, "lat": lat, "lng": lng,
        })

    # primary key -> countries (for cross-country collision filter)
    primary_countries = defaultdict(set)
    for r in recs:
        primary_countries[r["matchA"]].add(r["slug"])
        primary_countries[normalize_guess(r["matchA"])].add(r["slug"])

    # ---- load GeoNames ----
    gn_rows = []
    with open(GN, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 10:
                continue
            gn_rows.append({
                "name": parts[1], "ascii": parts[2], "alts": parts[3],
                "lat": float(parts[4]), "lng": float(parts[5]),
                "cc": parts[8],
            })
    print(f"geonames rows: {len(gn_rows)}")

    # index dataset cities by (iso, guess-normalized name/key)
    by_name = defaultdict(list)
    for r in recs:
        if not r["iso"]:
            continue
        for k in {r["nameNorm"], r["keyAGuess"], r["keyBGuess"]}:
            if k:
                by_name[(r["iso"], k)].append(r["idx"])
    # coord grid for fallback: (iso, lat//0.3, lng//0.3) -> gn row indices
    gn_by_name = defaultdict(list)
    for gi, g in enumerate(gn_rows):
        for raw in {g["name"], g["ascii"]}:
            k = normalize_guess(raw)
            if k:
                gn_by_name[(g["cc"], k)].append(gi)

    matched_gn_for_city = {}  # city idx -> gn row index

    def dist2(a_lat, a_lng, b_lat, b_lng):
        return (a_lat - b_lat) ** 2 + (a_lng - b_lng) ** 2

    # Pass 1: name matching
    for r in recs:
        if not r["iso"]:
            continue
        cand_gn = set()
        for k in {r["nameNorm"], r["keyAGuess"], r["keyBGuess"]}:
            cand_gn.update(gn_by_name.get((r["iso"], k), []))
        if not cand_gn:
            continue
        best = min(cand_gn, key=lambda gi: dist2(r["lat"], r["lng"], gn_rows[gi]["lat"], gn_rows[gi]["lng"]))
        matched_gn_for_city[r["idx"]] = best

    # Pass 2: coordinate fallback within 0.15 degrees, same country
    gn_grid = defaultdict(list)
    for gi, g in enumerate(gn_rows):
        gn_grid[(g["cc"], int(g["lat"] // 0.3), int(g["lng"] // 0.3))].append(gi)
    fallback_hits = 0
    for r in recs:
        if r["idx"] in matched_gn_for_city or not r["iso"]:
            continue
        cand = []
        base_lat = int(r["lat"] // 0.3); base_lng = int(r["lng"] // 0.3)
        for dlat in (-1, 0, 1):
            for dlng in (-1, 0, 1):
                cand.extend(gn_grid.get((r["iso"], base_lat + dlat, base_lng + dlng), []))
        best, bestd = None, None
        for gi in cand:
            g = gn_rows[gi]
            if abs(g["lat"] - r["lat"]) <= 0.15 and abs(g["lng"] - r["lng"]) <= 0.15:
                d = dist2(r["lat"], r["lng"], g["lat"], g["lng"])
                if bestd is None or d < bestd:
                    best, bestd = gi, d
        if best is not None:
            matched_gn_for_city[r["idx"]] = best
            fallback_hits += 1
    print(f"matched cities: {len(matched_gn_for_city)} (coord fallback: {fallback_hits})")

    # ---- harvest alternates ----
    gained = 0
    total_alts = 0
    for r in recs:
        gi = matched_gn_for_city.get(r["idx"])
        alts_out = []
        if gi is not None:
            g = gn_rows[gi]
            own = {r["matchA"], r["matchB"], normalize_guess(r["matchA"]), normalize_guess(r["matchB"])}
            seen = set()
            for raw_alt in g["alts"].split(","):
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
                # cross-country primary collision filter
                owners = primary_countries.get(norm, set())
                if any(slug != r["slug"] for slug in owners):
                    continue
                seen.add(norm)
                alts_out.append(norm)
                if len(alts_out) >= 50:
                    break
            # also the GeoNames name/asciiname themselves can be extra keys
            for raw in (g["name"], g["ascii"]):
                norm = normalize_guess(raw)
                if len(norm) >= 3 and re.fullmatch(r"[a-z]+", norm) and norm not in own and norm not in seen:
                    owners = primary_countries.get(norm, set())
                    if not any(slug != r["slug"] for slug in owners):
                        seen.add(norm)
                        alts_out.insert(0, norm)
        if alts_out:
            gained += 1
            total_alts += len(alts_out)
        row = cities[r["idx"]]
        while len(row) < 7:
            row.append(None)
        if len(row) == 7:
            row.append("|".join(alts_out))
        else:
            row[7] = "|".join(alts_out)

    print(f"cities gaining >=1 alternate: {gained} / {len(recs)}; total alternate keys: {total_alts}")

    # ---- filter alternates that would hijack typing ----
    # The game matches on every keystroke and clears the input on a
    # hit, so an alternate key that is a strict prefix of a canonical
    # name fires mid-word (e.g. GeoNames alternate "Orl" for Orlando).
    # Drop those, and drop alternate keys shorter than 4 chars (IATA
    # codes / fragments; inspected 2026-10-17, no genuine local names
    # among them). Primary keyA/keyB are never touched. The same
    # filter lives in filter_alternates.py for post-hoc runs.
    canonical = set()
    for r in recs:
        for mk in (r["matchA"], r["matchB"]):
            canonical.add(mk)
            canonical.add(normalize_guess(mk))
    canonical.discard("")
    proper_prefixes = set()
    for nm in canonical:
        for i in range(1, len(nm)):
            proper_prefixes.add(nm[:i])
    f_prefix = f_short = 0
    for r in recs:
        row = cities[r["idx"]]
        if len(row) < 8 or not row[7]:
            continue
        kept = []
        for alt in row[7].split("|"):
            if not alt:
                continue
            if alt in proper_prefixes:
                f_prefix += 1
                continue
            if len(alt) < 4:
                f_short += 1
                continue
            kept.append(alt)
        row[7] = "|".join(kept)
    print(f"alternates filtered: {f_prefix} prefix-of-canonical, {f_short} shorter than 4 chars")

    # spot checks
    def norm_guess_str(s):
        return normalize_guess(s)
    checks = [
        ("Warsaw", "poland", "Warszawa"),
        ("Munich", "germany", "Munich"),
        ("Munich", "germany", "München"),
        ("Vienna", "austria", "Wien"),
        ("Cologne", "germany", "Köln"),
        ("Prague", "czech_republic", "Praha"),
    ]
    by_name_slug = {(r["name"], r["slug"]): r for r in recs}
    for name, slug, guess in checks:
        r = by_name_slug.get((name, slug))
        if not r:
            print("CHECK MISSING CITY", name, slug); continue
        row = cities[r["idx"]]
        keys = {r["matchA"], r["matchB"]} | set(row[7].split("|") if len(row) > 7 and row[7] else [])
        gnorm = norm_guess_str(guess)
        # game matching normalizes stored keys with normalizeKey; stored alts are already guess-normalized
        hit = gnorm in keys or normalize_key(gnorm) in keys
        print(f"CHECK {guess!r} -> {name}/{slug}: guessNorm={gnorm} hit={hit} alts={(row[7] if len(row)>7 else '')[:120]}")

    json.dump(data, open(CITIES_JSON, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print("written", CITIES_JSON)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Filter the harvested GeoNames alternate keys in the app dataset.

Why: the game matches on EVERY keystroke and clears the input on a
hit. An alternate key that is a strict prefix of a city's canonical
name hijacks typing mid-word (typed "orl" on the way to "Orlando"
fired Orlando early via its GeoNames alternate "Orl", an airport-code
style short form, and wiped the rest of the word). Short alternate
keys (airport codes, fragments) carry the same risk class.

Rules, applied to ALTERNATE keys only (primary keyA and the HugeQuiz
alias keyB are the game's canonical names and are never touched):
  1. Drop an alternate key that is a strict prefix of any city's
     canonical typed name (the guess-normalized form of keyA or keyB,
     plus the stored-key form), anywhere in the dataset.
  2. Drop alternate keys shorter than 4 characters. The survivors of
     rule 1 in this class were inspected (2026-10-17): they are IATA
     airport codes and romanization fragments, not genuine local
     names, so no exceptions are kept.

Acceptance keys verified to survive (checked after a run): warszawa
(alternate), and the canonical aliases wien / munchen / koln / praha,
which live in keyB and are exempt by construction.

Run after build_alternates.py whenever the dataset is re-harvested.
"""
import json
import sys
import unicodedata

CITIES_JSON = "/home/hatch/workspace/ts-spaces/city-coverage-quiz/client/src/data/cities.json"

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


def main() -> None:
    data = json.load(open(CITIES_JSON, encoding="utf-8"))
    cities = data["cities"]

    # Canonical typed names: what a fully typed guess normalizes to.
    canonical = set()
    for row in cities:
        for key in (row[2], row[3]):
            canonical.add(normalize_key(key))
            canonical.add(normalize_guess(normalize_key(key)))
    canonical.discard("")
    proper_prefixes = set()
    for name in canonical:
        for i in range(1, len(name)):
            proper_prefixes.add(name[:i])

    total = dropped_prefix = dropped_short = 0
    cities_with_alts = 0
    for row in cities:
        if len(row) < 8 or not row[7]:
            continue
        kept = []
        for alt in row[7].split("|"):
            if not alt:
                continue
            total += 1
            if alt in proper_prefixes:
                dropped_prefix += 1
                continue
            if len(alt) < 4:
                dropped_short += 1
                continue
            kept.append(alt)
        row[7] = "|".join(kept)
        if kept:
            cities_with_alts += 1

    print(f"alternate keys before: {total}")
    print(f"dropped as strict prefix of a canonical name: {dropped_prefix}")
    print(f"dropped as shorter than 4 characters: {dropped_short}")
    print(f"alternate keys after: {total - dropped_prefix - dropped_short}")
    print(f"cities with >=1 alternate after: {cities_with_alts} / {len(cities)}")

    # Spot checks: acceptance spellings must still resolve.
    def keys_for(name, slug):
        for row in cities:
            if row[0] == name and row[1] == slug:
                keys = {normalize_key(row[2]), normalize_key(row[3])}
                if len(row) > 7 and row[7]:
                    keys |= set(row[7].split("|"))
                return keys
        return set()

    checks = [
        ("Warsaw", "poland", "Warszawa"),
        ("Munich", "germany", "München"),
        ("Vienna", "austria", "Wien"),
        ("Cologne", "germany", "Köln"),
        ("Prague", "czech_republic", "Praha"),
        ("Orlando, FL", "united_states", "Orlando"),
        ("Tallahassee, FL", "united_states", "Tallahassee"),
        ("West Palm Beach, FL", "united_states", "West Palm Beach"),
        ("Fort Lauderdale, FL", "united_states", "Fort Lauderdale"),
    ]
    ok = True
    for name, slug, guess in checks:
        hit = normalize_guess(guess) in keys_for(name, slug)
        print(f"CHECK {guess!r} -> {name}: {'OK' if hit else 'MISSING'}")
        ok = ok and hit
    for bad in ("orl", "mun"):
        hits = [
            row[0]
            for row in cities
            if len(row) > 7
            and row[7]
            and bad in row[7].split("|")
        ]
        print(f"REGRESSION alt key {bad!r} still present on: {hits or 'none'}")
        ok = ok and not hits

    json.dump(data, open(CITIES_JSON, "w", encoding="utf-8"),
              ensure_ascii=False, separators=(",", ":"))
    print("written", CITIES_JSON)
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()

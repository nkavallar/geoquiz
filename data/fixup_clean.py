#!/usr/bin/env python3
"""Finalize the clean GeoNames dataset for the app swap (approved by Niko
2026-10-19, "swap with both fixes"):

1) Merge GeoNames' same-place double entries: the 16 close pairs Niko
   approved on 2026-10-19 after the premise correction. Identification:
   group rows by (country, match-normalized keyA); pairs within 0.15 deg
   on both axes are "close pairs" (22 exist). Of those, pairs whose
   records sit within 0.065 deg max-axis (same urban footprint) are
   merged (16). Excluded, itemized in the audit: the 3 state-line twin
   cities (Kansas City MO/KS, Bristol TN/VA, Texarkana TX/AR; close by
   definition but distinct municipalities in different states, excluded
   by GeoNames id in the code) and the 3 far pairs 15-19 km apart
   (San Tin, Ahwiaa, Ad Dindar; distinct settlements sharing a name).
   Correction history: CLEAN-REBUILD-REPORT.md called all 18 non-twin
   close pairs identical-population doubles; that holds for only 4
   (Kashan, Changhua, Nasimshahr, Binyamina). The rest are city vs
   core/section records with different populations, merged on the
   distance evidence Niko approved. A looser gate (same population +
   close, regardless of name) was also tried and rejected: it falsely
   captures distinct neighborhoods that merely share a rounded GeoNames
   population (Moscow and Kuala Lumpur district entries).
   Merge mechanics: keep the higher-population row (tie: first in file
   order); the dropped row's keyA/keyB and alternates are unioned into
   the kept row's alternates so every spelling that fired the dropped
   row still fires the single merged city.

2) Wien canonical exception: Vienna's keyB becomes "wien" (canonical,
   filter-exempt), restoring the shipped behavior where typing Wien
   fires Vienna. Wiener Neustadt's canonical key is untouched.

Inputs:  cities-clean.json, cities-clean.provenance.json
Outputs: cities-final.json, cities-final.provenance.json, FIXUP-REPORT.md
"""
import json
import re
import sys
import unicodedata
from collections import defaultdict

BASE = "/home/hatch/workspace/geography-quiz/data"


def norm(key):
    s = unicodedata.normalize("NFD", key.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s)


with open(f"{BASE}/cities-clean.json") as f:
    data = json.load(f)
with open(f"{BASE}/cities-clean.provenance.json") as f:
    prov = json.load(f)

countries = data["countries"]
cities = data["cities"]
assert len(cities) == len(prov) == 34128, (len(cities), len(prov))

# --- 1) same-place merge (the report's audited 18) ------------------------
groups = defaultdict(list)
for i, row in enumerate(cities):
    groups[(row[1], norm(row[2]))].append(i)

close_pairs = []
for key, idxs in groups.items():
    for a in range(len(idxs)):
        for b in range(a + 1, len(idxs)):
            i, j = idxs[a], idxs[b]
            ri, rj = cities[i], cities[j]
            if abs(ri[5] - rj[5]) <= 0.15 and abs(ri[6] - rj[6]) <= 0.15:
                close_pairs.append((i, j))

assert len(close_pairs) == 22, f"expected 22 close pairs, found {len(close_pairs)}"

TWIN_ID_PAIRS = {
    frozenset((4393217, 4273837)),   # Kansas City MO / KS
    frozenset((4608657, 4748993)),   # Bristol TN / VA
    frozenset((4736096, 4133367)),   # Texarkana TX / AR
}

def max_axis(ri, rj):
    return max(abs(ri[5] - rj[5]), abs(ri[6] - rj[6]))

merge_pairs = []
far_pairs = []
for i, j in close_pairs:
    if frozenset((prov[i], prov[j])) in TWIN_ID_PAIRS:
        continue
    if max_axis(cities[i], cities[j]) <= 0.065:
        merge_pairs.append((i, j))
    else:
        far_pairs.append((i, j))
assert len(merge_pairs) == 16, f"expected 16 merges, found {len(merge_pairs)}"
assert len(far_pairs) == 3, f"expected 3 far pairs, found {len(far_pairs)}"
far_names = [(cities[i][0], cities[j][0]) for i, j in far_pairs]
used = set()
for i, j in merge_pairs:
    assert i not in used and j not in used, "chained merge pair"
    used.add(i)
    used.add(j)

merge_log = []
dropped = set()
for i, j in merge_pairs:
    # keep the higher-population row (tie: the earlier row in file order)
    if cities[j][4] > cities[i][4]:
        i, j = j, i
    keep, drop = cities[i], cities[j]
    alts = set()
    for src in (keep[7], drop[7]):
        if src:
            alts.update(src.split("|"))
    for k in (drop[2], drop[3]):
        if k and k not in (keep[2], keep[3]):
            alts.add(k)
    alts.discard(keep[2])
    alts.discard(keep[3])
    alts.discard("")
    keep[7] = "|".join(sorted(alts))
    dropped.add(j)
    merge_log.append(
        f"- kept {keep[0]} (id {prov[i]}, pop {keep[4]}) <- merged "
        f"{drop[0]} (id {prov[j]}, keys {drop[2]}/{drop[3]})"
    )

cities = [row for n, row in enumerate(cities) if n not in dropped]
prov = [p for n, p in enumerate(prov) if n not in dropped]
assert len(cities) == len(prov) == 34112, (len(cities), len(prov))
for tid in (4393217, 4273837, 4608657, 4748993, 4736096, 4133367):
    assert tid in prov, f"twin city id {tid} lost"

# --- 2) Wien exception ------------------------------------------------------
vienna = [r for r in cities if r[1] == "austria" and r[2] == "vienna"]
assert len(vienna) == 1, f"Vienna rows: {len(vienna)}"
v = vienna[0]
assert v[3] == "vienna", v
v[3] = "wien"
if v[7]:
    rest = [a for a in v[7].split("|") if a != "wien"]
    v[7] = "|".join(rest)
assert not any(
    r is not v and (r[2] == "wien" or r[3] == "wien") for r in cities
), "another row claims the wien key"
wn = [r for r in cities if r[2] == "wienerneustadt"]
assert len(wn) == 1, f"Wiener Neustadt rows: {len(wn)}"

# --- verification numbers ----------------------------------------------------
FLOORS = [15000, 25000, 50000, 100000, 250000, 500000, 1000000]

def floor_counts(rows):
    return {f: sum(1 for r in rows if r[4] >= f) for f in FLOORS}

world = floor_counts(cities)
us = floor_counts([r for r in cities if r[1] == "united_states"])
cont_sum = defaultdict(int)
for r in cities:
    cont_sum[countries[r[1]][1]] += 1
assert sum(cont_sum.values()) == len(cities)

burl = sorted(
    [(r[0], r[4]) for r in cities if r[1] == "united_states" and r[2].startswith("burlington")],
    key=lambda t: -t[1],
)
burl25 = [b for b in burl if b[1] >= 25000]
spr25 = [r for r in cities if r[1] == "united_states" and r[2] == "springfield" and r[4] >= 25000]
de100 = sum(1 for r in cities if r[1] == "germany" and r[4] >= 100000)
at15 = sum(1 for r in cities if r[1] == "austria" and r[4] >= 15000)

with open(f"{BASE}/cities-final.json", "w") as f:
    json.dump({"countries": countries, "cities": cities}, f, ensure_ascii=False)
with open(f"{BASE}/cities-final.provenance.json", "w") as f:
    json.dump(prov, f)

lines = []
lines.append("# Fixup Report: cities-final.json")
lines.append("")
lines.append("Built by `data/fixup_clean.py` from `cities-clean.json` "
             "(Niko's approval, 2026-10-19: swap with both fixes).")
lines.append("")
lines.append(f"Rows: 34,128 -> {len(cities)} ({len(merge_pairs)} same-place merges).")
lines.append(f"Far pairs kept as distinct cities: {far_names}. "
             "Twin cities (Kansas City, Bristol, Texarkana) verified present "
             "with both records.")
lines.append("")
lines.append("## Merge log (kept <- merged)")
lines.append("")
lines.extend(merge_log)
lines.append("")
lines.append("## Wien exception")
lines.append("")
lines.append(f"Vienna row: {v}. Wiener Neustadt untouched: {wn[0][:4]}.")
lines.append("")
lines.append("## Final floor counts (world)")
lines.append("")
for f_ in FLOORS:
    lines.append(f"- {f_}: {world[f_]}")
lines.append("")
lines.append("## Final floor counts (United States)")
lines.append("")
for f_ in FLOORS:
    lines.append(f"- {f_}: {us[f_]}")
lines.append("")
lines.append(f"US Burlingtons (all): {burl}; at 25K: {len(burl25)}.")
lines.append(f"US Springfields at 25K: {len(spr25)}.")
lines.append(f"Germany at 100K: {de100}. Austria at 15K: {at15}.")
lines.append(f"Per-continent totals sum: {sum(cont_sum.values())} "
             f"({dict(sorted(cont_sum.items()))}).")
with open(f"{BASE}/FIXUP-REPORT.md", "w") as f:
    f.write("\n".join(lines) + "\n")

print("\n".join(lines))
print("OK: cities-final.json written", file=sys.stderr)

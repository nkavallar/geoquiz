# Fixup Report: cities-final.json

Built by `data/fixup_clean.py` from `cities-clean.json` (Niko's approval, 2026-10-19: swap with both fixes).

Rows: 34,128 -> 34112 (16 same-place merges).
Far pairs kept as distinct cities: [('Ahwiaa', 'Ahwiaa'), ('Ad-Dindar', 'Ad Dindar'), ('San Tin', 'San Tin')]. Twin cities (Kansas City, Bristol, Texarkana) verified present with both records.

## Merge log (kept <- merged)

- kept E’zhou (id 6642286, pop 668727) <- merged Ezhou (id 1811619, keys ezhou/ezhou)
- kept Benito Juárez (id 6957079, pop 385439) <- merged Benito Juarez (id 3827406, keys benitojuarez/benitojuarez)
- kept Xilinhot (id 8054802, pop 349953) <- merged Xilin Hot (id 2033824, keys xilinhot/xilinhot)
- kept Kashan (id 128476, pop 304487) <- merged Kāshān (id 6861211, keys kashan/kāshān)
- kept Phu Quoc (id 8531735, pop 294419) <- merged Phú Quốc (id 12253704, keys phuquoc/phúquốc)
- kept Chang-hua (id 1679136, pop 226564) <- merged Changhua (id 1993459, keys changhua/changhua)
- kept La Ceiba (id 3608248, pop 222055) <- merged La Ceiba (id 8556321, keys laceiba/laceiba)
- kept Nasimshahr (id 13405749, pop 200393) <- merged Nasīm Shahr (id 6672634, keys nasimshahr/nasīmshahr)
- kept Latkrabang (id 11071484, pop 173987) <- merged Lat Krabang (id 6957690, keys latkrabang/latkrabang)
- kept Kot Kapūra (id 1265973, pop 91979) <- merged Kotkapura (id 7279734, keys kotkapura/kotkapura)
- kept Banga (id 1727401, pop 91536) <- merged Bañga (id 1727400, keys banga/bañga)
- kept Ābyek (id 144795, pop 60107) <- merged Ābyek (id 144794, keys abyek/ābyek)
- kept Panauti (id 7963596, pop 46595) <- merged Panauti̇̄ (id 1282950, keys panauti/panauti̇̄)
- kept Barbigha (id 9036524, pop 46075) <- merged Bar Bigha (id 1277038, keys barbigha/barbigha)
- kept Cañete (id 3950116, pop 31805) <- merged Cañete (id 3896924, keys canete/cañete)
- kept Binyamina-Giv'at Ada (id 12156557, pop 15847) <- merged Binyamina-Giv‘at ‘Ada (id 295410, keys binyamina-giv`at`ada/binyamina-giv‘at‘ada)

## Wien exception

Vienna row: ['Vienna', 'austria', 'vienna', 'wien', 1691468, 48.20849, 16.37208, 'becs|bienne|fiena|viden|vieden|viena|vieno|viin|vinarborg|vindobona|viyana|vjena|vjenna|vyana|wean|wene|wenen|wieden|wjedzyn|bienna|fyyna|weiyena|weiynna|wynh']. Wiener Neustadt untouched: ['Wiener Neustadt', 'austria', 'wienerneustadt', 'wienerneustadt'].

## Final floor counts (world)

- 15000: 34112
- 25000: 22847
- 50000: 12381
- 100000: 6276
- 250000: 2452
- 500000: 1210
- 1000000: 573

## Final floor counts (United States)

- 15000: 3408
- 25000: 2081
- 50000: 976
- 100000: 356
- 250000: 94
- 500000: 42
- 1000000: 15

US Burlingtons (all): [('Burlington', 52472), ('Burlington', 42452), ('Burlington', 25410), ('Burlington', 24498), ('Burlington', 15926)]; at 25K: 3.
US Springfields at 25K: 6.
Germany at 100K: 101. Austria at 15K: 66.
Per-continent totals sum: 34112 ({'Africa': 4047, 'Asia': 12577, 'Europe': 8164, 'North America': 5180, 'Oceania': 426, 'South America': 3718}).

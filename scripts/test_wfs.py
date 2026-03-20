import requests, json

WFS = "https://geoserver.museovirasto.fi/geoserver/rajapinta/wfs"

# 1) Etsi kalliomaalausten oikea tyyppinimi
print("1) Etsitaan kalliomaalausten tyyppinimi...")
params = {
    "SERVICE": "WFS",
    "VERSION": "2.0.0",
    "REQUEST": "GetFeature",
    "TYPENAMES": "rajapinta:muinaisjaannos_piste",
    "OUTPUTFORMAT": "application/json",
    "COUNT": "500",
    "CQL_FILTER": "kohdenimi LIKE '%kallio%'"
}
resp = requests.get(WFS, params=params, timeout=60)
data = resp.json()
for f in data.get("features", [])[:10]:
    p = f["properties"]
    print(f"  {p.get('kohdenimi','?')} | tyyppi: {p.get('tyyppi','?')} | ajoitus: {p.get('ajoitus','?')}")

# 2) Hae kaikki kivikautiset asuinpaikat ita-Suomesta
print("\n2) Kivikautiset asuinpaikat (kaikki)...")
params2 = {
    "SERVICE": "WFS",
    "VERSION": "2.0.0",
    "REQUEST": "GetFeature",
    "TYPENAMES": "rajapinta:muinaisjaannos_piste",
    "OUTPUTFORMAT": "application/json",
    "COUNT": "10000",
    "CQL_FILTER": "ajoitus LIKE '%kivikautinen%' AND tyyppi LIKE '%asuinpaikat%'"
}
resp2 = requests.get(WFS, params=params2, timeout=120)
data2 = resp2.json()
feats2 = data2.get("features", [])
print(f"Kivikautisia asuinpaikkoja: {len(feats2)}")

# 3) Hae pronssikautiset
print("\n3) Pronssikautiset kohteet...")
params3 = {
    "SERVICE": "WFS",
    "VERSION": "2.0.0",
    "REQUEST": "GetFeature",
    "TYPENAMES": "rajapinta:muinaisjaannos_piste",
    "OUTPUTFORMAT": "application/json",
    "COUNT": "10000",
    "CQL_FILTER": "ajoitus LIKE '%pronssikautinen%'"
}
resp3 = requests.get(WFS, params=params3, timeout=120)
data3 = resp3.json()
feats3 = data3.get("features", [])
print(f"Pronssikautisia kohteita: {len(feats3)}")

# 4) Hae kampakeraamiset
print("\n4) Kampakeraamiset...")
params4 = {
    "SERVICE": "WFS",
    "VERSION": "2.0.0",
    "REQUEST": "GetFeature",
    "TYPENAMES": "rajapinta:muinaisjaannos_piste",
    "OUTPUTFORMAT": "application/json",
    "COUNT": "10000",
    "CQL_FILTER": "ajoitus LIKE '%kampakeraami%'"
}
resp4 = requests.get(WFS, params=params4, timeout=120)
data4 = resp4.json()
feats4 = data4.get("features", [])
print(f"Kampakeraamiset: {len(feats4)}")

# 5) Yhdista ja tallenna
print("\n5) Yhdistetaan...")
all_ids = set()
combined = []
for feats in [feats2, feats3, feats4]:
    for f in feats:
        fid = f["properties"].get("mjtunnus", id(f))
        if fid not in all_ids:
            all_ids.add(fid)
            combined.append(f)

print(f"Yhteensa uniikkeja kohteita: {len(combined)}")

# Tallenna
out = {"type": "FeatureCollection", "features": combined}
with open("data/museovirasto/suodatettu.geojson", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False)
print(f"Tallennettu: data/museovirasto/suodatettu.geojson")

# Kuntatilasto
from collections import Counter
kunnat = Counter(f["properties"].get("kunta", "?") for f in combined)
print(f"\nTop 15 kunnat:")
for k, c in kunnat.most_common(15):
    print(f"  {c:4d}  {k}")
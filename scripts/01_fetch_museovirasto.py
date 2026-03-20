#!/usr/bin/env python3
"""Lataa ja suodata Museoviraston muinaisjäännösrekisteri. Ei vaadi API-avainta."""
import os, sys, json, requests
try:
    import geopandas as gpd
except ImportError:
    print("pip install geopandas fiona requests"); sys.exit(1)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "museovirasto")
os.makedirs(DATA_DIR, exist_ok=True)
WFS = "https://geoserver.museovirasto.fi/geoserver/rajapinta/wfs"
BBOX = "61.0,27.0,63.5,30.5,EPSG:4326"  # Kattaa kaikki kohteet

print("Haetaan muinaisjäännöksiä...")
params = {"SERVICE":"WFS","VERSION":"2.0.0","REQUEST":"GetFeature",
          "TYPENAMES":"rajapinta:muinaisjaannos_piste",
          "OUTPUTFORMAT":"application/json","COUNT":"50000","BBOX":BBOX}
resp = requests.get(WFS, params=params, timeout=120)
resp.raise_for_status()
data = resp.json()
print(f"Saatiin {len(data['features'])} kohdetta")

with open(os.path.join(DATA_DIR, "raaka.geojson"), "w") as f:
    json.dump(data, f, ensure_ascii=False)

gdf = gpd.GeoDataFrame.from_features(data["features"], crs="EPSG:4326")
keywords = ["kivikausi","kampakeraami","pronssikausi","varhaismetalli","kalliomaalau","asuinpaikka"]
mask = None
for col in [c for c in gdf.columns if gdf[c].dtype=="object"]:
    for kw in keywords:
        m = gdf[col].str.contains(kw, case=False, na=False)
        mask = m if mask is None else mask | m

filtered = gdf[mask] if mask is not None else gdf
filtered.to_file(os.path.join(DATA_DIR, "suodatettu.geojson"), driver="GeoJSON")
print(f"Suodatettu: {len(filtered)} kohdetta -> data/museovirasto/suodatettu.geojson")

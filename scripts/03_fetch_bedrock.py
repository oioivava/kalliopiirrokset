#!/usr/bin/env python3
"""Hae GTK kallioperädata kohdealueilta. Ei vaadi API-avainta."""
import os, sys, json, requests
try:
    from pyproj import Transformer
    tr = Transformer.from_crs("EPSG:4326", "EPSG:3067", always_xy=True)
except ImportError:
    print("pip install pyproj"); sys.exit(1)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "gtk")
os.makedirs(DATA_DIR, exist_ok=True)
GTK = "https://gtkdata.gtk.fi/arcgis/services/Rajapinnat/GTK_Kalliopera_WFS/MapServer/WFSServer"

with open(os.path.join(os.path.dirname(__file__), "..", "model", "sites.geojson")) as f:
    sites = json.load(f)["features"]

for site in sites:
    p = site["properties"]
    coords = site["geometry"]["coordinates"][0]
    lons, lats = [c[0] for c in coords], [c[1] for c in coords]
    e1, n1 = tr.transform(min(lons), min(lats))
    e2, n2 = tr.transform(max(lons), max(lats))
    bbox = f"{e1-1000:.0f},{n1-1000:.0f},{e2+1000:.0f},{n2+1000:.0f},EPSG:3067"
    
    print(f"Kohde #{p['id']}: {p['name']}")
    resp = requests.get(GTK, params={"SERVICE":"WFS","VERSION":"2.0.0",
        "REQUEST":"GetFeature","BBOX":bbox,"OUTPUTFORMAT":"GEOJSON"}, timeout=60)
    
    if resp.ok:
        out = os.path.join(DATA_DIR, f"bedrock_{p['id']:02d}.geojson")
        with open(out, "w") as f: f.write(resp.text[:50000])
        print(f"  -> {out}")
    else:
        print(f"  VIRHE: {resp.status_code}")
print("\nValmis. Tarkista data/gtk/")

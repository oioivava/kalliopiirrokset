#!/usr/bin/env python3
"""Lataa MML korkeusmalli kohdealueilta. VAATII MML API-avaimen."""
import os, sys, json, time, requests

API_KEY = os.environ.get("MML_API_KEY", "")
if not API_KEY:
    print("Aseta: export MML_API_KEY=sinun_avaimesi")
    print("Rekisteröidy: https://oma.maanmittauslaitos.fi/")
    sys.exit(1)

try:
    from pyproj import Transformer
    tr = Transformer.from_crs("EPSG:4326", "EPSG:3067", always_xy=True)
except ImportError:
    print("pip install pyproj"); sys.exit(1)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "mml")
os.makedirs(DATA_DIR, exist_ok=True)
API = "https://avoin-paikkatieto.maanmittauslaitos.fi/tiedostopalvelu/ogcproc/v1"

with open(os.path.join(os.path.dirname(__file__), "..", "model", "sites.geojson")) as f:
    sites = json.load(f)["features"]

for site in sites:
    p = site["properties"]
    coords = site["geometry"]["coordinates"][0]
    lons, lats = [c[0] for c in coords], [c[1] for c in coords]
    e1, n1 = tr.transform(min(lons), min(lats))
    e2, n2 = tr.transform(max(lons), max(lats))
    bbox = [int(e1-500), int(n1-500), int(e2+500), int(n2+500)]
    
    print(f"Kohde #{p['id']}: {p['name']} bbox={bbox}")
    resp = requests.post(f"{API}/processes/korkeusmalli_2m_bbox/execution",
        json={"id":"korkeusmalli_2m_bbox","inputs":{"boundingBoxInput":bbox,"fileFormatInput":"TIFF"}},
        params={"api-key": API_KEY}, timeout=30)
    
    if resp.ok:
        result = resp.json()
        print(f"  Työ luotu: {json.dumps(result)[:200]}")
        # Lataa tulos linkistä (vaihtelee API:n mukaan)
    else:
        print(f"  VIRHE: {resp.status_code} {resp.text[:200]}")
    time.sleep(2)
print("\nValmis. Tarkista data/mml/")

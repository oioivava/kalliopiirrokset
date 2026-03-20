import requests, re, json, time

WMS = "https://gtkdata.gtk.fi/arcgis/services/Rajapinnat/GTK_Kalliopera_WMS/MapServer/WMSServer"
LAYER = "kalliopera_5m_kivilajit"

VALID_ROCKS = ["granit", "gneiss", "gneis", "migmat", "granodiorit", "tonalit", "rapakivi"]

sites = [
    (1, "Haukkasalo", 517000, 6815000),
    (2, "Laukniemi", 530000, 6803000),
    (3, "Ukonkivi", 604000, 7004000),
    (4, "Kylanniemi", 536000, 6808000),
    (5, "Pihlajavesi", 549000, 6866000),
    (6, "Lietvesi", 532000, 6825000),
    (7, "Pyhajarvi", 651000, 6896000),
    (8, "Luonteri", 520000, 6842000),
    (9, "Kuolimo", 511000, 6792000),
    (10, "Haukivesi", 544000, 6906000),
]

print("KALLIOPERAKARTOITUS — 10 kohdealuetta\n")

results = []
for sid, name, e, n in sites:
    bbox = f"{e-1000},{n-1000},{e+1000},{n+1000}"
    
    for attempt in range(3):
        try:
            resp = requests.get(WMS, params={
                "SERVICE": "WMS",
                "VERSION": "1.1.1",
                "REQUEST": "GetFeatureInfo",
                "LAYERS": LAYER,
                "QUERY_LAYERS": LAYER,
                "INFO_FORMAT": "text/html",
                "SRS": "EPSG:3067",
                "BBOX": bbox,
                "WIDTH": "100",
                "HEIGHT": "100",
                "X": "50",
                "Y": "50"
            }, timeout=120)
            
            cells = re.findall(r"<t[hd][^>]*>([^<]*)</t[hd]>", resp.text)
            
            if len(cells) > 38:
                rock_class = cells[36]
                gen_1m = cells[38]
                gen_5m = cells[40] if len(cells) > 40 else "?"
                is_valid = any (v in gen_1m.lower() or v in rock_class.lower() for v in VALID_ROCKS)
                print(f"  #{sid} {name}")
                print(f"      {gen_1m}")
                print(f"      --> {'PIIRROSKELPOINEN' if is_valid else 'ei tunnistettu'}")
                results.append({"id": sid, "name": name, "gen_1m": gen_1m, "rock_class": rock_class, "suitable": is_valid})
            else:
                print(f"  #{sid} {name}: tyhja vastaus")
                results.append({"id": sid, "name": name, "gen_1m": "?", "rock_class": "?", "suitable": False})
            break
            
        except requests.exceptions.Timeout:
            print(f"  #{sid} {name}: timeout (yritys {attempt+1}/3)")
            time.sleep(5)
        except Exception as ex:
            print(f"  #{sid} {name}: virhe: {ex}")
            break
    
    time.sleep(3)

print(f"\nYHTEENVETO: {sum(1 for r in results if r.get('suitable'))}/{len(results)} piirroskelpoista")

with open("data/gtk/kivilajit_kohteet.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("Tallennettu: data/gtk/kivilajit_kohteet.json")
# Suomen kadonneet kalliopiirrokset

**Prediktiivinen malli löytymättömien petroglyfien paikantamiseksi Suomesta**

> ⚠️ **Status: Experimental / Alpha** — Parametrit ovat asiantuntija-arvioita, eivät empiirisesti validoituja.

## Hypoteesi

Kalliopiirrosten puuttuminen Suomesta on löydösvaje, ei todellinen poissaolo.

**Perusteet:**
- Sama kampakeraaminen kulttuuri teki piirroksia Äänisellä (4500+ kuvaa) ja maalauksia Suomessa (~145 kohdetta)
- Materiaalinen yhteys: Äänisen viherliusketta löytynyt Taipalsaaren asuinpaikoilta
- Ikonografinen jatkumo dokumentoitu (Lahelma 2008)
- Geologiset olosuhteet yhteensopivat

## Menetelmä

Kolme avointa geodata-kerrosta:
1. **MML korkeusmalli (2m DEM)** — korkeusasema vs. muinainen rantaviiva
2. **Museoviraston muinaisjäännösrekisteri** — kivi/pronssikautiset asuinpaikat
3. **GTK kallioperäkartta** — graniittialueet (piirroskelpoinen substraatti)

## Projektin vaiheet

- **Vaihe 1** (2026): Geodatan integrointi, 6 kenttäkartoitusta
- **Vaihe 2** (ehdollinen): Akateeminen julkaisu (Lahelma)
- **Vaihe 3** (ehdollinen): Open source + citizen science

## Akateeminen yhteistyö

Arkeologinen ohjaus: **Antti Lahelma**, Helsingin yliopisto

## Pikaohje

```bash
pip install -r requirements.txt
python scripts/01_fetch_museovirasto.py        # Ei vaadi API-avainta
export MML_API_KEY=sinun_avaimesi
python scripts/02_fetch_dem.py                 # Vaatii MML API-avaimen
python scripts/03_fetch_bedrock.py             # Ei vaadi API-avainta
python scripts/04_calculate_scores.py          # Yhdistää kaiken
```

## Lisenssi

© 2026 Timo Oiva. All rights reserved. Public viewing only.

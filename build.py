#!/usr/bin/env python3
"""Bygger index.html ud fra app-template.html + egne marker i WGS84.

egne_marker_wgs84.json er hentet fra Landbrugsstyrelsens WFS (Markblokke_2026,
EPSG:4326) med CQL-filter på de seks markbloknumre. Kortbaggrund (luftfoto,
vejkort) og markblok-laget hentes live i appen — intet indlejres længere.
"""
import json, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

geo = json.load(open("egne_marker_wgs84.json"))
# behold kun det, appen bruger
slank = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "MARKBLOKNR": f["properties"]["MARKBLOKNR"],
                "GB_AREAL": f["properties"]["GB_AREAL"],
            },
            "geometry": f["geometry"],
        }
        for f in geo["features"]
    ],
}

html = open("app-template.html", encoding="utf-8").read()
html = html.replace("__EGNE_GEOJSON__", json.dumps(slank, ensure_ascii=False))
open("index.html", "w", encoding="utf-8").write(html)
print("index.html bygget:", os.path.getsize("index.html") // 1024, "KB")

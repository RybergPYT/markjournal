#!/usr/bin/env python3
"""Bygger index.html ud fra app-template.html + kortdata.

Kortdata (genskabes med hent_data.py hvis de mangler):
- blokke_px.json : markblokke fra Landbrugsstyrelsens WFS, omregnet til SVG-koordinater
- luftfoto.jpg   : luftfoto af samme område (2x2 km, EPSG:25832 578500,6137000-580500,6139000)
"""
import json, base64, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

blokke = json.load(open("blokke_px.json"))
foto = base64.b64encode(open("luftfoto.jpg", "rb").read()).decode()

egne_def = [
    ("m1", "Nørremarken", "579138-47", "Vinterhvede", "#c9b36a"),
    ("m2", "Kirkestykket", "579138-54", "Vinterhvede", "#b9c77a"),
    ("m3", "Åmarken", "579137-56", "Vinterraps", "#e8d44d"),
    ("m4", "Bakkelodden", "578137-89", "Slætgræs", "#7d9a54"),
    ("m5", "Langager", "579137-84", "Majs", "#c2a95e"),
    ("m6", "Mosen", "578137-88", "Brak (MFO)", "#9aa984"),
]
bynr = {b["nr"]: b for b in blokke}
marker = {}
for mid, navn, nr, afgrode, farve in egne_def:
    b = bynr[nr]
    marker[mid] = {
        "navn": navn, "blok": nr, "afgrode": afgrode, "farve": farve,
        "ha": f"{b['ha']:.1f}".replace(".", ","), "haNum": round(b["ha"], 2),
        "path": b["path"], "cx": b["cx"], "cy": b["cy"],
    }

blocks_js = "const BLOKKE=" + json.dumps(
    [{"nr": b["nr"], "path": b["path"]} for b in blokke], ensure_ascii=False) + ";\n"
blocks_js += "const MARKER=" + json.dumps(marker, ensure_ascii=False) + ";"

html = open("app-template.html", encoding="utf-8").read()
html = html.replace("__FOTO__", "data:image/jpeg;base64," + foto)
html = html.replace("__BLOCKS__", blocks_js)
open("index.html", "w", encoding="utf-8").write(html)
print("index.html bygget:", os.path.getsize("index.html") // 1024, "KB")

#!/usr/bin/env python3
"""Henter godkendte plantebeskyttelsesmidler fra Miljøstyrelsens BMD til midler.json.

Kilde: https://bmd.mst.dk/External/ (offentlig eksport, ingen nøgle).
Kør igen når databasen skal opdateres — fx et par gange om året.
"""
import datetime, json, os, re, subprocess, tempfile, zipfile
from xml.etree import ElementTree as ET

NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
BASE = "https://bmd.mst.dk"
BOILER = [
    r'Brugsanvisningen skal følges for ikke at bringe menneskers sundhed og miljøet i fare\s*\(EUH401\)\.?',
    r'Overtrædelse af nedenstående særligt fremhævede forskrifter kan medføre straf\.?',
]

def sh(*a):
    return subprocess.run(a, capture_output=True, text=True).stdout

def hent_xlsx(sti):
    jar = os.path.join(tempfile.gettempdir(), "bmd.jar")
    dialog = sh("curl", "-s", "-c", jar, f"{BASE}/External/Entry/ExportDialog")
    token = re.search(r'name="__RequestVerificationToken"[^>]*value="([^"]*)"', dialog).group(1)
    svar = sh("curl", "-s", "-b", jar, "-X", "POST", f"{BASE}/External/Entry/GenerateDocument",
              "--data-urlencode", f"__RequestVerificationToken={token}",
              "--data", "ExportFormat=3&ProductType=0&Page=1&PageSize=20000&SortingDirection=0&IsIframeOffline=False")
    url = json.loads(svar)["Url"]
    sh("curl", "-s", "-b", jar, f"{BASE}{url}", "-o", sti)

def laes(sti):
    z = zipfile.ZipFile(sti)
    ss = [n for n in z.namelist() if 'haredString' in n]
    strings = ["".join(t.text or "" for t in si.iter(NS + 't'))
               for si in ET.fromstring(z.read(ss[0]))] if ss else []
    rows = []
    for row in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).iter(NS + 'row'):
        r = []
        for c in row.iter(NS + 'c'):
            t = c.get('t')
            if t == 'inlineStr':
                isn = c.find(NS + 'is')
                r.append("".join(x.text or "" for x in isn.iter(NS + 't')) if isn is not None else "")
            else:
                v = c.find(NS + 'v')
                r.append("" if v is None else (strings[int(v.text)] if t == 's' and strings else v.text))
        rows.append(r)
    return rows

def dato(v):
    try:
        return (datetime.date(1899, 12, 30) + datetime.timedelta(days=int(float(v)))).isoformat()
    except Exception:
        return None

def ren(s, maks=None):
    if not s:
        return ""
    s = re.sub(r'\s+', ' ', str(s)).strip()
    for b in BOILER:
        s = re.sub(b, '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return (s[:maks].rstrip() + "…") if maks and len(s) > maks else s

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    xlsx = os.path.join(tempfile.gettempdir(), "bmd_hent.xlsx")
    hent_xlsx(xlsx)
    rows = laes(xlsx)
    hdr = rows[3]
    i = lambda n: hdr.index(n)
    idag = datetime.date.today().isoformat()
    ud = []
    for r in (x for x in rows[4:] if x and x[0]):
        if r[i('Bekæmpelsesmiddeltype')] != 'Pesticid':
            continue
        st = r[i('Produktstatus')]
        frist = dato(r[i('Frist for anvendelse og besiddelse')])
        if st == 'Produkt godkendt':
            status = "godkendt"
        elif st in ('Produkt afmeldt', 'Produkt udløbet') and frist and frist >= idag:
            status = "udfases"
        else:
            continue
        ud.append({
            "n": ren(r[i('Produktnavn')]), "r": ren(r[i('Registrerings-nr.')]),
            "a": ren(r[i('Aktivstofnavn(e)')], 90),
            "k": (ren(r[i('Koncentration(er)')], 30) + " " + ren(r[i('Enhed(er)')], 20)).strip(),
            "b": {"Professionel": "pro", "Ikke-professionel": "privat"}.get(r[i('Bruger pesticid')], ""),
            "s": status, "f": frist, "t": ren(r[i('Anvendelse')], 400),
        })
    ud.sort(key=lambda p: p["n"].lower())
    json.dump({"meta": {"kilde": "Miljøstyrelsens Bekæmpelsesmiddeldatabase (BMD)",
                        "hentet": idag, "antal": len(ud)}, "midler": ud},
              open("midler.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"midler.json: {len(ud)} midler, {os.path.getsize('midler.json')//1024} KB")

if __name__ == "__main__":
    main()

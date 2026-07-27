# markjournal-web

Dansk web-app/PWA til markstyring og sprøjtejournal.
Live på **https://rybergpyt.github.io/markjournal/** · repo `RybergPYT/markjournal`.

Én selvstændig HTML-fil uden byggeværktøjer, framework eller npm. Al brugerdata
ligger i browserens localStorage — **ingen sky-synkronisering** (Sørens beslutning).

Mappen ligger i `~/Projekter/markjournal-web` og er sit eget git-repo. Åbn den
direkte i Claude Code — ikke via `~/Projekter`.

## Vigtigste regel: redigér aldrig index.html

`index.html` er **genereret** og committes med i repoet (GitHub Pages serverer den
direkte). Rettelser skal ske i `app-template.html`, hvorefter du bygger:

```bash
cd ~/Projekter/markjournal-web && python3 build.py
```

`build.py` erstatter pladsholderen `__EGNE_GEOJSON__` i templaten med indholdet af
`egne_marker_wgs84.json` (demobedriftens markblokke i WGS84) og skriver `index.html`.
Glemmer du at bygge, deployer du den gamle version.

## Kør lokalt og deploy

**Start altid appen, når Søren nævner markjournal.** Han vil se appen live i højre
side af skærmen — også selv om opgaven bare er et spørgsmål eller en lille rettelse.
Kør `preview_start` med navnet `markjournal-web` som noget af det første, og sæt
vinduet til mobilstørrelse (`resize_window` med preset `mobile`), så det ligner en
telefon. Byg med `build.py` og genindlæs, når du har rettet noget, så det han ser i
panelet er den nyeste version.

Der findes en preview-konfiguration `markjournal-web` i `.claude/launch.json` (port 8090) —
brug `preview_start` med det navn frem for at starte serveren manuelt. Manuelt svarer det til:

```bash
python3 -m http.server 8090 -d ~/Projekter/markjournal-web
```

Deploy = `git push` herfra. GitHub Pages bygger derefter automatisk;
det tager typisk 30–60 sekunder. Verificér med:

```bash
gh api repos/RybergPYT/markjournal/pages/builds/latest --jq .status
```

`gh` er installeret via Homebrew i `~/homebrew/bin` (ikke i standard-PATH — brug
`export PATH="$HOME/homebrew/bin:$PATH"`) og er autentificeret som RybergPYT.

## Opdatér middeldatabasen

```bash
cd ~/Projekter/markjournal-web && python3 hent_midler.py
```

Henter godkendte plantebeskyttelsesmidler fra Miljøstyrelsens BMD og skriver
`midler.json` (~440 midler, ~230 KB). Scriptet klarer selv CSRF-token + cookie mod
det offentlige eksport-endpoint. Kør et par gange om året. Filen er statisk data —
den kræver ikke `build.py` bagefter.

## Arkitektur

**Én fil, sektionsopdelt.** `app-template.html` (~2000 linjer) indeholder HTML, CSS og
JS samlet. JS'en er opdelt i navngivne sektioner (`/* ===== MIDDELDATABASE ===== */`,
`/* ===== LEAFLET-KORT ===== */`, …) — brug dem til at navigere.

**Skærme og ark.** Hver skærm er en `.scr`-div; `go(id)` skifter mellem dem.
Modale trin (registrering, ny mark, indstillinger …) er `#step-*`-divs inde i ét
delt ark, styret af `showStep(navn)`. **Tilføjer du et nyt trin, skal navnet med i
arrayet inde i `showStep()`** — ellers bliver det aldrig skjult igen.

**Fanelinjen har fire faner** + plus-knappen: Kort, Marker, Download (`scr-sj` —
sprøjtejournal med PDF/CSV-eksport) og Mere. **Opgave-funktionen er fjernet
(27. juli 2026)** på Sørens ønske og erstattet af Download-fanen — genindfør den
ikke. Nøglen `markjournal-opgaver-v1` kan stadig ligge i localStorage og i gamle
sikkerhedskopier hos brugere; den bliver bare ignoreret.

**Rækkefølge betyder noget.** Alt kører i ét stort script-tag uden moduler.
`const`-erklæringer må ikke bruges før de er nået (temporal dead zone) — det har
sprængt appen ved start én gang. Ved tvivl: brug funktionserklæringer (hoistes) eller
skriv strenge direkte i stedet for at referere konstanter defineret længere nede.

**Data i localStorage** (7 nøgler, alle med `-v1`-suffix):

| Nøgle | Indhold | I backup? |
|-------|---------|-----------|
| `markjournal-journal-v1` | Alle registreringer pr. mark | ✅ |
| `markjournal-marker-v1` | Brugerens egne oprettede marker | ✅ |
| `markjournal-tilpasninger-v1` | Omdøbte/skjulte demomarker | ✅ |
| `markjournal-hotspots-v1` | Markeringer på kortet | ✅ |
| `markjournal-indstillinger-v1` | Bedriftsnavn og CVR | ✅ |
| `markjournal-onboarding-set-v1` | Er velkomstguiden vist? | ❌ (bevidst) |
| `markjournal-sidste-backup-v1` | Dato for sidste sikkerhedskopi | ❌ (bevidst) |

Tilføjer du en ny datanøgle, skal den med i `BACKUP_NOEGLER`, ellers ryger den ved
skift af telefon.

**Demomarker vs. egne marker.** De seks marker fra `egne_marker_wgs84.json` er
indbygget og kan ikke slettes rigtigt — de "skjules" via `tilpasninger`-nøglen.
Brugerens egne marker fjernes derimod helt. `MARKER` (objekt i hukommelsen) er
resultatet af begge dele lagt sammen ved opstart.

**Service worker.** `sw.js` cacher kun appens egne filer (netværk først, cache som
fallback); kort-tiles og vejr-API rammer altid nettet. **Bump `CACHE`-versionen
(`markjournal-v3` → `-v4`) når du tilføjer eller fjerner filer i `ASSETS`.**

## Eksterne tjenester (alle gratis, ingen API-nøgle)

| Tjeneste | Bruges til | Bemærkning |
|----------|-----------|------------|
| `api.open-meteo.com` (`models=dmi_seamless`) | DMI HARMONIE-vejr | Driver sprøjte-anbefalingen og auto-udfyldt vejr i journalen |
| `geodata.fvm.dk/geoserver` | Landbrugsstyrelsens markblokke (WMS-lag + WFS-opslag) | Sender CORS `*`. WFS-bbox: prøv begge akse-rækkefølger — serveren er inkonsistent |
| `api.dataforsyningen.dk/autocomplete` | Adressesøgning (DAWA) | |
| `server.arcgisonline.com` / `tile.openstreetmap.org` | Luftfoto / vejkort | |

Leaflet er **vendored** i `leaflet/` — ingen CDN (appen skal virke offline, og
GitHub Pages har ingen build-proces).

## Test og verifikation

Der er ingen testramme. Verifikation sker ved at køre appen i browser-panelet og
kalde funktionerne direkte med `javascript_tool`, fx:

```js
openSheet(Object.keys(MARKER)[0]); pickType("Sprøjtning");
```

Faldgruber lært af tidligere fejl:
- **Test altid med frisk indlæsning.** Kortet zoomede engang ud til hele verden ved
  opstart, fordi `fitBounds` kørte før layoutet var færdigt — det ses ikke i en
  allerede varm side. `sikrKortUdsnit()` findes nu som værn.
- **Syntetiske klik driller Leaflet** (utilsigtede pan/hop). Verificér korttilstand
  med JS-kald (`kort.getZoom()`, `kort.getCenter()`) frem for klik+screenshot.
- Ryd testdata bagefter: `localStorage.removeItem("markjournal-journal-v1")`.

## Forbedringsloop

`FORBEDRINGER.md` er backlog + selv-feedback, ført iteration for iteration. Hver
iteration: implementér én ting → test → deploy → skriv ærlig kritik (inkl. fundne
bugs og bevidste fravalg) → næste iteration tager feedbacken op. Læs den nyeste
iteration øverst, før du vælger næste opgave.

## Fagligt og juridisk

- **Appen dømmer ikke om lovlighed.** Tidligere skrev den "ikke godkendt i
  vinterhvede" ud fra en opdigtet liste. Nu vises Miljøstyrelsens juridisk bindende
  etikettekst, og landmanden bekræfter selv. Afgrøde-matchet (`AFGRODE_ORD`) er ren
  tekstsøgning og må kun bruges til at sortere og fremhæve — aldrig til at afgøre.
- **Sæson = dansk høstår**, 1. august → 31. juli (`datoTilSaeson()`).
- Datoer i journalen gemmes som `dd.mm.åå`-strenge; sortering sker ved at vende dem
  om til `ååmmdd`.
- Sprøjtejournalen skal kunne fremvises ved kontrolbesøg — PDF-eksporten skal
  indeholde dato, mark, markblok, afgrøde, areal, middel og dosering.

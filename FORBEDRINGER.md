# Markjournal — forbedrings-loop

Backlog og selv-feedback for det løbende forbedringsloop. Én forbedring pr.
iteration; hver iteration slutter med kritisk feedback, som næste iteration
tager først. INGEN sky-synkronisering (Sørens beslutning, juli 2026).

## Backlog (prioriteret)

**Top 3 vurdering (26.07.26):** 1) ~~sikkerhedskopi~~ ✅ it. 12 · 2) rigtig middeldatabase (BMD) ·
3) flere marker på én registrering. Kemilager nedprioriteret.

1. ~~Alle registreringstyper (gødskning, såning, jordbearbejdning, vanding, høst)~~ ✅ iteration 1
1b. ~~SØRENS ØNSKER: adressesøgning + tilføj mark fra markblok + tegn egen mark~~ ✅ iteration 2
2. ~~Slet/redigér en registrering OG slet/omdøb en mark~~ ✅ iteration 3
3. ~~Hotspots: opret på kortet, gem lokalt, egne noter~~ ✅ iteration 10
4. Registrér på flere marker på én gang (fx sprøjtning af 3 marker i træk)
5. ~~Sæson-vælger i journal, udbytter, PDF og CSV~~ ✅ iteration 8
6. ~~Opgaver: rigtige opgaver med localStorage (opret/afslut)~~ ✅ iteration 6
7. ~~PDF-eksport af sprøjtejournal (print-venlig side + window.print())~~ ✅ iteration 4
8. Kemilager: simpel beholdning pr. middel, træk ved registrering
9. ~~Udbytte-oversigt pr. mark under "Mere → Udbytter"~~ ✅ iteration 7
10. ~~Middeldatabase: Miljøstyrelsens BMD-udtræk~~ ✅ iteration 16
11. ~~Onboarding: første gang appen åbnes → kort guide~~ ✅ iteration 9 (Sørens ønske)
12. Egne marker: vælg markblok på kortet og navngiv den (WFS point-query — CORS er ok)

## Selv-feedback pr. iteration

### Iteration 20 (læsbar aktivstof-linje) — 28.07.26
Tog første punkt op fra iteration 17's egen feedback.
- ✅ BMD leverer aktivstof og styrke som to parallelle lister klistret sammen til
  én streng: `a="prosulfocarb; clodinafop-propargyl"`, `k="800; 10 g/l; g/l"`.
  Rå viste appen "prosulfocarb; clodinafop-propargyl · 800; 10 g/l; g/l" — hvor
  "g/l; g/l" er ren støj. `formatAktivstof()` parrer dem nu:
  **"prosulfocarb 800 + clodinafop-propargyl 10 g/l"**
- ✅ Enheden skrives kun én gang til sidst. Kontrolleret mod hele databasen:
  enhederne er **aldrig** blandede inden for ét middel, så det er entydigt
- ✅ Verificeret på alle 440 midler: 439 formateres rent, 0 giver `undefined`/`NaN`
- ✅ Bruges både i middellisten og på etiket-skærmen
- ✅ Sidegevinst: de fleste rækker fylder nu én linje i stedet for to, så der er
  flere midler synlige pr. skærm
- ⚠️ Isomate CLR falder tilbage til rådata, fordi kilden selv er afkortet med "…"
  (5 værdier, 3 aktivstoffer). Bevidst: funktionen gætter ikke, den viser rådata.
  Det er 1 af 440
- ⚠️ Fejlen stammer egentlig fra `hent_midler.py`, som sætter de to lister sammen
  til én streng. Rettes den ved kilden (to separate felter), bliver visningen
  simplere — men det kræver, at `midler.json` hentes igen
- ⚠️ Resten af iteration 17's fund er stadig ikke rettet: markbloknumre ombryder,
  blå tæller-chips i en grøn app, "Vælg en mark" ser trykbar ud mens den er
  deaktiveret, journalrækker mangler chevron, og 💦/💧 er næsten samme ikon


### Iteration 19 (appen leveres tom — Sørens ønske) — 28.07.26
- ✅ Alle demodata fjernet: de seks demomarker (tom `egne_marker_wgs84.json` + tom
  `MARK_CONFIG`) og de fem demoregistreringer (`DEFAULT_JOURNAL = {}`). index.html
  faldt fra 104 til 91 KB
- ✅ Uden marker giver `bedriftOmraade()` `null`, og kortet ville zoome ud til hele
  verden. `startKortUdsnit()` viser nu Danmark straks og zoomer derefter til GPS;
  nægtes position, bliver Danmark stående. Kortet venter aldrig på GPS
- ✅ `sikrKortUdsnit()` sænker zoom-tærsklen fra 10 til 5 uden marker — Danmark
  ligger omkring zoom 7 og ville ellers blive re-fittet i det uendelige
- ✅ `hentVejr()` bruger kortets centrum, når der ingen marker er
- ✅ To tomme tilstande som demodataene har skjult hele vejen: marklisten sagde
  ingenting, og markvalget i registreringsflowet var en **blindgyde** (tom liste +
  deaktiveret knap). Sidstnævnte fører nu direkte til "Opret din første mark"
- ✅ "Nulstil til demodata" henviste til noget, der ikke findes mere → "Slet alle
  registreringer"
- ⚠️ **Konsekvens for eksisterende brugere:** registreringer, der ligger på m1–m6 i
  localStorage, peger nu på marker, der ikke findes, og forsvinder ud af journalen
  uden at blive slettet. Der er ingen oprydning eller migrering — bevidst fravalg,
  da appen reelt kun har én bruger
- ⚠️ Demomarkerne var det eneste, der viste appen i brug. Onboardingen forklarer
  nu funktioner, som en ny bruger ikke kan se effekten af, før de selv har oprettet
  en mark

### Iteration 18 (kortknapper efter Sørens ønske) — 28.07.26
- ✅ "Mine marker"-knappen (hus-ikon) fjernet helt, og `hjemTilBedrift()` slettet,
  da den kun blev kaldt derfra. Opstartszoom går via `bedriftOmraade()` og er urørt
- ✅ "Min placering" er nu en ren ikonknap (44×44) uden tekst; navnet ligger i
  `aria-label` + `title`
- ✅ Knappen skiftede før tekst til "Søger …" under GPS-opslag — det gav et
  layout-hop. Nu bliver ikonet stående, og `.soeger` (grøn baggrund) + toast viser
  tilstanden
- ✅ `.kortbox` havde ingen brugere tilbage og er erstattet af `.kortikon`
- ⚠️ Kortet har nu ingen genvej tilbage til bedriften, når man har panoreret væk.
  Det var Sørens eksplicitte ønske, men det er den slags, man savner først efter
  et stykke tids brug

### Iteration 17 (designgennemgang: tre rettelser) — 28.07.26
Struktureret designkritik af hele appen kørt i browserpanelet, derefter de tre
højest prioriterede fund rettet.
- ✅ **Fanen "Download" → "Journal"** (nyt dokumentikon). Skærmen *er*
  sprøjtejournalen; download er blot måden at få den ud på. Den, der leder efter
  "hvad har jeg sprøjtet?", ledte aldrig under Download
- ✅ **Læsbarhed i sol og med handsker:** alle kortknapper op fra 32–38 px til
  mindst 44 px. `--muted` mørkere (#79816F → #5F6857), sektionsoverskrifter og
  pills op i størrelse. Chevronerne (›) stod i kantfarven med 1,3:1 og var reelt
  usynlige. Målt bagefter: **alle tekster på Kort, Journal, Marker og Mere består
  nu WCAG AA (4,5:1)** — seks dumpede før
- ✅ **Middellisten** sorteres ikke længere rent alfabetisk gennem 440 midler. Uden
  søgning vises "Senest brugt" (op til 6 fra journalen, nyeste først), "Nævner
  <afgrøde>" og "Øvrige midler". Mærkatet "Nævner vinterhvede" stod på **hver
  eneste række** og bar derfor ingen information — fjernet fra rækkerne og gjort
  til sektionsoverskrift. Kun den reelle advarsel "Må bruges til <dato>" står
  stadig på rækken
- ⚠️ Fundet, men ikke rettet i denne iteration: aktivstof-linjen viser rå data
  ("800; 10 g/l; g/l"), markbloknumre ombryder midt i nummeret, tæller-chips er
  blå i en grøn app, "Vælg en mark"-knappen ser trykbar ud mens den er deaktiveret,
  journalrækker mangler chevron (kan en fejlregistrering rettes?), og ikonerne for
  Sprøjtning 💦 og Vanding 💧 er næsten ens
- ⚠️ Doserings-, vejr- og etikettrinnene i sprøjteflowet blev **ikke** gennemgået —
  programmatiske klik kom ikke forbi middelvalget. De er stadig ubedømte
- ⚠️ "Senest brugt" kunne ikke verificeres med demodata, fordi demojournalens
  midler (Propulse SE 250, Mavrik Vita) slet ikke findes i `midler.json`. Måtte
  testes med rigtige midler fra databasen. Det betyder også, at "Som sidst" ikke
  kan slå etiketten op for et middel, databasen ikke kender


### Iteration 16 (rigtig middeldatabase fra Miljøstyrelsen) — 27.07.26
- ✅ De 5 opdigtede demo-produkter er erstattet af **440 rigtige midler** fra Miljøstyrelsens
  Bekæmpelsesmiddeldatabase (420 godkendte + 20 under udfasning med gyldig anvendelsesfrist)
- ✅ Fandt BMD's offentlige eksport-endpoint (/External/Entry/GenerateDocument, CSRF-token +
  cookie, Excel-format). hent_midler.py gentager hele hentningen når data skal opdateres
- ✅ Ny etiket-skærm: viser den **juridisk bindende anvendelsestekst** ("Må kun anvendes til
  ukrudtsbekæmpelse i vintersæd, kartofler og frøgræs"), aktivstof, koncentration, reg.nr. og kilde
- ✅ Udfasede midler får gul advarsel med den præcise frist ("må kun anvendes og opbevares
  til og med 30.06.2027") — vigtigt og svært at holde styr på selv
- ✅ Midler der nævner markens afgrøde sorteres øverst og markeres grønt; øvrige får "Tjek etiket"
- ⚠️ **Bevidst designvalg:** appen dømmer IKKE længere "ikke godkendt i X" som før. Afgrøde-matchet
  er tekstsøgning i etiketten og kan ikke være juridisk præcis — derfor vises den rigtige tekst,
  og landmanden bekræfter selv. Det er mere ærligt end en opdigtet godkendelse
- ⚠️ Ingen doseringsgrænser pr. afgrøde (findes ikke i BMD-udtrækket, kun i etiketten)
- ⚠️ Data skal opdateres manuelt med hent_midler.py — bør nok gøres et par gange om året

### Iteration 15 (brugervenlighedspakke — Sørens ønske) — 26.07.26
Fem forbedringer der alle sigter mod: brugbar stående i marken, én hånd, handsker på.
- ✅ **Genvej fra GPS**: "Du står på Bakkelodden · [Registrér her]" — grøn boks på kortet
  med knap der åbner registrering med marken forvalgt. Sparer 3 tryk på den hyppigste handling
- ✅ **Færre trin**: starter man fra en mark (mark-siden eller GPS-boksen), springes markvalget
  helt over: type → middel → detaljer. Titlen viser marken, så man ved hvor det havner
- ✅ **"Som sidst"**: grøn genvej øverst i middel-listen der gentager seneste sprøjtning på
  netop den mark (middel + dosering) og hopper direkte til detaljer. Vælger man samme middel
  manuelt, foreslås sidste dosering automatisk
- ✅ **Hurtigvalg til dosering**: 0,25 / 0,5 / 0,75 / 1,0 / 1,5 / 2,0 l/ha som store knapper —
  intet taltastatur i traktoren. Sidste dosering lægges forrest hvis den afviger
- ✅ **Større trykflader**: rækker min. 56 px, chips og knapper min. 46 px (handsketilpasset)
- ✅ **Falske knapper fjernet**: "Kemilager" og "Brugere på bedriften" sagde bare
  "kommer i næste version" — de er væk, så alt i menuen nu virker
- ✅ Fanget bug: "📍 Min placering"-knappen mistede sin tekst efter brug (gammel ◎-kode)
- ⚠️ "Som sidst" findes kun for sprøjtning — gødskning og de andre typer kunne få samme
- ⚠️ Hurtigvalg er faste tal; kunne læres af brugerens egne hyppigste doseringer

### Iteration 14 (tydelige kortknapper + kritisk kortfejl) — 26.07.26
- ✅ Sørens ønske: ◎ og ⌂ erstattet af tekstknapper "📍 Min placering" og "🏠 Mine marker"
- ✅ FANGET ALVORLIG FEJL: kortet åbnede zoomet ud på HELE VERDEN (zoom 0), fordi fitBounds
  kørte før layoutet var færdigt. Ramte alle brugere ved appstart på telefon.
  Fix: sikrKortUdsnit() med invalidateSize + gen-zoom ved load, resize og efter 400 ms
- ⚠️ Lære: alt der måler skærmstørrelse skal verificeres EFTER load, ikke kun i test hvor
  siden allerede er varm — test altid med frisk indlæsning

### Iteration 13 (min GPS-position — Sørens ønske) — 26.07.26
- ✅ ◎-knap på kortet: finder din position, zoomer derhen, viser blå prik med
  nøjagtighedscirkel (±m) og siger HVILKEN af dine marker du står på (punkt-i-polygon).
  Følger positionen mens du kører, men stopper efter 5 min og når appen lukkes (batteri)
- ✅ Position hentes nu først når man trykker — ingen tilladelses-prompt ved opstart
- ✅ Verificeret: inde i mark → "Du står på Bakkelodden ±6 m"; udenfor → korrekt besked;
  afvist tilladelse og timeout giver hver sin brugbare fejlbesked
- ⚠️ "Du står på X" kunne tilbyde en genvej: "Registrér på Bakkelodden nu" — stærk kobling
- ⚠️ Ingen visuel markering af at følge-tilstanden er aktiv

### Iteration 12 (sikkerhedskopi og gendannelse) — 26.07.26
- ✅ Mere → "Gem sikkerhedskopi": alle 6 datanøgler i én JSON-fil med dato i filnavnet;
  "Gendan fra sikkerhedskopi" med bekræftelse der viser dato + antal registreringer.
  Datoen for sidste kopi vises i menuen som påmindelse
- ✅ Fanget alvorlig fejl før deploy: BACKUP_NOEGLER refererede konstanter defineret senere i filen
  (temporal dead zone) → ville sprænge hele appen ved start. Nøglenavnene skrives nu direkte
- ✅ Verificeret: fuld cyklus gem → localStorage.clear() → gendan giver alt tilbage;
  ugyldige og fremmede filer afvises uden at røre eksisterende data
- ⚠️ Ingen automatisk påmindelse om at tage backup — kunne advare hvis sidste kopi er > 30 dage
- ⚠️ Backup er manuel; brugeren skal selv lægge filen et sikkert sted (bevidst — ingen sky endnu)

### Iteration 11 (GPS-hotspot + hotspot-liste) — 26.07.26
- ✅ "📍 Her hvor jeg står"-knap i hotspot-tilstand: bruger telefonens GPS, zoomer derhen og
  åbner arket — ingen præcisionstryk med handsker på. Knappen vises kun i hotspot-tilstand
- ✅ Mere → "Markeringer på kortet": liste med ikon, type og note; tryk = zoom til pin på kortet,
  ✕ = slet. Listen opdaterer sig selv efter sletning. Hele flowet verificeret med simuleret GPS
- ⚠️ Ingen afstands-visning ("340 m herfra") — ville hjælpe med at prioritere i listen
- ⚠️ Hotspots kan stadig ikke redigeres, kun slettes
- → Næste kandidater: kemilager (#8), flere marker på én registrering (#4), rigtig middeldatabase (#10)

### Iteration 10 (hotspots på kortet) — 26.07.26
- ✅ Plus-knappen → Hotspot: tryk på kortet, vælg type (🪨 sten, 💧 drænbrønd, 🦌 vildtskade,
  🌊 vådt hul, 📍 andet) + note. Vises som emoji-pin, gemmes lokalt, tryk på pin = slet.
  Hele livscyklussen verificeret inkl. genindlæsning. De to fake demo-hotspots er væk
- ⚠️ Hotspots kan ikke redigeres, kun slettes og oprettes igen
- ⚠️ Ingen liste over hotspots — ved mange pins bliver de svære at finde uden at scanne kortet
- ⚠️ "Brug min GPS-position" ville være hurtigere end at trykke præcist, når man står ved stenen
- → Næste kandidater: kemilager (#8), flere marker på én registrering (#4), rigtig middeldatabase (#10)

### Iteration 9 (onboarding — Sørens ønske) — 15.07.26
- ✅ 5-trins velkomstguide første gang appen åbnes: velkomst, kortet/markblokke, plus-knappen,
  opret egen mark, PDF til kontrolbesøg. Prikker viser hvor man er, "Spring over" skjules på sidste trin,
  valget huskes i localStorage. Kan altid genses via Mere → "Sådan bruger du appen"
- ✅ Fandt bug undervejs: `window.kort` er altid falsk (const bindes ikke til window),
  så kortets invalidateSize kørte aldrig — rettet to steder til typeof-tjek
- ⚠️ Guiden er tekst+emoji; små skærmbilleder af de faktiske skærme ville være stærkere
- ⚠️ Ingen swipe mellem trin — kun knappen. Fint på traktor-fingre, men swipe forventes af mange

### Iteration 8 (sæson-filter) — 15.07.26
- ✅ Dansk høstår (1. aug → 31. juli) beregnes af datoen; sæson-chips i sprøjtejournal og udbytter,
  "Alle år" som ekstra valg. PDF-titel og CSV følger valget (CSV har nu egen sæson-kolonne).
  Verificeret: 25/26 vs 26/27 giver korrekt opdelte rækker og totaler
- ⚠️ Valget nulstilles til indeværende sæson ved genstart — bevidst, men bør måske huskes
- ⚠️ Mark-detaljens journal viser stadig ALLE sæsoner uden filter

### Iteration 7 (udbytte-oversigt) — 15.07.26
- ✅ Mere → Udbytter er nu en rigtig side: høst-registreringer pr. mark, nyeste først,
  med automatisk t/ha × ha = samlet tons pr. mark og totalsum i pill'en.
  Beregning verificeret mod manuelt regnestykke (202 t)
- ⚠️ Ingen sæson-opdeling — når to års høst ligger i samme liste, bliver totalen misvisende.
  Sæson-filter (#5) er nu den vigtigste manglende brik og bør tages næste gang
- ⚠️ Udbytte pr. afgrøde (fx alle hvedemarker samlet) kunne være næste niveau

### Iteration 6 (rigtige opgaver) — 15.07.26
- ✅ Opgaver-fanen er nu ægte: opret (titel, note, valgfri mark), afkryds, slet — localStorage,
  tæller-pill ("2 åbne"/"Alt klaret"), afsluttede vises overstreget nederst. Fuld livscyklus verificeret
- ✅ Demo-påmindelserne fjernet (forvirrende fake-indhold)
- ⚠️ Opgaver har ingen dato/frist — "i morgen"-planlægning kunne være næste niveau
- ⚠️ En afsluttet sprøjte-opgave kunne tilbyde "registrér i journalen nu?" — stærk kobling
- → Næste kandidater: sæson-filter i journal (#5), udbytte-oversigt (#9), hotspots på kort (#3)

### Iteration 5 (Indstillinger: bedriftsnavn + CVR) — 15.07.26
- ✅ Mere → Indstillinger: bedriftsnavn og CVR gemmes lokalt og sættes automatisk ind i
  PDF-rapporten (verificeret: værdier optræder i rapport-HTML + persistens)
- ⚠️ Registrering kan stadig kun slettes, ikke redigeres — overvej redigér-flow
- → Næste gode kandidater: opgaver med localStorage (#6), sæson-filter i journal (#5),
  udbytte-oversigt (#9) eller hotspots på kortet (#3). Opgaver (#6) giver mest dagligdags-værdi

### Iteration 4 (print/PDF af sprøjtejournal) — 15.07.26
- ✅ "Gem / print som PDF" bygger en kontrolklar rapport (dato, mark, blok, afgrøde, areal,
  middel+dosering+vejr) sorteret nyeste først, med CVR/underskriftsfelter, og åbner print-dialogen
  (på iPhone: Del → Gem som PDF). Verificeret med stubbet window.print + visuel inspektion
- ⚠️ Bedrift/CVR er blanke linjer til håndudfyldning — burde hentes fra Indstillinger (som ikke findes endnu)
  → tag "Indstillinger med bedriftsnavn/CVR" som del af næste iteration, så rapporten bliver helt færdig
- ⚠️ Rapporten viser kun sprøjtninger; gødskning kunne med fordel få sin egen rapport senere

### Iteration 3 (slet/omdøb marker + slet registreringer) — 15.07.26
- ✅ "Redigér"-knap på mark-siden: omdøb navn/afgrøde, slet mark (m. journal-advarsel);
  demomarker skjules via tilpasnings-lag, egne marker fjernes helt. Verificeret på tværs af genindlæsning
- ✅ Tryk på journal-række → bekræft → slet. Guards i sprøjtejournal/CSV mod slettede marker
- ⚠️ Sletning bruger window.confirm — fungerer, men et pænt dansk bekræftelses-ark ville være bedre UX
- ⚠️ Journal-rækken viser ✕ men intet "redigér" — redigering af en registrering mangler stadig (kun slet+opret-ny)
- → Næste: opgaver med localStorage (backlog #6) eller print-venlig PDF (#7); PDF er nok mest værdifuld til kontrolbesøg

### Iteration 2 (Sørens ønsker: adressesøgning, mark fra markblok, tegn mark) — 15.07.26
- ✅ DAWA-adressesøgning (gratis, ingen nøgle), WFS-punktopslag med akse-fallback,
  tegnefunktion med korrekt geodætisk arealberegning (verificeret: trekant 190×200 m = 1,9 ha)
- ✅ Fandt og fiksede dublet-bug: dobbelt tryk på "Opret mark" gav to marker → kladde-vagt
- ⚠️ Marker kan oprettes men IKKE slettes/omdøbes — kritisk hul, tag som næste iteration
- ⚠️ Tegn-tilstand: intet visuelt punkt-nummer; svært at se om første punkt er sat
- ⚠️ MARK_CONFIG-demomarkerne bør kunne skjules, når brugeren har egne marker

### Iteration 1 (alle registreringstyper) — 15.07.26
- ✅ Generisk formular-motor (TYPEDEF) gør nye typer billige at tilføje
- ⚠️ Journal-rækker kan stadig ikke rettes/slettes — en fejlindtastning er permanent.
  Det er det største "easy to use"-hul for en landmand med handsker på → tag backlog #2 næste gang
- ⚠️ "Udbytter" under Mere er stadig en død knap, selvom Høst-typen nu findes → kobl til #9
- ⚠️ Sprøjtejournal-skærmen viser kun sprøjtninger; overvej fane/filter for alle typer

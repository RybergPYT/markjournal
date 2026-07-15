# Markjournal — forbedrings-loop

Backlog og selv-feedback for det løbende forbedringsloop. Én forbedring pr.
iteration; hver iteration slutter med kritisk feedback, som næste iteration
tager først. INGEN sky-synkronisering (Sørens beslutning, juli 2026).

## Backlog (prioriteret)

1. ~~Alle registreringstyper (gødskning, såning, jordbearbejdning, vanding, høst)~~ ✅ iteration 1
1b. ~~SØRENS ØNSKER: adressesøgning + tilføj mark fra markblok + tegn egen mark~~ ✅ iteration 2
2. Slet/redigér en registrering OG slet/omdøb en mark (tap → handlingsark) — VIGTIGST NU: man kan oprette marker men aldrig fjerne dem igen!
3. Hotspots: opret på kortet med tryk-og-hold / knap, gem i localStorage, egne noter
4. Registrér på flere marker på én gang (fx sprøjtning af 3 marker i træk)
5. Sæson-vælger i journalen (25/26, 26/27 …) i stedet for fast tekst
6. Opgaver: rigtige opgaver med localStorage (opret/afslut) i stedet for demo-indhold
7. PDF-eksport af sprøjtejournal (print-venlig side + window.print())
8. Kemilager: simpel beholdning pr. middel, træk ved registrering
9. Udbytte-oversigt pr. mark under "Mere → Udbytter" (data findes fra Høst-typen)
10. Middeldatabase: erstat demo-listen med Miljøstyrelsens BMD-udtræk (statisk JSON i repo)
11. Onboarding: første gang appen åbnes → kort guide (3 skærme)
12. Egne marker: vælg markblok på kortet og navngiv den (WFS point-query — CORS er ok)

## Selv-feedback pr. iteration

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

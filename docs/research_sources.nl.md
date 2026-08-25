# Onderzoeksbronnen

Elke regel in [`src/ats_xray/rules.py`](../src/ats_xray/rules.py) draagt een
`source`-sleutel die naar een item hier verwijst, in plaats van een URL vast in
de code — zo corrigeer of vul je een bronvermelding op één plek aan zonder
Python aan te raken.

De meeste items hieronder verwijzen naar loopbaanadvies- en ATS-testbronnen in
plaats van naar één peer-reviewed studie, omdat deze kennis daar werkelijk
leeft: Applicant Tracking Systems zijn closed source en ongedocumenteerd. Wat
bekend is over hun parsinggedrag komt van leveranciers en coaches die echte
cv's tegen echte ATS-producten testen en publiceren wat ze vinden — niet uit de
documentatie van de ATS-leveranciers zelf of uit academisch onderzoek. Zie het
als consistente, breed herhaalde consensus in de sector, niet als
gecontroleerde experimenten. Links opgehaald in augustus 2026 en in het Engels
gelaten: de artikelen zijn Engelstalig.

## ats-fonts

Niet-standaard of niet-ingesloten lettertypen lopen het risico verkeerd gelezen, vervangen of volledig weggelaten te worden, met verminkte of ontbrekende tekst tot gevolg.

- [How ATS Handles Fonts: Complete Guide to Resume Formatting](https://hireflow.net/blog/how-ats-handles-fonts)

## ats-headers-footers

Inhoud in de kop- of voettekst van een document wordt door ATS-parsers vaak volledig overgeslagen; zij zien het als opvulling buiten de hoofdtekst van het document.

- [How ATS Reads Headers and Footers: Complete Guide to Resume Parsing](https://hireflow.net/blog/how-ats-reads-headers-and-footers)

## ats-text-boxes

Tekstvakken plaatsen inhoud buiten de normale alineastroom; veel parsers negeren die laag volledig, waardoor daar geplaatste tekst stilzwijgend verdwijnt.

- [Why ATS Rejects Resumes with Text Boxes: Complete Guide to ATS-Friendly Formatting](https://hireflow.net/blog/why-ats-rejects-resumes-with-text-boxes)

## ats-tables-columns

Indelingen met meerdere kolommen en tabellen worden door veel parsers rij voor rij dwars over de kolommen gelezen, waardoor door elkaar raakt welke waarde bij welk label hoort ("woordsalade").

- [Why ATS Tables and Columns Break Your Resume Parsing](https://www.jobscan.co/blog/resume-tables-columns-ats/)
- [Can ATS Read Tables & Columns? We Tested 8 Systems](https://cvcraft.roynex.com/blog/can-ats-read-tables-columns-formatting-2026)

## ats-graphics

Cv's die als afbeelding zijn geëxporteerd (gebruikelijk bij sjablonen uit ontwerpprogramma's zoals Canva) zetten inhoud in een vorm die de meeste parsers helemaal niet als tekst kunnen lezen.

- [Can ATS Read Tables, Columns and Canva Resumes?](https://www.mployee.me/blog/can-ats-read-tables-columns-canva-resumes)

## practical-necessity

Geen externe bron: wie geen contactgegevens in het cv zet, is voor een recruiter onbereikbaar, ongeacht wat een parser verder correct heeft gehaald. Deze regel bestaat om praktische, niet om onderzoeksredenen.

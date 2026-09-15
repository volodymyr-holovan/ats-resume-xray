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

---

De onderdelen hieronder zijn een ander soort regel. Ze gaan niet over wat software kan lezen, maar over wat recruiters in een bepaald land in een cv verwachten, en ze tellen nooit mee voor de score van 100. De bronnen zijn loopbaanadviezen uit dat land, geciteerd in de taal ervan. Geraadpleegd in september 2026.

## cv-volunteering

Duits advies is eensgezind dat vrijwilligerswerk (Ehrenamt) geen werkervaring vervangt en in een eigen rubriek hoort, na werkervaring en opleiding. Starters mogen relevant vrijwilligerswerk als ervaring vermelden, en een Freiwilliges Soziales Jahr of Bundesfreiwilligendienst kan als praktijkervaring tellen. Oekraïens advies plaatst vrijwilligerswerk in een eigen rubriek, tenzij het de hoofdbezigheid was. Nederlands, Spaans, Frans, Brits en Russisch advies accepteert vrijwilligerswerk onder werkervaring als het relevant is of betaalde ervaring beperkt is — daarom geldt de controle alleen voor Duitse en Oekraïense cv's.

- [Ehrenamt im Lebenslauf: Beispiele, wie angeben? — karrierebibel.de](https://karrierebibel.de/ehrenamt-lebenslauf/)
- [Ehrenamt im Lebenslauf angeben: Wo es hingehört — cvlotse.de](https://cvlotse.de/ratgeber/ehrenamt-im-lebenslauf)
- [FSJ und BFD im Lebenslauf angeben — cvlotse.de](https://cvlotse.de/ratgeber/fsj-bfd-im-lebenslauf)
- [Як і навіщо описувати волонтерство у резюме — happymonday.ua](https://happymonday.ua/yak-opysuvaty-volonterstvo-v-rezyume)
- [Vrijwilligerswerk op je cv vermelden — cvmaker.nl](https://www.cvmaker.nl/blog/cv/vrijwilligerswerk-cv)
- [¿Deberías incluir experiencia como voluntario en tu currículum? — Forbes España](https://forbes.es/empresas/356465/deberias-incluir-experiencia-como-voluntario-en-tu-curriculum/)
- [Bénévolat sur le CV : conseils et exemples — OnlineCV](https://www.onlinecv.fr/comment-faire-un-cv/travail-volontaire/)
- [How to include volunteer experience on a CV — Indeed UK](https://uk.indeed.com/career-advice/cvs-cover-letters/volunteer-experience-cv)
- [Какой опыт волонтерства указывать в резюме — HR Time](https://hrtime.ru/material/kakoy-opyt-volonterstva-ukazyvat-v-reziume-89267/)

## cv-gaps

Duits advies ziet een periode van meer dan twee maanden zonder werk of opleiding als een gat, vindt acht tot tien weken onschuldig en verwacht dat gaten vanaf drie tot vier maanden op het cv worden verklaard. Na het afronden van een opleiding geldt ongeveer zes maanden zoeken als normaal.

- [Lücken im Lebenslauf: Sinnvoll füllen und erklären — karrierebibel.de](https://karrierebibel.de/luecken-im-lebenslauf/)
- [Lücke im Lebenslauf — StepStone](https://www.stepstone.de/magazin/artikel/luecke-im-lebenslauf)
- [Lücken im Lebenslauf füllen und erklären — workwise](https://www.workwise.io/karriereguide/bewerbung/luecken-im-lebenslauf)

## cv-date-logic

Sollicitatiesystemen berekenen jaren ervaring uit de data van elk onderdeel, en recruiters filteren op dat getal. Data die het systeem niet kan berekenen, laten het ervaringsveld leeg of verkeerd geteld.

- [Resume Date Format: A Complete How-To Guide — Jobscan](https://www.jobscan.co/blog/resume-dates/)

## cv-first-person

Duits advies over de tabellarische Lebenslauf noemt onderdelen in fragmenten in plaats van hele zinnen, met een kort profiel in de ik-vorm als enige uitzondering. Amerikaans loopbaanadvies raadt eveneens aan persoonlijke voornaamwoorden te vermijden.

- [Tabellarischer Lebenslauf: Aufbau, Inhalt, Vorlagen — karrierebibel.de](https://karrierebibel.de/tabellarischer-lebenslauf/)
- [Tabellarischer Lebenslauf: Tipps & Muster — e-fellows.net](https://www.e-fellows.net/bewerbung/lebenslauf/tabellarischer-lebenslauf)
- [Resume Tips — Duke University Career Center](https://careerhub.students.duke.edu/resources/resume-tips/)

## cv-personal-details

§ 1 van de Allgemeines Gleichbehandlungsgesetz beschermt sollicitanten tegen benadeling op gronden waaronder geloof of levensovertuiging. Burgerlijke staat en kinderen horen niet bij die gronden; Duits advies beschrijft ze, net als geloof, als optionele gegevens die de meesten niet meer vermelden, waarbij geloof vooral voor kerkelijke werkgevers relevant is.

- [§ 1 Allgemeines Gleichbehandlungsgesetz — gesetze-im-internet.de](https://www.gesetze-im-internet.de/agg/__1.html)
- [Im Lebenslauf die Konfession angeben? — Indeed Deutschland](https://de.indeed.com/karriere-guide/bewerbung/lebenslauf-konfession)
- [Konfession im Lebenslauf: angeben oder weglassen? — cvlotse.de](https://cvlotse.de/ratgeber/konfession-im-lebenslauf)
- [Familienstand im Lebenslauf angeben oder nicht? — die-bewerbungsschreiber.de](https://www.die-bewerbungsschreiber.de/familienstand-lebenslauf)

## cv-reverse-chronological

Omgekeerd chronologische volgorde — de meest recente functie eerst — is de standaard geworden voor Duitse cv's, overgenomen uit het Amerikaanse formaat, waar loopbaanadvies ook elke rubriek zo ordent.

- [Antichronologischer Lebenslauf — Indeed Deutschland](https://de.indeed.com/karriere-guide/bewerbung/antichronologischer-lebenslauf)
- [Lebenslauf chronologisch: Absteigend oder aufsteigend? — karrierebibel.de](https://karrierebibel.de/lebenslauf-chronologisch/)
- [Chronologischer oder antichronologischer Lebenslauf — cvlotse.de](https://cvlotse.de/ratgeber/lebenslauf-reihenfolge)
- [Resume Tips — Duke University Career Center](https://careerhub.students.duke.edu/resources/resume-tips/)

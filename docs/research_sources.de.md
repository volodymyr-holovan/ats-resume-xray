# Forschungsquellen

Jede Regel in [`src/ats_xray/rules.py`](../src/ats_xray/rules.py) trägt einen
`source`-Schlüssel, der auf einen Eintrag hier verweist, statt einer fest im
Code stehenden URL — so lässt sich eine Quelle an einer Stelle korrigieren
oder ergänzen, ohne Python anzufassen.

Die meisten Einträge zitieren Karriereberatungs- und ATS-Testressourcen statt
einer einzelnen begutachteten Studie, weil dieses Wissen tatsächlich dort
liegt: Applicant Tracking Systems sind Closed Source und undokumentiert. Was
über ihr Parsing-Verhalten bekannt ist, stammt von Anbietern und Coaches, die
echte Lebensläufe gegen echte ATS-Produkte testen und veröffentlichen, was sie
finden — nicht aus der Dokumentation der ATS-Anbieter oder aus akademischer
Forschung. Behandeln Sie das als konsistenten, vielfach wiederholten
Branchenkonsens, nicht als kontrollierte Experimente. Links abgerufen im
August 2026 und auf Englisch belassen: die Artikel selbst sind englisch.

## ats-fonts

Nicht standardisierte oder nicht eingebettete Schriften können falsch gelesen, ersetzt oder ganz verworfen werden — mit verstümmeltem oder fehlendem Text als Folge.

- [How ATS Handles Fonts: Complete Guide to Resume Formatting](https://hireflow.net/blog/how-ats-handles-fonts)

## ats-headers-footers

Inhalte in Kopf- oder Fußzeilen werden von ATS-Parsern häufig vollständig übersprungen, weil sie als "Seitenbeiwerk" außerhalb des Textkörpers gelten.

- [How ATS Reads Headers and Footers: Complete Guide to Resume Parsing](https://hireflow.net/blog/how-ats-reads-headers-and-footers)

## ats-text-boxes

Textfelder legen Inhalte außerhalb des normalen Absatzflusses ab; viele Parser ignorieren diese Ebene komplett, sodass dortiger Text stillschweigend verloren geht.

- [Why ATS Rejects Resumes with Text Boxes: Complete Guide to ATS-Friendly Formatting](https://hireflow.net/blog/why-ats-rejects-resumes-with-text-boxes)

## ats-tables-columns

Mehrspaltige Layouts und Tabellen werden von vielen Parsern zeilenweise quer über die Spalten gelesen, wodurch die Zuordnung von Wert und Bezeichnung durcheinandergerät ("Wortsalat").

- [Why ATS Tables and Columns Break Your Resume Parsing](https://www.jobscan.co/blog/resume-tables-columns-ats/)
- [Can ATS Read Tables & Columns? We Tested 8 Systems](https://cvcraft.roynex.com/blog/can-ats-read-tables-columns-formatting-2026)

## ats-graphics

Als Bild exportierte Lebensläufe (häufig bei Design-Tool-Vorlagen wie Canva) bringen Inhalte in eine Form, die die meisten Parser gar nicht als Text lesen können.

- [Can ATS Read Tables, Columns and Canva Resumes?](https://www.mployee.me/blog/can-ats-read-tables-columns-canva-resumes)

## practical-necessity

Keine externe Quelle: Wer keine Kontaktdaten in den Lebenslauf schreibt, ist für Personalverantwortliche nicht erreichbar — unabhängig davon, was ein Parser korrekt extrahiert hat. Diese Regel besteht aus praktischen, nicht aus Forschungsgründen.

---

Die folgenden Einträge sind eine andere Art von Regel. Sie betreffen nicht, was Software lesen kann, sondern was Personalverantwortliche in einem bestimmten Land in einem Lebenslauf erwarten, und sie zählen nie zur Punktzahl von 100. Ihre Quellen sind Karriereratgeber des jeweiligen Landes, zitiert in dessen Sprache. Abgerufen im September 2026.

## cv-volunteering

Die deutsche Beratung ist sich einig, dass ein Ehrenamt keine Berufserfahrung ersetzt und in eine eigene Rubrik nach Berufserfahrung und Ausbildung gehört. Berufseinsteiger dürfen relevantes Ehrenamt unter Berufserfahrung nennen, und ein Freiwilliges Soziales Jahr oder ein Bundesfreiwilligendienst kann als Praxiserfahrung zählen. Die ukrainische Beratung ordnet Freiwilligenarbeit einer eigenen Rubrik zu, sofern sie nicht die Haupttätigkeit war. Niederländische, spanische, französische, britische und russische Ratgeber akzeptieren Ehrenamt unter Berufserfahrung, wenn es relevant ist oder bezahlte Erfahrung fehlt — deshalb gilt die Prüfung nur für deutsche und ukrainische Lebensläufe.

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

Die deutsche Beratung wertet einen Zeitraum von mehr als zwei Monaten ohne Beschäftigung oder Weiterbildung als Lücke, hält acht bis zehn Wochen für unbedenklich und erwartet, dass Lücken ab drei bis vier Monaten im Lebenslauf erklärt werden. Nach einem Abschluss gelten rund sechs Monate Stellensuche als normal.

- [Lücken im Lebenslauf: Sinnvoll füllen und erklären — karrierebibel.de](https://karrierebibel.de/luecken-im-lebenslauf/)
- [Lücke im Lebenslauf — StepStone](https://www.stepstone.de/magazin/artikel/luecke-im-lebenslauf)
- [Lücken im Lebenslauf füllen und erklären — workwise](https://www.workwise.io/karriereguide/bewerbung/luecken-im-lebenslauf)

## cv-date-logic

Bewerbermanagementsysteme berechnen die Berufsjahre aus den Daten jeder Station, und Personalverantwortliche filtern nach dieser Zahl. Daten, die das System nicht berechnen kann, lassen das Erfahrungsfeld leer oder falsch gezählt.

- [Resume Date Format: A Complete How-To Guide — Jobscan](https://www.jobscan.co/blog/resume-dates/)

## cv-first-person

Die deutsche Beratung zum tabellarischen Lebenslauf nennt Stationen in Stichpunkten statt in ganzen Sätzen, mit einem kurzen Profil in der Ich-Form als einziger Ausnahme. Auch US-amerikanische Karriereberatung rät, Personalpronomen zu vermeiden.

- [Tabellarischer Lebenslauf: Aufbau, Inhalt, Vorlagen — karrierebibel.de](https://karrierebibel.de/tabellarischer-lebenslauf/)
- [Tabellarischer Lebenslauf: Tipps & Muster — e-fellows.net](https://www.e-fellows.net/bewerbung/lebenslauf/tabellarischer-lebenslauf)
- [Resume Tips — Duke University Career Center](https://careerhub.students.duke.edu/resources/resume-tips/)

## cv-personal-details

§ 1 des Allgemeinen Gleichbehandlungsgesetzes schützt Bewerbende unter anderem vor Benachteiligung wegen der Religion oder Weltanschauung. Familienstand und Kinder gehören nicht zu den dort genannten Merkmalen; die deutsche Beratung beschreibt sie, ebenso wie die Konfession, als freiwillige Angaben, die die meisten nicht mehr machen — die Konfession ist vor allem bei kirchlichen Arbeitgebern relevant.

- [§ 1 Allgemeines Gleichbehandlungsgesetz — gesetze-im-internet.de](https://www.gesetze-im-internet.de/agg/__1.html)
- [Im Lebenslauf die Konfession angeben? — Indeed Deutschland](https://de.indeed.com/karriere-guide/bewerbung/lebenslauf-konfession)
- [Konfession im Lebenslauf: angeben oder weglassen? — cvlotse.de](https://cvlotse.de/ratgeber/konfession-im-lebenslauf)
- [Familienstand im Lebenslauf angeben oder nicht? — die-bewerbungsschreiber.de](https://www.die-bewerbungsschreiber.de/familienstand-lebenslauf)

## cv-reverse-chronological

Die antichronologische Reihenfolge — die jüngste Station zuerst — ist im deutschen Lebenslauf Standard geworden, übernommen aus dem US-Format, in dem auch die Karriereberatung jede Rubrik so ordnet.

- [Antichronologischer Lebenslauf — Indeed Deutschland](https://de.indeed.com/karriere-guide/bewerbung/antichronologischer-lebenslauf)
- [Lebenslauf chronologisch: Absteigend oder aufsteigend? — karrierebibel.de](https://karrierebibel.de/lebenslauf-chronologisch/)
- [Chronologischer oder antichronologischer Lebenslauf — cvlotse.de](https://cvlotse.de/ratgeber/lebenslauf-reihenfolge)
- [Resume Tips — Duke University Career Center](https://careerhub.students.duke.edu/resources/resume-tips/)

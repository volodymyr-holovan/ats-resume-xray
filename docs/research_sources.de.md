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

Nicht standardisierte oder nicht eingebettete Schriften riskieren, falsch gelesen, ersetzt oder ganz verworfen zu werden — mit verstümmeltem oder fehlendem Text als Folge.

- [How ATS Handles Fonts: Complete Guide to Resume Formatting](https://hireflow.net/blog/how-ats-handles-fonts)

## ats-headers-footers

Inhalte in Kopf- oder Fußzeilen werden von ATS-Parsern häufig vollständig übersprungen, weil sie als "Seitenbeiwerk" außerhalb des Dokumentkörpers gelten.

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

Keine externe Quelle: Ein Lebenslauf, auf dem eine recruitende Person keine Kontaktdaten findet, ist unerreichbar — unabhängig davon, was ein Parser korrekt extrahiert hat. Diese Regel besteht aus praktischen, nicht aus Forschungsgründen.

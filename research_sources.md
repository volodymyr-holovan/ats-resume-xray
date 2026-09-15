# Research sources

Every rule in [`src/ats_xray/rules.py`](src/ats_xray/rules.py) carries a
`source` key pointing to an entry here, instead of a raw URL baked into the
code, so a citation can be corrected or expanded in one place without
touching any Python.

Most entries below cite career-coaching / ATS-testing resources rather than a
single peer-reviewed study, because that is genuinely where this knowledge
lives: Applicant Tracking Systems are closed-source and undocumented, so what
is known about their parsing behaviour comes from vendors and coaches who test
real resumes against real ATS products and publish what they find — not from
the ATS vendors' own documentation or from academic parsing research. Treat
these as consistent, widely repeated industry consensus, not as controlled
experiments. Links retrieved August 2026, and kept in English: the articles
themselves are English.

## ats-fonts

Non-standard or non-embedded fonts risk being misread, substituted, or dropped entirely, producing garbled or missing text.

- [How ATS Handles Fonts: Complete Guide to Resume Formatting](https://hireflow.net/blog/how-ats-handles-fonts)

## ats-headers-footers

Content placed in a document's header or footer is commonly skipped entirely by ATS parsers, which treat it as "page furniture" outside the document body.

- [How ATS Reads Headers and Footers: Complete Guide to Resume Parsing](https://hireflow.net/blog/how-ats-reads-headers-and-footers)

## ats-text-boxes

Text boxes place content outside the normal paragraph flow; many parsers ignore that layer entirely, so text placed there is silently dropped.

- [Why ATS Rejects Resumes with Text Boxes: Complete Guide to ATS-Friendly Formatting](https://hireflow.net/blog/why-ats-rejects-resumes-with-text-boxes)

## ats-tables-columns

Multi-column layouts and tables get read row by row across columns by many parsers, scrambling which value belongs to which label ("word salad").

- [Why ATS Tables and Columns Break Your Resume Parsing](https://www.jobscan.co/blog/resume-tables-columns-ats/)
- [Can ATS Read Tables & Columns? We Tested 8 Systems](https://cvcraft.roynex.com/blog/can-ats-read-tables-columns-formatting-2026)

## ats-graphics

Resumes exported as images (common with design-tool templates like Canva) put content in a form most parsers cannot read as text at all.

- [Can ATS Read Tables, Columns and Canva Resumes?](https://www.mployee.me/blog/can-ats-read-tables-columns-canva-resumes)

## practical-necessity

Not an external citation: a resume a recruiter cannot find contact details on is unreachable regardless of what any parser extracted correctly. This rule exists for practical, not research, reasons.

---

The entries below are a different kind of rule. They are not about what software can read but about what recruiters in a particular country expect a CV to say, and they never count towards the parse-readiness score. Their sources are national career guidance, cited in the language of the country the convention belongs to. Retrieved September 2026.

## cv-volunteering

German guidance is consistent that volunteer work (Ehrenamt) does not replace Berufserfahrung and belongs in its own section after experience and education. Career starters may list relevant volunteering as experience, and a Freiwilliges Soziales Jahr or Bundesfreiwilligendienst can count as practical experience. Ukrainian guidance places volunteering in its own section unless it was the person's full-time occupation. Dutch, Spanish, French, UK and Russian guidance accept volunteering under work experience when it is relevant or paid experience is limited, which is why the check applies to German and Ukrainian CVs only.

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

German guidance treats a period of more than two months without employment or training as a gap, considers eight to ten weeks harmless, and expects gaps from three to four months to be explained on the CV. After finishing education around six months of job searching is regarded as normal.

- [Lücken im Lebenslauf: Sinnvoll füllen und erklären — karrierebibel.de](https://karrierebibel.de/luecken-im-lebenslauf/)
- [Lücke im Lebenslauf — StepStone](https://www.stepstone.de/magazin/artikel/luecke-im-lebenslauf)
- [Lücken im Lebenslauf füllen und erklären — workwise](https://www.workwise.io/karriereguide/bewerbung/luecken-im-lebenslauf)

## cv-date-logic

Applicant tracking systems calculate years of experience from the dates on each entry, and recruiters filter candidates by that figure. Dates the system cannot compute leave the experience field blank or miscounted.

- [Resume Date Format: A Complete How-To Guide — Jobscan](https://www.jobscan.co/blog/resume-dates/)

## cv-first-person

German guidance on the tabular Lebenslauf lists entries as fragments rather than full sentences, with a short first-person profile as the only exception. US career-office guidance likewise advises avoiding personal pronouns.

- [Tabellarischer Lebenslauf: Aufbau, Inhalt, Vorlagen — karrierebibel.de](https://karrierebibel.de/tabellarischer-lebenslauf/)
- [Tabellarischer Lebenslauf: Tipps & Muster — e-fellows.net](https://www.e-fellows.net/bewerbung/lebenslauf/tabellarischer-lebenslauf)
- [Resume Tips — Duke University Career Center](https://careerhub.students.duke.edu/resources/resume-tips/)

## cv-personal-details

§ 1 of the Allgemeines Gleichbehandlungsgesetz protects applicants against disadvantage on grounds including religion or belief. Marital status and children are not among its grounds; German guidance describes them, and religion, as optional details most applicants no longer include, with religion relevant mainly for church employers.

- [§ 1 Allgemeines Gleichbehandlungsgesetz — gesetze-im-internet.de](https://www.gesetze-im-internet.de/agg/__1.html)
- [Im Lebenslauf die Konfession angeben? — Indeed Deutschland](https://de.indeed.com/karriere-guide/bewerbung/lebenslauf-konfession)
- [Konfession im Lebenslauf: angeben oder weglassen? — cvlotse.de](https://cvlotse.de/ratgeber/konfession-im-lebenslauf)
- [Familienstand im Lebenslauf angeben oder nicht? — die-bewerbungsschreiber.de](https://www.die-bewerbungsschreiber.de/familienstand-lebenslauf)

## cv-reverse-chronological

Reverse chronological order — most recent position first — has become the standard for German CVs, adopted from the US format, where career-office guidance also organises each section that way.

- [Antichronologischer Lebenslauf — Indeed Deutschland](https://de.indeed.com/karriere-guide/bewerbung/antichronologischer-lebenslauf)
- [Lebenslauf chronologisch: Absteigend oder aufsteigend? — karrierebibel.de](https://karrierebibel.de/lebenslauf-chronologisch/)
- [Chronologischer oder antichronologischer Lebenslauf — cvlotse.de](https://cvlotse.de/ratgeber/lebenslauf-reihenfolge)
- [Resume Tips — Duke University Career Center](https://careerhub.students.duke.edu/resources/resume-tips/)

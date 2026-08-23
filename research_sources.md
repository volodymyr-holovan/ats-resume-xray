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

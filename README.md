# ATS Resume X-Ray

[![Tests](https://github.com/volodymyr-holovan/ats-resume-xray/actions/workflows/tests.yml/badge.svg)](https://github.com/volodymyr-holovan/ats-resume-xray/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)

**See your resume the way a parser sees it — not a fake "ATS score", an actual diff.**

Most "ATS score checkers" are black boxes: you upload a resume, get a number like
"87/100", and no idea what it actually means. This project does the opposite:
it shows you the extracted text, the exact structural issue behind each
finding, and a citation for why that pattern matters — nothing hidden.

Available as a web app (`streamlit run app.py`) or a CLI (`atsxray`).

## What it does

1. **Extracts text two ways** from your PDF/DOCX resume:
   - *Naive* — mimics a basic, layout-blind parser (the default behavior of
     common text-extraction libraries).
   - *Layout-aware* — detects columns and tables, and reads content in the
     order a human actually intends.

   Comparing the two reveals exactly where a real parsing pipeline would
   mangle or silently drop your content: a two-column layout that gets its
   lines interleaved, a table whose cells vanish entirely, text that only
   exists inside an image.

2. **Runs structural detectors** for other common failure patterns: non-embedded
   fonts, text hidden in headers/footers or Word text boxes, and large images
   standing in for real text.

3. **Recognizes fields** (name, email, phone, and the Experience/Education/Skills
   sections) under both extraction strategies, so it can flag content that's
   only readable in the best case. Section headings are recognized in English,
   German, Ukrainian, Russian, Spanish, Dutch and French — all at once, so a
   CV that mixes languages still resolves.

4. **Runs a rule engine** over all of the above: each documented risk pattern
   is a `Rule` with a citation into
   [`research_sources.md`](research_sources.md) — a transparent finding with
   evidence, a longer explanation of what it means, and concrete steps to fix
   it. Severity is judged per finding rather than fixed per rule: a repeated
   footer holding your phone number is serious, the same rule firing on
   "Page 1 of 2" is not.

5. **Shows you where the problem is.** Each finding carries the coordinates
   of the text it refers to, and the app renders your pages with those areas
   boxed. The section that disappears under naive parsing gets a red box
   drawn around it, on your actual resume.

   A DOCX stores content but no page positions, so it is laid out with
   LibreOffice first and the findings are then located on the result by
   searching for the text they reported. Without LibreOffice installed the
   app falls back to the text-only view rather than guessing at a layout
   your own word processor would disagree with.

6. **Scores parse readiness** — see below.

7. **Matches your CV against a job ad** — see below.

## Matching a CV against a job ad

Paste a job advert and the requirements are read out of it, then compared
against what the CV actually contains.

**The advert is read as three blocks, not as one bag of words.** German ads
label them ("Ihre Aufgaben", "Ihr Profil", "Wir bieten") and the labels mean
different things: the profile block states requirements, the tasks block only
implies them, and the offer block describes the employer. The offer block is
never scanned, which is what stops a company's Kubernetes training budget from
being reported as a skill you are missing.

**Requirements are weighted by how the ad phrases them.** "Zwingend
erforderlich" and "von Vorteil" are separated by cue phrase, and a required
item counts three times a preferred one. Where a line carries both kinds of
cue the softer reading wins, because overstating a blocking gap is the more
alarming error.

**Every profession, not just IT.** The gazetteer in
[`src/ats_xray/skills_data.py`](src/ats_xray/skills_data.py) holds around 400
skills across roughly fifty categories: care and medicine, the building
trades, logistics and driving, hospitality, cleaning and facilities, retail
and sales, finance and banking, law, consulting, design and media, teaching,
religious work, agriculture, textiles, security, production and office work,
alongside the software stack. Adding a trade means adding a line to that file
and nothing else.

**What the gazetteer does not know is guessed at.** A curated list is
accurate and finite; an advert for a job nobody thought to add would
otherwise come back empty, which is worse than a rough list because the
reader has nothing to correct. Two cheap signals fill the gap: German
capitalises its nouns, which is a better part-of-speech tagger than anything
that would fit in this project's dependencies, and every language announces
requirements with the same few phrases ("Kenntnisse in", "experience with",
"conocimiento de", "досвід роботи з"). The hard part is rejection, not
detection: a German bullet starts with a capital letter whatever word is
there, so "Abgeschlossene", "Gute" and "Mindestens" all look like nouns until
a stoplist says otherwise.

**The language is detected once, then only that language is read.** A CV and
the advert measured against it are written in one language, with English
turning up inside both. Reading all seven vocabularies at once was not merely
wasteful, it was wrong: Spanish "diploma" sits inside German "Diplomatie",
and Dutch "promotie" means a doctorate in Dutch and a sales campaign in
German. Detection is a function-word count with two extra signals, because a
CV is not prose -- a terse German one can contain as few as two German
function words, so section headings ("Berufserfahrung") and letters only one
language uses (ä, ö, ü, ß) count as evidence too.

**Case never matters.** Adverts arrive shouted, lower-cased and everything
between; all matching runs over a folded form, and an all-capitals line is
skipped by the noun heuristic rather than treated as a page of German nouns.

**Not everything is a keyword.** Degrees, years of experience, language levels
and driving licences compare by their own rules:

| Requirement | How it compares |
|---|---|
| Education | By level, so a Master satisfies an ad asking for a Bachelor. "Oder vergleichbare Qualifikation" turns the degree from a gate into a preference, and "Quereinsteiger willkommen" drops it entirely. Field of study is checked separately, and a level match in the wrong field scores partial. |
| Experience | Date ranges inside the experience section are summed, with overlapping periods merged rather than added. Study dates are not counted as work. Numbers written as words count too: "mindestens zwei Jahre" is as common as "mindestens 2 Jahre". |
| Languages | By CEFR level, reading the level whether it sits before the language ("verhandlungssichere Deutschkenntnisse") or after it ("Deutsch – B2"), and reading the language's name in whatever language the ad is written in. One level short scores partial. |
| Licence | Class is read where the ad names one, defaulting to B. |

**Extraction is a guess, and the guess is editable.** Everything found is shown
in an expandable list before anything is scored; you can delete what the parser
got wrong and type in what the ad only implied. Keywords you add yourself are
searched in the CV as phrases, with the same tolerance for German inflection
the built-in lexicon gets.

**A match only counts if a parser can see it.** Because the tool already knows
which parts of a CV survive a layout-blind read, a requirement met only in the
layout-aware text is reported as *at risk*: a human reader would find it, the
software filtering the pile might not.

The lexicon deliberately leaves out names that collide with ordinary words.
"Go" and "R" are real languages, but an ad saying "go live" should not acquire
a Go requirement, so they are reachable through "Golang" and "R-Programmierung"
instead. Abbreviations are held to word boundaries for the same reason: "bsc"
sits inside "Abschlussstärke" and "m sc" inside "zum Schichtdienst", and both
once invented a degree that the advert never asked for.

This is keyword and rule matching, not a judgement of your work. It reports
whether the ad's requirements are findable in your CV, and it says so on the
page.

## The parse readiness score

Commercial checkers blend two different things into one number: whether your
file parses, and how well its wording matches a specific job posting. The
second half needs the posting and the employer's weighting, which is why the
same resume scores 71 on one tool and 55 on another against the same job.

This scores only the half that is knowable from the file alone, and shows the
full arithmetic:

| Component | Weight | What it measures |
| --- | --- | --- |
| Contact reachability | 30% | Can an email or phone be recovered from the *naive* extraction? |
| Section survival | 30% | Of the sections that actually exist, how many survive naive reading? |
| Structural integrity | 40% | 100 minus a deduction per structural finding, by severity |

Two deliberate choices: sections the candidate never wrote are excluded from
the denominator rather than counted as failures, and any high-severity finding
caps the headline number — a resume whose skills table gets swallowed should
not be able to read as "parses cleanly" on a weighted average.

## Languages

The interface, the rule descriptions, the longer explanations, the
suggested fixes and the evidence text are translated into **English, German,
Ukrainian, Russian, Spanish, Dutch and French**; the web app has a language
switcher in the sidebar and the CLI takes `--language`. So is the sources
file: findings link to the translation matching the interface language
([de](docs/research_sources.de.md) · [uk](docs/research_sources.uk.md) ·
[ru](docs/research_sources.ru.md) · [es](docs/research_sources.es.md) ·
[nl](docs/research_sources.nl.md) · [fr](docs/research_sources.fr.md)).

Rule ids, source keys and the section anchors inside the sources files stay
in English — they are identifiers, not prose, which is what lets one citation
key resolve in all seven translations.

Resume *content* is matched against every language's section headings at
once, so the interface language and the CV language are independent.

## Why this exists

Applicant Tracking Systems are proprietary and undocumented, so no open-source
tool can claim to *replicate* Workday, Taleo, or Greenhouse exactly. What we
*can* do is document known, common failure patterns in resume parsing and
show you, transparently, whether your specific file triggers them — with the
raw extracted text as evidence.

## Download for Windows

Grab `ATS-Resume-X-Ray.exe` from the
[latest release](https://github.com/volodymyr-holovan/ats-resume-xray/releases/latest)
and run it. No installer, no Python needed — it opens in your browser and
runs entirely on your machine. It checks for a newer release on startup and
tells you if one exists.

Two things to expect:

- **Windows SmartScreen will warn you** that the publisher is unknown, and
  some antivirus tools flag PyInstaller executables generically. The file
  carries author and version metadata, but that is identification, not a
  signature — silencing those warnings needs a paid code-signing
  certificate. Build it yourself with `python build_exe.py` if you would
  rather not trust a download.
- **DOCX page previews need LibreOffice** installed separately; everything
  else works offline.

## Install from source

You need [Python 3.9 or newer](https://www.python.org/downloads/). Then run
these three commands:

```bash
git clone https://github.com/volodymyr-holovan/ats-resume-xray.git
cd ats-resume-xray
pip install ".[web]"
```

That's it — you now have both the web app and the `atsxray` command.

## Usage

### Web app

```bash
streamlit run app.py
```

This opens the app in your browser. Drag in a resume and you'll see what a
parser extracts from it, plus any findings.

### CLI

```bash
atsxray my-resume.pdf              # naive vs. layout-aware extraction
atsxray my-resume.pdf --report     # + findings, with evidence and sources
atsxray my-resume.pdf --score      # + parse readiness score and its arithmetic
```

The boxed page previews are a web-app feature; the CLI is text-only.

### Optional: page previews for DOCX

PDF previews work out of the box. To also preview DOCX files, install
[LibreOffice](https://www.libreoffice.org/download/) — the app finds it
automatically, or set `ATS_XRAY_SOFFICE` to the `soffice` binary if it lives
somewhere unusual. Deployments get it from `packages.txt`.

Two more flags show the intermediate steps behind the findings:
`--structure` (fonts, headers/footers, images) and `--fields`
(name/email/phone/section detection).

## How the layout-aware PDF extraction works

1. Collect every word on the page with its bounding box.
2. Cluster words into columns by finding horizontal gaps wider than a
   threshold — a real column boundary, not just space between words.
3. Within each column, sort words into reading order (top to bottom, left to
   right within a line).
4. Emit columns left to right.

The naive pass skips step 2 entirely — words are sorted purely by vertical
position, so a two-column resume gets its left and right column text
interleaved line by line.

## How the DOCX extraction works

- **Naive**: reads only `document.paragraphs` — the common shortcut in
  simple parsers. Any text placed inside a Word **table** (a popular way to
  build a two-column resume) never appears in `.paragraphs` at all, so it is
  silently dropped.
- **Full**: walks the document body in true XML order, handling paragraphs
  and tables as they actually appear in the file, so table content is never
  lost. Headers, footers, and text boxes live outside the document body
  entirely — a separate set of detectors checks those.

## The rule engine

Every finding traces back to a `Rule`: an id, a plain-language description,
a severity, and a `source` key pointing into
[`research_sources.md`](research_sources.md), which documents where the
underlying claim comes from. Findings always include the specific evidence
found in *your* file — no rule fires on vibes.

## Testing

The test suite includes a golden-fixture regression harness
(`tests/test_golden_fixtures.py`): labeled resume fixtures, each with the
exact set of rule ids it must trigger, so a change that silently breaks a
detector — or makes one over-fire — shows up as a failing test.

To work on the project, install it in editable mode with the dev extras
instead of the plain install above:

```bash
pip install -e ".[dev,web]"
pytest
```

## Contributing

Adding a rule, a detector, or a fixture? See [CONTRIBUTING.md](CONTRIBUTING.md).

## Disclaimer

This tool approximates *documented, common* resume-parsing failure modes. It
does not have access to, and does not claim to replicate, any specific
commercial ATS product. Treat its output as a diagnostic aid, not a
guarantee of how any particular employer's system will behave.

## License

MIT — see [LICENSE](LICENSE).

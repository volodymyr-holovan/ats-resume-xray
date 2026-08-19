# ATS Resume X-Ray

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
   sections, in English and German) under both extraction strategies, so it
   can flag content that's only readable in the best case.

4. **Runs a rule engine** over all of the above: each documented risk pattern
   is a `Rule` with a severity and a citation into
   [`research_sources.md`](research_sources.md) — a transparent finding with
   evidence, not an opaque score.

## Why this exists

Applicant Tracking Systems are proprietary and undocumented, so no open-source
tool can claim to *replicate* Workday, Taleo, or Greenhouse exactly. What we
*can* do is document known, common failure patterns in resume parsing and
show you, transparently, whether your specific file triggers them — with the
raw extracted text as evidence.

## Usage

### Web app

```bash
pip install -e ".[web]"
streamlit run app.py
```

Upload a resume, see the naive/layout-aware diff and the rule engine's
findings in your browser.

### CLI

```bash
pip install -e .

atsxray path/to/resume.pdf                # naive vs. layout-aware extraction
atsxray path/to/resume.pdf --structure     # + fonts, headers/footers, images
atsxray path/to/resume.pdf --fields        # + name/email/phone/section detection
atsxray path/to/resume.pdf --report        # + full rule engine report
```

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

```bash
pip install -e ".[dev,web]"
pytest
```

## Disclaimer

This tool approximates *documented, common* resume-parsing failure modes. It
does not have access to, and does not claim to replicate, any specific
commercial ATS product. Treat its output as a diagnostic aid, not a
guarantee of how any particular employer's system will behave.

## License

MIT — see [LICENSE](LICENSE).

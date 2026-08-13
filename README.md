# ATS Resume X-Ray

**See your resume the way a parser sees it — not a fake "ATS score", an actual diff.**

Most "ATS score checkers" are black boxes: you upload a resume, get a number like
"87/100", and no idea what it actually means. This project does the opposite.

ATS Resume X-Ray extracts text from your PDF/DOCX resume using two strategies:

- **Naive extraction** — mimics how a basic, layout-blind parser reads your file
  (the default behavior of common PDF/DOCX text-extraction libraries).
- **Layout-aware extraction** — detects columns and tables, and reads content
  in the order a human actually intends.

Comparing the two outputs reveals exactly where a real parsing pipeline would
mangle or silently drop your content — a two-column layout that gets its lines
interleaved, a table whose cells vanish entirely, text that only exists inside
an image, and so on.

## Why this exists

Applicant Tracking Systems are proprietary and undocumented, so no open-source
tool can claim to *replicate* Workday, Taleo, or Greenhouse exactly. What we
*can* do is document known, research-backed failure patterns in resume
parsing (multi-column layouts, tables, text boxes, non-standard fonts, missing
alt-text) and show you, transparently, whether your specific file triggers
them — with the raw extracted text as evidence, not a mystery score.

## Usage

```bash
pip install -e .
atsxray path/to/resume.pdf
atsxray path/to/resume.docx
```

This prints both extractions side by side so you can visually compare what
the naive pass saw against what the layout-aware pass recovered.

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
  lost.

## Disclaimer

This tool approximates *documented, common* resume-parsing failure modes. It
does not have access to, and does not claim to replicate, any specific
commercial ATS product. Treat its output as a diagnostic aid, not a
guarantee of how any particular employer's system will behave.

## License

MIT — see [LICENSE](LICENSE).

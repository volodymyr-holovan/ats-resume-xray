# Contributing

## Development setup

```bash
pip install -e ".[dev,web]"
pytest
```

## Adding a new rule

1. Register a `Rule` in `src/ats_xray/rules.py` — id, description, severity,
   and a `source` key.
2. Add the citation for that `source` key to
   [`research_sources.md`](research_sources.md). No rule ships without one
   (or an honest `practical-necessity` label, for the handful that aren't
   really research claims).
3. Implement the detection signal — a new function in the relevant
   `pdf_*`/`docx_*` module, or reuse an existing one — and wire it into
   `analyze_structure()` in `structure.py` if it's structural.
4. Add the trigger condition to `evaluate()` in `engine.py`.
5. Add a golden fixture: a generator in `tests/golden_generators.py` and its
   expected rule ids in `tests/golden_expectations.py`, proving the rule
   fires. Where it's easy, add a second, similar-but-clean fixture proving
   it *doesn't* false-positive.
6. `pytest` — the full suite, golden fixtures included, should pass.

## Code style

- No comments explaining *what* code does — only *why*, when it's genuinely
  non-obvious.
- Prefer small, pure functions over stateful classes; see `_pdf_words.py`,
  `contact.py`, and `sections.py` for the pattern this codebase follows.
  They're easy to unit-test with plain dicts, no real files required.
- Detectors and rules exist to make a specific, checkable claim. If you
  can't point to why a pattern is a real parsing risk, it probably doesn't
  belong as a rule yet.

## Reporting a parsing pattern we don't cover

Open an issue with a minimal resume file (or a description of the
formatting pattern), and a source if you have one. We're intentionally
conservative about adding rules without a citation — see the note at the
top of `research_sources.md` for why.

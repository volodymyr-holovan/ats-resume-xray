# Contributing

## Development setup

```bash
pip install -e ".[dev,web]"
pytest
```

The suite is the specification. Run all of it before every commit, not the
file you happened to touch: the tests that break when a detector changes are
usually in some other file, and the ones that guard the seven languages break
in all seven at once.

Python 3.10 is the floor, and CI runs 3.10 and 3.12. A test reads the floor
out of `pyproject.toml` and checks the workflow matrix still covers it, so
raising one without the other fails rather than drifting.

## Two kinds of rule

The distinction runs through the whole codebase, so it is worth getting right
before writing anything.

A **parsing rule** says the file does not survive being read by software:
content in a table, a section that disappears under a layout-blind read, a
name that is a picture. These are detected in `engine.py` from the structural
detectors, they carry `category=PARSING`, and they move the score.

A **convention rule** says the file reads perfectly and still says something
a recruiter in that country does not expect: an Ehrenamt under
Berufserfahrung, a silent gap in the dates, a religion in the personal
details. These live in `conventions.py`, carry `category=CONVENTION`, are
gated to the languages whose guidance actually says so, and **never move the
score.** Parse readiness measures whether the file can be read; a custom in
one country is not a defect in another, and mixing the two makes the number
meaningless.

## Adding a parsing rule

1. Register a `Rule` in `src/ats_xray/rules.py` — id, description, severity,
   `source`, `category=PARSING`.
2. Add the citation for that `source` key to
   [`research_sources.md`](research_sources.md) **and to all six
   translations** in `docs/research_sources.<lang>.md`. A test resolves every
   cited anchor in every language, so an English-only citation fails. No rule
   ships without one (or an honest `practical-necessity` label, for the
   handful that aren't really research claims).
3. Implement the detection signal — a new function in the relevant
   `pdf_*`/`docx_*` module, or reuse an existing one — and wire it into
   `analyze_structure()` in `structure.py` if it's structural.
4. Add the trigger condition to `evaluate()` in `engine.py`.
5. Translate it. See the next section; this is the step people forget.
6. Add a golden fixture: a generator in `tests/golden_generators.py` and its
   expected rule ids in `tests/golden_expectations.py`, proving the rule
   fires. Where it's easy, add a second, similar-but-clean fixture proving
   it *doesn't* false-positive.
7. `pytest` — the full suite, golden fixtures included, should pass.

## Adding a convention rule

1. Register the `Rule` with `category=CONVENTION` and cite it the same way.
2. Write the detector in `conventions.py` and return a `ConventionFinding`.
3. **Gate it by language**, with a module constant naming the languages whose
   guidance supports it and a docstring saying what that guidance is. The
   volunteering rule applies to German and Ukrainian CVs and to no others;
   flagging it on a Spanish one would be inventing a custom.
4. Add it to the dict `analyze_conventions()` returns. It returns an entry for
   every rule id, `None` when the rule did not fire — callers filter, so
   leaving a key out breaks them rather than reporting nothing.
5. Translate it, add tests for the exceptions as well as the hits, and run the
   suite.

## Translating a rule

Seven languages: `en`, `de`, `uk`, `ru`, `es`, `nl`, `fr`. Five tables in
`i18n.py` need an entry for every new rule id, in every one of them:

| Table | What it holds |
|---|---|
| `RULE_NAMES` | the short label |
| `RULE_DESCRIPTIONS` | one sentence on what was found |
| `RULE_DETAILS` | why it matters |
| `RULE_FIXES` | the steps, as actual steps |
| `RULE_PLAN` | one instruction for the action plan |

Tests enforce all of it: completeness per language, that the placeholders
match across languages, that no English leaks into another language, that a
fix is a list of steps rather than a one-liner, that a plan line is a single
instruction naming no application and no menu path, and that Slavic counts
take all three plural forms. Write the English first and the other six
against it.

## Code style

- No comments explaining *what* code does — only *why*, when it's genuinely
  non-obvious. A comment that records the failure a line prevents is worth
  keeping; one that restates the line is not.
- Prefer small, pure functions over stateful classes; see `_pdf_words.py`,
  `contact.py`, and `sections.py` for the pattern this codebase follows.
  They're easy to unit-test with plain dicts, no real files required.
- Detectors and rules exist to make a specific, checkable claim. If you
  can't point to why a pattern is a real parsing risk, it probably doesn't
  belong as a rule yet.
- Never take an offset into folded text. `fold()` expands umlauts and drops
  punctuation, so it does not preserve length; cut the raw string first and
  fold each piece. This has caused a real bug more than once.

## Sending a change

Work on a branch, open a pull request, let CI go green, then merge. CI is two
Python versions and the whole suite; it is the same thing you ran locally, on
a machine that has none of your cached state.

## Reporting a parsing pattern we don't cover

Open an issue with a minimal resume file (or a description of the
formatting pattern), and a source if you have one. We're intentionally
conservative about adding rules without a citation — see the note at the
top of `research_sources.md` for why.

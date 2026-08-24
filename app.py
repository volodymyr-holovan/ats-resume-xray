"""ATS Resume X-Ray — the web interface.

The page is built as four zones in the order someone actually works through
them: load the file, look at it, compare it against a job ad, then fix what
came back. They are numbered on screen because a stack of equal-looking
panels cannot say by itself that it is a sequence.

Wide screens get a two-pane document review -- pages on the left, the
readability verdict on the right -- because that is what the task is. You
cannot judge a finding without seeing the place it refers to, and every tool
built for reviewing a document, from proof marks to code review, puts the
artefact and the notes side by side. Below 1000px the panes stack; a
two-pane review on a phone is two unreadable slivers.

Run locally with: streamlit run app.py
"""

import html
from contextlib import nullcontext
import logging
from dataclasses import replace
from pathlib import Path

import streamlit as st

from ats_xray.i18n import (
    DEFAULT_LANGUAGE,
    UI_LANGUAGES,
    rule_description,
    rule_detail,
    rule_fixes,
    sources_path,
    t,
    tn,
)
from ats_xray.match import evaluate_match
from ats_xray.normalize import fold
from ats_xray.overlay import SEVERITY_COLORS
from ats_xray.pipeline import analyze_bytes
from ats_xray.skills_lexicon import label_for
from ats_xray.updates import check_for_update
from ats_xray.vacancy import Requirement, parse_vacancy

logger = logging.getLogger(__name__)

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}
STATUS_TONE = {"met": "green", "partial": "orange", "missing": "red"}
JOB_AD_HEIGHT = 200
REPO_URL = "https://github.com/volodymyr-holovan/ats-resume-xray"
BLOB_URL = f"{REPO_URL}/blob/master"
STYLESHEET = Path(__file__).parent / "assets" / "app.css"

st.set_page_config(
    page_title="ATS Resume X-Ray",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_data(show_spinner=False)
def _stylesheet() -> str:
    """Read once rather than on every rerun. It is a few kilobytes, but a
    rerun happens on every keystroke in the job-ad box."""
    return STYLESHEET.read_text(encoding="utf-8") if STYLESHEET.exists() else ""


@st.cache_data(ttl=3600, show_spinner=False)
def _cached_update_check():
    """Checked once an hour per session rather than on every rerun, which
    would mean a network round trip each time a widget changes."""
    return check_for_update()


@st.cache_data(show_spinner=False)
def _parse_vacancy_cached(ad_text: str):
    """Parsing is pure and the same text is re-parsed on every widget
    interaction, so cache on the text itself."""
    return parse_vacancy(ad_text)


# --------------------------------------------------------------------------
# Chrome
# --------------------------------------------------------------------------


def _pick_language() -> str:
    """A globe in the masthead rather than a dropdown in a collapsed sidebar.

    The language control was previously behind a sidebar most readers never
    opened, which made six of the seven translations unreachable in practice.
    A globe is the one icon everybody already reads as "language", and the
    current language sits next to it so the control says what it does before
    it is clicked.
    """
    current = st.session_state.get("language", DEFAULT_LANGUAGE)
    codes = list(UI_LANGUAGES)
    with st.container(key="axr-language"):
        with st.popover(
            UI_LANGUAGES[current], icon=":material/language:", use_container_width=True
        ):
            return st.radio(
                t("language_menu", current),
                options=codes,
                index=codes.index(current),
                format_func=lambda code: UI_LANGUAGES[code],
                key="language",
                label_visibility="collapsed",
            )


def _masthead(lang: str) -> None:
    name_col, language_col = st.columns([5, 1], vertical_alignment="center")
    with name_col:
        st.markdown(
            f'<div class="axr-masthead">'
            f'<h1 class="axr-wordmark">ATS Resume X-Ray</h1>'
            f'<p class="axr-tagline">{t("tagline", lang)}</p>'
            f"</div>",
            unsafe_allow_html=True,
        )
    with language_col:
        _pick_language()


def _jump_links(lang: str) -> None:
    st.markdown(
        '<nav class="axr-jump">'
        f'<a href="#zone-document">{t("jump_document", lang)}</a>'
        f'<a href="#zone-match">{t("jump_match", lang)}</a>'
        f'<a href="#zone-fixes">{t("jump_fixes", lang)}</a>'
        "</nav>",
        unsafe_allow_html=True,
    )


def _zone(number: str, title: str, note: str, anchor: str) -> None:
    st.markdown(
        f'<div class="axr-zone" id="{anchor}">'
        f'<span class="axr-zone-number">{number}</span>'
        f'<h2 class="axr-zone-title">{title}</h2>'
        f"</div>"
        f'<p class="axr-zone-note">{note}</p>',
        unsafe_allow_html=True,
    )


def _show_update_notice(lang: str) -> None:
    update = _cached_update_check()
    if update is None:
        return
    st.info(
        t("update_available", lang, latest=update.latest, current=update.current, url=update.url),
        icon=":material/upgrade:",
    )


# --------------------------------------------------------------------------
# Zone 1 — the file
# --------------------------------------------------------------------------


def _upload_zone(lang: str):
    _zone("01", t("zone_upload_title", lang), t("zone_upload_note", lang), "zone-upload")
    # A stable key keeps the upload across the rerun a language change
    # triggers; without it, switching language silently discards the file.
    with st.container(key="axr-upload"):
        return st.file_uploader(
            t("upload_label", lang), type=["pdf", "docx"], key="resume", label_visibility="collapsed"
        )


def _empty_state(lang: str) -> None:
    """What the reader gets, in one sentence, and nothing else.

    The privacy promise is not repeated here: the zone note above the
    dropzone already says the file is deleted within seconds, and saying it
    twice in the same eyeful reads as protesting. The full wording stands in
    the footer, where it is a standing statement rather than a reassurance
    aimed at one moment.
    """
    st.markdown(
        f'<p class="axr-zone-note" style="margin-left:0">{t("empty_hint", lang)}</p>',
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------
# Zone 2 — the document
# --------------------------------------------------------------------------


def _legend(lang: str) -> str:
    names = {"high": t("severity_high", lang), "medium": t("severity_medium", lang),
             "low": t("severity_low", lang)}
    swatches = "".join(
        f'<span><span class="axr-swatch" style="background:rgb{SEVERITY_COLORS[severity]}"></span>'
        f"{names[severity]}</span>"
        for severity in ("high", "medium", "low")
        if severity in SEVERITY_COLORS
    )
    return f'<div class="axr-legend">{swatches}</div>'


PAGE_PANE_HEIGHT = 900
"""Tall enough for a whole A4 page at the width this column gets, so the
scroller never cuts one in half."""


def _render_pages(pages, is_pdf: bool, lang: str) -> None:
    if not pages:
        if not is_pdf:
            st.info(t("docx_no_libreoffice", lang))
        return

    # The swatches carry the colours overlay.py drew, not the theme's, so a
    # dark-mode reader still sees the legend match the boxes on the page.
    st.markdown(_legend(lang), unsafe_allow_html=True)
    if not is_pdf:
        st.caption(t("docx_layout_note", lang))

    # One page needs no scroller. Several do: a six-page CV rendered at full
    # width runs past everything else on the screen, and the reader loses
    # the score sitting beside it.
    frame = st.container(height=PAGE_PANE_HEIGHT) if len(pages) > 1 else nullcontext()
    with frame:
        for page in pages:
            label = f"{t('page', lang)} {page.page_number}"
            if page.marked_findings:
                label += " — " + ", ".join(sorted({f.rule.id for f in page.marked_findings}))
            else:
                label += f" — {t('nothing_flagged', lang)}"
            st.image(page.image, caption=label, use_container_width=True)


def _render_scorecard(breakdown, findings, lang: str) -> None:
    st.metric(label=t(breakdown.rating_key, lang), value=f"{breakdown.total}/100")
    st.caption(t("score_caption", lang))

    tally = {severity: sum(1 for f in findings if f.severity == severity)
             for severity in ("high", "medium", "low")}
    st.markdown(
        f'<p class="axr-zone-note" style="margin-left:0">{t("issue_tally", lang, **tally)}</p>',
        unsafe_allow_html=True,
    )

    if breakdown.cap_key:
        st.warning(tn(breakdown.cap_key, breakdown.cap_params.get("count", 1), lang, **breakdown.cap_params))

    for component in breakdown.components:
        name = t(component.name_key, lang)
        detail = t(component.detail_key, lang, **component.detail_params)
        if component.weight == 0:
            st.caption(f"**{name}** — {t('not_scored', lang)}. {detail}")
            continue
        st.progress(
            component.score / 100,
            text=f"**{name}** {component.score:.0f}/100 ({t('weight', lang)} {component.weight}%)",
        )
        st.caption(detail)


def _document_zone(result, is_pdf: bool, lang: str) -> None:
    _zone("02", t("pages_heading", lang), t("zone_document_note", lang), "zone-document")

    with st.container(key="axr-split"):
        pages_col, score_col = st.columns([3, 2], gap="large")
        with pages_col:
            _render_pages(result.rendered_pages, is_pdf, lang)
            with st.expander(t("naive_expander", lang)):
                st.text(result.naive_text)
            with st.expander(t("aware_expander", lang)):
                st.text(result.aware_text)
        with score_col:
            _render_scorecard(result.score, result.findings, lang)


# --------------------------------------------------------------------------
# Zone 3 — the job ad
# --------------------------------------------------------------------------


def _requirement_key(text: str) -> str:
    """A short stable id for the pasted advert.

    Widget keys are derived from it so that editing the advert produces a
    fresh set of widgets with fresh defaults, while merely clicking around
    keeps whatever the reader edited.
    """
    return str(abs(hash(text.strip())) % (10**10))


def _keyword_editor(profile, lang: str) -> list:
    """Show what was extracted and let the reader correct it.

    Extraction is the tool's guess, and a guess the reader cannot overrule is
    worse than no guess: they know the job, the parser only has the text.
    """
    stamp = _requirement_key(st.session_state.get("job_ad", ""))
    by_label = {r.label: r for r in profile.requirements}

    must_default = [r.label for r in profile.requirements if r.kind == "skill" and r.must]
    nice_default = [r.label for r in profile.requirements if r.kind == "skill" and not r.must]
    others = [r for r in profile.requirements if r.kind != "skill"]

    with st.expander(t("match_keywords_expander", lang), expanded=True):
        st.caption(t("match_add_hint", lang))
        with st.container(key="axr-split-keywords"):
            must_col, nice_col = st.columns(2, gap="large")
            with must_col:
                chosen_must = st.multiselect(
                    t("match_must_label", lang), options=must_default, default=must_default,
                    accept_new_options=True, key=f"must_{stamp}",
                )
            with nice_col:
                chosen_nice = st.multiselect(
                    t("match_nice_label", lang), options=nice_default, default=nice_default,
                    accept_new_options=True, key=f"nice_{stamp}",
                )

        kept_others = []
        if others:
            st.markdown(f"**{t('match_other_label', lang)}**")
            for index, requirement in enumerate(others):
                weight = t("match_must_label" if requirement.must else "match_nice_label", lang)
                if st.checkbox(
                    f"{requirement.label} — {weight}", value=True, key=f"other_{stamp}_{index}"
                ):
                    kept_others.append(requirement)

    selected = kept_others[:]
    for labels, must in ((chosen_must, True), (chosen_nice, False)):
        for label in labels:
            existing = by_label.get(label)
            if existing is not None and existing.kind == "skill":
                selected.append(existing if existing.must == must else replace(existing, must=must))
            else:
                # A keyword the reader typed. It has no lexicon id, so the
                # matcher falls back to searching the CV for the phrase.
                selected.append(
                    Requirement(kind="skill", key=f"custom:{fold(label)}", label=label, must=must)
                )
    return selected


OUTCOME_PANE_HEIGHT = 340
"""How tall a result column may grow before it scrolls inside itself.

An advert can state thirty requirements. Left unbounded, one column pushes
the other two off the screen and the reader loses the comparison, which is
the only reason the three columns are side by side."""


def _outcome_pane(heading_key: str, tone: str, outcomes, lang: str, extras=None) -> None:
    """One bordered, height-capped column of results.

    The border is what makes three lists read as three lists rather than as
    one long page of bold words.
    """
    count = len(outcomes) if extras is None else len(extras)
    st.markdown(
        f'<p class="axr-column-heading axr-severity-{tone}">'
        f"{t(heading_key, lang)} <span class=\"axr-count\">{count}</span></p>",
        unsafe_allow_html=True,
    )
    with st.container(border=True, height=OUTCOME_PANE_HEIGHT):
        if extras is not None:
            if not extras:
                st.caption("—")
                return
            st.markdown("  \n".join(label_for(skill_id) for skill_id in extras))
            return

        if not outcomes:
            st.caption("—")
            return
        for outcome in outcomes:
            # Escaped before anything is appended. This label can be a
            # keyword the reader typed into the multiselect, and it can be a
            # term lifted out of a pasted advert; neither is ours to trust
            # in a sink that renders markup.
            label = html.escape(outcome.requirement.label)
            if outcome.status == "partial":
                # A partial belongs with the gaps -- it is something to act
                # on -- but the reader has to see that it is not a blank.
                label += f' <span class="axr-partly">{t("match_partly_tag", lang)}</span>'
            st.markdown(f"**{label}**", unsafe_allow_html=True)
            if outcome.note_key:
                st.caption(t(outcome.note_key, lang, **outcome.note_params))


def _render_match_report(report, lang: str) -> None:
    with st.container(key="axr-split-score"):
        score_col, verdict_col = st.columns([1, 3], gap="large")
        with score_col:
            st.metric(label=t(report.rating_key, lang), value=f"{report.score}/100")
        with verdict_col:
            if report.missing_must:
                st.error(tn("match_missing_must_warning", len(report.missing_must), lang))
            else:
                st.success(t("match_all_must_covered", lang))
            st.caption(t("match_score_caption", lang))

    # Three columns, and the middle one is not "partly covered". That column
    # was almost always empty: only a language level, a degree or a span of
    # years can be partly met, and a skill never can. Partials now sit with
    # the gaps, where the reader can act on them, and the freed column shows
    # what the CV has that the advert did not ask for -- which is what you
    # need when deciding what to cut.
    gaps = report.of_status("missing") + report.of_status("partial")
    with st.container(key="axr-split-outcomes"):
        gaps_col, met_col, extras_col = st.columns(3, gap="medium")
        with gaps_col:
            _outcome_pane("match_gaps_heading", "high", gaps, lang)
        with met_col:
            _outcome_pane("match_met_heading", "low", report.of_status("met"), lang)
        with extras_col:
            _outcome_pane("match_extras_heading", "neutral", [], lang, extras=report.extras)
            st.caption(t("match_extras_caption", lang))

    if report.at_risk:
        st.warning(f"**{t('match_at_risk_heading', lang)}** ({len(report.at_risk)})")
        st.caption(t("match_at_risk_caption", lang))
        st.markdown(", ".join(o.requirement.label for o in report.at_risk))


def _match_zone(analysis, lang: str) -> None:
    _zone("03", t("match_heading", lang), t("match_intro", lang), "zone-match")

    ad_text = st.text_area(
        t("match_paste_label", lang), key="job_ad", height=JOB_AD_HEIGHT,
        placeholder=t("match_paste_placeholder", lang), label_visibility="collapsed",
    )
    if not ad_text.strip():
        return

    profile = _parse_vacancy_cached(ad_text)
    if not profile.requirements:
        st.info(t("match_no_requirements", lang))

    selected = _keyword_editor(profile, lang)

    if analysis is None:
        st.info(t("match_needs_cv", lang))
        return

    if st.button(t("match_evaluate_button", lang), type="primary", disabled=not selected):
        st.session_state["match_report"] = evaluate_match(
            selected, analysis.aware_text, analysis.naive_text
        )

    report = st.session_state.get("match_report")
    if report is not None:
        _render_match_report(report, lang)


# --------------------------------------------------------------------------
# Zone 4 — findings and fixes
# --------------------------------------------------------------------------


def _sources_url(rule, lang: str) -> str:
    """Deep link to this rule's entry in the sources file, in the language the
    reader is currently using. The anchors are identical across translations,
    so only the filename changes."""
    return f"{BLOB_URL}/{sources_path(lang)}#{rule.source}"


def _render_finding(finding, lang: str) -> None:
    description = rule_description(finding.rule.id, lang, finding.rule.description)
    severity = finding.severity
    st.markdown(
        f'<div class="axr-finding axr-finding-{severity}">'
        f'<span class="axr-severity axr-severity-{severity}">{t(f"severity_{severity}", lang)}</span>'
        f'<p class="axr-finding-text">{description}</p>'
        f"</div>",
        unsafe_allow_html=True,
    )

    # The headline says what is wrong; everything needed to act on it lives
    # one click away, so a CV with five findings stays skimmable.
    with st.expander(t("details_expander", lang)):
        detail = rule_detail(finding.rule.id, lang)
        if detail:
            st.write(detail)

        fixes = rule_fixes(finding.rule.id, lang)
        if fixes:
            st.markdown(f"**{t('how_to_fix', lang)}**")
            st.markdown("\n".join(f"{i}. {fix}" for i, fix in enumerate(fixes, 1)))

        evidence = t(finding.evidence_key, lang, **finding.evidence_params)
        st.caption(f"{t('evidence', lang)}: {evidence}")
        st.caption(
            f"{t('source', lang)}: [{t('read_more', lang)}]({_sources_url(finding.rule, lang)})"
        )


def _fixes_zone(findings, lang: str) -> None:
    _zone("04", t("findings_heading", lang), t("zone_fixes_note", lang), "zone-fixes")

    if not findings:
        st.success(t("no_findings", lang))
        return

    ordered = sorted(findings, key=lambda f: SEVERITY_ORDER[f.severity])
    with st.container(key="axr-split-fixes"):
        columns = st.columns(2, gap="large")
        for index, finding in enumerate(ordered):
            with columns[index % 2]:
                with st.container(border=True):
                    _render_finding(finding, lang)


# --------------------------------------------------------------------------
# Page
# --------------------------------------------------------------------------

st.markdown(f"<style>{_stylesheet()}</style>", unsafe_allow_html=True)

# The masthead draws the language control, so the chosen language is only
# known after it has run; everything below the masthead uses that value.
_masthead(st.session_state.get("language", DEFAULT_LANGUAGE))
language = st.session_state.get("language", DEFAULT_LANGUAGE)
_jump_links(language)
_show_update_notice(language)

uploaded_file = _upload_zone(language)
analysis = None

if uploaded_file is None:
    _empty_state(language)
else:
    is_pdf = uploaded_file.name.lower().endswith(".pdf")
    try:
        with st.spinner(t("analyzing", language)):
            result = analyze_bytes(uploaded_file.getvalue(), uploaded_file.name, render=True)
    except ValueError as exc:
        st.error(str(exc))
    except Exception:
        # Log the real cause server-side while showing the reader a plain
        # message. Swallowing it entirely made a production failure
        # undiagnosable from the deployment logs.
        logger.exception("Analysis failed for an uploaded %s file", "PDF" if is_pdf else "DOCX")
        st.error(t("error_unreadable", language))
    else:
        analysis = result
        # In backticks: a filename is arbitrary text and st.caption renders
        # Markdown, so an asterisk or a bracket pair would reformat the line.
        st.caption(
            t(
                "file_loaded",
                language,
                name=f"`{uploaded_file.name}`",
                pages=len(result.rendered_pages),
            )
        )
        _document_zone(result, is_pdf, language)

_match_zone(analysis, language)

if analysis is not None:
    _fixes_zone(analysis.findings, language)

st.divider()
st.caption(t("privacy", language))
st.caption(f"{t('open_source', language)}: [{REPO_URL.removeprefix('https://')}]({REPO_URL})")

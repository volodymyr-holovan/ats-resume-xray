"""Streamlit demo: upload a resume and see what a parsing pipeline actually
extracts from it — naive (layout-blind) vs. layout-aware — which documented
parsing risks it triggers, where those risks sit on the page, and how much of
the resume survives an automated read.

Run locally with: streamlit run app.py
"""

import logging
from dataclasses import replace

import streamlit as st

from ats_xray.i18n import (
    DEFAULT_LANGUAGE,
    UI_LANGUAGES,
    rule_description,
    rule_detail,
    rule_fixes,
    sources_path,
    t,
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
SEVERITY_RENDERER = {"high": st.error, "medium": st.warning, "low": st.info}
PAGE_PREVIEW_WIDTH = 640
JOB_AD_HEIGHT = 220
STATUS_ICON = {"met": ":green[+]", "partial": ":orange[~]", "missing": ":red[-]"}
REPO_URL = "https://github.com/volodymyr-holovan/ats-resume-xray"
BLOB_URL = f"{REPO_URL}/blob/master"

st.set_page_config(page_title="ATS Resume X-Ray", page_icon="🔎")


@st.cache_data(ttl=3600, show_spinner=False)
def _cached_update_check():
    """Checked once an hour per session rather than on every rerun, which
    would mean a network round trip each time a widget changes."""
    return check_for_update()


def _show_update_notice(lang: str) -> None:
    update = _cached_update_check()
    if update is None:
        return
    st.info(
        t("update_available", lang, latest=update.latest, current=update.current, url=update.url),
        icon="⬆️",
    )


def _pick_language() -> str:
    codes = list(UI_LANGUAGES)
    default_index = codes.index(DEFAULT_LANGUAGE)
    with st.sidebar:
        return st.selectbox(
            t("language_label", st.session_state.get("language", DEFAULT_LANGUAGE)),
            options=codes,
            index=default_index,
            format_func=lambda code: UI_LANGUAGES[code],
            key="language",
        )


def _render_score(breakdown, lang: str) -> None:
    st.subheader(t("score_heading", lang))
    st.caption(t("score_caption", lang))

    score_col, detail_col = st.columns([1, 3])
    with score_col:
        st.metric(label=t(breakdown.rating_key, lang), value=f"{breakdown.total}/100")
    with detail_col:
        if breakdown.cap_key:
            st.warning(t(breakdown.cap_key, lang, **breakdown.cap_params))
        for component in breakdown.components:
            name = t(component.name_key, lang)
            detail = t(component.detail_key, lang, **component.detail_params)
            if component.weight == 0:
                st.caption(f"**{name}** — {t('not_scored', lang)}. {detail}")
                continue
            st.progress(
                component.score / 100,
                text=f"**{name}** {component.score:.0f}/100 "
                f"({t('weight', lang)} {component.weight}%) — {detail}",
            )


def _sources_url(rule, lang: str) -> str:
    """Deep link to this rule's entry in the sources file, in the language
    the reader is currently using. The anchors are identical across
    translations, so only the filename changes."""
    return f"{BLOB_URL}/{sources_path(lang)}#{rule.source}"


def _render_findings(findings, lang: str) -> None:
    st.subheader(t("findings_heading", lang))
    if not findings:
        st.success(t("no_findings", lang))
        return

    for finding in sorted(findings, key=lambda f: SEVERITY_ORDER[f.severity]):
        description = rule_description(finding.rule.id, lang, finding.rule.description)
        severity_label = t(f"severity_{finding.severity}", lang)
        SEVERITY_RENDERER[finding.severity](f"**[{severity_label}]** {description}")

        # The headline says what is wrong; everything a reader needs to act
        # on it lives one click away, so a resume with several findings
        # stays skimmable instead of turning into a wall of advice.
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
                f"{t('source', lang)}: [{t('read_more', lang)}]"
                f"({_sources_url(finding.rule, lang)})"
            )


def _render_pages(pages, is_pdf: bool, lang: str) -> None:
    st.subheader(t("pages_heading", lang))

    if not pages:
        if not is_pdf:
            st.info(t("docx_no_libreoffice", lang))
        return

    legend = "  ".join(
        f":{name}[■] {severity}"
        for severity, name in (("high", "red"), ("medium", "orange"), ("low", "blue"))
        if severity in SEVERITY_COLORS
    )
    caption = f"{t('legend', lang)} {legend}"
    if not is_pdf:
        caption += "  \n" + t("docx_layout_note", lang)
    st.caption(caption)

    for page in pages:
        label = f"{t('page', lang)} {page.page_number}"
        if page.marked_findings:
            label += " — " + ", ".join(sorted({f.rule.id for f in page.marked_findings}))
        else:
            label += f" — {t('nothing_flagged', lang)}"
        # Held to a page-like width: a resume shown at full container width
        # reads as a billboard rather than a document.
        st.image(page.image, caption=label, width=PAGE_PREVIEW_WIDTH)



@st.cache_data(show_spinner=False)
def _parse_vacancy_cached(ad_text: str):
    """Parsing is pure and the same text is re-parsed on every widget
    interaction, so cache on the text itself."""
    return parse_vacancy(ad_text)


def _requirement_key(text: str) -> str:
    """A short stable id for the pasted advert.

    Widget keys are derived from it so that editing the advert produces a
    fresh set of widgets with fresh defaults, while merely clicking around
    keeps whatever the reader edited.
    """
    return str(abs(hash(text.strip())) % (10**10))


def _keyword_editor(profile, lang: str) -> list:
    """Show what was extracted and let the reader correct it.

    Extraction is the tool's guess, and a guess the reader cannot overrule
    is worse than no guess: they know the job, the parser only has the
    text. Everything here is editable before anything is scored.
    """
    stamp = _requirement_key(st.session_state.get("job_ad", ""))
    by_label = {r.label: r for r in profile.requirements}

    must_default = [r.label for r in profile.requirements if r.kind == "skill" and r.must]
    nice_default = [r.label for r in profile.requirements if r.kind == "skill" and not r.must]
    others = [r for r in profile.requirements if r.kind != "skill"]

    with st.expander(t("match_keywords_expander", lang), expanded=True):
        st.caption(t("match_add_hint", lang))
        chosen_must = st.multiselect(
            t("match_must_label", lang),
            options=must_default,
            default=must_default,
            accept_new_options=True,
            key=f"must_{stamp}",
        )
        chosen_nice = st.multiselect(
            t("match_nice_label", lang),
            options=nice_default,
            default=nice_default,
            accept_new_options=True,
            key=f"nice_{stamp}",
        )

        kept_others = []
        if others:
            st.markdown(f"**{t('match_other_label', lang)}**")
            for index, requirement in enumerate(others):
                weight = t("match_must_label" if requirement.must else "match_nice_label", lang)
                if st.checkbox(
                    f"{requirement.label} — {weight}",
                    value=True,
                    key=f"other_{stamp}_{index}",
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


def _render_outcome_group(outcomes, heading: str, renderer, lang: str) -> None:
    if not outcomes:
        return
    renderer(f"**{heading}** ({len(outcomes)})")
    for outcome in outcomes:
        line = f"{STATUS_ICON[outcome.status]} **{outcome.requirement.label}**"
        if outcome.note_key:
            line += f" — {t(outcome.note_key, lang, **outcome.note_params)}"
        st.markdown(line)
        if outcome.evidence and outcome.status != "missing":
            st.caption(f"{t('evidence', lang)}: {outcome.evidence}")


def _render_match_report(report, lang: str) -> None:
    st.subheader(t("match_score_heading", lang))
    st.caption(t("match_score_caption", lang))

    score_col, detail_col = st.columns([1, 3])
    with score_col:
        st.metric(label=t(report.rating_key, lang), value=f"{report.score}/100")
    with detail_col:
        if report.missing_must:
            st.error(t("match_missing_must_warning", lang, count=len(report.missing_must)))
        else:
            st.success(t("match_all_must_covered", lang))

    _render_outcome_group(report.of_status("missing"), t("match_missing_heading", lang), st.error, lang)
    _render_outcome_group(report.of_status("partial"), t("match_partial_heading", lang), st.warning, lang)
    _render_outcome_group(report.of_status("met"), t("match_met_heading", lang), st.success, lang)

    if report.at_risk:
        st.warning(f"**{t('match_at_risk_heading', lang)}** ({len(report.at_risk)})")
        st.caption(t("match_at_risk_caption", lang))
        for outcome in report.at_risk:
            st.markdown(f"- {outcome.requirement.label}")

    if report.extras:
        with st.expander(f"{t('match_extras_heading', lang)} ({len(report.extras)})"):
            st.caption(t("match_extras_caption", lang))
            st.markdown(", ".join(label_for(skill_id) for skill_id in report.extras))


def _render_match(analysis, lang: str) -> None:
    st.divider()
    st.subheader(t("match_heading", lang))
    st.caption(t("match_intro", lang))

    ad_text = st.text_area(
        t("match_paste_label", lang),
        key="job_ad",
        height=JOB_AD_HEIGHT,
        placeholder=t("match_paste_placeholder", lang),
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

language = _pick_language()

st.title("ATS Resume X-Ray")
_show_update_notice(language)
st.write(t("intro", language, sources_url=f"{BLOB_URL}/{sources_path(language)}"))
st.caption(t("privacy", language))

# A stable key keeps the upload across the rerun that a language change
# triggers; without it, switching language silently discards the file and
# the reader has to upload again to see the same result in another language.
uploaded_file = st.file_uploader(t("upload_label", language), type=["pdf", "docx"], key="resume")

analysis = None

if uploaded_file is not None:
    is_pdf = uploaded_file.name.lower().endswith(".pdf")

    try:
        with st.spinner(t("analyzing", language)):
            result = analyze_bytes(uploaded_file.getvalue(), uploaded_file.name, render=True)
    except ValueError as exc:
        st.error(str(exc))
    except Exception:
        # Log the real cause server-side while showing the reader a plain
        # message. Swallowing it entirely made a production failure
        # undiagnosable from the deployment logs: all they showed was that
        # something went wrong, never what.
        logger.exception("Analysis failed for an uploaded %s file", "PDF" if is_pdf else "DOCX")
        st.error(t("error_unreadable", language))
    else:
        analysis = result
        _render_score(result.score, language)
        _render_findings(result.findings, language)
        _render_pages(result.rendered_pages, is_pdf, language)

        naive_col, aware_col = st.columns(2)
        with naive_col:
            with st.expander(t("naive_expander", language)):
                st.text(result.naive_text)
        with aware_col:
            with st.expander(t("aware_expander", language)):
                st.text(result.aware_text)

_render_match(analysis, language)

st.divider()
st.caption(f"{t('open_source', language)}: [{REPO_URL.removeprefix('https://')}]({REPO_URL})")

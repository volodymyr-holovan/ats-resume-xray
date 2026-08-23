"""Streamlit demo: upload a resume and see what a parsing pipeline actually
extracts from it — naive (layout-blind) vs. layout-aware — which documented
parsing risks it triggers, where those risks sit on the page, and how much of
the resume survives an automated read.

Run locally with: streamlit run app.py
"""

import logging

import streamlit as st

from ats_xray.i18n import DEFAULT_LANGUAGE, UI_LANGUAGES, rule_description, t
from ats_xray.overlay import SEVERITY_COLORS
from ats_xray.pipeline import analyze_bytes
from ats_xray.updates import check_for_update

logger = logging.getLogger(__name__)

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}
SEVERITY_RENDERER = {"high": st.error, "medium": st.warning, "low": st.info}
PAGE_PREVIEW_WIDTH = 640
REPO_URL = "https://github.com/volodymyr-holovan/ats-resume-xray"
SOURCES_URL = f"{REPO_URL}/blob/master/research_sources.md"

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


def _render_findings(findings, lang: str) -> None:
    st.subheader(t("findings_heading", lang))
    if not findings:
        st.success(t("no_findings", lang))
        return

    for finding in sorted(findings, key=lambda f: SEVERITY_ORDER[f.rule.severity]):
        description = rule_description(finding.rule.id, lang, finding.rule.description)
        SEVERITY_RENDERER[finding.rule.severity](
            f"**[{finding.rule.severity.upper()}]** {description}"
        )
        evidence = t(finding.evidence_key, lang, **finding.evidence_params)
        st.caption(f"{t('evidence', lang)}: {evidence}")
        st.caption(f"{t('source', lang)}: research_sources.md#{finding.rule.source}")


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


language = _pick_language()

st.title("ATS Resume X-Ray")
_show_update_notice(language)
st.write(t("intro", language, sources_url=SOURCES_URL))
st.caption(t("privacy", language))

# A stable key keeps the upload across the rerun that a language change
# triggers; without it, switching language silently discards the file and
# the reader has to upload again to see the same result in another language.
uploaded_file = st.file_uploader(t("upload_label", language), type=["pdf", "docx"], key="resume")

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

st.divider()
st.caption(f"{t('open_source', language)}: [{REPO_URL.removeprefix('https://')}]({REPO_URL})")

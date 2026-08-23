"""Streamlit demo: upload a resume and see what a parsing pipeline actually
extracts from it — naive (layout-blind) vs. layout-aware — which documented
parsing risks it triggers, where those risks sit on the page, and how much of
the resume survives an automated read.

Run locally with: streamlit run app.py
"""

import logging

import streamlit as st

from ats_xray.overlay import SEVERITY_COLORS
from ats_xray.pipeline import analyze_bytes

logger = logging.getLogger(__name__)

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}
SEVERITY_RENDERER = {"high": st.error, "medium": st.warning, "low": st.info}
PAGE_PREVIEW_WIDTH = 640

st.set_page_config(page_title="ATS Resume X-Ray", page_icon="🔎")

st.title("ATS Resume X-Ray")
st.write(
    "Upload a resume (PDF or DOCX) to see what a resume-parsing pipeline "
    "actually extracts from it — not a black-box score, an actual diff. "
    "Findings are documented, common failure patterns "
    "([sources](https://github.com/volodymyr-holovan/ats-resume-xray/blob/master/research_sources.md)), "
    "not a guarantee of how any specific employer's system will behave."
)
st.caption(
    "🔒 Your file is written to a temporary location only for the few seconds "
    "needed to process it, then deleted immediately. Nothing is stored, logged, "
    "or sent anywhere else."
)

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])


def _render_score(breakdown) -> None:
    st.subheader("Parse readiness")
    st.caption(
        "How much of this resume survives an automated read. This is **not** a "
        "keyword-match score against a job posting: that needs the posting and "
        "the employer's weighting, neither of which this tool has. Every number "
        "below is derived from evidence in your file, shown in full."
    )

    score_col, detail_col = st.columns([1, 3])
    with score_col:
        st.metric(label=breakdown.rating, value=f"{breakdown.total}/100")
    with detail_col:
        if breakdown.cap_reason:
            st.warning(f"{breakdown.cap_reason} (before the cap: {breakdown.uncapped_total}/100)")
        for component in breakdown.components:
            if component.weight == 0:
                st.caption(f"**{component.name}** — not scored. {component.detail}")
                continue
            st.progress(
                component.score / 100,
                text=f"**{component.name}** {component.score:.0f}/100 "
                f"(weight {component.weight}%) — {component.detail}",
            )


def _render_findings(findings) -> None:
    st.subheader("Findings")
    if not findings:
        st.success("No documented parsing risks triggered.")
        return

    for finding in sorted(findings, key=lambda f: SEVERITY_ORDER[f.rule.severity]):
        SEVERITY_RENDERER[finding.rule.severity](
            f"**[{finding.rule.severity.upper()}]** {finding.rule.description}"
        )
        st.caption(f"Evidence: {finding.evidence}")
        st.caption(f"Source: research_sources.md#{finding.rule.source}")


def _render_pages(pages, is_pdf: bool) -> None:
    st.subheader("Where the problems are")

    if not pages:
        if is_pdf:
            return
        st.info(
            "Page previews for DOCX need LibreOffice, which isn't available here. "
            "A DOCX stores content but no page positions, so it has to be laid out "
            "before anything can be drawn on it. The findings above still apply."
        )
        return

    legend = "  ".join(
        f":{name}[■] {severity}"
        for severity, name in (("high", "red"), ("medium", "orange"), ("low", "blue"))
        if severity in SEVERITY_COLORS
    )
    caption = f"Boxes mark the exact area each finding refers to. {legend}"
    if not is_pdf:
        caption += (
            "  \nThis DOCX was laid out with LibreOffice to produce pages; your own "
            "word processor may break lines slightly differently."
        )
    st.caption(caption)

    for page in pages:
        caption = f"Page {page.page_number}"
        if page.marked_findings:
            caption += " — " + ", ".join(sorted({f.rule.id for f in page.marked_findings}))
        else:
            caption += " — nothing flagged"
        # Held to a page-like width: a resume shown at full container width
        # reads as a billboard rather than a document.
        st.image(page.image, caption=caption, width=PAGE_PREVIEW_WIDTH)


if uploaded_file is not None:
    is_pdf = uploaded_file.name.lower().endswith(".pdf")

    try:
        with st.spinner("Analyzing…"):
            result = analyze_bytes(uploaded_file.getvalue(), uploaded_file.name, render=True)
    except ValueError as exc:
        st.error(str(exc))
    except Exception:
        # Log the real cause server-side while showing the reader a plain
        # message. Swallowing it entirely made a production failure
        # undiagnosable from the deployment logs: all they showed was that
        # something went wrong, never what.
        logger.exception("Analysis failed for an uploaded %s file", "PDF" if is_pdf else "DOCX")
        st.error(
            "Couldn't read this file — it may be corrupted, password-protected, "
            "or not a valid PDF/DOCX. Try re-exporting it and uploading again."
        )
    else:
        _render_score(result.score)
        _render_findings(result.findings)
        _render_pages(result.rendered_pages, is_pdf)

        naive_col, aware_col = st.columns(2)
        with naive_col:
            with st.expander("Naive extraction — what a basic, layout-blind parser sees"):
                st.text(result.naive_text)
        with aware_col:
            with st.expander("Layout-aware extraction — columns and tables handled"):
                st.text(result.aware_text)

st.divider()
st.caption("Open source: [github.com/volodymyr-holovan/ats-resume-xray](https://github.com/volodymyr-holovan/ats-resume-xray)")

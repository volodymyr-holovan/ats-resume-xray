"""Streamlit demo: upload a resume and see what a parsing pipeline actually
extracts from it — naive (layout-blind) vs. layout-aware — plus which
documented parsing risks it triggers.

Run locally with: streamlit run app.py
"""

import tempfile
from pathlib import Path

import streamlit as st

from ats_xray.docx_extract import extract_docx_full, extract_docx_naive
from ats_xray.engine import run_rules
from ats_xray.extract import extract_layout_aware, extract_naive

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}
SEVERITY_RENDERER = {"high": st.error, "medium": st.warning, "low": st.info}

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

if uploaded_file is not None:
    suffix = Path(uploaded_file.name).suffix.lower()

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    try:
        if suffix == ".pdf":
            naive_text = extract_naive(tmp_path)
            aware_text = extract_layout_aware(tmp_path)
        else:
            naive_text = extract_docx_naive(tmp_path)
            aware_text = extract_docx_full(tmp_path)
        findings = run_rules(tmp_path, naive_text, aware_text)
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    st.subheader("Findings")
    if not findings:
        st.success("No documented parsing risks triggered.")
    else:
        ordered_findings = sorted(findings, key=lambda f: SEVERITY_ORDER[f.rule.severity])
        for finding in ordered_findings:
            render = SEVERITY_RENDERER[finding.rule.severity]
            render(f"**[{finding.rule.severity.upper()}]** {finding.rule.description}")
            st.caption(f"Evidence: {finding.evidence}")
            st.caption(f"Source: research_sources.md#{finding.rule.source}")

    naive_col, aware_col = st.columns(2)
    with naive_col:
        with st.expander("Naive extraction — what a basic, layout-blind parser sees"):
            st.text(naive_text)
    with aware_col:
        with st.expander("Layout-aware extraction — columns and tables handled"):
            st.text(aware_text)

st.divider()
st.caption("Open source: [github.com/volodymyr-holovan/ats-resume-xray](https://github.com/volodymyr-holovan/ats-resume-xray)")

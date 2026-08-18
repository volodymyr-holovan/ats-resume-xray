"""Streamlit demo: upload a resume and see what a parsing pipeline actually
extracts from it — naive (layout-blind) vs. layout-aware — plus which
documented parsing risks it triggers.

Run locally with: streamlit run app.py
"""

import streamlit as st

from ats_xray.pipeline import analyze_bytes

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
    try:
        result = analyze_bytes(uploaded_file.getvalue(), uploaded_file.name)
    except ValueError as exc:
        st.error(str(exc))
    except Exception:
        st.error(
            "Couldn't read this file — it may be corrupted, password-protected, "
            "or not a valid PDF/DOCX. Try re-exporting it and uploading again."
        )
    else:
        naive_text, aware_text, findings = result.naive_text, result.aware_text, result.findings

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

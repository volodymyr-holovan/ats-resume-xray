"""Streamlit demo: upload a resume and see what a parsing pipeline actually
extracts from it — naive (layout-blind) vs. layout-aware.

Run locally with: streamlit run app.py
"""

import tempfile
from pathlib import Path

import streamlit as st

from ats_xray.docx_extract import extract_docx_full, extract_docx_naive
from ats_xray.extract import extract_layout_aware, extract_naive

st.set_page_config(page_title="ATS Resume X-Ray", page_icon="🔎")

st.title("ATS Resume X-Ray")
st.write(
    "Upload a resume (PDF or DOCX) to see what a resume-parsing pipeline "
    "actually extracts from it — not a black-box score, an actual diff."
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
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    naive_col, aware_col = st.columns(2)
    with naive_col:
        st.subheader("Naive extraction")
        st.caption("What a basic, layout-blind parser sees")
        st.text(naive_text)
    with aware_col:
        st.subheader("Layout-aware extraction")
        st.caption("Columns and tables handled")
        st.text(aware_text)

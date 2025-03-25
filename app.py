# app.py

import streamlit as st
from pages import tab1_existing_project, tab2_custom_analysis, tab0_readme

st.set_page_config(page_title="Tokenomics Lab", layout="wide")

st.title("🚀 Tokenomics Analysis & Evaluation")

tab0, tab1, tab2 = st.tabs(["📘Readme- Hướng dẫn sử dụng", "📊 Dự Án Có Sẵn", "🧪 Phân Tích Tùy Chỉnh"])

with tab0:
    tab0_readme.render_tab0()

with tab1:
    tab1_existing_project.render_tab()

with tab2:
    tab2_custom_analysis.render_tab()
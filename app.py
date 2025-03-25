# app.py

import streamlit as st
from pages import tab1_existing_project, tab2_custom_analysis

st.set_page_config(page_title="Tokenomics Lab", layout="wide")

st.title("🚀 Tokenomics Analysis & Evaluation")

tab1, tab2 = st.tabs(["📊 Dự Án Có Sẵn", "🧪 Phân Tích Tùy Chỉnh"])

with tab1:
    tab1_existing_project.render_tab()

with tab2:
    tab2_custom_analysis.render_tab()
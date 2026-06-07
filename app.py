import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
import dashboard_lib as L

st.set_page_config(page_title="Day 2 · 도구 호출 & 결과 분리", page_icon="2️⃣", layout="wide")
st.title("2️⃣ Day 2 · 도구 호출 & 결과 분리")

tabs = st.tabs(["🏠 개요", "🤔 왜 만드나?", "Day 2"])
with tabs[0]:
    L.render_overview()
with tabs[1]:
    L.render_why()
with tabs[2]:
    L.render_day2()

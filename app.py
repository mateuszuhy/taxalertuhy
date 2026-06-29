import streamlit as st
from engine import run_engine

st.set_page_config(page_title="UHY Tax Alert V3.2", layout="wide")

st.title("🔵 UHY Tax Alert Factory – V3.2 (Stable AI Engine)")

api_key = st.text_input("OpenAI API Key", type="password")

if "result" not in st.session_state:
    st.session_state.result = None

if st.button("🚀 Generate Tax Alert"):

    if not api_key:
        st.error("Missing API key")
    else:
        st.session_state.result = run_engine(api_key)

if st.session_state.result:

    result = st.session_state.result

    st.subheader("🟢 LEAD NEWS")
    for n in result["lead"]:
        st.write(n)

    st.subheader("🟡 STANDARD NEWS")
    for n in result["standard"]:
        st.write(n)

    with open("output/tax_alert.pptx", "rb") as f:
        st.download_button("⬇ Download PPT", f, "tax_alert.pptx")

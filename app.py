import streamlit as st
from engine import run_tax_engine

st.set_page_config(page_title="UHY Tax Alert Factory", layout="wide")

st.title("🔵 UHY Tax Alert Factory – V3 AI Engine")

api_key = st.text_input("OpenAI API Key", type="password")

if st.button("🚀 Generate Tax Alert"):

    if not api_key:
        st.error("Missing API key")
    else:
        result = run_tax_engine(api_key)

        st.success("Tax Alert generated!")

        st.subheader("LEAD NEWS")
        st.write(result["lead"])

        st.subheader("STANDARD NEWS")
        st.write(result["standard"])

        with open("output/tax_alert.pptx", "rb") as f:
            st.download_button(
                "⬇ Download PPTX",
                f,
                file_name="tax_alert.pptx"
            )

import streamlit as st
from engine import run_engine

st.set_page_config(page_title="UHY Tax Alert V3.4", layout="wide")

st.title("🔵 UHY Tax Alert Factory – V3.4 (Tax Intelligence Engine)")

api_key = st.text_input("OpenAI API Key", type="password")

if "result" not in st.session_state:
    st.session_state.result = None

if st.button("🚀 Generate Tax Alert"):

    if not api_key:
        st.error("Missing API key")

    else:
        try:
            st.session_state.result = run_engine(api_key)

        except Exception as e:
            st.error(f"Engine error: {str(e)}")


if st.session_state.result:

    result = st.session_state.result

    st.subheader("🟢 LEAD TAX NEWS")

    for n in result["lead"]:
        st.write(f"**{n['title']}**")
        st.write(n.get("summary", []))

    st.subheader("🟡 STANDARD TAX NEWS")

    for n in result["standard"]:
        st.write(f"**{n['title']}**")
        st.write(n.get("summary", []))

    file_path = result.get("file_path")

    if file_path:
        with open(file_path, "rb") as f:
            st.download_button(
                "⬇ Download PPT",
                f,
                file_name="tax_alert.pptx"
            )

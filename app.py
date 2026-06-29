import streamlit as st
from engine import run_engine

api_key = st.text_input("OpenAI API Key", type="password")

if api_key:

    result = run_engine(api_key)

    st.subheader("🟢 Żeneruj TAX ALERT")

    for n in result["items"]:

        st.markdown(f"### {n.title}")
        st.write(n.what_changed)
        st.write(n.impact)
        st.write(n.legal_basis)
        st.write(f"Źródło: {n.source}")
        st.write(n.url)
        st.write("---")

    st.download_button(
        "Pobierz PPT",
        open(result["file_path"], "rb"),
        file_name="tax_alert.pptx"
    )

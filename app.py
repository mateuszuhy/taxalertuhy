import streamlit as st
from engine import run_engine

st.set_page_config(page_title="UHY Tax Alert V5.2", layout="wide")

st.title("🔵 UHY TAX ALERT ENGINE V5.2")

# API KEY
api_key = st.text_input("Wprowadź OpenAI API Key", type="password")

# 🔵 PRZYCISK START (KLUCZOWE)
run = st.button("🚀 Generuj Tax Alert")

if api_key and run:

    with st.spinner("Generowanie analizy podatkowej..."):

        result = run_engine(api_key)

    st.success("Gotowe!")

    # NEWSY
    st.subheader("🟢 Tax Alert")

    for n in result["items"]:

        st.markdown(f"### {n.title}")
        st.write("📌", n.what_changed)
        st.write("📊", n.impact)
        st.write("⚖️", n.legal_basis)
        st.write(f"🔗 {n.source}")
        st.write(n.url)
        st.write("---")

    # DOWNLOAD PPT
    with open(result["file_path"], "rb") as f:
        st.download_button(
            "⬇️ Pobierz prezentację PPT",
            f,
            file_name="uhy_tax_alert_v5_2.pptx"
        )

elif api_key and not run:
    st.info("Kliknij przycisk, aby wygenerować Tax Alert.")

else:
    st.warning("Wprowadź OpenAI API Key, aby rozpocząć.")

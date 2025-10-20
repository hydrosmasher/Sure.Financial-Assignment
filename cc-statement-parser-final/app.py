import streamlit as st
from ccparser import parse_pdf
import tempfile

st.set_page_config(page_title="Credit Card Statement Parser", layout="wide")
st.title("Credit Card Statement Parser — LayoutSign")

uploaded = st.file_uploader("Upload one or more credit card statement PDFs", type=["pdf"], accept_multiple_files=True)
if uploaded:
    results = []
    for up in uploaded:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(up.read()); path = tmp.name
        res = parse_pdf(path)
        results.append((up.name, res))

    for name, res in results:
        st.subheader(f":page_facing_up: {name}  —  Provider: **{res.meta.get('provider')}**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Issuer", res.issuer.value or "—")
            st.metric("Card Last-4", res.card_last4.value or "—")
        with col2:
            st.metric("Billing Start", res.billing_start.value or "—")
            st.metric("Billing End", res.billing_end.value or "—")
        with col3:
            st.metric("Payment Due", res.due_date.value or "—")
            st.metric("Statement Balance", res.statement_balance.value or "—")

        with st.expander("Evidence & Confidence (raw JSON)"):
            st.json(res.model_dump())

        if res.transactions:
            import pandas as pd
            df = pd.DataFrame([t.model_dump() for t in res.transactions])
            st.dataframe(df, use_container_width=True)

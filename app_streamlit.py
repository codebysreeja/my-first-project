import streamlit as st
import pandas as pd
import requests

st.title("Amazon Return Fraud Detector")

uploaded_file = st.file_uploader("Upload Online Retail dataset (Excel)", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Data Preview:", df.head())
    return_rate = df['InvoiceNo'].astype(str).str.startswith('C').mean()
    st.write(f"Overall return rate: {return_rate:.2%}")

    st.subheader("Manual Feature Entry")
    quantity = st.number_input("Quantity", min_value=0)
    unit_price = st.number_input("Unit Price", min_value=0.0)
    features = [[quantity, unit_price]]

    if st.button("Predict Fraud"):
        response = requests.post("http://127.0.0.1:8000/predict", json={"features": features})
        prediction = response.json()
        if prediction["fraudulent"]:
            st.error("Warning: This return may be fraudulent!")
        else:
            st.success("This return seems legitimate.")
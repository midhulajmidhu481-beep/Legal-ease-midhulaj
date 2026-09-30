import streamlit as st
import requests
st.set_page_config(page_title="LegalEaseAI - 210PocketSmart")
st.title("LegalEaseAI - Legal Document Simplifier")
uploaded_file = st.file_uploader("Upload Legal PDF", type="pdf")
if uploaded_file:
    # call backend API
    st.success("Document simplified!")

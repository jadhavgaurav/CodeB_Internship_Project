import streamlit as st
import pandas as pd
import os
import joblib
from feature_scraper import extract_features_from_url
import subprocess
import json
import tempfile
import streamlit as st
from google.oauth2 import service_account

# Config
st.set_page_config(page_title="Phishing Website Detector", page_icon="🔐", layout="centered")

# ========== Constants ==========
MODEL_PATH = "models/xgb_pipeline.pkl"
GCP_KEY_PATH = "secret/gcp_key.json"

# Authenticate GCP
if os.path.exists(GCP_KEY_PATH):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(GCP_KEY_PATH)
else:
    st.error("🚨 GCP credentials file not found.")
    st.stop()

# Pull model using DVC
if not os.path.exists(MODEL_PATH):
    with st.spinner("🔁 Downloading model from GCS using DVC..."):
        try:
            subprocess.run(["dvc", "pull", f"{MODEL_PATH}.dvc"], check=True)
        except subprocess.CalledProcessError:
            st.error("❌ Failed to pull model from DVC. Check credentials or DVC setup.")
            st.stop()

# Load model
pipeline = joblib.load(MODEL_PATH)
st.success("✅ Model loaded and ready.")

# ========== Custom CSS Styling ==========
st.markdown("""
<style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1549921296-3a4c24821eb0");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .title-style {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #23a9f2;
        margin: 2rem 0 1.5rem 0;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
    }
    .main-box {
        padding: 2rem;
        border-radius: 15px;
        max-width: 700px;
        margin: auto;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        background-color: rgba(255, 255, 255, 0.9);
    }
    .predict-btn > button {
        background-color: #dc3545 !important;
        color: white !important;
        font-size: 16px !important;
        border-radius: 8px !important;
        padding: 10px 24px;
    }
</style>
""", unsafe_allow_html=True)

# ========== Title ==========
st.markdown('<div class="title-style">🔍 Phishing URL Detector</div>', unsafe_allow_html=True)

# ========== Main UI ==========
st.markdown('<div class="main-box">', unsafe_allow_html=True)

url_input = st.text_input("Enter Website URL:", placeholder="https://example.com")

col = st.columns([1, 1, 1])
with col[1]:
    predict_btn = st.button("🚀 Predict")

if predict_btn:
    if not url_input:
        st.warning("⚠️ Please enter a URL.")
    else:
        try:
            with st.spinner("🔄 Extracting features & predicting..."):
                features_df = extract_features_from_url(url_input)

                phishing_prob = pipeline.predict_proba(features_df)[0][1]

                st.info(f"📊 Model Confidence (Phishing): **{phishing_prob:.2%}**")

                if phishing_prob > 0.5:
                    st.error("🚨 This is likely a **Phishing Website**")
                else:
                    st.success("✅ This appears to be a **Legitimate Website**")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

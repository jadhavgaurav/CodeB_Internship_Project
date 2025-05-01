import streamlit as st
import pandas as pd
import joblib
from feature_scraper import extract_features_from_url

# ========== Page Config ==========
st.set_page_config(
    page_title="Phishing Website Detector",
    page_icon="🔐",
    layout="centered"
)

# ========== Custom Styling ==========
st.markdown("""
<style>
    .stApp {
        background-image: url("https://t4.ftcdn.net/jpg/03/58/10/87/360_F_358108785_rNJtmort9m65M3pft5swd7lnKJcTCB8u.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .main-box {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 3rem 2rem;
        border-radius: 15px;
        max-width: 700px;
        margin: auto;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .title-style {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #003366;
        margin-bottom: 2rem;
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

# ========== Load Model ==========
pipeline = joblib.load("xgb_pipeline.pkl")

# ========== UI ==========
st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.markdown('<div class="title-style">🔍 Phishing URL Detector</div>', unsafe_allow_html=True)

url_input = st.text_input("Enter Website URL:", placeholder="https://example.com")

col = st.columns([1, 1, 1])
with col[1]:
    predict_btn = st.button("🚀 Predict")

if predict_btn:
    if url_input:
        try:
            with st.spinner("🔄 Extracting features & predicting..."):
                features = extract_features_from_url(url_input)
                df = pd.DataFrame(features)
                prob_phishing = pipeline.predict_proba(df)[0][1]  # Probability of phishing

            st.info(f"🔢 Confidence (Phishing): **{prob_phishing:.2%}**")

            if prob_phishing > 0.5:
                st.error("🚨 Phishing Website Detected")
            else:
                st.success("✅ Legitimate Website")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a URL.")

st.markdown('</div>', unsafe_allow_html=True)

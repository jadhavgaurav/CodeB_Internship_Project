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

# ========== CSS Styling ==========
st.markdown("""
<style>
    .stApp {
        background-image: url("https://t4.ftcdn.net/jpg/03/58/10/87/360_F_358108785_rNJtmort9m65M3pft5swd7lnKJcTCB8u.jpg");
        background-size: cover;
        background-attachment: fixed;
    }

    .main-container {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 3rem 2rem;
        border-radius: 15px;
        max-width: 700px;
        margin: 5vh auto;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        text-align: center;
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #003366;
        margin-bottom: 1.5rem;
    }

    .predict-btn button {
        background-color: #dc3545 !important;
        color: white !important;
        font-size: 16px !important;
        border-radius: 8px !important;
        padding: 10px 24px;
        width: 100%;
    }

    .stTextInput > div > div > input {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ========== Load Model ==========
pipeline = joblib.load("xgb_pipeline.pkl")

# ========== App Layout ==========
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown('<div class="main-title">🔍 Phishing URL Detector</div>', unsafe_allow_html=True)

url_input = st.text_input("Enter Website URL", placeholder="https://example.com")

if st.button("🚀 Predict", key="predict"):
    if url_input:
        try:
            with st.spinner("🔄 Extracting features & predicting..."):
                features = extract_features_from_url(url_input)
                df = pd.DataFrame(features)
                prediction = pipeline.predict(df)[0]
            st.success("✅ Legitimate Website" if prediction == 0 else "🚨 Phishing Website")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("Please enter a URL.")

st.markdown('</div>', unsafe_allow_html=True)

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

# ========== Custom CSS ==========
st.markdown("""
<style>
    .stApp {
        background-image: url("https://t4.ftcdn.net/jpg/03/58/10/87/360_F_358108785_rNJtmort9m65M3pft5swd7lnKJcTCB8u.jpg");
        background-size: cover;
        background-attachment: fixed;
    }

    .title-style {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        margin-top: 40px;
        margin-bottom: 30px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }

    .stTextInput input {
        text-align: center;
    }

    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        padding: 10px 24px;
        font-size: 16px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ========== Load Trained Pipeline ==========
pipeline = joblib.load("xgb_pipeline.pkl")

# ========== App UI ==========
st.markdown('<div class="title-style">🔍 Phishing URL Detector</div>', unsafe_allow_html=True)

url_input = st.text_input("Enter Website URL", placeholder="https://example.com")

if st.button("🚀 Predict"):
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
        st.warning("⚠️ Please enter a URL.")

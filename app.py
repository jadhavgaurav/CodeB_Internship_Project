import streamlit as st
import pandas as pd
import joblib
from feature_scraper import extract_features_from_url

# ========== Page Config & Styling ==========
st.set_page_config(
    page_title="Phishing Website Detector",
    page_icon="🔐",
    layout="centered"
)

# ========== Custom CSS Styling ==========
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://t4.ftcdn.net/jpg/03/58/10/87/360_F_358108785_rNJtmort9m65M3pft5swd7lnKJcTCB8u.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .main-box {
        background-color: rgba(255, 255, 255, 0.88);
        padding: 2rem;
        border-radius: 15px;
        max-width: 700px;
        margin: 3rem auto;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }
    .title-style {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        color: #004080;
        margin-bottom: 20px;
    }
    .predict-btn > button {
        background-color: #004080 !important;
        color: white !important;
        border-radius: 8px;
        font-size: 16px;
        padding: 10px 24px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ========== Load Trained Pipeline ==========
pipeline = joblib.load("xgb_pipeline.pkl")  # Ensure this path is valid

# ========== App UI ==========
st.markdown('<div class="main-box">', unsafe_allow_html=True)

# Title
st.markdown("""
    <div class="title-style">
        <div style="display: flex; justify-content: center; align-items: center;">
            <span style="font-size: 40px;">🔍</span>&nbsp;
            <span>Phishing URL Detector</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# URL Input
url_input = st.text_input("Enter Website URL:", placeholder="https://example.com")

# Predict Button
col_center = st.columns([1, 2, 1])[1]
with col_center:
    predict_btn = st.button("🚀 Predict", key="predict", help="Click to predict", type="primary")

# Prediction Logic
if predict_btn and url_input:
    try:
        with st.spinner("🔄 Extracting features & predicting..."):
            features = extract_features_from_url(url_input)
            df_features = pd.DataFrame(features)
            prediction = pipeline.predict(df_features)[0]

        if prediction == 0:
            st.success("✅ Legitimate Website")
        else:
            st.error("🚨 Phishing Website")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# End of container
st.markdown('</div>', unsafe_allow_html=True)

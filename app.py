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

# Background Image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://images.unsplash.com/photo-1549921296-3a4c24821eb0");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .main-box {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }}
    .title-style {{
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        color: #004080;
        margin-bottom: 20px;
    }}
    .btn-style > button {{
        background-color: #008CBA;
        color: white;
        padding: 10px 24px;
        font-size: 16px;
        border-radius: 8px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ========== Load Pipeline ==========
pipeline = joblib.load("xgb_pipeline.pkl")  # Make sure path is correct

# ========== App UI ==========
with st.container():
    st.markdown('<div class="main-box">', unsafe_allow_html=True)

    st.markdown('<div class="title-style">🔍 Phishing URL Detector</div>', unsafe_allow_html=True)

    url_input = st.text_input("Enter Website URL:", placeholder="https://example.com")

    paste_col, predict_col = st.columns([1, 2])
    with paste_col:
        if st.button("📋 Paste from Clipboard"):
            import pyperclip
            try:
                pasted_url = pyperclip.paste()
                st.experimental_set_query_params(url=pasted_url)
                url_input = pasted_url
            except:
                st.warning("Clipboard access not available.")

    with predict_col:
        predict_btn = st.button("🚀 Predict", key="predict", help="Click to predict phishing or legitimate.")

    if predict_btn and url_input:
        try:
            with st.spinner("🔄 Extracting features & predicting..."):
                features = extract_features_from_url(url_input)
                df_features = pd.DataFrame(features)
                prediction = pipeline.predict(df_features)[0]

            st.success("✅ Legitimate Website" if prediction == 0 else "🚨 Phishing Website")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)

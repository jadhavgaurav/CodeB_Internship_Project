import streamlit as st
import pandas as pd
import os
import joblib
import shap
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
from feature_scraper import extract_features_from_url

# Config
st.set_page_config(page_title="Phishing Website Detector", page_icon="🔐", layout="centered")

MODEL_PATH = "md/xgb_pipeline.pkl"

# Load model directly
if os.path.exists(MODEL_PATH):
    pipeline = joblib.load(MODEL_PATH)
    st.success("✅ Model loaded successfully and ready for prediction.")
else:
    st.error(f"❌ Model file not found at: {MODEL_PATH}")
    st.stop()

# Initialize SHAP TreeExplainer
try:
    explainer = shap.TreeExplainer(pipeline.named_steps["classifier"])
except Exception as e:
    st.warning(f"⚠️ SHAP explainer initialization failed: {e}")
    explainer = None

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
        color: #2b7cd3;
        margin: 2rem 0 1.5rem 0;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
    }
    .main-box {
        padding: 2rem;
        max-width: 700px;
        margin: auto;
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

url_input = st.text_input("Enter Website URL:", placeholder="https://example.com")

col = st.columns([1, 1, 1])
with col[1]:
    predict_btn = st.button("🚀 Predict")

# Store features for explanation if needed
features_df = None
phishing_prob = None

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

# Explain Button
if features_df is not None and st.button("🔎 Explain"):
    if explainer:
        try:
            # Preprocess the features manually using pipeline steps
            transformed = pipeline.named_steps["power_transformer"].transform(features_df)
            scaled = pipeline.named_steps["scaler"].transform(transformed)

            shap_values = explainer.shap_values(scaled)

            st.subheader("🔍 SHAP Explanation (Local Prediction)")

            fig = plt.figure()
            shap.plots._waterfall.waterfall_legacy(explainer.expected_value, shap_values[0], features_df.columns, show=False)
            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ SHAP explanation failed: {str(e)}")
    else:
        st.warning("⚠️ SHAP explainer is not initialized.")

st.markdown('</div>', unsafe_allow_html=True)

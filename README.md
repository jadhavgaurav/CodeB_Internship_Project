# 🔐 Phishing Website Detection Using Machine Learning

This repository contains the end-to-end solution for detecting phishing websites using advanced machine learning techniques. The project was developed as part of the **CodeB Data Science Integrated Internship** at IT Vedant.

🚀 **Live App**: [website-phishing-detection.streamlit.app](https://website-phishing-detection.streamlit.app)

---

## 📌 Problem Statement

Phishing websites trick users into revealing sensitive information by mimicking legitimate domains. This project builds a **machine learning classification model** to detect whether a website is **phishing** or **legitimate**, based on URL and HTML/JS behavior features. It also explains predictions using **LIME** and **SHAP**.

---

## 🗂️ Dataset

- Source: Provided by the institute (CSV format)
- Shape: `11430 rows × 89 columns`
- Target column: `status` — (`legitimate`: 0, `phishing`: 1)

---

## ✅ Project Timeline Summary

### 📅 Week 1–4 – Data Exploration & Preprocessing
- Dropped irrelevant columns (`url`)
- Balanced classes → no oversampling needed
- Performed correlation filtering and skewness handling
- Applied robust scaling and Yeo-Johnson transformation
- Feature Engineering:
  - `url_complexity`, `tag_to_link_ratio`, `domain_numeric_intensity`, `path_word_complexity`
- Final Features Selected: ✅ 28 (via Correlation, ANOVA, RFE, Random Forest Importance, VIF)

### 📅 Week 5–6 – Model Building, Evaluation & Explanation
- Trained multiple models: Logistic Regression, KNN, SVM, Decision Tree, Random Forest, XGBoost, ANN
- ✅ Best Model: **XGBoostClassifier**
- Hyperparameter tuning via `GridSearchCV`
- ROC-AUC: **0.990**, F1 Score: **95.86%**

---

## ⚙️ Tech Stack

| Component        | Tool/Library         |
|------------------|----------------------|
| Data Processing  | Pandas, NumPy        |
| Visualization    | Matplotlib, Seaborn  |
| ML Models        | Scikit-learn, XGBoost|
| Explainability   | SHAP, LIME           |
| Frontend         | Streamlit            |
| Deployment       | Streamlit Cloud      |
| Version Control  | Git, DVC             |
| Containerization | Docker               |
| CI/CD            | GitHub Actions       |

---

## 📁 Project Structure

```
phishing-detector/
├── app.py                  # Streamlit frontend
├── feature_scrapper.py     # URL feature extraction
├── model.pkl               # Trained model
├── explainer.pkl           # Optional LIME/SHAP objects
├── .env                    # API keys
├── Dockerfile              # Docker container setup
├── requirements.txt        # Python dependencies
├── dvc.yaml                # DVC pipeline
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Actions workflow
├── data/
│   └── dataset_phishing.csv
└── model/
    └── xgb_pipeline.pkl
```

---

## 🔍 Explainable AI – LIME & SHAP

### LIME Highlights
- Local explanation for individual predictions
- Interactive `.html` visualizations
- Top influential features:
  - `google_index`, `page_rank`, `phish_hints`, `ratio_intHyperlinks`

### SHAP Highlights
- Global feature importance and summary plots
- SHAP bar plot aligns with domain intuition:
  - Low trust scores → phishing
  - Legitimate indicators (title-domain match, indexing) → non-phishing

---

## 🎯 Evaluation Metrics

| Metric       | Value   |
|--------------|---------|
| Accuracy     | 95.83%  |
| Precision    | 95.46%  |
| Recall       | 96.23%  |
| F1 Score     | 95.86%  |
| ROC-AUC      | 0.990   |

### Visual Tools
- Confusion Matrix Heatmap
- ROC Curve
- Precision-Recall Curve

---

## 🧪 Sample Use Case (LIME)

**URL:** `http://secure-login-info.confirmupdate.biz`  
**Prediction:** Phishing  
**Top Contributors:**  
- `google_index = 0` → +0.31  
- `phish_hints = 1` → +0.22  
- `page_rank = 1` → +0.18

---

## 🧠 Run the App Locally

```bash
git clone https://github.com/<your-username>/phishing-detector.git
cd phishing-detector
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Add .env file
echo "GOOGLE_API_KEY=your_key
PAGERANK_API_KEY=your_key" > .env

# Launch app
streamlit run app.py
```

---

## 🐳 Docker Deployment

```bash
docker build -t phishing-detector .
docker run -p 8501:8501 phishing-detector
```

---

## ☁️ Streamlit Cloud Deployment

1. Push code to GitHub
2. Connect repo to [streamlit.io](https://streamlit.io)
3. Add secrets for `GOOGLE_API_KEY` and `PAGERANK_API_KEY`
4. Click **Deploy**

---

## 📦 DVC Usage

```bash
dvc pull         # Downloads model and dataset files
```

Tracked:
- `data/dataset_phishing.csv`
- `model/model.pkl`

---

## 📜 License

MIT License © 2025 Gaurav Jadhav  
[GitHub](https://github.com/jadhavgaurav) | [Portfolio](https://jadhavgaurav.github.io/portfolio) | [LinkedIn](https://linkedin.com/in/gaurav-jadhav-617740213)

---

## 🙏 Credits

- SHAP, LIME, OpenPageRank API, Google CSE API
- IT Vedant – CodeB Data Science Internship
- Streamlit & GitHub Actions team
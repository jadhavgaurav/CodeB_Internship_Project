# 🔐 Phishing Website Detection Using Machine Learning

This repository contains the end-to-end solution for detecting phishing websites using advanced machine learning techniques. The project was developed as part of the **CodeB Data Science Integrated Internship** at IT Vedant.

---

## 📌 Problem Statement

Phishing websites trick users into revealing sensitive information by mimicking legitimate domains. This project aims to build a **machine learning classification model** that can detect whether a website is **phishing** or **legitimate**, based on URL features and HTML/JS behavior.

---

## 🗂️ Dataset

- Source: Provided by the institute (CSV format)
- Shape: `11430 rows × 89 columns`
- Target column: `status` — (`legitimate`: 0, `phishing`: 1)

---

## ✅ Project Timeline (Week-wise Summary)

### 📅 Week 1 – Problem Understanding & Dataset Exploration
- Understood phishing behaviors and detection strategies
- Dropped the `url` column (non-informative)
- Target analysis: `status` distribution is balanced (no resampling needed)
- Performed EDA:
  - Histograms, KDE plots, correlation heatmaps
  - Identified skewed and highly variable features
- Insights:
  - Phishing URLs often have higher `nb_qm`, `nb_www`, `ratio_digits_url`
  - Legitimate sites have more stable HTML tag distributions

### 📅 Week 2 – Feature Understanding & Selection
- Feature description created for all 88 usable features
- Target label encoded (`legitimate` → 0, `phishing` → 1)
- Feature Selection Pipeline:
  1. 🔁 **Correlation Check** (dropped features with `corr > 0.9`)
  2. 📊 **Univariate ANOVA (f_classif)** – top 30 features
  3. 🌲 **Random Forest Feature Importance** – top 30 features
  4. 🔍 **RFE (Recursive Feature Elimination)** – top 30 features
  5. 🔗 Final features = Intersection of ANOVA & RFE results
  6. 🚫 **VIF Analysis** – removed multicollinear features (`VIF > 10`)

### 📅 Week 3 – Data Cleaning & Preprocessing
- Checked for null values (none found)
- No duplicates present
- Feature scaling: ✔️ **RobustScaler**
- Target-preserving split: 80% train / 20% test
- Skewness handled using: ✔️ **PowerTransformer (Yeo-Johnson)**
- Applied final outlier-safe transformations
- Total final features used: ✅ 28

### 📅 Week 4 – Feature Engineering
Created 4 high-impact custom features:
1. `url_complexity` – sum of suspicious symbols
2. `tag_to_link_ratio` – ratio of tags vs hyperlinks
3. `domain_numeric_intensity` – digit density × domain age
4. `path_word_complexity` – avg path word length × longest word

Dropped 5 redundant features based on correlation & low importance.

### 📅 Week 5–6 – Model Building, Evaluation & Interpretation

🔍 **Models Trained**:
- Logistic Regression
- KNN
- SVM
- Decision Tree
- Random Forest ✅
- XGBoost
- ANN

🎯 **Best Model**: `XGBoostClassifier`
- **Hyperparameter tuning**: `GridSearchCV` with `roc_auc` scoring
- **Best params**:
```python
RandomForestClassifier(
    'colsample_bytree': 0.8, 
    'gamma': 0.1, 
    'learning_rate': 0.1, 
    'max_depth': 10, 
    'n_estimators': 100, 
    'subsample': 0.8
)
```

## ✅ Model Evaluation & Performance

### 📊 Evaluation Metrics

| Metric       | Value   |
|--------------|---------|
| Accuracy     | 95.83%   |
| Precision    | 95.46%   |
| Recall       | 96.23%   |
| F-1 Score    | 95.86    |
| ROC-AUC      | 0.990   |

These metrics indicate that the model is highly effective in distinguishing between **phishing** and **legitimate** websites.

---

### 📈 Visualizations

- ✅ **Confusion Matrix Heatmap**
- ✅ **ROC Curve**
- ✅ **Precision-Recall Curve** *(with threshold annotations)*

All plots were generated to visually assess the model's classification confidence and performance balance.

---

## 🔍 Model Explainability (LIME)

LIME was used to explain the **top 5 individual predictions** made by the final Random Forest model.

### 🔑 Key Contributing Features:
- `google_index`
- `page_rank`
- `nb_www`
- `ratio_intHyperlinks`

### 📂 Output Format:
- Interactive LIME explanations saved as `.html` files (`lime_explanation_instance_*.html`)
- Feature contribution bar plots highlight which features pushed predictions toward phishing or legitimate.

These interpretations help build **trust** and **transparency** in the model by showing how it makes decisions for specific URLs.


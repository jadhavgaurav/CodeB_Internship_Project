import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PowerTransformer, RobustScaler
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

# === Load Dataset ===
df = pd.read_csv("phishing_dataset.csv")  # Replace with your actual CSV

# === Final Feature Columns ===
final_features = [
    'shortest_word_host', 'nb_www', 'phish_hints', 'ratio_digits_host', 'google_index',
    'longest_words_raw', 'ratio_digits_url', 'length_words_raw', 'avg_word_path',
    'nb_qm', 'nb_dots', 'page_rank', 'domain_in_title', 'ratio_intHyperlinks'
]

# Replace 'Legitimate' with 0 and 'Phishing' with 1 in the 'status' column
df['status'] = df['status'].map({'legitimate':0, 'phishing':1})

X = df[final_features]
y = df['status']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42, 
)

# === Pipeline Setup ===
pipeline = Pipeline([
    ("power", PowerTransformer(method="yeo-johnson", standardize=False)),
    ("scaler", RobustScaler()),
    ("model", XGBClassifier(
        n_estimators=100,
        max_depth=10,
        learning_rate=0.1,
        colsample_bytree=0.8,
        subsample=0.8,
        gamma=0.1,
        use_label_encoder=False,
        eval_metric="logloss",
        random_state=42
    ))
])

# === Fit and Save ===
pipeline.fit(X, y)
joblib.dump(pipeline, "xgb_pipeline.pkl")
print("✅ Training completed and pipeline saved as 'xgb_pipeline.pkl'")


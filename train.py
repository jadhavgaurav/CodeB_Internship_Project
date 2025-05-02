import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PowerTransformer, RobustScaler
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

# === Load Dataset ===
data_path = 'data/dataset_phishing.csv'
df = pd.read_csv(data_path)

# === Final Features Used for Modeling ===
final_features = [
    'phish_hints', 'domain_in_title', 'length_words_raw', 'nb_www',
    'shortest_word_host', 'nb_qm', 'ratio_digits_host', 'google_index',
    'nb_dots', 'longest_words_raw', 'ratio_intHyperlinks',
    'page_rank', 'avg_word_path', 'ratio_digits_url'
]

# === Target Mapping ===
df['status'] = df['status'].map({'legitimate': 0, 'phishing': 1})

X = df[final_features]
y = df['status']

# === Define Pipeline ===
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

# === Train on full dataset (X, y) 
pipeline.fit(X, y)

# === Save Trained Pipeline
output_path = "models/xgb_pipeline.pkl"
joblib.dump(pipeline, output_path)
print(f"✅ Training completed and pipeline saved to: {output_path}")

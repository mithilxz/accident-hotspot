import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

from xgboost import XGBClassifier

from preprocessing import preprocess_data


# Load and preprocess
df,_ = preprocess_data("data/accident_prediction_india.csv")

# Encode target column
le = LabelEncoder()
df["Accident Severity"] = le.fit_transform(df["Accident Severity"])

# Features and target
X = df.drop("Accident Severity", axis=1)
y = df["Accident Severity"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Random Forest
rf = RandomForestClassifier(n_estimators=200)
rf.fit(X_train, y_train)

pred_rf = rf.predict(X_test)

print("RF Accuracy:", accuracy_score(y_test, pred_rf))


# XGBoost
xgb = XGBClassifier(
    objective="multi:softmax",
    num_class=3
)

xgb.fit(X_train, y_train)

pred_xgb = xgb.predict(X_test)

print("XGB Accuracy:", accuracy_score(y_test, pred_xgb))


# Save model
pickle.dump(rf, open("models/accident_model.pkl", "wb"))
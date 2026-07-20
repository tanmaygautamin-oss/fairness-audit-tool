"""
    ml/data.py
            WHAT: Downloads (once, then caches) the REAL Adult Census Income dataset
                from OpenML, and prepares it for machine learning.
"""

import pandas as pd
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split

def load_real_data():
    """
        WHAT: Fetches real U.S. Census data -- ~48,000 real individual records.
        WHY 'as_frame=True': gives us a clean pandas DataFrame instead of raw
            arrays, which is much easier to inspect and reason about.
        RETURNS: (X_train, X_test, y_train, y_test) as pandas DataFrames"""
    
    print("Downloading real Adult Census Income dataset (first run only)...")
    data = fetch_openml(name="adult", version=2, as_frame=True)
    df = data.frame.dropna() # drop rows with missing real-world values

    # The target column tells us whether income is >50K or <=50K
    df["target"] = (df["class"] == ">50K").astype(int)

    # Sensitive attributes we will audit fairness against
    sensitive_columns = ["sex", "race"]

    # Feature columns: everything except target and the raw class column
    feature_columns = [c for c in df.columns if c not in ["class", "target"]]

    # One-hot encode categorical features so the model can use them
    X = pd.get_dummies(df[feature_columns], drop_first=True)
    y = df["target"]
    sensitive = df[sensitive_columns].reset_index(drop=True)

    X_train, X_test, y_train, y_test, sens_train, sens_test = train_test_split(
        X, y, sensitive, test_size=0.3, random_state=42, stratify=y
    )

    return X_train, X_test, y_train, y_test, sens_train, sens_test

if __name__ == "__main__":

    # Quick manual test: run "python ml/data.py" to confirm real data loads

    X_train, X_test, y_train, y_test, sens_train, sens_test = load_real_data()
    print(f"Loaded {len(X_train) + len(X_test)} real records.")
    print(f"Sensitive attribute samples:\n{sens_test.head()}")
    
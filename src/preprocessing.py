import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess_data(df):

    # Remove missing values
    df = df.dropna()

    # Feature engineering
    df['Weekend'] = df['Day of Week'].apply(
        lambda x: 1 if x in ['Saturday', 'Sunday'] else 0
    )

    categorical_cols = [
        'State Name','City Name','Month','Day of Week',
        'Time of Day','Vehicle Type Involved',
        'Weather Conditions','Road Type','Road Condition',
        'Lighting Conditions','Traffic Control Presence',
        'Driver Gender','Driver License Status',
        'Alcohol Involvement','Accident Location Details'
    ]

    encoders = {}

    for col in categorical_cols:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            encoders[col] = le

    return df, encoders
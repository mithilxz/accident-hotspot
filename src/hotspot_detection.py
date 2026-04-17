import pandas as pd
from sklearn.cluster import KMeans

def detect_hotspots(df):

    features = df[['Number of Casualties','Number of Fatalities']]

    kmeans = KMeans(n_clusters=5, random_state=42)

    df['Hotspot Cluster'] = kmeans.fit_predict(features)

    return df
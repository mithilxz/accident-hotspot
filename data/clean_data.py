import pandas as pd

# Load dataset
df = pd.read_csv("C:\\Users\\mithi\\Downloads\\final_data.csv")  # change filename

# Remove fake/default coordinates
df = df[(df["Latitude"] != 22.9734) & (df["Longitude"] != 78.6569)]

# Remove missing values
df = df.dropna(subset=["Latitude", "Longitude", "Accident Severity"])

# Save cleaned dataset
df.to_csv("data/cleaned_accident_data.csv", index=False)

print("✅ Cleaned dataset saved!")
print("Remaining rows:", len(df))
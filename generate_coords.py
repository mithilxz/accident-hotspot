import pandas as pd

# Load dataset
df = pd.read_csv("data/accident_prediction_india.csv")

# Create location column
df['Full_Location'] = df['City Name'] + ", " + df['State Name']

# 🔥 Predefined major Indian cities (expandable)
city_coords = {
    "Bangalore, Karnataka": (12.9716, 77.5946),
    "Mumbai, Maharashtra": (19.0760, 72.8777),
    "Delhi, Delhi": (28.7041, 77.1025),
    "Chennai, Tamil Nadu": (13.0827, 80.2707),
    "Hyderabad, Telangana": (17.3850, 78.4867),
    "Kolkata, West Bengal": (22.5726, 88.3639),
    "Pune, Maharashtra": (18.5204, 73.8567),
    "Ahmedabad, Gujarat": (23.0225, 72.5714),
    "Jaipur, Rajasthan": (26.9124, 75.7873),
    "Lucknow, Uttar Pradesh": (26.8467, 80.9462),
    "Bhopal, Madhya Pradesh": (23.2599, 77.4126),
    "Patna, Bihar": (25.5941, 85.1376),
    "Chandigarh, Chandigarh": (30.7333, 76.7794),
    "Kochi, Kerala": (9.9312, 76.2673),
    "Goa, Goa": (15.2993, 74.1240),
    "Visakhapatnam, Andhra Pradesh": (17.6868, 83.2185),
    "Nagpur, Maharashtra": (21.1458, 79.0882),
    "Indore, Madhya Pradesh": (22.7196, 75.8577),
    "Surat, Gujarat": (21.1702, 72.8311),
    "Kanpur, Uttar Pradesh": (26.4499, 80.3319),
}

# 🧠 Fallback: assign random-ish India center if not found
def get_coords(location):
    return city_coords.get(location, (22.9734, 78.6569))  # center of India

# Apply mapping
df['Latitude'] = df['Full_Location'].apply(lambda x: get_coords(x)[0])
df['Longitude'] = df['Full_Location'].apply(lambda x: get_coords(x)[1])

# Save
df.to_csv("data/final_data.csv", index=False)

print("✅ DONE instantly! (No delay)")
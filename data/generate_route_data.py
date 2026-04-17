import pandas as pd
import random

data = []

routes = [
    # TOP TIER
    ((28.61, 77.20), (19.07, 72.87)),  # Delhi → Mumbai
    ((12.97, 77.59), (28.61, 77.20)),  # Bangalore → Delhi
    ((12.97, 77.59), (19.07, 72.87)),  # Bangalore → Mumbai
    ((28.61, 77.20), (17.38, 78.48)),  # Delhi → Hyderabad
    ((28.61, 77.20), (22.57, 88.36)),  # Delhi → Kolkata

    # SOUTH INDIA
    ((13.08, 80.27), (12.97, 77.59)),  # Chennai → Bangalore
    ((13.08, 80.27), (17.38, 78.48)),  # Chennai → Hyderabad
    ((12.97, 77.59), (9.93, 76.26)),   # Bangalore → Kochi
    ((12.97, 77.59), (11.01, 76.96)),  # Bangalore → Coimbatore

    # WEST INDIA
    ((19.07, 72.87), (18.52, 73.85)),  # Mumbai → Pune
    ((19.07, 72.87), (21.14, 79.08)),  # Mumbai → Nagpur
    ((19.07, 72.87), (23.03, 72.58)),  # Mumbai → Ahmedabad

    # NORTH INDIA
    ((28.61, 77.20), (26.91, 75.78)),  # Delhi → Jaipur
    ((28.61, 77.20), (30.73, 76.77)),  # Delhi → Chandigarh
    ((28.61, 77.20), (30.31, 78.03)),  # Delhi → Dehradun

    # EAST INDIA
    ((22.57, 88.36), (20.30, 85.82)),  # Kolkata → Bhubaneswar
    ((22.57, 88.36), (23.34, 85.31)),  # Kolkata → Ranchi

    # EXTRA CONNECTIVITY
    ((17.38, 78.48), (15.49, 73.82)),  # Hyderabad → Goa
    ((18.52, 73.85), (12.97, 77.59)),  # Pune → Bangalore
    ((15.30, 74.12), (12.97, 77.59)),  # Goa → Bangalore
]

severities = ["Minor", "Serious", "Fatal"]
weather = ["Clear", "Rainy", "Foggy"]
road_type = ["Highway", "Urban", "Rural"]

for _ in range(5000):

    (lat1, lon1), (lat2, lon2) = random.choice(routes)

    t = random.random()

    lat = lat1 + t * (lat2 - lat1)
    lon = lon1 + t * (lon2 - lon1)

    lat += random.uniform(-0.03, 0.03)
    lon += random.uniform(-0.03, 0.03)

    severity = random.choices(
        ["Minor", "Serious", "Fatal"],
        weights=[0.6, 0.3, 0.1]
    )[0]

    data.append([
        lat, lon,
        severity,
        random.choice(weather),
        random.choice(road_type),
        random.randint(0, 23)
    ])

df = pd.DataFrame(data, columns=[
    "Latitude", "Longitude", "Accident Severity",
    "Weather", "Road Type", "Hour"
])

df.to_csv("data/cleaned_accident_data.csv", index=False)

print("✅ Multi-route dataset created!")
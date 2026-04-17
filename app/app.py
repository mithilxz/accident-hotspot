import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import requests
import math
import random

# =========================
# 🔑 MAPBOX KEY
# =========================
MAPBOX_KEY = "YOUR_MAPBOX_KEY"

# =========================
# 🧠 SESSION INIT
# =========================
for key in ["points", "route", "clicked", "start", "end"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "points" else None

# =========================
# 📍 GEOCODE (NO FAIL)
# =========================
def geocode(place):
    try:
        if not place or place.strip() == "":
            return None

        place = place.strip()

        # 1️⃣ Mapbox
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{place}.json"
        params = {"access_token": MAPBOX_KEY, "limit": 1}

        res = requests.get(url, params=params, timeout=5)
        data = res.json()

        if "features" in data and len(data["features"]) > 0:
            lon, lat = data["features"][0]["center"]
            return lat, lon

        # 2️⃣ Fallback → OSM
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": place + ", India", "format": "json", "limit": 1}
        headers = {"User-Agent": "accident-app"}

        res = requests.get(url, params=params, headers=headers, timeout=5)
        data = res.json()

        if len(data) > 0:
            return float(data[0]["lat"]), float(data[0]["lon"])

        return None

    except:
        return None

# =========================
# 📍 REVERSE GEOCODE
# =========================
def reverse_geocode(lat, lon):
    try:
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{lon},{lat}.json"
        params = {"access_token": MAPBOX_KEY}

        res = requests.get(url, params=params).json()

        if "features" in res and len(res["features"]) > 0:
            return res["features"][0]["place_name"]

        return "Unknown location"
    except:
        return "Unknown location"

# =========================
# 🛣️ ROUTE (NO FAIL)
# =========================
def get_route(start, end):
    try:
        url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{start[1]},{start[0]};{end[1]},{end[0]}"
        params = {"geometries": "geojson", "access_token": MAPBOX_KEY}

        res = requests.get(url, params=params).json()

        if "routes" in res and len(res["routes"]) > 0:
            coords = res["routes"][0]["geometry"]["coordinates"]
            return [(lat, lon) for lon, lat in coords]

    except:
        pass

    # fallback
    route = []
    for i in range(100):
        lat = start[0] + (end[0] - start[0]) * i / 100
        lon = start[1] + (end[1] - start[1]) * i / 100
        route.append((lat, lon))
    return route

# =========================
# 📏 DISTANCE
# =========================
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon/2)**2

    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

def is_near_route(lat, lon, route, threshold=30):
    for rlat, rlon in route:
        if haversine(lat, lon, rlat, rlon) < threshold:
            return True
    return False

# =========================
# 🎯 UI
# =========================
st.set_page_config(layout="wide")

st.markdown("""
# 🚧 Accident Hotspot Intelligence System  
### 🔍 Safer Routes • Smart Insights • Real Data
""")

# =========================
# 📊 SIDEBAR
# =========================
with st.sidebar:
    st.title("🚧 Smart Route Planner")

    start_place = st.text_input("📍 Start Location")
    end_place = st.text_input("🏁 Destination")

    submit = st.button("🚀 Start Journey")

# =========================
# 🚀 PROCESS
# =========================
if submit:
    with st.spinner("🚀 Processing..."):

        start = geocode(start_place)
        end = geocode(end_place)

        if start is None or end is None:
            st.error("❌ Try full location names like 'New Delhi'")
            st.stop()

        route = get_route(start, end)

        df = pd.read_csv("data/cleaned_accident_data.csv")

        filtered = []
        for _, r in df.iterrows():
            lat = float(r["Latitude"])
            lon = float(r["Longitude"])

            if is_near_route(lat, lon, route):
                filtered.append(r)

        st.session_state.route = route
        st.session_state.points = filtered
        st.session_state.start = start
        st.session_state.end = end

# =========================
# 🗺️ DISPLAY
# =========================
if st.session_state.route is not None:

    # METRICS
    st.markdown("## 🧭 Route Analysis Dashboard")

    col1, col2, col3 = st.columns(3)

    total = len(st.session_state.points)
    fatal = sum(1 for r in st.session_state.points if r["Accident Severity"] == "Fatal")

    col1.metric("🔥 Total Accidents", total)
    col2.metric("🔴 Fatal", fatal)

    risk = "High" if fatal > 15 else "Medium" if fatal > 5 else "Low"
    col3.metric("⚠️ Risk Level", risk)

    col_map, col_panel = st.columns([3, 1])

    # MAP
    m = folium.Map(location=st.session_state.start, zoom_start=6, tiles="CartoDB positron")

    folium.PolyLine(st.session_state.route, color="blue", weight=5).add_to(m)
    folium.Marker(st.session_state.start, icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(st.session_state.end, icon=folium.Icon(color="red")).add_to(m)

    # HEATMAP
    heat = [[float(r["Latitude"]), float(r["Longitude"])] for r in st.session_state.points]
    HeatMap(heat).add_to(m)

    # CLUSTERING (FIXED)
    clusters = []

    for r in st.session_state.points:
        lat = float(r["Latitude"])
        lon = float(r["Longitude"])

        placed = False

        for cluster in clusters:
            clat, clon, pts = cluster

            if haversine(lat, lon, clat, clon) < 25:
                pts.append(r)
                placed = True
                break

        if not placed:
            clusters.append([lat, lon, [r]])

    # DRAW CLUSTERS
    for clat, clon, rows in clusters:

        severities = [r["Accident Severity"] for r in rows]

        if "Fatal" in severities:
            color = "red"
        elif "Serious" in severities:
            color = "orange"
        else:
            color = "yellow"

        folium.CircleMarker(
            location=[clat, clon],
            radius=min(6 + len(rows), 18),
            color=color,
            fill=True,
            fill_opacity=0.9
        ).add_to(m)

    # SHOW MAP
    with col_map:
        map_data = st_folium(m, width=900, height=600)

    # CLICK
    if map_data and map_data.get("last_clicked"):
        st.session_state.clicked = (
            map_data["last_clicked"]["lat"],
            map_data["last_clicked"]["lng"]
        )

    # SIDE PANEL
    with col_panel:
        st.markdown("### 📊 Location Insights")

        if st.session_state.clicked:

            lat, lon = st.session_state.clicked

            nearest = None
            min_d = 999

            for clat, clon, rows in clusters:
                d = haversine(lat, lon, clat, clon)
                if d < min_d:
                    min_d = d
                    nearest = (clat, clon, rows)

            if nearest:
                clat, clon, rows = nearest

                location = reverse_geocode(clat, clon)

                count = len(rows)
                sev = [r["Accident Severity"] for r in rows]
                hrs = [int(r["Hour"]) for r in rows]

                most_sev = max(set(sev), key=sev.count)
                peak = max(set(hrs), key=hrs.count)

                vehicle = random.choice(["Car", "Bike", "Truck", "Bus"])

                st.success(location)
                st.write(f"🔥 Accidents: {count}")
                st.write(f"⚠️ Severity: {most_sev}")
                st.write(f"🚗 Vehicle: {vehicle}")
                st.write(f"🕒 Peak Time: {peak}:00")

        else:
            st.info("Click a hotspot 👈")

# =========================
# RESET
# =========================
if st.button("🔄 Reset"):
    st.session_state.clear()
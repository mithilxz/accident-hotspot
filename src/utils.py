import folium

def create_map(df):

    india_map = folium.Map(location=[22.59,78.96], zoom_start=5)

    for _,row in df.iterrows():

        folium.CircleMarker(
            location=[22.59,78.96], # placeholder
            radius=5,
            popup=str(row['Hotspot Cluster']),
            color='red'
        ).add_to(india_map)

    india_map.save("hotspots.html")
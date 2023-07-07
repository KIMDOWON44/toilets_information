import streamlit as st
import pandas as pd
import folium
from streamlit.components.v1 import html

df = pd.read_csv("./data/Seoul_toilet_locations.csv", encoding="utf-8")
sampled_df = df.sample(10)

tile_seoul_map = folium.Map(location=[37.55, 126.98], zoom_start=12, tiles="Stamen Terrain")

for i in range(len(sampled_df)):
    name, latitude, longitude = sampled_df.iloc[i]
    folium.Marker([latitude, longitude], popup=name).add_to(tile_seoul_map)

st.title("Seoul Toilet Locations")

# Get user's location
user_location = st.empty()
user_latitude = None
user_longitude = None

if st.button("Get My Location"):
    user_location.text("Locating...")

    # Request user's location using the Geolocation API
    js_code = """
    navigator.geolocation.getCurrentPosition(
        function(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            const accuracy = position.coords.accuracy;

            // Update the Streamlit app with the user's location
            const location = {latitude, longitude, accuracy};
            streamlit.sessionState.location = location;
        },
        function(error) {
            console.error(error.message);
        }
    );
    """
    html("<script>{}</script>".format(js_code))

    # Wait for the user's location to be updated
    if "location" in st.session_state and st.session_state.location is not None:
        user_latitude = st.session_state.location["latitude"]
        user_longitude = st.session_state.location["longitude"]
        user_location.text("Location Found!")

if user_latitude is not None and user_longitude is not None:
    # Add user's location marker
    folium.Marker([user_latitude, user_longitude], popup="My Location", icon=folium.Icon(color='red')).add_to(tile_seoul_map)

map_html = tile_seoul_map.get_root().render()

html(map_html, height=500)
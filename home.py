import pandas as pd
import streamlit as st
from streamlit.components.v1 import html
import folium
from streamlit.components.v1 import declare_component

# JavaScript code to get the user's geolocation
geolocation_js = """
const successCallback = (position) => {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    const location = [latitude, longitude];
    window.postMessage(location);
};

const errorCallback = (error) => {
    console.error(error.message);
};

navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
"""

# Streamlit's JavaScript event listener to receive geolocation data
event_listener_js = """
window.addEventListener("message", (event) => {
    const location = event.data;
    const latitude = location[0];
    const longitude = location[1];
    const marker = L.marker([latitude, longitude], { icon: L.icon({ iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png', iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], }) }).addTo(tile_seoul_map);
});
"""

# Streamlit app code
def display_map_with_current_location():
    tile_seoul_map = folium.Map(location=[37.55, 126.98], zoom_start=12, tiles="Stamen Terrain")

    df = pd.read_csv("./data/Seoul_toilet_locations.csv", encoding="utf-8")
    sampled_df = df.sample(10)

    for i in range(len(sampled_df)):
        name, latitude, longitude = sampled_df.iloc[i]
        folium.Marker([latitude, longitude], popup=name).add_to(tile_seoul_map)

    map_html = tile_seoul_map.get_root().render()

    html("<div id='map'></div>", height=500)
    html("""
        <script src="https://cdn.jsdelivr.net/npm/leaflet@1.7.1/dist/leaflet.js"></script>
        <script>{}</script>
        <script>{}</script>
    """.format(geolocation_js, event_listener_js))
    html(map_html)

if __name__ == "__main__":
    st.title("Seoul Toilet Locations")
    display_map_with_current_location()
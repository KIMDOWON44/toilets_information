import streamlit as st
from streamlit.components.v1 import html
import folium

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
    const marker = L.marker([latitude, longitude]).addTo(tile_seoul_map);
});
"""

# Streamlit app code
def display_map_with_current_location():
    tile_seoul_map = folium.Map(location=[37.55, 126.98], zoom_start=12, tiles="Stamen Terrain")

    html("<div id='map'></div>", height=500)
    html("""
        <script src="https://cdn.jsdelivr.net/npm/leaflet@1.7.1/dist/leaflet.js"></script>
        <script>{}</script>
        <script>{}</script>
    """.format(geolocation_js, event_listener_js))

if __name__ == "__main__":
    st.title("Seoul Toilet Locations")
    display_map_with_current_location()
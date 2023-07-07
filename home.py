import streamlit as st
import pandas as pd
import folium
from streamlit.components.v1 import html

# 스마트폰의 위치 정보를 얻어오는 JavaScript 코드
geolocation_js = """
<script>
if ('geolocation' in navigator) {
    navigator.geolocation.getCurrentPosition(function(position) {
        var lat = position.coords.latitude;
        var lon = position.coords.longitude;
        var location = [lat, lon];
        window.location = location;
    });
} else {
    alert("Geolocation is not supported by this browser.");
}
</script>
"""

# 스마트폰의 위치 정보를 얻어오는 JavaScript 코드를 실행
html(geolocation_js)


df = pd.read_csv("./data/Seoul_toilet_locations.csv", encoding="utf-8")
sampled_df = df.sample(10)

tile_seoul_map = folium.Map(location=[37.55, 126.98], zoom_start=12, tiles="Stamen Terrain")

for i in range(len(sampled_df)):
    name, latitude, longitude = sampled_df.iloc[i]
    folium.Marker([latitude, longitude], popup=name).add_to(tile_seoul_map)

# 스마트폰의 위치 정보를 얻어오는 JavaScript 코드
geolocation_js = """
<script>
if ('geolocation' in navigator) {
    navigator.geolocation.getCurrentPosition(function(position) {
        var lat = position.coords.latitude;
        var lon = position.coords.longitude;
        var location = [lat, lon];
        window.location = location;
    });
} else {
    alert("Geolocation is not supported by this browser.");
}
</script>
"""

# 스마트폰의 위치 정보를 얻어오는 JavaScript 코드를 실행
html(geolocation_js)

# 사용자의 위치 정보를 얻어옴
user_location = st.session_state.get('location', None)

if user_location:
    # 사용자의 위치에 마커 추가
    folium.Marker(user_location, popup="My Location", icon=folium.Icon(color='red')).add_to(tile_seoul_map)

map_html = tile_seoul_map.get_root().render()

st.title("Seoul Toilet Locations")
html(map_html, height=500)
import streamlit as st
from streamlit.components.v1 import html
import folium
from streamlit.components.v1 import declare_component

# 스마트폰 위치정보를 가져오는 JavaScript 코드
geolocation_js = """
navigator.geolocation.getCurrentPosition(function(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    const location = [latitude, longitude];
    const event = new CustomEvent('location', { detail: location });
    document.dispatchEvent(event);
});
"""

# 스마트폰 위치를 가져오는 JavaScript 코드를 Streamlit 컴포넌트로 등록
declare_component("geolocation", url="http://localhost:3001", js_code=geolocation_js)

# 스마트폰 위치를 받아오는 Streamlit 컴포넌트를 사용하여 지도에 마커 표시
def display_map_with_current_location():
    tile_seoul_map = folium.Map(location=[37.55, 126.98], zoom_start=12, tiles="Stamen Terrain")

    # 스마트폰 위치를 받아오는 JavaScript 이벤트 리스너
    js_code = """
    document.addEventListener("location", function(event) {
        const location = event.detail;
        const latitude = location[0];
        const longitude = location[1];
        const marker = L.marker([latitude, longitude]).addTo(tile_seoul_map);
    });
    """

    html("<div id='map'></div>", height=500)
    html("""
        <script src="https://cdn.jsdelivr.net/npm/leaflet@1.7.1/dist/leaflet.js"></script>
        <script>{}</script>
    """.format(js_code))

# Streamlit 앱 실행
if __name__ == "__main__":
    st.title("Seoul Toilet Locations")
    display_map_with_current_location()
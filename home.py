import streamlit as st
import pandas as pd
from streamlit.components.v1 import html
import folium
from geopy.geocoders import Nominatim
import requests


def get_gps_location():
    geolocator = Nominatim(user_agent='my-application')
    location = geolocator.geocode('')

    if location:
        return location.latitude, location.longitude
    else:
        return None, None


def get_ip_location():
    response = requests.get('http://ip-api.com/json')
    data = response.json()

    if data['status'] == 'success':
        return data['lat'], data['lon']
    else:
        return None, None


df = pd.read_csv("./data/Seoul_toilet_locations.csv", encoding="utf-8")
sampled_df = df.sample(10)

# GPS 기반 위치 가져오기
latitude, longitude = get_gps_location()

# GPS 정보가 없는 경우 IP 기반 위치 가져오기
if latitude is None or longitude is None:
    latitude, longitude = get_ip_location()

# folium 지도 생성
tile_seoul_map = folium.Map(location=[37.55, 126.98], zoom_start=12, tiles="Stamen Terrain")

for i in range(len(sampled_df)):
    name, lat, lon = sampled_df.iloc[i]
    folium.Marker([lat, lon], popup=name).add_to(tile_seoul_map)

# 위치 마커 추가
folium.Marker([latitude, longitude], popup='내 위치', icon=folium.Icon(color='blue', icon='cloud')).add_to(tile_seoul_map)

map_html = tile_seoul_map.get_root().render()

st.title("Seoul Toilet Locations")
html(map_html, height=500)
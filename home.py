import streamlit as st
import pandas as pd
from streamlit.components.v1 import html
import folium

df = pd.read_csv("./data/Seoul_toilet_locations.csv", encoding="utf-8")

sampled_df = df.sample(10)

tile_seoul_map = folium.Map(location=[37.55, 126.98], zoom_start=12, tiles="Stamen Terrain")

for i in range(len(sampled_df)):
    name, latitude, longitude = sampled_df.iloc[i]
    folium.Marker([latitude, longitude], popup=name).add_to(tile_seoul_map)

map_html = tile_seoul_map.get_root().render()

st.title("Seoul Toilet Locations")
html(map_html, height=500)
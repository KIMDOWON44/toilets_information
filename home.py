import streamlit as st
import pandas as pd
import requests

df = pd.read_csv("./data/Seoul_toilet_locations.csv", encoding="utf-8")
sampled_df = df.sample(10)

kakao_api_key = "KAKAOMAP_API"  # Replace with your Kakao Maps API key
kakao_map_url = "https://dapi.kakao.com/v2/maps/staticmap"
map_params = {
    "center": "126.98,37.55",
    "level": "3",
    "width": "800",
    "height": "500",
    "markers": "size:mid|color:red|" + "|".join(f"{row['longitude']},{row['latitude']}" for _, row in sampled_df.iterrows()),
    "key": kakao_api_key
}

response = requests.get(kakao_map_url, params=map_params)

st.title("Seoul Toilet Locations")

# Get user's location
user_location = st.empty()
user_latitude = None
user_longitude = None

if st.button("Get My Location"):
    user_location.text("Locating...")
    user_latitude = 37.2113408  # Replace with actual latitude
    user_longitude = 127.0611968  # Replace with actual longitude
    user_location.text("Location Found!")

if user_latitude is not None and user_longitude is not None:
    # Append user's location to the marker list
    map_params["markers"] += f"|{user_longitude},{user_latitude}"
    response = requests.get(kakao_map_url, params=map_params)

if response.status_code == 200:
    st.image(response.content, width=800)
else:
    st.error("Failed to retrieve the map image.")

content_type = response.headers.get('Content-Type')
if content_type and content_type.startswith('image/'):
    st.image(response.content, width=800)
else:
    st.error("The response is not a valid image.")
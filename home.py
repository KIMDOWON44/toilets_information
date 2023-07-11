import streamlit as st
import pandas as pd
from streamlit.components.v1 import html

df = pd.read_csv("./data/Seoul_toilet_locations.csv", encoding="utf-8")
sampled_df = df.sample(10)

# Create a template for the Kakao Maps API
kakao_template = """
<div id="map" style="width: 100%; height: 500px;"></div>
<script type="text/javascript" src="https://dapi.kakao.com/v2/maps/sdk.js?appkey=CACAOMAP_API"></script>
<script>
    const mapOptions = {{
        center: new kakao.maps.LatLng({center_latitude}, {center_longitude}),
        level: 12
    }};
    const map = new kakao.maps.Map(document.getElementById('map'), mapOptions);

    // Add markers to the map
    {marker_script}
</script>
"""

# Generate the marker script
marker_script = ""
for _, row in sampled_df.iterrows():
    name, latitude, longitude = row
    marker_script += f"""
    const marker = new kakao.maps.Marker({{
        position: new kakao.maps.LatLng({latitude}, {longitude}),
        map: map
    }});
    const infowindow = new kakao.maps.InfoWindow({{ content: '{name}' }});
    kakao.maps.event.addListener(marker, 'click', function() {{
        infowindow.open(map, marker);
    }});
    """

# Insert the marker script and center coordinates into the template
kakao_html = kakao_template.format(
    center_latitude=37.55,  # Replace with actual center latitude
    center_longitude=126.98,  # Replace with actual center longitude
    marker_script=marker_script
)

st.title("Seoul Toilet Locations")

# Display the Kakao Maps HTML using the `html` component
html(kakao_html)
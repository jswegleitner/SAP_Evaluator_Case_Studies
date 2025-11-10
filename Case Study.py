# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 12:46:22 2025

@author: jwegleitner
"""

import folium
from folium import IFrame

# Create base map
m = folium.Map(location=[37.7749, -122.4194], zoom_start=15)

# Add default OpenStreetMap layer (already included)
# Add satellite layer (ESRI World Imagery)
folium.TileLayer('OpenStreetMap').add_to(m)
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri Satellite',
    overlay=False,
    control=True
).add_to(m)

# Add Layer Control
folium.LayerControl().add_to(m)


# Example damage locations with image URLs
damage_sites = [
    {
        "name": "Building A",
        "location": [37.7750, -122.4183],
        "image_url": "https://example.com/image1.jpg"
    },
    {
        "name": "Building B",
        "location": [37.7740, -122.4200],
        "image_url": "https://example.com/image2.jpg"
    },
    {
        "name": "Building C",
        "location": [37.791187516917894, -122.44426156272114],
        "image_url": "https://drive.google.com/uc?export=view&id=1xKPpqjvONfL_e7hJnsweIWNDeM5oaf2E"
    }
]

# Add markers with image popups
for site in damage_sites:
    html = f"""<h4>{site['name']}</h4>
<imge["""
    
    iframe = IFrame(html, width=340, height=360)
    popup = folium.Popup(iframe, max_width=500)
    folium.Marker(location=site["location"], popup=popup).add_to(m)

# Save to HTML
m.save("sap_case_study_map.html")
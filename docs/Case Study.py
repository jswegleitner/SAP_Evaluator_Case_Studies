# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 12:46:22 2025

@author: jwegleitner
"""

import folium
from folium import IFrame
# (Removed URL-checking and auto-fix imports — using hosted Pages URLs or local paths directly)

# Create base map
m = folium.Map(location=[37.7749, -122.4194], zoom_start=14)

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
        "image_url":[
            "https://jswegleitner.github.io/sap-case-study/images/IMG_0944.JPG",
            "https://jswegleitner.github.io/sap-case-study/images/IMG_0945.JPG",
            "https://jswegleitner.github.io/sap-case-study/images/IMG_0946.JPG",
            "https://jswegleitner.github.io/sap-case-study/images/IMG_0948.JPG"
        ]

    }
]

# Add markers with image popups


for idx, site in enumerate(damage_sites):
    # Create unique carousel id per site
    carousel_id = f"carousel{idx}"

    # If multiple images, build a Bootstrap carousel inside the popup iframe
    if isinstance(site["image_url"], list):
        indicators = []
        items = []
        for i, img in enumerate(site["image_url"]):
            indicators.append(
                f'<button type="button" data-bs-target="#{carousel_id}" data-bs-slide-to="{i}" '
                + ("class=\"active\" aria-current=\"true\"" if i == 0 else "")
                + f' aria-label="Slide {i+1}"></button>'
            )
            item_class = "carousel-item active" if i == 0 else "carousel-item"
            items.append(
                f'<div class="{item_class}">'
                f'<img src="{img}" class="d-block w-100" style="max-height:300px; object-fit:contain;">'
                f'</div>'
            )

        carousel_html = (
            # Include Bootstrap 5 CSS/JS via CDN inside the iframe. This is scoped to the iframe content.
            f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">'
            f'<div id="{carousel_id}" class="carousel slide" data-bs-ride="carousel">'
            f'<div class="carousel-indicators">{"".join(indicators)}</div>'
            f'<div class="carousel-inner">{"".join(items)}</div>'
            f'<button class="carousel-control-prev" type="button" data-bs-target="#' + carousel_id + '" data-bs-slide="prev">'
            f'<span class="carousel-control-prev-icon" aria-hidden="true"></span>'
            f'<span class="visually-hidden">Previous</span>'
            f'</button>'
            f'<button class="carousel-control-next" type="button" data-bs-target="#' + carousel_id + '" data-bs-slide="next">'
            f'<span class="carousel-control-next-icon" aria-hidden="true"></span>'
            f'<span class="visually-hidden">Next</span>'
            f'</button>'
            # Bootstrap JS bundle for carousel functionality
            f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>'
        )

        iframe = IFrame(f"<h4>{site['name']}</h4>" + carousel_html, width=420, height=360)

    else:
        # Single image: simple img tag (assumed correct hosted URL or local relative path)
        img = site.get("image_url")
        images_html = f'<img src="{img}" style="max-width:300px;"><br>'
        iframe = IFrame(f"<h4>{site['name']}</h4>" + images_html, width=340, height=240)

    popup = folium.Popup(iframe, max_width=600)
    folium.Marker(location=site["location"], popup=popup).add_to(m)



# Save to HTML
m.save("sap_case_study_map.html")
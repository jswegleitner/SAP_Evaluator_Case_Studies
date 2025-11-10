# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 12:46:22 2025

@author: jwegleitner
"""

import folium
from folium import IFrame
import urllib.request
import urllib.error
from urllib.parse import urlparse

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

    # Helper: check URL exists (HEAD request)
    def url_exists(url, timeout=6):
        try:
            req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status == 200
        except Exception:
            return False

    # Try automatic URL fixes for common GitHub raw URL problems
    def try_fix_url(url):
        # Known repo/owner from this project (used for automated fixes)
        owner = 'jswegleitner'
        repo_name = 'sap-case-study'

        parsed = urlparse(url)
        # Only attempt fixes for raw.githubusercontent URLs
        if 'raw.githubusercontent.com' in parsed.netloc:
            path_parts = parsed.path.lstrip('/').split('/')
            if len(path_parts) >= 4:
                user = path_parts[0]
                repo = path_parts[1]
                branch = path_parts[2]
                rest = '/'.join(path_parts[3:])

                candidates = []
                # Try swapping username to the repo owner if they differ
                if user != owner:
                    candidates.append(f'https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{rest}')
                # Try swapping branch main<->master
                swap_branch = 'main' if branch != 'main' else 'master'
                candidates.append(f'https://raw.githubusercontent.com/{user}/{repo}/{swap_branch}/{rest}')
                if user != owner:
                    candidates.append(f'https://raw.githubusercontent.com/{owner}/{repo}/{swap_branch}/{rest}')
                # Try GitHub Pages URL for the repo
                candidates.append(f'https://{owner}.github.io/{repo}/{rest}')
                # Try raw.githack.com proxy (helps with CORS sometimes)
                candidates.append(f'https://raw.githack.com/{user}/{repo}/{branch}/{rest}')

                for c in candidates:
                    if url_exists(c):
                        print(f"Auto-fixed image URL:\n  from: {url}\n  to:   {c}")
                        return c

        # Not fixed
        return None

    # Normalize and validate image URLs for the current site
    def resolve_image_url(img_url):
        if url_exists(img_url):
            return img_url
        fixed = try_fix_url(img_url)
        if fixed:
            return fixed
        # fallback placeholder
        print(f'Image not reachable, using placeholder: {img_url}')
        return 'https://via.placeholder.com/320x240.png?text=Image+not+found'

    # If multiple images, build a Bootstrap carousel inside the popup iframe
    if isinstance(site["image_url"], list):
        # Build carousel indicators and items
        indicators = []
        items = []
        for i, img in enumerate(site["image_url"]):
            # resolve each image URL (auto-fix or placeholder)
            img = resolve_image_url(img)
            indicators.append(f'<button type="button" data-bs-target="#' + carousel_id + f'" data-bs-slide-to="{i}" '
                              + ("class=\"active\" aria-current=\"true\"" if i == 0 else "")
                              + f' aria-label="Slide {i+1}"></button>')
            item_class = "carousel-item active" if i == 0 else "carousel-item"
            items.append(f'<div class="{item_class}">'
                         f'<img src="{img}" class="d-block w-100" style="max-height:300px; object-fit:contain;">'
                         f'</div>')

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

        images_html = carousel_html
        # Slightly larger iframe for carousel
        iframe = IFrame(f"<h4>{site['name']}</h4>" + images_html, width=420, height=360)

    else:
        # Single image: simple img tag
        img = resolve_image_url(site["image_url"]) if isinstance(site.get("image_url"), str) else 'https://via.placeholder.com/320x240.png?text=Image+not+found'
        images_html = f'<img src="{img}" style="max-width:300px;"><br>'
        iframe = IFrame(f"<h4>{site['name']}</h4>" + images_html, width=340, height=240)

    popup = folium.Popup(iframe, max_width=600)
    folium.Marker(location=site["location"], popup=popup).add_to(m)



# Save to HTML
m.save("sap_case_study_map.html")
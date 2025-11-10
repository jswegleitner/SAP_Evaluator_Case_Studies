# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 12:46:22 2025

@author: jwegleitner
"""

"""Case Study map generator

This file was restored to a clean, stable state. It generates a folium map with:
- Bootstrap carousels for sites with multiple images (click-only, no auto-rotate)
- Black carousel arrows via injected CSS
- Marker popups containing color-change buttons and an "Open Form" button that opens
    a shared inspection PDF in a Bootstrap modal with a small HTML form saved per-site in localStorage.

Notes:
- The inspection PDF is expected at `docs/inspection_form.pdf`. Change `INSPECTION_PDF_URL` below if needed.
"""

import folium
from folium import IFrame

# Configuration
INSPECTION_PDF_URL = "inspection_form.pdf"  # relative to the served site (docs/ when using Pages)

# Create base map
m = folium.Map(location=[37.7749, -122.4194], zoom_start=14)

# Add base layers
folium.TileLayer('OpenStreetMap').add_to(m)
folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri Satellite',
        overlay=False,
        control=True
).add_to(m)
folium.LayerControl().add_to(m)

# Define sites (use your Pages-hosted image URLs or local relative paths)
damage_sites = [
        {
                "name": "Building A",
                "location": [37.78882458093672, -122.39127790986115],
                "image_url": "https://jswegleitner.github.io/SAP_Evaluator_Case_Studies/images/375-Beale-St-San-Francisco-CA-Primary-Photo-1-Large.jpg"
        },
        {
                "name": "Building B",
                "location": [37.779569006965744, -122.41922021805215],
                "image_url": "https://jswegleitner.github.io/SAP_Evaluator_Case_Studies/images/San_Francisco_City_Hall_1906-04-20.jpg"
        },
        {
                "name": "Building C",
                "location": [37.791187516917894, -122.44426156272114],
                "image_url": [
                        "https://jswegleitner.github.io/SAP_Evaluator_Case_Studies/images/IMG_0944.JPG",
                        "https://jswegleitner.github.io/SAP_Evaluator_Case_Studies/images/IMG_0945.JPG",
                        "https://jswegleitner.github.io/SAP_Evaluator_Case_Studies/images/IMG_0946.JPG",
                        "https://jswegleitner.github.io/SAP_Evaluator_Case_Studies/images/IMG_0948.JPG",
                ],
        },
]

# Build markers/popups
for idx, site in enumerate(damage_sites):
        carousel_id = f"carousel{idx}"

        if isinstance(site.get("image_url"), list):
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
                                f'<div class="{item_class}">' +
                                f'<img src="{img}" class="d-block w-100" style="max-height:360px; object-fit:contain;">' +
                                '</div>'
                        )

                carousel_html = (
                        f'<div id="{carousel_id}" class="carousel slide" data-bs-interval="false" data-bs-touch="false">'
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
                        f'</div>'
                )

                popup_html = f"<h4>{site['name']}</h4>" + carousel_html

        else:
                img = site.get("image_url")
                popup_html = f"<h4>{site['name']}</h4><img src=\"{img}\" style=\"max-width:420px;\"><br>"

        # Add marker color buttons and Open Form button
        popup_html += (
                '<div class="mt-2">'
                '<button class="btn btn-sm btn-outline-dark mark-btn" data-color="red">Mark Red</button> '
                '<button class="btn btn-sm btn-outline-dark mark-btn" data-color="yellow">Mark Yellow</button> '
                '<button class="btn btn-sm btn-outline-dark mark-btn" data-color="green">Mark Green</button> '
                f'<button class="btn btn-sm btn-primary" onclick="openInspectionForm({idx})">Open Form</button>'
                '</div>'
        )

        html_obj = folium.Html(popup_html, script=True)
        popup = folium.Popup(html_obj, max_width=650)
        folium.Marker(location=site["location"], popup=popup).add_to(m)


# Inject global assets and scripts (Bootstrap, FontAwesome) and custom styles/scripts
assets = '''
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
'''

m.get_root().html.add_child(folium.Element('{% raw %}' + assets + '{% endraw %}'))

# Black carousel arrows
css = '''
<style>
.carousel-control-prev-icon, .carousel-control-next-icon {
        background-image: url("data:image/svg+xml;charset=UTF-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath fill='%23000' d='M11.354 1.646a.5.5 0 0 1 .707.708L6.707 8l5.354 5.646a.5.5 0 0 1-.707.708l-6-6a.5.5 0 0 1 0-.708l6-6z'/%3E%3C/svg%3E");
        width: 1.6rem; height: 1.6rem; background-size: 100% 100%;
}
.carousel-control-next-icon { transform: rotate(180deg); }
.custom-div-icon { background: transparent; }
</style>
'''

m.get_root().html.add_child(folium.Element('{% raw %}' + css + '{% endraw %}'))

# JS: wait for map object, wire popup button handlers, and provide color-change + modal form
script = '''
<script>
(function(){
    function findMap(){
        for(var k in window){{ if(k.indexOf('map_')===0 && window[k] && typeof window[k].on === 'function') return window[k]; }}
        return null;
    }

    function init(){
        var map = findMap();
        if(!map){{ setTimeout(init, 100); return; }}

        function changeMarkerColor(marker, color){
            try{
                var cssColor = color === 'yellow' ? '#f0ad4e' : (color === 'red' ? '#d9534f' : (color === 'green' ? '#5cb85c' : color));
                var html = '<i class="fa fa-map-marker" style="color: ' + cssColor + '; font-size: 28px; text-shadow: 0 0 2px rgba(0,0,0,0.6);"></i>';
                var icon = L.divIcon({className:'custom-div-icon', html: html, iconSize:[28,28], iconAnchor:[14,28]});
                try{ marker.setIcon(icon); }catch(e){}
                try{
                    if(marker.__coloredMarker && marker.__coloredMarker.setIcon){ marker.__coloredMarker.setIcon(icon); }
                    else { var colored = L.marker(marker.getLatLng(), {icon:icon, interactive:false}); colored.addTo(map); marker.__coloredMarker = colored; }
                    if(marker.setOpacity) marker.setOpacity(0);
                }catch(e){}
            }catch(e){ console.warn('changeMarkerColor failed', e); }
        }

        window.changeMarkerColorByPopup = function(btn, color){
            try{
                var popupEl = btn.closest('.leaflet-popup'); if(!popupEl) return;
                var target = null;
                for(var id in map._layers){ var layer = map._layers[id]; if(layer && layer._popup && layer._popup._container === popupEl){ target = layer; break; } }
                if(target) changeMarkerColor(target, color);
            }catch(e){ console.warn(e); }
        };

        map.on('popupopen', function(e){
            var marker = e.popup._source; var popupEl = e.popup.getElement(); if(!popupEl) return;
            var btns = popupEl.querySelectorAll('.mark-btn'); btns.forEach(function(b){ if(b._h) return; b._h = true; b.addEventListener('click', function(){ var c = this.getAttribute('data-color'); changeMarkerColor(marker, c); }); });
        });
    }

    if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
</script>
'''

m.get_root().html.add_child(folium.Element('{% raw %}' + script + '{% endraw %}'))

# Modal + form for inspection (uses INSPECTION_PDF_URL variable on client side)
modal_and_form = '''
<div class="modal fade" id="inspectionModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-xl modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Inspection Form - <span id="inspectionTitle"></span></h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body" style="height:75vh;">
                <div class="row h-100">
                    <div class="col-md-7 h-100">
                        <iframe id="inspectionPdfFrame" src="{INSPECTION_PDF_URL}" style="width:100%; height:100%; border:1px solid #ddd;"></iframe>
                    </div>
                    <div class="col-md-5 h-100" style="overflow:auto;">
                        <form id="inspectionForm" style="padding-bottom:1rem;">
                            <div class="mb-2">
                                <label class="form-label">Inspector</label>
                                <input class="form-control" id="inspectorName" />
                            </div>
                            <div class="mb-2">
                                <label class="form-label">Date</label>
                                <input type="date" class="form-control" id="inspectionDate" />
                            </div>
                            <div class="mb-2">
                                <label class="form-label">Severity</label>
                                <select id="inspectionSeverity" class="form-select">
                                    <option value="low">Low</option>
                                    <option value="medium">Medium</option>
                                    <option value="high">High</option>
                                </select>
                            </div>
                            <div class="mb-2">
                                <label class="form-label">Notes</label>
                                <textarea id="inspectionNotes" class="form-control" rows="6"></textarea>
                            </div>
                            <div class="d-flex gap-2">
                                <button type="button" class="btn btn-primary" id="saveInspectionBtn">Save</button>
                                <button type="button" class="btn btn-secondary" id="downloadInspectionBtn">Download JSON</button>
                                <button type="button" class="btn btn-outline-secondary" id="clearInspectionBtn">Clear</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
function openInspectionForm(siteId){
    document.getElementById('inspectionTitle').textContent = 'Site ' + siteId;
    var key = 'inspection_' + siteId; var data = localStorage.getItem(key); if(data){ try{ data = JSON.parse(data);}catch(e){data=null;} }
    document.getElementById('inspectorName').value = data && data.inspector ? data.inspector : '';
    document.getElementById('inspectionDate').value = data && data.date ? data.date : '';
    document.getElementById('inspectionSeverity').value = data && data.severity ? data.severity : 'low';
    document.getElementById('inspectionNotes').value = data && data.notes ? data.notes : '';
    document.getElementById('inspectionPdfFrame').src = '{INSPECTION_PDF_URL}' + '?_t=' + Date.now();
    document.getElementById('saveInspectionBtn').onclick = function(){ var payload = {inspector:document.getElementById('inspectorName').value, date:document.getElementById('inspectionDate').value, severity:document.getElementById('inspectionSeverity').value, notes:document.getElementById('inspectionNotes').value}; localStorage.setItem(key, JSON.stringify(payload)); this.textContent='Saved'; var btn=this; setTimeout(function(){btn.textContent='Save';},1200); };
    document.getElementById('downloadInspectionBtn').onclick = function(){ var saved = localStorage.getItem(key)||'{}'; var blob=new Blob([saved],{type:'application/json'}); var url=URL.createObjectURL(blob); var a=document.createElement('a'); a.href=url; a.download='inspection_site_'+siteId+'.json'; document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url); };
    document.getElementById('clearInspectionBtn').onclick = function(){ if(confirm('Clear saved inspection for site '+siteId+'?')){ localStorage.removeItem(key); document.getElementById('inspectorName').value=''; document.getElementById('inspectionDate').value=''; document.getElementById('inspectionSeverity').value='low'; document.getElementById('inspectionNotes').value=''; } };
    var modal = new bootstrap.Modal(document.getElementById('inspectionModal')); modal.show();
}
</script>
'''

# Replace placeholder with configured PDF URL (safe, avoids f-string brace issues)
modal_and_form = modal_and_form.replace('{INSPECTION_PDF_URL}', INSPECTION_PDF_URL)
m.get_root().html.add_child(folium.Element('{% raw %}' + modal_and_form + '{% endraw %}'))

# Save final HTML
m.save("sap_case_study_map.html")
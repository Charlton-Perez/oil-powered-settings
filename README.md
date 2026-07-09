# Oil-Powered Settings in England

Interactive map dashboard of oil-heated education settings in England, merged with
[Get Information About Schools](https://get-information-schools.service.gov.uk/) (GIAS)
records and Sustainability Support Programme (SSP) engagement data.

- Pan/zoom Leaflet map; each dot is a setting (green = engaged with at least one SSP programme, orange = not engaged)
- Filter by English government region (listed north to south), phase of education, heating type (oil only / oil + gas), and SSP engagement
- Sortable table of the filtered settings (setting, LA, phase, pupils, FSM%, SSP programme count); click a row to zoom to it on the map
- Click a dot for full details: contacts, pupil numbers, FSM%, trust, address, and per-programme SSP engagement (Climate Ambassadors, Let's Go Zero, Nature Park, NZAP/GBESP, Sustainability Support)

## Files

- `index.html` — the dashboard (static, Leaflet from CDN)
- `data.js` — merged dataset consumed by the page
- `build_data.py` — regenerates `data.js` from the SSP Excel extract and a GIAS full extract CSV (paths at the top of the script; requires `openpyxl` and `pyproj`)

## Data notes

- Closed settings in the SSP list are mapped to their successor URN in GIAS; the popup notes the original URN
- Coordinates converted from OS National Grid (Easting/Northing, EPSG:27700) to WGS84
- Region comes from the GIAS GOR field; phase from GIAS, falling back to the SSP list where GIAS says "Not applicable"

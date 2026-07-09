# Oil-Powered Schools in England

Interactive map dashboard of oil-heated schools in England, merged with
[Get Information About Schools](https://get-information-schools.service.gov.uk/) (GIAS)
records and Sustainability Support Programme (SSP) engagement data.

- Pan/zoom Leaflet map; each dot is a school (green = engaged with at least one SSP programme, orange = not engaged)
- Filter by English government region, phase of education, heating type (oil only / oil + gas), and SSP engagement
- Click a dot for full details: contacts, pupil numbers, FSM%, trust, address, and per-programme SSP engagement (Climate Ambassadors, Let's Go Zero, Nature Park, NZAP/GBESP, Sustainability Support)

## Files

- `index.html` — the dashboard (static, Leaflet from CDN)
- `data.js` — merged dataset consumed by the page
- `build_data.py` — regenerates `data.js` from the SSP Excel extract and a GIAS full extract CSV (paths at the top of the script; requires `openpyxl` and `pyproj`)

## Data notes

- Closed schools in the SSP list are mapped to their successor URN in GIAS; the popup notes the original URN
- Coordinates converted from OS National Grid (Easting/Northing, EPSG:27700) to WGS84
- Region comes from the GIAS GOR field; phase from GIAS, falling back to the SSP list where GIAS says "Not applicable"

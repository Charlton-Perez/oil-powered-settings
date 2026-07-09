#!/usr/bin/env python3
"""Merge the oil-powered schools SSP list with GIAS (Get Information About Schools)
and emit data.js for the dashboard map."""
import csv
import json
import sys

import openpyxl
from pyproj import Transformer

XLSX = "/Users/sws05ajc/Library/CloudStorage/OneDrive-UniversityofReading/CA National Project Coordination/National Project Coordination/oil_powered_schools/Oil School x SSP May Data (3).xlsx"
GIAS = "/Users/sws05ajc/Library/CloudStorage/OneDrive-UniversityofReading/dashboards/heatwave-school-closures/data/raw/edubasealldata20260705.csv"
OUT = "/Users/sws05ajc/Library/CloudStorage/OneDrive-UniversityofReading/dashboards/oil-schools/data.js"


def num(v):
    """SSP engagement cells hold ints or '#N/A' strings."""
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def main():
    wb = openpyxl.load_workbook(XLSX, read_only=True)
    ws = wb["Original List"]
    rows = list(ws.iter_rows(min_row=2, values_only=True))

    oil = {}  # effective GIAS URN -> ssp record
    for r in rows:
        urn = str(r[0]).strip()
        status, link_urn, link_name, link_type = r[1], r[2], r[3], r[4]
        # Closed schools point at their successor URN in GIAS
        effective = urn
        if link_type and str(link_type).startswith("Successor") and link_urn:
            effective = str(link_urn).strip()
        oil[effective] = {
            "urn": urn,
            "sspStatus": status,
            "linkName": link_name if link_type and str(link_type).startswith("Successor") else None,
            "heat": r[5],
            "phase": r[6],
            "region": r[7],
            "sisters": num(r[9]),
            "ca": num(r[10]),
            "lgz": num(r[11]),
            "np": num(r[12]),
            "nzap": num(r[13]),
            "ss": num(r[14]),
        }

    schools = []
    tf = Transformer.from_crs("EPSG:27700", "EPSG:4326", always_xy=True)
    matched = set()
    with open(GIAS, encoding="cp1252", newline="") as f:
        for row in csv.DictReader(f):
            urn = row["URN"].strip()
            if urn not in oil:
                continue
            matched.add(urn)
            s = oil[urn]
            lat = lon = None
            if row["Easting"] and row["Northing"]:
                lon, lat = tf.transform(float(row["Easting"]), float(row["Northing"]))
                lat, lon = round(lat, 5), round(lon, 5)
            head = " ".join(x for x in (row["HeadTitle (name)"], row["HeadFirstName"], row["HeadLastName"]) if x)
            address = ", ".join(x for x in (row["Street"], row["Locality"], row["Town"], row["Postcode"]) if x)
            schools.append({
                "urn": urn,
                "origUrn": s["urn"] if s["urn"] != urn else None,
                "name": row["EstablishmentName"],
                "lat": lat, "lon": lon,
                "region": row["GOR (name)"] or s["region"],
                "la": row["LA (name)"],
                "status": row["EstablishmentStatus (name)"],
                "type": row["TypeOfEstablishment (name)"],
                "phase": (row["PhaseOfEducation (name)"] not in ("", "Not applicable") and row["PhaseOfEducation (name)"]) or s["phase"],
                "heat": s["heat"],
                "pupils": row["NumberOfPupils"] or None,
                "capacity": row["SchoolCapacity"] or None,
                "fsm": row["PercentageFSM"] or None,
                "ages": f'{row["StatutoryLowAge"]}-{row["StatutoryHighAge"]}' if row["StatutoryLowAge"] else None,
                "address": address,
                "phone": row["TelephoneNum"] or None,
                "website": row["SchoolWebsite"] or None,
                "head": head or None,
                "headRole": row["HeadPreferredJobTitle"] or None,
                "trust": row["Trusts (name)"] or None,
                "sisters": s["sisters"], "ca": s["ca"], "lgz": s["lgz"],
                "np": s["np"], "nzap": s["nzap"], "ss": s["ss"],
            })

    missing = set(oil) - matched
    no_coords = sum(1 for s in schools if s["lat"] is None)
    print(f"oil list: {len(oil)} | matched in GIAS: {len(schools)} | unmatched: {len(missing)} | no coords: {no_coords}")
    if missing:
        print("unmatched URNs:", sorted(missing)[:20], file=sys.stderr)

    with open(OUT, "w") as f:
        f.write("const SCHOOLS = ")
        json.dump(schools, f, separators=(",", ":"))
        f.write(";\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

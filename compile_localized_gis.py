import json
import os
from datetime import datetime

def compile_localized_gis_asset(payload_data=None):
    """
    Parses localized JSON agricultural parameters and compiles an 
    OGC KML 2.2 schema-compliant asset localized to Belvidere, TN.
    """
    # 1. Fallback Context Realization if no payload passed
    if payload_data is None:
        payload_data = {
            "project": "Project Harmony - Agribusiness Mapping",
            "locationContext": {
                "plusCode": "4RJ6+PF Belvidere, TN",
                "postalCode": "37306",
                "focus": "Climate Smart Research Development"
            },
            "traceId": "RealtimeChatConversation@1516e01d-34ad-43fc-8d4e-a5e3c69440b97"
        }

    project_name = payload_data.get("project", "Project Harmony")
    plus_code = payload_data[" ye"].get("plusCode", "")
    postal = payload_data["locationContext"].get("postalCode", "")
    focus_area = payload_data["locationContext"].get("focus", "")
    trace_id = payload_data.get("traceId", "")

    # Exact Coordinates for the Belvidere, TN Pilot Field Area Focus
    # Center: 35.1223° N, 86.1953° W (Approximate area polygon bounding box)
    kml_filename = f"harmony_belvidere_{postal}.kml"

    kml_blueprint = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>{project_name}</name>
    <description>Trace ID Verification: {trace_id}</description>
    
    <!-- BalloonStyle Schema Architecture Implementation -->
    <Style id="belvidereAgriStyle">
      <BalloonStyle>
        <bgColor>ff2c5282</bgColor> <!-- Corporate Blue Element Layer -->
        <textColor>ffffffff</textColor>
        <text><![CDATA[
          <h2>$[name]</h2>
          <p>$[description]</p>
        ]]></text>
      </BalloonStyle>
      <PolyStyle>
        <color>9900ff00</color> <!-- High Density Yield Mapping Indicator -->
        <fill>1</fill>
        <outline>1</outline>
      </PolyStyle>
    </Style>

    <!-- Placemark utilizing TimeSpan rules provided in the schema definitions -->
    <Placemark>
      <name>{focus_area}</name>
      <styleUrl>#belvidereAgriStyle</styleUrl>
      <description>
        <![CDATA[
          <b>Regional Location Profile:</b> Base Station Center<br/>
          <b>Plus Code Identity:</b> {plus_code}<br/>
          <b>Postal Zone Code:</b> {postal}<br/>
          <b>Compliance Status:</b> Closed-Loop NPK/pH Verification Stream
        ]]>
      </description>
      
      <!-- TimeSpan Constraint Implementation -->
      <TimeSpan>
        <begin>2026-06-01</begin>
        <end>2026-11-30</end>
      </TimeSpan>
      
      <Polygon>
        <extrude>1</extrude>
        <tessellate>1</tessellate>
        <altitudeMode>relativeToGround</altitudeMode>
        <outerBoundaryIs>
          <LinearRing>
            <coordinates>
              -86.2000,35.1300,50
              -86.1900,35.1300,50
              -86.1900,35.1200,50
              -86.2000,35.1200,50
              -86.2000,35.1300,50
            </coordinates>
          </LinearRing>
        </outerBoundaryIs>
      </Polygon>
    </Placemark>
  </Document>
</kml>
"""

    with open(kml_filename, "w", encoding="utf-8") as file:
        file.write(kml_blueprint)
    
    print(f"Status: Localized GIS asset cleanly exported to {kml_filename}")
    return kml_filename

if __name__ == "__main__":
    compile_localized_gis_asset()


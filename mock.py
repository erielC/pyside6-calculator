<mxfile host="app.diagrams.net" modified="2024-01-02T12:00:00.000Z" agent="Manual" version="22.1.16">
  <diagram id="bess-architecture" name="BESS System">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1400" pageHeight="2000">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <mxCell id="2" value="BESS MONITORING SYSTEM ARCHITECTURE" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=24;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="400" y="40" width="600" height="40" as="geometry"/>
        </mxCell>
        
        <mxCell id="3" value="LAYER 1: EDGE DEVICES" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=14;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="80" y="120" width="1240" height="40" as="geometry"/>
        </mxCell>
        
        <mxCell id="4" value="CA-Site-001&lt;br&gt;&lt;br&gt;Modbus TCP/IP&lt;br&gt;BMS Sensors" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="120" y="200" width="140" height="80" as="geometry"/>
        </mxCell>
        
        <mxCell id="5" value="TX-Site-002&lt;br&gt;&lt;br&gt;Modbus TCP/IP&lt;br&gt;BMS Sensors" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="300" y="200" width="140" height="80" as="geometry"/>
        </mxCell>
        
        <mxCell id="6" value="NY-Site-003&lt;br&gt;&lt;br&gt;Modbus TCP/IP&lt;br&gt;BMS Sensors" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="480" y="200" width="140" height="80" as="geometry"/>
        </mxCell>
        
        <mxCell id="7" value="... 100+ Sites" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="660" y="225" width="120" height="30" as="geometry"/>
        </mxCell>
        
        <mxCell id="8" value="Data every 5 seconds&lt;br&gt;HTTPS/MQTT" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="1000" y="200" width="200" height="80" as="geometry"/>
        </mxCell>
        
        <mxCell id="9" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#82b366;" edge="1" parent="1" source="8" target="10">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="10" value="LAYER 2: DATA INGESTION" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=14;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="80" y="360" width="1240" height="40" as="geometry"/>
        </mxCell>
        
        <mxCell id="11" value="Azure IoT Hub&lt;br&gt;&lt;br&gt;• Device Registry&lt;br&gt;• Authentication&lt;br&gt;• Message Routing&lt;br&gt;• Validation" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="200" y="440" width="200" height="120" as="geometry"/>
        </mxCell>
        
        <mxCell id="12" value="Azure Function&lt;br&gt;(Python)&lt;br&gt;&lt;br&gt;• Validate&lt;br&gt;• Transform&lt;br&gt;• Alert Generation" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="500" y="440" width="180" height="120" as="geometry"/>
        </mxCell>
        
        <mxCell id="13" value="OR&lt;br&gt;&lt;br&gt;Go Service&lt;br&gt;&lt;br&gt;• High throughput&lt;br&gt;• Low latency" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;dashed=1;" vertex="1" parent="1">
          <mxGeometry x="800" y="440" width="140" height="120" as="geometry"/>
        </mxCell>
        
        <mxCell id="14" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#d79b00;" edge="1" parent="1" source="11" target="12">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="15" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#d79b00;" edge="1" parent="1" source="12" target="16">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="16" value="LAYER 3: DATABASE" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=14;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="80" y="640" width="1240" height="40" as="geometry"/>
        </mxCell>
        
        <mxCell id="17" value="PostgreSQL + TimescaleDB&lt;br&gt;(Azure Database)&lt;br&gt;&lt;br&gt;Tables:&lt;br&gt;• bess_sites&lt;br&gt;• bess_telemetry&lt;br&gt;• bess_alerts&lt;br&gt;&lt;br&gt;Features:&lt;br&gt;• Time-series optimization&lt;br&gt;• Compression&lt;br&gt;• Retention policies" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;align=left;" vertex="1" parent="1">
          <mxGeometry x="400" y="720" width="600" height="160" as="geometry"/>
        </mxCell>
        
        <mxCell id="18" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#9673a6;dashed=1;" edge="1" parent="1" source="17" target="19">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="19" value="LAYER 4: BACKEND API" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="80" y="960" width="1240" height="40" as="geometry"/>
        </mxCell>
        
        <mxCell id="20" value="Django REST API&lt;br&gt;(Azure App Service)&lt;br&gt;&lt;br&gt;Endpoints:&lt;br&gt;GET /api/locations/&lt;br&gt;GET /api/data/&lt;br&gt;GET /api/stats/&lt;br&gt;GET /api/alerts/&lt;br&gt;&lt;br&gt;Auth: JWT + API Keys" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;align=left;" vertex="1" parent="1">
          <mxGeometry x="400" y="1040" width="600" height="160" as="geometry"/>
        </mxCell>
        
        <mxCell id="21" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#6c8ebf;" edge="1" parent="1" source="20" target="22">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="22" value="LAYER 5: FRONTEND DASHBOARD" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=14;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="80" y="1280" width="1240" height="40" as="geometry"/>
        </mxCell>
        
        <mxCell id="23" value="Dash Dashboard (Python)&lt;br&gt;(Azure App Service)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="500" y="1360" width="400" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="24" value="KPI Cards" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="120" y="1460" width="200" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="25" value="Filters" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="360" y="1460" width="200" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="26" value="Interactive Map" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="600" y="1460" width="200" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="27" value="Data Table" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="1">
          <mxGeometry x="840" y="1460" width="200" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="28" value="Time-Series Charts&lt;br&gt;• SOC&lt;br&gt;• Power Flow&lt;br&gt;• Voltage&lt;br&gt;• Temperature&lt;br&gt;• Revenue" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;align=left;" vertex="1" parent="1">
          <mxGeometry x="400" y="1560" width="600" height="100" as="geometry"/>
        </mxCell>
        
        <mxCell id="29" value="End User&lt;br&gt;(Web Browser)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#b0e3e6;strokeColor=#0e8088;fontSize=14;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="550" y="1720" width="300" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="30" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#0e8088;dashed=1;" edge="1" parent="1" source="28" target="29">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>

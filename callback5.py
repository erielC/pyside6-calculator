# === Callback 5: Update Map ===
@callback(Output("us-bess-map", "figure"), Input("filtered-sites-store", "data"))
def update_map(filtered_sites):
    """Create map with BESS markers"""

    print(f"\n🗺️  Updating map...")

    if not filtered_sites:
        print("   No sites to display")
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox=dict(
                style="carto-positron", center=dict(lat=39.5, lon=-98.35), zoom=3
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=config.MAP_HEIGHT,
        )
        return fig

    # Convert to DataFrame
    df = pd.DataFrame(filtered_sites)

    print(f"   Total sites: {len(df)}")

    # Extract coordinates - note "Lattitude" spelling
    df["lat"] = pd.to_numeric(df["Lattitude"], errors="coerce")
    df["lon"] = pd.to_numeric(df["Longitude"], errors="coerce")

    # Remove invalid
    df = df.dropna(subset=["lat", "lon"])

    print(f"   Valid coordinates: {len(df)}")
    print(f"   Sample: {df.iloc[0]['Project/Plant Name']}")
    print(f"     → lat={df.iloc[0]['lat']}, lon={df.iloc[0]['lon']}")

    if df.empty:
        print("   ❌ No valid coordinates!")
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox=dict(
                style="carto-positron", center=dict(lat=39.5, lon=-98.35), zoom=3
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=config.MAP_HEIGHT,
        )
        return fig

    # Colors by status
    status_colors = {
        "Operational": "#28a745",
        "Under Construction": "#ffc107",
        "Planned": "#17a2b8",
    }
    df["color"] = df["Status"].map(status_colors).fillna("#6c757d")

    # Marker sizes
    df["size"] = 12

    # Hover text
    df["hover_text"] = "<b>" + df["Project/Plant Name"] + "</b><br>Click for details"

    # Store full site data
    customdata = df.to_dict("records")

    # Create figure
    fig = go.Figure()

    fig.add_trace(
        go.Scattermapbox(
            lat=df["lat"],  # ← Latitude (36)
            lon=df["lon"],  # ← Longitude (-105)
            mode="markers",
            marker=dict(size=df["size"], color=df["color"], opacity=0.8),
            text=df["hover_text"],
            hoverinfo="text",
            customdata=customdata,
        )
    )

    # Center on data
    center_lat = df["lat"].mean()
    center_lon = df["lon"].mean()

    print(f"   Map center: ({center_lat:.2f}, {center_lon:.2f})\n")

    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=dict(lat=center_lat, lon=center_lon),
            zoom=3.5,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        height=config.MAP_HEIGHT,
        hovermode="closest",
        clickmode="event+select",
    )

    return fig

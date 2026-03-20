# === Callback 5: Update Map (FIXED) ===
@callback(Output("us-bess-map", "figure"), Input("filtered-sites-store", "data"))
def update_map(filtered_sites):
    """Create map with correctly positioned markers"""

    if not filtered_sites or len(filtered_sites) == 0:
        # Return empty map
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox=dict(
                style=config.MAP_STYLE, center=dict(lat=39.5, lon=-98.35), zoom=3
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=config.MAP_HEIGHT,
        )
        return fig

    # Convert to DataFrame
    df = pd.DataFrame(filtered_sites)

    # CRITICAL: Clean and validate coordinates
    # Handle "Lattitude" typo (note the spelling)
    if "Lattitude" in df.columns:
        df["lat"] = df["Lattitude"]
    elif "Latitude" in df.columns:
        df["lat"] = df["Latitude"]
    else:
        print("❌ No latitude column found!")
        return go.Figure()

    if "Longitude" in df.columns:
        df["lon"] = df["Longitude"]
    else:
        print("❌ No longitude column found!")
        return go.Figure()

    # Convert to numeric (handles strings)
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")

    # Remove invalid coordinates
    df = df.dropna(subset=["lat", "lon"])

    # VALIDATE: Check if coordinates are in valid US range
    # US bounds: lat 24-50, lon -125 to -66
    df = df[
        (df["lat"] >= 24) & (df["lat"] <= 50) & (df["lon"] >= -125) & (df["lon"] <= -66)
    ]

    print(f"\n🗺️  Valid coordinates: {len(df)} sites")
    print(f"   Lat range: {df['lat'].min():.2f} to {df['lat'].max():.2f}")
    print(f"   Lon range: {df['lon'].min():.2f} to {df['lon'].max():.2f}\n")

    if df.empty:
        print("❌ No valid coordinates after filtering!")
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox=dict(
                style=config.MAP_STYLE, center=dict(lat=39.5, lon=-98.35), zoom=3
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=config.MAP_HEIGHT,
        )
        return fig

    # Add colors
    status_colors = {
        "Operational": config.COLOR_OPERATIONAL,
        "Under Construction": config.COLOR_CONSTRUCTION,
        "Planned": config.COLOR_PLANNED,
    }
    df["color"] = df["Status"].map(status_colors).fillna(config.COLOR_NEUTRAL)

    # Add sizes
    df["size"] = (
        df["Rated Power (kW)"]
        .fillna(0)
        .apply(
            lambda x: 15 if config.MAP_SIZE_STANDARD else min(30, max(10, 10 + x / 100))
        )
    )

    # Hover text
    df["hover_text"] = (
        "<b>"
        + df["Project/Plant Name"].fillna("Unknown")
        + "</b><br>"
        + "<i>Click for details</i><br>"
        + "Lat: "
        + df["lat"].round(2).astype(str)
        + "<br>"
        + "Lon: "
        + df["lon"].round(2).astype(str)
    )

    # Store full site data in customdata
    customdata_list = []
    for idx, row in df.iterrows():
        site_name = row["Project/Plant Name"]
        original_site = next(
            (s for s in filtered_sites if s.get("Project/Plant Name") == site_name),
            row.to_dict(),
        )
        customdata_list.append(original_site)

    # Create figure
    fig = go.Figure()

    fig.add_trace(
        go.Scattermapbox(
            lat=df["lat"],  # ← Use cleaned lat
            lon=df["lon"],  # ← Use cleaned lon
            mode="markers",
            marker=dict(
                size=df["size"],
                color=df["color"],
                opacity=0.8,
            ),
            text=df["hover_text"],
            hoverinfo="text",
            customdata=customdata_list,
            name="",
        )
    )

    # Center on data
    center_lat = df["lat"].mean()
    center_lon = df["lon"].mean()

    print(f"   Map center: ({center_lat:.2f}, {center_lon:.2f})\n")

    fig.update_layout(
        mapbox=dict(
            style=config.MAP_STYLE,
            center=dict(lat=center_lat, lon=center_lon),
            zoom=3.5,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        height=config.MAP_HEIGHT,
        hovermode="closest",
        clickmode="event+select",
    )

    # At the end of update_map, before return fig:

    # Add a TEST marker at a known location (New York City)
    fig.add_trace(
        go.Scattermapbox(
            lat=[40.7128],
            lon=[-74.0060],
            mode="markers",
            marker=dict(size=25, color="red", symbol="star"),
            text=["TEST MARKER - NYC"],
            hoverinfo="text",
            customdata=[{"test": "marker", "Project/Plant Name": "Test Site NYC"}],
            name="Test",
        )
    )

    return fig

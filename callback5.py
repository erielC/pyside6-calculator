# === Callback 5: Update Map (FIX LONGITUDE SIGNS) ===
@callback(Output("us-bess-map", "figure"), Input("filtered-sites-store", "data"))
def update_map(filtered_sites):
    """Create map with CORRECTED longitude signs"""

    if not filtered_sites or len(filtered_sites) == 0:
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

    # Extract coordinates
    df["lat"] = pd.to_numeric(df.get("Lattitude", df.get("Latitude")), errors="coerce")
    df["lon"] = pd.to_numeric(df.get("Longitude"), errors="coerce")

    # Remove NaN
    df = df.dropna(subset=["lat", "lon"])

    # CRITICAL FIX: Force longitude to be negative for US sites
    # US is in Western Hemisphere (negative longitude)
    df["lon"] = df["lon"].abs() * -1  # Make all longitudes negative

    print(f"\n🗺️  After longitude fix:")
    print(f"   Sites: {len(df)}")
    print(f"   Lat range: {df['lat'].min():.2f} to {df['lat'].max():.2f}")
    print(f"   Lon range: {df['lon'].min():.2f} to {df['lon'].max():.2f}")
    print(f"   Sample site: {df.iloc[0]['Project/Plant Name']}")
    print(f"     → ({df.iloc[0]['lat']:.2f}, {df.iloc[0]['lon']:.2f})\n")

    # Validate US bounds
    df = df[
        (df["lat"] >= 24) & (df["lat"] <= 50) & (df["lon"] >= -125) & (df["lon"] <= -66)
    ]

    if df.empty:
        print("❌ No valid coordinates!")
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox=dict(
                style=config.MAP_STYLE, center=dict(lat=39.5, lon=-98.35), zoom=3
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=config.MAP_HEIGHT,
        )
        return fig

    # Colors
    status_colors = {
        "Operational": config.COLOR_OPERATIONAL,
        "Under Construction": config.COLOR_CONSTRUCTION,
        "Planned": config.COLOR_PLANNED,
    }
    df["color"] = df["Status"].map(status_colors).fillna(config.COLOR_NEUTRAL)

    # Sizes
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
        + "<i>Click for details</i>"
    )

    # Store full site data
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
            lat=df["lat"],
            lon=df["lon"],  # ← Now negative
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

    return fig

# === Callback 5: Update Map ===
@callback(Output("us-bess-map", "figure"), Input("filtered-sites-store", "data"))
def update_map(filtered_sites):
    """Create map - restricted to United States only"""

    print(f"\n🗺️  Updating map...")

    if not filtered_sites:
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox=dict(
                style="carto-positron",
                center=dict(lat=39.5, lon=-98.35),
                zoom=3,
                # Restrict map to US bounds
                bounds=dict(
                    west=-125,  # West Coast
                    east=-66,  # East Coast
                    south=24,  # Southern tip (Florida Keys)
                    north=50,  # Northern border (Canada)
                ),
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=config.MAP_HEIGHT,
        )
        return fig

    # Filter to ONLY sites with valid coordinates
    mappable_sites = [
        site for site in filtered_sites if site.get("has_coordinates", False)
    ]

    print(f"   Total sites: {len(filtered_sites)}")
    print(f"   Mappable sites (with coords): {len(mappable_sites)}")

    if not mappable_sites:
        print("   ❌ No sites have valid coordinates to map")
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox=dict(
                style="carto-positron",
                center=dict(lat=39.5, lon=-98.35),
                zoom=3,
                bounds=dict(west=-125, east=-66, south=24, north=50),
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=config.MAP_HEIGHT,
        )
        return fig

    # Convert to DataFrame
    df = pd.DataFrame(mappable_sites)

    # Extract coordinates
    df["lat"] = df["Lattitude"]
    df["lon"] = df["Longitude"]

    print(f"   Sample: {df.iloc[0]['Project/Plant Name']}")
    print(f"     → lat={df.iloc[0]['lat']}, lon={df.iloc[0]['lon']}")

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
            lat=df["lat"],
            lon=df["lon"],
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
            # RESTRICT TO US BOUNDS - Can't pan outside these coordinates
            bounds=dict(
                west=-125,  # West Coast (includes Alaska)
                east=-66,  # East Coast
                south=24,  # Southern tip (includes Puerto Rico)
                north=50,  # Northern border
            ),
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        height=config.MAP_HEIGHT,
        hovermode="closest",
        clickmode="event+select",
    )

    return fig

# === Callback 5: Update Map (SAFE VERSION) ===
@callback(Output("us-bess-map", "figure"), Input("filtered-sites-store", "data"))
def update_map(filtered_sites):
    """Create map with BESS markers"""

    print(f"\n🗺️  Updating map...")

    # Check 1: No sites at all
    if not filtered_sites:
        print("   ❌ filtered_sites is None or empty")
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox=dict(
                style="carto-positron", center=dict(lat=39.5, lon=-98.35), zoom=3
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=config.MAP_HEIGHT,
        )
        return fig

    print(f"   Total sites received: {len(filtered_sites)}")

    # Check 2: Print first site to debug
    if len(filtered_sites) > 0:
        first = filtered_sites[0]
        print(f"   First site: {first.get('Project/Plant Name', 'NO NAME')}")
        print(f"     Keys: {list(first.keys())[:5]}...")  # Show first 5 keys
        print(
            f"     Lattitude: {first.get('Lattitude')} (type: {type(first.get('Lattitude'))})"
        )
        print(
            f"     Longitude: {first.get('Longitude')} (type: {type(first.get('Longitude'))})"
        )

    # Convert to DataFrame
    df = pd.DataFrame(filtered_sites)

    # Check 3: Do the columns exist?
    if "Lattitude" not in df.columns:
        print(
            f"   ❌ 'Lattitude' column not found! Available columns: {df.columns.tolist()}"
        )
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox=dict(
                style="carto-positron", center=dict(lat=39.5, lon=-98.35), zoom=3
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=config.MAP_HEIGHT,
        )
        return fig

    if "Longitude" not in df.columns:
        print(
            f"   ❌ 'Longitude' column not found! Available columns: {df.columns.tolist()}"
        )
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox=dict(
                style="carto-positron", center=dict(lat=39.5, lon=-98.35), zoom=3
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=config.MAP_HEIGHT,
        )
        return fig

    # Extract coordinates
    df["lat"] = pd.to_numeric(df["Lattitude"], errors="coerce")
    df["lon"] = pd.to_numeric(df["Longitude"], errors="coerce")

    print(f"   After numeric conversion: {len(df)} rows")
    print(f"     NaN lats: {df['lat'].isna().sum()}")
    print(f"     NaN lons: {df['lon'].isna().sum()}")

    # Remove invalid
    df = df.dropna(subset=["lat", "lon"])

    print(f"   After dropping NaN: {len(df)} rows")

    # Check 4: DataFrame empty after cleaning?
    if df.empty:
        print("   ❌ DataFrame is empty after cleaning coordinates!")
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox=dict(
                style="carto-positron", center=dict(lat=39.5, lon=-98.35), zoom=3
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=config.MAP_HEIGHT,
        )
        return fig

    # NOW it's safe to access df.iloc[0]
    print(f"   ✅ Valid coordinates: {len(df)}")
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
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        height=config.MAP_HEIGHT,
        hovermode="closest",
        clickmode="event+select",
    )

    return fig

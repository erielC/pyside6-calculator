# === Callback 5: Update Map ===
@callback(Output("us-bess-map", "figure"), Input("filtered-sites-store", "data"))
def update_map(filtered_sites):
    """Create simple working map"""

    print(f"\n🗺️  Updating map...")

    if not filtered_sites:
        # Empty map
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox=dict(
                style="carto-positron", center=dict(lat=39.5, lon=-98.35), zoom=3
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=700,
        )
        return fig

    # Convert to DataFrame
    df = pd.DataFrame(filtered_sites)

    print(f"   Total sites: {len(df)}")

    # Get coordinates - handle both spellings
    if "Lattitude" in df.columns:
        df["lat"] = pd.to_numeric(df["Lattitude"], errors="coerce")
    elif "Latitude" in df.columns:
        df["lat"] = pd.to_numeric(df["Latitude"], errors="coerce")
    else:
        print("   ❌ No latitude column found")
        return go.Figure()

    df["lon"] = pd.to_numeric(df["Longitude"], errors="coerce")

    # Remove invalid coordinates
    df = df.dropna(subset=["lat", "lon"])

    print(f"   Valid coordinates: {len(df)}")

    if df.empty:
        print("   ❌ No valid coordinates")
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox=dict(
                style="carto-positron", center=dict(lat=39.5, lon=-98.35), zoom=3
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=700,
        )
        return fig

    print(f"   Sample: {df.iloc[0]['Project/Plant Name']}")
    print(f"     Lat: {df.iloc[0]['lat']}, Lon: {df.iloc[0]['lon']}")

    # Add colors
    df["color"] = "#0d6efd"  # Simple blue for now

    # Create figure
    fig = go.Figure()

    fig.add_trace(
        go.Scattermapbox(
            lat=df["lat"],
            lon=df["lon"],
            mode="markers",
            marker=dict(size=10, color=df["color"]),
            text=df["Project/Plant Name"],
            customdata=df.to_dict("records"),
        )
    )

    # Center on data
    center_lat = df["lat"].mean()
    center_lon = df["lon"].mean()

    print(f"   Map center: ({center_lat:.2f}, {center_lon:.2f})\n")

    fig.update_layout(
        mapbox=dict(
            style="carto-positron", center=dict(lat=center_lat, lon=center_lon), zoom=3
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=700,
        clickmode="event+select",
    )

    return fig

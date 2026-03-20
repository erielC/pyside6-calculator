# === Callback 5: Update Map ===
@callback(Output("us-bess-map", "figure"), Input("filtered-sites-store", "data"))
def update_map(filtered_sites):
    """
    Create interactive map with BESS site markers

    CRITICAL: Must configure clickmode and customdata properly
    for click events to work
    """

    # Handle empty case
    if not filtered_sites or len(filtered_sites) == 0:
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox=dict(
                style=config.MAP_STYLE,
                center=dict(lat=config.MAP_CENTER_LAT, lon=config.MAP_CENTER_LON),
                zoom=config.MAP_ZOOM,
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            height=config.MAP_HEIGHT,
        )
        return fig

    # Convert to DataFrame
    df = pd.DataFrame(filtered_sites)
    df = df.dropna(subset=["Lattitude", "Longitude"])
    df["Lattitude"] = pd.to_numeric(df["Lattitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
    df = df.dropna(subset=["Lattitude", "Longitude"])

    if df.empty:
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox=dict(
                style=config.MAP_STYLE,
                center=dict(lat=config.MAP_CENTER_LAT, lon=config.MAP_CENTER_LON),
                zoom=config.MAP_ZOOM,
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
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
            lambda x: 12 if config.MAP_SIZE_STANDARD else min(25, max(8, 8 + x / 100))
        )
    )

    # Simple hover text
    df["hover_text"] = (
        "<b>"
        + df["Project/Plant Name"].fillna("Unknown")
        + "</b><br>"
        + "<i>Click for details</i>"
    )

    # CRITICAL: Store full site dict in customdata (one per point)
    # Convert DataFrame rows back to original site dictionaries
    customdata_list = []
    for idx, row in df.iterrows():
        site_name = row["Project/Plant Name"]
        # Find original site dict from filtered_sites
        original_site = next(
            (s for s in filtered_sites if s.get("Project/Plant Name") == site_name),
            row.to_dict(),  # Fallback to DataFrame row as dict
        )
        customdata_list.append(original_site)

    # Create figure with SINGLE trace
    fig = go.Figure()

    fig.add_trace(
        go.Scattermapbox(
            lat=df["Lattitude"],
            lon=df["Longitude"],
            mode="markers",
            marker=dict(
                size=df["size"],
                color=df["color"],
                opacity=0.85,
            ),
            text=df["hover_text"],
            hoverinfo="text",
            customdata=customdata_list,  # Full site dicts
            name="",  # No legend name
        )
    )

    # Center map
    center_lat = df["Lattitude"].mean()
    center_lon = df["Longitude"].mean()

    # CRITICAL: Layout configuration for clicks
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
        clickmode="event+select",  # CRITICAL for click events
        uirevision="constant",  # Prevents map from resetting on update
    )

    return fig

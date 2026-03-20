# === Callback 5: Update Map ===
@callback(Output("us-bess-map", "figure"), Input("filtered-sites-store", "data"))
def update_map(filtered_sites):
    """
    Create interactive map with BESS site markers

    Triggers: When filtered sites change
    Creates: Plotly scattermapbox with clickable markers
    Returns: Plotly figure object
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

    # Convert to DataFrame and clean data
    df = pd.DataFrame(filtered_sites)
    df = df.dropna(subset=["Lattitude", "Longitude"])
    df["Lattitude"] = pd.to_numeric(df["Lattitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
    df = df.dropna(subset=["Lattitude", "Longitude"])

    if df.empty:
        # Return empty map if no valid coordinates
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

    # Add color based on status
    status_colors = {
        "Operational": config.COLOR_OPERATIONAL,
        "Under Construction": config.COLOR_CONSTRUCTION,
        "Planned": config.COLOR_PLANNED,
    }
    df["color"] = df["Status"].map(status_colors).fillna(config.COLOR_NEUTRAL)

    # Add marker size based on capacity
    df["size"] = (
        df["Rated Power (kW)"]
        .fillna(0)
        .apply(
            lambda x: 12 if config.MAP_SIZE_STANDARD else min(25, max(8, 8 + x / 100))
        )
    )

    # Create simple hover text (just name, click for details)
    df["hover_text"] = (
        "<b>"
        + df["Project/Plant Name"].fillna("Unknown")
        + "</b><br>"
        + "<i>Click marker for details</i>"
    )

    # Create scatter trace
    fig = go.Figure(
        go.Scattermapbox(
            lat=df["Lattitude"],
            lon=df["Longitude"],
            mode="markers",
            marker=dict(size=df["size"], color=df["color"], opacity=0.85),
            text=df["hover_text"],
            hoverinfo="text",
            customdata=df.index.tolist(),  # Store row index for click callback
        )
    )

    # Center map on data
    center_lat = df["Lattitude"].mean()
    center_lon = df["Longitude"].mean()

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
        clickmode="event+select",  # Enable click events
    )

    return fig


# === NEW Callback: Map Click Handler ===
@callback(
    Output("map-selected-site-panel", "children"),
    Input("us-bess-map", "clickData"),
    State("filtered-sites-store", "data"),
)
def display_selected_site_from_map(click_data, filtered_sites):
    """
    Display selected site information when map marker is clicked

    Triggers: Map marker click
    Returns: Site info panel or empty div
    """

    if not click_data or not filtered_sites:
        return html.Div()  # Empty - no selection

    # Get the clicked point's index
    point_index = click_data["points"][0].get("customdata")

    if point_index is None:
        return html.Div()

    # Get site data
    site = filtered_sites[point_index]

    # Create detailed info panel
    return dbc.Card(
        [
            dbc.CardHeader(
                [
                    html.H4(
                        [
                            html.I(className="fas fa-map-marker-alt me-2 text-primary"),
                            "Selected Site Details",
                        ],
                        className="mb-0",
                    )
                ]
            ),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            # Left column - Basic Info
                            dbc.Col(
                                [
                                    html.H5(
                                        site.get("Project/Plant Name", "Unknown"),
                                        className="text-primary mb-3",
                                    ),
                                    html.Div(
                                        [
                                            html.Strong("Location: "),
                                            f"{site.get('State/Province', 'N/A')}, {site.get('County', 'N/A')}",
                                        ],
                                        className="mb-2",
                                    ),
                                    html.Div(
                                        [
                                            html.Strong("Status: "),
                                            html.Span(
                                                site.get("Status", "Unknown"),
                                                className=f"badge bg-{'success' if site.get('Status') == 'Operational' else 'warning' if site.get('Status') == 'Under Construction' else 'info'}",
                                            ),
                                        ],
                                        className="mb-2",
                                    ),
                                    html.Div(
                                        [
                                            html.Strong("Commissioned Date: "),
                                            site.get("Commissioned Date", "N/A"),
                                        ],
                                        className="mb-2",
                                    ),
                                ],
                                width=12,
                                md=4,
                            ),
                            # Middle column - Technical Specs
                            dbc.Col(
                                [
                                    html.H6(
                                        "Technical Specifications",
                                        className="text-muted mb-3",
                                    ),
                                    html.Div(
                                        [
                                            html.Strong("Rated Power: "),
                                            f"{site.get('Rated Power (kW)', 0):,.0f} kW",
                                        ],
                                        className="mb-2",
                                    ),
                                    html.Div(
                                        [
                                            html.Strong("Energy Capacity: "),
                                            f"{site.get('Energy Capacity (kWh)', 0):,.0f} kWh",
                                        ],
                                        className="mb-2",
                                    ),
                                    html.Div(
                                        [
                                            html.Strong("Duration: "),
                                            f"{site.get('Duration (hours)', 'N/A')} hours",
                                        ],
                                        className="mb-2",
                                    ),
                                    html.Div(
                                        [
                                            html.Strong("Technology: "),
                                            site.get(
                                                "Storage Device Technology Mid-Type",
                                                "N/A",
                                            ),
                                        ],
                                        className="mb-2",
                                    ),
                                    html.Div(
                                        [
                                            html.Strong("Sub-Type: "),
                                            site.get(
                                                "Storage Device Technology Sub-Type",
                                                "N/A",
                                            ),
                                        ],
                                        className="mb-2",
                                    ),
                                ],
                                width=12,
                                md=4,
                            ),
                            # Right column - Utility/Operator Info
                            dbc.Col(
                                [
                                    html.H6(
                                        "Operator Information",
                                        className="text-muted mb-3",
                                    ),
                                    html.Div(
                                        [
                                            html.Strong("Utility: "),
                                            site.get("Utility", "N/A"),
                                        ],
                                        className="mb-2",
                                    ),
                                    html.Div(
                                        [
                                            html.Strong("Coordinates: "),
                                            f"{site.get('Lattitude', 'N/A')}, {site.get('Longitude', 'N/A')}",
                                        ],
                                        className="mb-2",
                                    ),
                                    # Note about time-series data
                                    html.Hr(className="my-3"),
                                    html.Div(
                                        [
                                            html.I(
                                                className="fas fa-info-circle me-2 text-info"
                                            ),
                                            html.Small(
                                                "Time-series data coming soon",
                                                className="text-muted",
                                            ),
                                        ]
                                    ),
                                ],
                                width=12,
                                md=4,
                            ),
                        ]
                    ),
                ]
            ),
        ],
        className="mt-3 shadow-sm border-primary",
        style={"borderLeft": "4px solid"},
    )

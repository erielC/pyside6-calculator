# === Map Click Callback ===
@callback(
    Output("map-selected-site-panel", "children"),
    Input("us-bess-map", "clickData"),
)
def display_selected_site_from_map(click_data):
    """Display site details when marker clicked"""

    # Debug print
    print(f"\n🔔 Map click: {click_data}\n")

    # No click yet
    if not click_data:
        return html.P(
            "Click a marker to see details", className="text-muted text-center py-3"
        )

    # Extract site from customdata
    try:
        site = click_data["points"][0]["customdata"]
    except (KeyError, IndexError, TypeError) as e:
        print(f"❌ Error extracting site: {e}")
        return html.P("Error loading site data", className="text-danger text-center")

    # Build info panel
    return dbc.Card(
        [
            dbc.CardHeader(
                [
                    html.H4(
                        [
                            html.I(className="fas fa-map-marker-alt me-2 text-primary"),
                            "Selected Site",
                        ],
                        className="mb-0",
                    )
                ]
            ),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            # Column 1: Basic Info
                            dbc.Col(
                                [
                                    html.H5(
                                        site.get("Project/Plant Name", "Unknown"),
                                        className="text-primary mb-3",
                                    ),
                                    html.P(
                                        [
                                            html.Strong("State: "),
                                            site.get("State/Province", "N/A"),
                                        ]
                                    ),
                                    html.P(
                                        [
                                            html.Strong("Status: "),
                                            html.Span(
                                                site.get("Status", "Unknown"),
                                                className=f"badge bg-{'success' if site.get('Status') == 'Operational' else 'warning'}",
                                            ),
                                        ]
                                    ),
                                ],
                                width=12,
                                md=4,
                            ),
                            # Column 2: Technical
                            dbc.Col(
                                [
                                    html.H6(
                                        "Technical Specs", className="text-muted mb-3"
                                    ),
                                    html.P(
                                        [
                                            html.Strong("Power: "),
                                            f"{site.get('Rated Power (kW)', 0):,.0f} kW",
                                        ]
                                    ),
                                    html.P(
                                        [
                                            html.Strong("Energy: "),
                                            f"{site.get('Energy Capacity (kWh)', 0):,.0f} kWh",
                                        ]
                                    ),
                                    html.P(
                                        [
                                            html.Strong("Duration: "),
                                            f"{site.get('Duration (hours)', 'N/A')} hours",
                                        ]
                                    ),
                                ],
                                width=12,
                                md=4,
                            ),
                            # Column 3: Other
                            dbc.Col(
                                [
                                    html.H6("Details", className="text-muted mb-3"),
                                    html.P(
                                        [
                                            html.Strong("Technology: "),
                                            site.get(
                                                "Storage Device Technology Mid-Type",
                                                "N/A",
                                            ),
                                        ]
                                    ),
                                    html.P(
                                        [
                                            html.Strong("Utility: "),
                                            site.get("Utility", "N/A"),
                                        ]
                                    ),
                                ],
                                width=12,
                                md=4,
                            ),
                        ]
                    )
                ]
            ),
        ],
        className="mt-3 shadow-sm border-primary",
        style={"borderLeft": "4px solid"},
    )

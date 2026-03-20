# === Callback: Map Click ===
@callback(
    Output("map-selected-site-panel", "children"),
    Input("us-bess-map", "clickData"),
)
def handle_map_click(click_data):
    """Handle map marker click"""

    print(f"\n🔔 Map click: {click_data is not None}\n")

    if not click_data:
        return html.P("Click a marker to see details", className="text-muted")

    # Get site from customdata
    try:
        site = click_data["points"][0]["customdata"]
    except:
        return html.P("Error loading site", className="text-danger")

    # Show site info
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H5(site.get("Project/Plant Name", "Unknown")),
                    html.P(f"State: {site.get('State/Province', 'N/A')}"),
                    html.P(f"Status: {site.get('Status', 'N/A')}"),
                    html.P(f"Power: {site.get('Rated Power (kW)', 0):,.0f} kW"),
                ]
            )
        ]
    )

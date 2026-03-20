# === Map Click Callback - ULTRA DEBUG ===
@callback(
    Output("map-selected-site-panel", "children"),
    Input("us-bess-map", "clickData"),
    prevent_initial_call=False,  # ← Let it fire immediately
)
def display_selected_site_from_map(click_data):
    """Display site details - ULTRA DEBUG VERSION"""

    import json

    print("\n" + "=" * 80)
    print("🔔🔔🔔 MAP CLICK CALLBACK EXECUTED 🔔🔔🔔")
    print("=" * 80)
    print(f"Callback triggered at: {pd.Timestamp.now()}")
    print(f"click_data type: {type(click_data)}")
    print(f"click_data is None: {click_data is None}")

    if click_data:
        print(f"click_data keys: {click_data.keys()}")
        print(
            f"click_data full content:\n{json.dumps(click_data, indent=2, default=str)}"
        )
    else:
        print("click_data is None or empty")

    print("=" * 80 + "\n")

    # ALWAYS return something visible
    if not click_data:
        return html.Div(
            [
                html.H3(
                    "⏳ Waiting for click...", className="text-center text-muted py-5"
                ),
                html.P(
                    f"Callback last fired: {pd.Timestamp.now()}",
                    className="text-center small text-muted",
                ),
            ],
            style={
                "backgroundColor": "#f0f0f0",
                "border": "3px dashed #666",
                "padding": "30px",
            },
        )

    # Extract site
    try:
        point = click_data["points"][0]
        print(f"Point keys: {point.keys()}")

        site = point.get("customdata")
        print(f"Site extracted: {site is not None}")

        if not site:
            return html.Div(
                [
                    html.H3(
                        "❌ No customdata found", className="text-danger text-center"
                    ),
                    html.Pre(json.dumps(point, indent=2, default=str)),
                ]
            )

    except Exception as e:
        print(f"❌ Error extracting site: {e}")
        return html.Div(
            [
                html.H3("❌ Error extracting site", className="text-danger"),
                html.P(str(e)),
            ]
        )

    # Success - show site
    return html.Div(
        [
            html.H2("✅ CLICK WORKED!", className="text-success text-center mb-4"),
            html.Hr(),
            html.H4(site.get("Project/Plant Name", "Unknown")),
            html.P(f"State: {site.get('State/Province', 'N/A')}"),
            html.P(f"Status: {site.get('Status', 'N/A')}"),
            html.P(f"Power: {site.get('Rated Power (kW)', 0):,.0f} kW"),
        ],
        style={
            "backgroundColor": "#d4edda",
            "border": "3px solid green",
            "padding": "30px",
        },
    )

# =================== LAYOUT ===================
layout = dbc.Container(
    [
        # Stores
        dcc.Store(id="selected-site-store"),
        dcc.Store(id="filtered-sites-store"),
        dcc.Store(id="national-stats-store"),
        # KPI cards
        create_kpi_section(),
        html.Hr(),
        # Filter panel
        create_filter_panel(),
        html.Hr(),
        # Map section (with click-to-view details)
        create_map_section(),
        html.Hr(),
        # Site table
        html.H3("BESS Deployments", className="mt-4 mb-3"),
        create_site_table(),
        html.Hr(),
        # CHARTS SECTION - COMMENTED OUT (waiting for time-series data)
        # html.Div(
        #     id="charts-section",
        #     children=create_charts_section(),
        #     style={"display": "none"},
        # ),
    ],
    fluid=True,
    className="px-4",
)


# === Callback 7: Store Selected Site === COMMENTED OUT
# @callback(
#     Output("selected-site-store", "data"),
#     Input("bess-sites-table", "selected_rows"),
#     State("bess-sites-table", "data"),
# )
# def store_selected_sites(selected_rows, table_data):
#     """Store selected site from table click"""
#     if not selected_rows or not table_data:
#         return None
#     return table_data[selected_rows[0]]


# === Callback 8: Toggle Charts Section === COMMENTED OUT
# @callback(
#     Output("charts-section", "style"),
#     Input("selected-site-store", "data"),
# )
# def toggle_charts_section(selected_site):
#     """Show/hide charts based on site selection"""
#     if not selected_site:
#         return {"display": "none"}
#     return {"display": "block"}


# === Callback 9: Update All Charts === COMMENTED OUT (no time-series data yet)
# @callback(
#     [
#         Output("selected-site-name", "children"),
#         Output("chart-soc", "figure"),
#         Output("chart-power", "figure"),
#         Output("chart-ac-voltage", "figure"),
#         Output("chart-dc-voltage", "figure"),
#         Output("chart-temperature", "figure"),
#         Output("chart-revenue", "figure"),
#         Output("chart-data-quality", "children"),
#     ],
#     [
#         Input("selected-site-store", "data"),
#         Input("chart-time-range", "value"),
#     ],
# )
# def update_all_charts(selected_site, time_range):
#     """
#     Update all time-series charts
#
#     CURRENTLY COMMENTED OUT - Waiting for time-series data from backend
#     """
#     pass

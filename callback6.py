# === Callback 6: Update Table ===
@callback(
    [
        Output("bess-sites-table", "data"),
        Output("table-site-count", "children"),
    ],
    Input("filtered-sites-store", "data"),
)
def update_table(filtered_sites):
    """
    Fill table with filtered BESS sites

    Triggers: When filtered sites change
    Returns: Table data (list of dicts) + site count
    """

    if not filtered_sites or len(filtered_sites) == 0:
        return [], "0 sites"

    # Prepare table data - select only columns needed for table
    table_data = []
    for site in filtered_sites:
        table_data.append(
            {
                "Project/Plant Name": site.get("Project/Plant Name", "Unknown"),
                "State/Province": site.get("State/Province", ""),
                "Status": site.get("Status", "Unknown"),
                "Rated Power (kW)": site.get("Rated Power (kW)", 0),
                "Energy Capacity (kWh)": site.get("Energy Capacity (kWh)", 0),
                "Duration (hours)": site.get("Duration (hours)", ""),
                "Storage Device Technology Mid-Type": site.get(
                    "Storage Device Technology Mid-Type", ""
                ),
                "Utility": site.get("Utility", ""),
                "Commissioned Date": site.get("Commissioned Date", ""),
            }
        )

    count_text = f"{len(filtered_sites):,} sites"

    return table_data, count_text

def register_data_callbacks(app):
    """
    Register all data-related callbacks
    """
    
    # =========================================================================
    # MASTER CALLBACK: Fetch All Data (Single Source of Truth)
    # =========================================================================
    @app.callback(
        Output('all-sites-store', 'data'),
        Input('data-refresh-interval', 'n_intervals')
    )
    def fetch_all_sites(n):
        """
        MASTER DATA FETCH - Single source of truth
        
        This is the ONLY callback that fetches data from API/mock
        All other callbacks consume from 'all-sites-store'
        
        Triggers:
        - Page load (n=0)
        - Every 30 seconds (interval)
        
        In production with real API:
        - This will call Django API
        - Get latest BESS data
        - Store in centralized location
        - All UI updates automatically
        
        Returns:
        - List of all BESS sites
        """
        print(f"🔄 Fetching data (update #{n})...")
        
        # This is the ONLY place that calls get_locations()
        locations = data_service.get_locations()
        
        print(f"✅ Fetched {len(locations)} sites")
        
        return locations
    
    
    # =========================================================================
    # CALLBACK: Calculate National Statistics (Consumer)
    # =========================================================================
    @app.callback(
        [
            Output('kpi-total-capacity', 'children'),
            Output('kpi-operational', 'children'),
            Output('kpi-construction', 'children'),
            Output('kpi-duration', 'children'),
            Output('national-stats-store', 'data'),
        ],
        Input('all-sites-store', 'data')  # ← READS from store, doesn't fetch
    )
    def update_kpi_cards(all_sites):
        """
        Calculate and display KPI cards
        
        Triggers:
        - When all-sites-store updates
        
        NOTE: Does NOT fetch data - consumes from store!
        """
        if not all_sites:
            # Return empty cards
            empty_card = create_single_kpi_card("", 0, "", "", "fas fa-spinner", "secondary")
            return empty_card, empty_card, empty_card, empty_card, {}
        
        # Calculate stats from provided data
        total_power = sum(s.get('power_mw', 0) for s in all_sites)
        total_energy = sum(s.get('energy_mwh', 0) for s in all_sites)
        
        operational = [s for s in all_sites if s.get('status') == 'Operational']
        construction = [s for s in all_sites if s.get('status') == 'Under Construction']
        planned = [s for s in all_sites if s.get('status') == 'Planned']
        
        operational_power = sum(s.get('power_mw', 0) for s in operational)
        construction_power = sum(s.get('power_mw', 0) for s in construction)
        
        stats = {
            'total_sites': len(all_sites),
            'total_power_mw': round(total_power, 1),
            'total_energy_mwh': round(total_energy, 1),
            'avg_duration_hours': round(total_energy / total_power, 1) if total_power > 0 else 0,
            'operational_sites': len(operational),
            'operational_power_mw': round(operational_power, 1),
            'construction_sites': len(construction),
            'construction_power_mw': round(construction_power, 1),
            'planned_sites': len(planned),
        }
        
        # Create KPI cards
        kpi_total = create_single_kpi_card(
            title="Total Capacity",
            value=stats['total_power_mw'],
            unit="MW",
            subtitle=f"{stats['total_energy_mwh']:,.0f} MWh nationwide",
            icon="fas fa-bolt",
            color="success"
        )
        
        kpi_operational = create_single_kpi_card(
            title="Operational Sites",
            value=stats['operational_sites'],
            unit="sites",
            subtitle=f"{stats['operational_power_mw']:,.0f} MW online",
            icon="fas fa-check-circle",
            color="success"
        )
        
        kpi_construction = create_single_kpi_card(
            title="Under Construction",
            value=stats['construction_sites'],
            unit="sites",
            subtitle=f"{stats['construction_power_mw']:,.0f} MW in pipeline",
            icon="fas fa-hard-hat",
            color="warning"
        )
        
        kpi_duration = create_single_kpi_card(
            title="Avg Duration",
            value=stats['avg_duration_hours'],
            unit="hours",
            subtitle="Storage capacity",
            icon="fas fa-clock",
            color="info"
        )
        
        return kpi_total, kpi_operational, kpi_construction, kpi_duration, stats
    
    
    # =========================================================================
    # CALLBACK: Populate Filter Dropdowns (Consumer)
    # =========================================================================
    @app.callback(
        [
            Output('filter-state', 'options'),
            Output('filter-technology', 'options'),
        ],
        Input('all-sites-store', 'data')  # ← READS from store
    )
    def populate_filters(all_sites):
        """
        Populate filter dropdowns
        
        Triggers:
        - When all-sites-store updates
        
        NOTE: Consumes from store, doesn't fetch!
        """
        if not all_sites:
            return [], []
        
        # Get unique states
        states = sorted(list(set(s['state'] for s in all_sites)))
        state_options = [{'label': state, 'value': state} for state in states]
        
        # Get unique technologies
        technologies = sorted(list(set(s['technology'] for s in all_sites)))
        tech_options = [{'label': tech, 'value': tech} for tech in technologies]
        
        return state_options, tech_options
    
    
    # =========================================================================
    # CALLBACK: Filter Sites (Consumer)
    # =========================================================================
    @app.callback(
        [
            Output('filtered-sites-store', 'data'),
            Output('filter-summary', 'children'),
        ],
        [
            Input('all-sites-store', 'data'),  # ← READS from store
            Input('filter-state', 'value'),
            Input('filter-status', 'value'),
            Input('filter-technology', 'value'),
            Input('filter-min-capacity', 'value'),
        ]
    )
    def filter_sites(all_sites, states, statuses, technologies, min_capacity):
        """
        Filter sites based on user selections
        
        Triggers:
        - When all-sites-store updates (new data)
        - When any filter changes
        
        NOTE: Filters the data from store, doesn't fetch!
        """
        if not all_sites:
            return [], "No sites"
        
        total_sites = len(all_sites)
        filtered = all_sites
        
        # Apply filters
        if states and len(states) > 0:
            filtered = [s for s in filtered if s['state'] in states]
        
        if statuses and len(statuses) > 0:
            filtered = [s for s in filtered if s['status'] in statuses]
        
        if technologies and len(technologies) > 0:
            filtered = [s for s in filtered if s['technology'] in technologies]
        
        if min_capacity and min_capacity > 0:
            filtered = [s for s in filtered if s['power_mw'] >= min_capacity]
        
        # Summary
        filtered_count = len(filtered)
        summary = f"Showing {filtered_count:,} of {total_sites:,} sites"
        
        return filtered, summary
    
    
    # =========================================================================
    # CALLBACK: Reset Filters
    # =========================================================================
    @app.callback(
        [
            Output('filter-state', 'value'),
            Output('filter-status', 'value'),
            Output('filter-technology', 'value'),
            Output('filter-min-capacity', 'value'),
        ],
        Input('reset-filters-btn', 'n_clicks'),
        prevent_initial_call=True
    )
    def reset_filters(n_clicks):
        """Clear all filters"""
        return None, None, None, None

"""
=============================================================================
CHART CALLBACKS - Time-Series Charts
=============================================================================

CALLBACKS:
1. Show/hide charts section based on site selection
2. Update all 6 charts when site selected or time range changes

BEGINNER NOTES:
- Charts only appear when user selects a site from table
- All 6 charts update together in one callback (efficient!)
- Uses Plotly for interactive charts (zoom, pan, hover)
=============================================================================
"""

from dash import Input, Output, State, html
import plotly.graph_objects as go
import pandas as pd
from config import config
from src.data import data_service
from src.components.charts import create_empty_charts_section, create_charts_section


def register_chart_callbacks(app):
    """
    Register chart-related callbacks
    
    Args:
        app: Dash app instance
    """
    
    # =========================================================================
    # CALLBACK 1: Show/Hide Charts Section
    # =========================================================================
    @app.callback(
        Output('charts-section', 'children'),
        Input('selected-site-store', 'data')
    )
    def toggle_charts_section(selected_site):
        """
        Show charts when site selected, hide when not
        
        Triggers:
        - When user selects/deselects a site
        
        Returns:
        - Empty placeholder OR charts structure
        """
        
        if not selected_site:
            # No site selected - show placeholder
            return create_empty_charts_section()
        
        # Site selected - show charts structure
        return create_charts_section()
    
    
    # =========================================================================
    # CALLBACK 2: Update All Charts
    # =========================================================================
    @app.callback(
        [
            Output('selected-site-name', 'children'),
            Output('chart-soc', 'figure'),
            Output('chart-power', 'figure'),
            Output('chart-ac-voltage', 'figure'),
            Output('chart-dc-voltage', 'figure'),
            Output('chart-temperature', 'figure'),
            Output('chart-revenue', 'figure'),
            Output('chart-data-quality', 'children'),
        ],
        [
            Input('selected-site-store', 'data'),
            Input('chart-time-range', 'value'),
        ]
    )
    def update_all_charts(selected_site, time_range):
        """
        Update all 6 charts for the selected site
        
        Triggers:
        - Site selection changes
        - Time range dropdown changes
        
        Returns:
        - Site name
        - 6 Plotly figures (one for each chart)
        - Data quality message
        """
        
        # Create empty figure for error cases
        empty_fig = go.Figure()
        empty_fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[dict(
                text="No data",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=16, color='gray')
            )]
        )
        
        # No site selected
        if not selected_site:
            return (
                "",
                empty_fig, empty_fig, empty_fig,
                empty_fig, empty_fig, empty_fig,
                ""
            )
        
        # Get site info
        site_id = selected_site['site_id']
        site_name = selected_site['name']
        
        # Fetch time-series data
        data = data_service.get_site_data(site_id, hours=time_range or 24)
        
        # No data available
        if not data or len(data) == 0:
            return (
                site_name,
                empty_fig, empty_fig, empty_fig,
                empty_fig, empty_fig, empty_fig,
                "No time-series data available for this site"
            )
        
        # Convert to pandas DataFrame for easier manipulation
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')  # Chronological order
        
        # =====================================================================
        # CHART 1: State of Charge (%)
        # =====================================================================
        fig_soc = go.Figure()
        fig_soc.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['state_of_charge'],
            mode='lines',
            name='SOC',
            line=dict(color=config.COLOR_SUCCESS, width=2),
            fill='tozeroy',
            fillcolor='rgba(6, 167, 125, 0.2)'
        ))
        fig_soc.update_layout(
            template=config.CHART_TEMPLATE,
            xaxis_title='Time',
            yaxis_title='State of Charge (%)',
            yaxis=dict(range=[0, 100]),
            hovermode='x unified',
            margin=dict(l=50, r=20, t=20, b=40),
        )
        
        # =====================================================================
        # CHART 2: Power Flow (MW)
        # =====================================================================
        fig_power = go.Figure()
        
        # Separate charging (positive) and discharging (negative)
        df_charging = df[df['power_mw'] >= 0]
        df_discharging = df[df['power_mw'] < 0]
        
        if not df_charging.empty:
            fig_power.add_trace(go.Scatter(
                x=df_charging['timestamp'],
                y=df_charging['power_mw'],
                mode='lines',
                name='Charging',
                line=dict(color=config.COLOR_SUCCESS, width=2),
                fill='tozeroy',
                fillcolor='rgba(6, 167, 125, 0.2)'
            ))
        
        if not df_discharging.empty:
            fig_power.add_trace(go.Scatter(
                x=df_discharging['timestamp'],
                y=df_discharging['power_mw'],
                mode='lines',
                name='Discharging',
                line=dict(color=config.COLOR_DANGER, width=2),
                fill='tozeroy',
                fillcolor='rgba(214, 40, 40, 0.2)'
            ))
        
        fig_power.update_layout(
            template=config.CHART_TEMPLATE,
            xaxis_title='Time',
            yaxis_title='Power (MW)',
            hovermode='x unified',
            margin=dict(l=50, r=20, t=20, b=40),
            # Zero line
            shapes=[dict(
                type='line',
                x0=df['timestamp'].min(),
                x1=df['timestamp'].max(),
                y0=0, y1=0,
                line=dict(color='gray', width=1, dash='dash')
            )]
        )
        
        # =====================================================================
        # CHART 3: AC Bus Voltage
        # =====================================================================
        fig_ac_voltage = go.Figure()
        fig_ac_voltage.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['ac_bus_voltage'],
            mode='lines',
            name='AC Voltage',
            line=dict(color=config.COLOR_PRIMARY, width=2)
        ))
        fig_ac_voltage.update_layout(
            template=config.CHART_TEMPLATE,
            xaxis_title='Time',
            yaxis_title='AC Bus Voltage (V)',
            hovermode='x unified',
            margin=dict(l=50, r=20, t=20, b=40),
        )
        
        # =====================================================================
        # CHART 4: DC Bus Voltage
        # =====================================================================
        fig_dc_voltage = go.Figure()
        fig_dc_voltage.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['dc_bus_voltage'],
            mode='lines',
            name='DC Voltage',
            line=dict(color='#9b59b6', width=2)
        ))
        fig_dc_voltage.update_layout(
            template=config.CHART_TEMPLATE,
            xaxis_title='Time',
            yaxis_title='DC Bus Voltage (V)',
            hovermode='x unified',
            margin=dict(l=50, r=20, t=20, b=40),
        )
        
        # =====================================================================
        # CHART 5: Temperature
        # =====================================================================
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['temperature'],
            mode='lines',
            name='Battery Temp',
            line=dict(color=config.COLOR_WARNING, width=2)
        ))
        fig_temp.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['inverter_temp'],
            mode='lines',
            name='Inverter Temp',
            line=dict(color=config.COLOR_DANGER, width=2, dash='dash')
        ))
        
        # Warning zone (high temperature)
        fig_temp.add_hrect(
            y0=40, y1=60,
            fillcolor='red', opacity=0.1,
            annotation_text='High Temp Zone',
            annotation_position='top left'
        )
        
        fig_temp.update_layout(
            template=config.CHART_TEMPLATE,
            xaxis_title='Time',
            yaxis_title='Temperature (°C)',
            hovermode='x unified',
            margin=dict(l=50, r=20, t=20, b=40),
        )
        
        # =====================================================================
        # CHART 6: Revenue Estimate
        # =====================================================================
        fig_revenue = go.Figure()
        
        if 'revenue_usd_per_hour' in df.columns:
            fig_revenue.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['revenue_usd_per_hour'],
                mode='lines',
                name='Revenue',
                line=dict(color='#2ecc71', width=2),
                fill='tozeroy',
                fillcolor='rgba(46, 204, 113, 0.2)'
            ))
            fig_revenue.update_layout(
                template=config.CHART_TEMPLATE,
                xaxis_title='Time',
                yaxis_title='Revenue ($/hour)',
                hovermode='x unified',
                margin=dict(l=50, r=20, t=20, b=40),
            )
        else:
            fig_revenue = empty_fig
        
        # Data quality message
        data_quality = f"Displaying {len(df):,} data points over {time_range or 24} hours"
        
        return (
            site_name,
            fig_soc,
            fig_power,
            fig_ac_voltage,
            fig_dc_voltage,
            fig_temp,
            fig_revenue,
            data_quality
        )

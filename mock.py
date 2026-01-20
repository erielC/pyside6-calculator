"""
Dashboard Page
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from config import config

# SIMPLE VERSION FIRST - Test if routing works
layout = dbc.Container([
    
    # Header
    html.H1([
        html.I(className="fas fa-chart-line me-3"),
        "Dashboard"
    ], className="mb-4"),
    
    # Test content
    dbc.Alert([
        html.H4("✅ Dashboard Page Loaded Successfully!", className="alert-heading"),
        html.P("Routing is working! Now we can add components."),
    ], color="success"),
    
    # Placeholder sections
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("KPIs Coming Soon"),
                    html.P("Key performance indicators will appear here"),
                ])
            ])
        ], width=12, className="mb-4"),
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Map Coming Soon"),
                    html.P("Interactive BESS map will appear here"),
                ])
            ])
        ], width=12, className="mb-4"),
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Charts Coming Soon"),
                    html.P("Time-series charts will appear here"),
                ])
            ])
        ], width=12),
    ]),
    
], fluid=True, className="px-4 py-4")

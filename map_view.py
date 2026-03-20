"""
Map View Component - Simple and Working
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from config import config


def create_map_section():
    """Create simple map section"""

    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H3(
                        [
                            html.I(className="fas fa-map-marked-alt me-2 text-primary"),
                            "BESS Deployment Map",
                        ]
                    ),
                    # Map
                    dcc.Graph(
                        id="us-bess-map",
                        config={
                            "displayModeBar": True,
                            "displaylogo": False,
                            "scrollZoom": True,
                        },
                        style={"height": "700px"},
                    ),
                    html.Hr(),
                    # Click info panel
                    html.Div(id="map-selected-site-panel"),
                ]
            )
        ],
        className="mb-4",
    )

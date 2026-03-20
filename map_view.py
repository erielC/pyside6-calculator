"""
MAP VIEW COMPONENT - Interactive US Map

Shows BESS locations - restricted to United States only
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from config import config


def create_map_section():
    """
    Create map section with US-only restrictions

    Features:
    - Cannot pan outside US bounds
    - Zoom restricted to reasonable levels
    - Click markers for details
    """

    return dbc.Card(
        [
            dbc.CardBody(
                [
                    # Map title
                    html.H3(
                        [
                            html.I(className="fas fa-map-marked-alt me-2 text-primary"),
                            "BESS Deployment Map - United States",
                        ],
                        className="mb-4",
                    ),
                    # Instructions
                    dbc.Alert(
                        [
                            html.I(className="fas fa-info-circle me-2"),
                            "Click on a marker to view site details below",
                        ],
                        color="info",
                        className="py-2 mb-3",
                    ),
                    # Map (plotly graph component)
                    dcc.Graph(
                        id="us-bess-map",
                        config={
                            "scrollZoom": True,  # Allow scroll to zoom
                            "displayModeBar": True,  # Show toolbar
                            "displaylogo": False,  # Hide plotly logo
                            "doubleClick": "reset",  # Double-click resets to US view
                            "modeBarButtonsToRemove": [
                                "lasso2d",
                                "select2d",
                                "autoScale2d",
                                "resetScale2d",  # Remove global reset (use double-click)
                            ],
                        },
                        style={"height": f"{config.MAP_HEIGHT}px"},
                    ),
                    # Map legend
                    html.Div(
                        [
                            html.Small(
                                [
                                    html.Span(
                                        [
                                            html.I(
                                                className="fas fa-circle text-success me-1"
                                            ),
                                            "Operational",
                                        ],
                                        className="me-3",
                                    ),
                                    html.Span(
                                        [
                                            html.I(
                                                className="fas fa-circle text-warning me-1"
                                            ),
                                            "Under Construction",
                                        ],
                                        className="me-3",
                                    ),
                                    html.Span(
                                        [
                                            html.I(
                                                className="fas fa-circle text-info me-1"
                                            ),
                                            "Planned",
                                        ]
                                    ),
                                ],
                                className="text-muted",
                            ),
                        ],
                        className="mt-3 text-center",
                    ),
                    html.Hr(className="my-4"),
                    # Selected site info panel (hidden initially)
                    html.Div(
                        id="map-selected-site-panel",
                        children=[
                            html.P(
                                "Click a marker to see details",
                                className="text-muted text-center py-3",
                            )
                        ],
                        style={"minHeight": "100px"},
                    ),
                ]
            )
        ],
        className="shadow-sm border-0 mb-4",
        id="map-section",
    )

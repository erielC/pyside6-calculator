"""
US BESS Tracker - Index
"""

import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

from app import app
from config import config

# ==================== LAYOUT ====================

app.layout = html.Div([
    
    # Location component
    dcc.Location(id='url', refresh=False),
    
    # Simple navbar (we'll improve this later)
    html.Div([
        html.H3(config.APP_TITLE, style={
            'padding': '15px 20px',
            'backgroundColor': config.COLOR_PRIMARY,
            'color': 'white',
            'margin': '0'
        }),
        html.Div([
            html.A('Home', href='/', style={'padding': '10px 20px', 'color': 'white', 'textDecoration': 'none'}),
            html.A('Dashboard', href='/dashboard', style={'padding': '10px 20px', 'color': 'white', 'textDecoration': 'none'}),
            html.A('Sites', href='/sites', style={'padding': '10px 20px', 'color': 'white', 'textDecoration': 'none'}),
            html.A('Analytics', href='/analytics', style={'padding': '10px 20px', 'color': 'white', 'textDecoration': 'none'}),
        ], style={'backgroundColor': '#0056b3', 'padding': '10px 0'}),
    ]),
    
    # Page content
    html.Div(id='page-content', style={'padding': '20px'}),
    
])


# ==================== ROUTING CALLBACK ====================

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    """Route to different pages"""
    
    print(f"\n{'='*70}")
    print(f"🔍 ROUTING: {pathname}")
    print(f"{'='*70}\n")
    
    if pathname is None:
        pathname = '/'
    
    # Home page
    if pathname == '/' or pathname == '/home':
        return html.Div([
            html.H1("🏠 Home", className="mb-4"),
            html.P("Welcome to the US BESS Tracker", className="lead"),
            dbc.Button("Go to Dashboard", href="/dashboard", color="primary", size="lg"),
        ])
    
    # Dashboard page
    elif pathname == '/dashboard':
        print("→ Loading dashboard...")
        try:
            from src.pages.dashboard import layout
            print("✅ Dashboard loaded")
            return layout
        except Exception as e:
            print(f"❌ Error loading dashboard: {e}")
            import traceback
            traceback.print_exc()
            return html.Div([
                html.H1("Error Loading Dashboard", className="text-danger"),
                html.Pre(str(e)),
                html.A("← Back to Home", href="/", className="btn btn-secondary"),
            ])
    
    # Sites page
    elif pathname == '/sites':
        print("→ Loading sites...")
        try:
            from src.pages.sites import layout
            print("✅ Sites loaded")
            return layout
        except Exception as e:
            print(f"❌ Error loading sites: {e}")
            return html.Div([
                html.H1("Sites Page - Coming Soon", className="text-info"),
                html.A("← Back to Home", href="/", className="btn btn-secondary"),
            ])
    
    # Analytics page
    elif pathname == '/analytics':
        print("→ Loading analytics...")
        try:
            from src.pages.analytics import layout
            print("✅ Analytics loaded")
            return layout
        except Exception as e:
            print(f"❌ Error loading analytics: {e}")
            return html.Div([
                html.H1("Analytics Page - Coming Soon", className="text-info"),
                html.A("← Back to Home", href="/", className="btn btn-secondary"),
            ])
    
    # 404
    else:
        return html.Div([
            html.H1("404 - Page Not Found", className="text-center mt-5"),
            html.P(f"The page '{pathname}' does not exist.", className="text-center"),
            dbc.Button("Go Home", href="/", color="primary", className="mt-3"),
        ], className="text-center")


# ==================== REGISTER OTHER CALLBACKS ====================

print("📞 Registering callbacks...")
try:
    from src.callbacks import register_all_callbacks
    register_all_callbacks(app)
    print("✅ Callbacks registered\n")
except Exception as e:
    print(f"⚠️  Warning: {e}\n")


# ==================== RUN ====================

if __name__ == '__main__':
    print("="*70)
    print(f"🚀 {config.APP_TITLE}")
    print("="*70)
    print(f"📍 http://localhost:{config.APP_PORT}/")
    print("="*70)
    print()
    
    app.run_server(
        debug=config.DEBUG,
        host=config.APP_HOST,
        port=config.APP_PORT
    )

"""
Simplest possible multi-page test
"""

import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

# Create app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = html.Div([
    
    dcc.Location(id='url', refresh=False),
    
    html.Div([
        html.H2("Simple Test App", style={'padding': '20px', 'backgroundColor': 'lightblue'}),
        html.Div([
            html.A('HOME', href='/', style={'padding': '10px', 'fontSize': '20px'}),
            html.Span(' | '),
            html.A('DASHBOARD', href='/dashboard', style={'padding': '10px', 'fontSize': '20px'}),
        ], style={'padding': '20px'}),
    ]),
    
    html.Div(id='page-content', style={
        'padding': '40px',
        'minHeight': '400px',
        'border': '3px solid red',
        'margin': '20px'
    }),
])

# Callback
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def show_page(pathname):
    
    # ALWAYS print
    print("\n" + "="*60)
    print(f"CALLBACK TRIGGERED!")
    print(f"pathname = {pathname}")
    print("="*60 + "\n")
    
    if pathname == '/dashboard':
        return html.Div([
            html.H1("🎉 DASHBOARD WORKS!", style={'color': 'green', 'fontSize': '48px'}),
            html.P(f"pathname = {pathname}"),
        ])
    else:
        return html.Div([
            html.H1("🏠 HOME", style={'color': 'blue', 'fontSize': '48px'}),
            html.P(f"pathname = {pathname}"),
        ])

# Run
if __name__ == '__main__':
    print("\n🚀 Starting simple test...\n")
    app.run_server(debug=True, host='127.0.0.1', port=8051)  # ← Different port!

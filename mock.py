"""
Dashboard - DATA FLOW TEST
"""

from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc


# ==================== LAYOUT ====================

layout = dbc.Container([
    
    html.H1("DASHBOARD LOADED", className="text-success mb-4"),
    
    html.Hr(),
    
    html.H2("Test 1: Static Content"),
    html.P("If you see this, the layout works.", className="bg-info text-white p-3"),
    
    html.Hr(),
    
    html.H2("Test 2: Callback Test"),
    html.Div(id='test-output', style={
        'padding': '40px',
        'backgroundColor': '#ffeb3b',
        'border': '5px solid red',
        'fontSize': '24px',
        'fontWeight': 'bold'
    }),
    
], fluid=True, className="p-4")


# ==================== CALLBACK ====================

@callback(
    Output('test-output', 'children'),
    Input('all-sites-store', 'data')
)
def test_callback(all_sites):
    
    print("\n" + "="*70)
    print("🔔 TEST CALLBACK FIRED!")
    print(f"   all_sites is None: {all_sites is None}")
    print(f"   all_sites type: {type(all_sites)}")
    
    if all_sites is not None:
        print(f"   all_sites length: {len(all_sites)}")
    
    print("="*70 + "\n")
    
    if all_sites is None:
        return "❌ all_sites is None"
    
    if not all_sites:
        return "❌ all_sites is empty list []"
    
    return f"✅ SUCCESS! Received {len(all_sites)} sites"

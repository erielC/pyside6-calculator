"""
Dashboard Page - DATA FLOW TEST
"""

from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc


# ==================== LAYOUT ====================

layout = dbc.Container([
    
    dbc.Alert("✅ Dashboard Loaded", color="success"),
    
    html.H3("Data Test:"),
    html.Div(id='data-test-output', style={
        'padding': '20px',
        'border': '3px solid red',
        'backgroundColor': '#f0f0f0',
        'minHeight': '200px'
    }),
    
], fluid=True, className="px-4 py-4")


# ==================== TEST CALLBACK ====================

@callback(
    Output('data-test-output', 'children'),
    Input('all-sites-store', 'data')
)
def test_data_flow(all_sites):
    """Test if data flows from store to dashboard"""
    
    print("\n" + "="*70)
    print("🔔 DASHBOARD CALLBACK FIRED!")
    print(f"   all_sites is None: {all_sites is None}")
    print(f"   all_sites type: {type(all_sites)}")
    
    if all_sites:
        print(f"   all_sites length: {len(all_sites)}")
        print(f"   First site: {all_sites[0]}")
    else:
        print("   all_sites is EMPTY or None!")
    
    print("="*70 + "\n")
    
    if not all_sites:
        return html.H2("❌ NO DATA RECEIVED", className="text-danger")
    
    return html.Div([
        html.H2(f"✅ SUCCESS! Got {len(all_sites)} sites", className="text-success"),
        html.Hr(),
        html.H4("First 3 sites:"),
        html.Ul([
            html.Li(f"{site['name']} - {site['state']} - {site['power_mw']} MW")
            for site in all_sites[:3]
        ]),
        html.Hr(),
        html.P(f"Total capacity: {sum(s['power_mw'] for s in all_sites):,.0f} MW"),
    ])
```

**Save, restart, visit dashboard.**

---

### **Expected Results:**

**Terminal should show:**
```
🔄 Master data fetch (update #0)...
✅ Fetched 69 sites

======================================================================
🔔 DASHBOARD CALLBACK FIRED!
   all_sites is None: False
   all_sites type: <class 'list'>
   all_sites length: 69
   First site: {'site_id': 'CA-Site-001', 'name': '...', ...}
======================================================================
```

**Browser should show:**
- Green "Dashboard Loaded" alert
- Red box with "✅ SUCCESS! Got 69 sites"
- List of first 3 sites
- Total capacity

---

## What Do You See?

### **Scenario A: You see "NO DATA RECEIVED"**

**Terminal shows:**
```
🔔 DASHBOARD CALLBACK FIRED!
   all_sites is None: True
   all_sites is EMPTY or None!

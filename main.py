import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from flask import Response  # Needed for the health check

# 1. Initialize the Dash app
app = dash.Dash(__name__)

# 2. Expose the Flask server for Gunicorn
server = app.server

# --- NEW: HEALTH CHECK ROUTE ---
@server.route('/health')
def health_check():
    """
    Lightweight endpoint for Coolify to 'ping'.
    Returning a simple 200 OK prevents the server from loading 
    the entire dashboard/graphs during a health check.
    """
    return Response("OK", status=200)
# -------------------------------

# 3. Create sample data
df = pd.DataFrame({
    "Asset": ["BTC", "ETH", "SOL", "DOT"],
    "Price": [45000, 2500, 100, 7],
    "Signal": ["BUY", "HOLD", "BUY", "SELL"]
})

fig = px.bar(df, x="Asset", y="Price", color="Signal", title="Bot Status")

# 4. Define the Layout
app.layout = html.Div([
    html.H1("AI Trading Bot Dashboard"),
    html.Div("Real-time performance from KVM 2 Server"),
    dcc.Graph(figure=fig),
    
    # Auto-refresh component (updates every 60 seconds)
    dcc.Interval(id='interval-component', interval=60*1000, n_intervals=0)
])

if __name__ == '__main__':
    # Default to 8050 for local testing
    app.run(debug=False, host='0.0.0.0', port=8050)

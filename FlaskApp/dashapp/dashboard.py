from dash import dash
import dash_html_components as html


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=['/static/style.css']
    )
    # Create Layout
    dash_app.layout = html.Div("Coming soon")

    return dash_app.server

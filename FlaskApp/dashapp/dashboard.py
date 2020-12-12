from dash import dash
import dash_html_components as html
import plotly.express as px
import sqlalchemy as db
from textwrap import dedent
from dash.dependencies import Input, Output, State
from FlaskApp.dashapp.sqlqueries import *

from FlaskApp.dashapp.dashcontrols import *


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[dbc.themes.SUPERHERO]
    )

    # Data Connection
    engine = db.create_engine('sqlite:///C://Users//raman//master.db')
    connection = engine.connect()

    # Get values for controls
    state = get_unique(connection, "data", "STATE")
    year = get_unique(connection, "data", "YEAR")
    week_flag = get_unique(connection, "data", "Weekened_Flag")
    holiday_flag = get_unique(connection, "data", "Holiday_Flag")
    connection.close()

    # Build Components
    controls = [
        dcc_multiselect(id="states", label="State", values=state),
        dcc_multiselect(id="years", label="Year", values=year),
        option_menu(id="week_flag", label="Weekend_Flag", values=week_flag),
        option_menu(id="holiday_flag", label="Holiday_Flag", values=holiday_flag),
        dbc.Button("Refresh", color="primary", id="button_refresh"),
    ]
    app_graph1 = dcc.Graph(id="app_graph1", style={"width": "800px", "height": "400px"})
    app_graph2 = dcc.Graph(id="app_graph2", style={"width": "800px", "height": "400px"})
    card1 = dbc.Card(controls, body=True)
    card2 = dbc.Card([dcc.Markdown(id="sql-query")], body=True)

    # Create Layout
    dash_app.layout = dbc.Container(
        fluid=True,
        children=[
            html.H1("A dash embedded application for electricity forecast in FLASK",
                    style={'color': '#ff6600',
                           'fontSize': 20, 'textAlign': 'center'}),
            html.Hr(),
            dbc.Row(
                [
                 dbc.Col([card1, card2], md=3),
                 dbc.Col([app_graph1, app_graph2], md=4),
                ]
             ),
            ],
        style={"margin": "auto"},
    )

    @dash_app.callback(
        [
            Output("app_graph1", "figure"),
            Output("app_graph2", "figure"),
            Output("sql-query", "children"),
        ],
        [Input("button_refresh", "n_clicks")],
        [
            State("states", "value"),
            State("years", "value"),
            State("week_flag", "value"),
            State("holiday_flag", "value"),
        ],
    )
    def update(n_clicks, states, years, week_flag, holiday_flag):
        if len(states) == 1:
            states = "('" + states[0] + "')"
        else:
            states = tuple(states)

        if len(years) == 1:
            years = "('" + str(years[0]) + "')"
        else:
            years = tuple(years)
        query = dedent(
            f"""
            SELECT CAST(DEMAND AS DECIMAL(10,2)) AS DEMAND, MAX_TEMP, MIN_TEMP, STATE, YEAR, Holiday_Flag, Weekened_Flag 
            FROM data 
            WHERE
            STATE IN {states} AND
            YEAR IN {years} AND
            Weekened_Flag = '{week_flag}' AND
            Holiday_Flag = '{holiday_flag}';
            """
        )
        df = connect_read_sql(query=query, engine=engine)
        connection.close()

        #data manipulation

        df1 = pd.DataFrame({'DEMAND': df.groupby(['STATE', 'YEAR'])['DEMAND'].sum()}).reset_index()

        #figures
        app_graph1 = px.line(df1, x="YEAR", y="DEMAND", color="STATE", title='Electricity Consumption in Australia')
        app_graph1.update_xaxes(type='category')
        app_graph2 = px.scatter(df, x="MAX_TEMP", y="DEMAND", color="STATE",
                                title='Scatter Plot Demand Vs Maxmimum Temperature')

        return app_graph1, app_graph2, f"```\n{query}\n```"

    return dash_app.server

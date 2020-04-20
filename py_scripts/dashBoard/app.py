import sys
path = '/Users/marinabennett/Desktop/Hertie/1._Spring_2020/Hertie-NLP-Python-Project/py_scripts/dashBoard'
sys.path.append(path)

from datetime import datetime as dt
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

from dashDataPrep import DashData


# initialize data
mentions_per_day = DashData().mentions_per_day()
mentions_day_publisher = DashData().mentions_day_publisher()
sentiment_per_day = DashData().sentiment_per_day()
sentiment_day_publisher = DashData().sentiment_day_publisher()

# initialize app
app = dash.Dash()

# dashboard layout
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.H2("MONITORING MEDIA COVERAGE OF THE PRESIDENTIAL PRIMARY"),
                        html.P(
                            """Select different days using the date picker."""
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=dt(2020, 3, 1),
                                    max_date_allowed=dt(2020, 4, 15),
                                    initial_visible_month=dt(2020, 3, 1),
                                    date=dt(2020, 3, 1).date(),
                                    display_format="MMMM D, YYYY",
                                    style={"border": "0px solid black"},
                                )
                            ],
                        ),
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="publisher-dropdown",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in mentions_day_publisher['publisher'].unique()
                                            ],
                                            placeholder="Select a publisher",
                                        )
                                    ],
                                ),
                            ],
                        ),
                        html.P(id="total-rides"),
                        html.P(id="total-rides-selection"),
                        html.P(id="date-value"),
                        dcc.Markdown(
                            children=[
                                "Sources: New York Times, Breitbart, AP, Washington Times, Buzzfeed, Politico, NBC & Fox"
                            ]
                        ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="coverage")
                    ],
                ),
            ],
        )
    ]
)


def generate_coverage_plot(publisher):
    filtered_df = mentions_day_publisher[(mentions_day_publisher["Publisher"] == publisher)]

    figure = go.Figure(
        data=[
            go.Bar(x=filtered_df["candidate"], y=filtered_df["count"])
        ],
        layout=go.Layout(
            title='Mentions Per Candidate',
            showlegend=True
        )
    )


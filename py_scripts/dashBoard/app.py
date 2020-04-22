import sys
path = '/Users/marinabennett/Desktop/Hertie/1._Spring_2020/Hertie-NLP-Python-Project/py_scripts/dashBoard'
sys.path.append(path)

from datetime import datetime as dt
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go

from dashDataPrep import DashData


# initialize data
mentions_per_day = DashData().mentions_per_day()
mentions_day_publisher = DashData().mentions_day_publisher()
sentiment_per_day = DashData().sentiment_per_day()
sentiment_day_publisher = DashData().sentiment_day_publisher()

# layout colors
colors = {
    'text': '#ffffff',
    'background_color': '#696969'
}

# initialize app
app = dash.Dash()

# layout
app.layout = html.Div([
    html.Label('Select a publisher'),

    dcc.Dropdown(
        id = 'publisher_choice',
        options = [
            {'label': i, 'value': i}
            for i in mentions_day_publisher['publisher'].unique()],
        placeholder = 'Select a publisher'
            ),

    dcc.Checklist(
        id = 'candidate_choice',
        options = [
            {'label': i, 'value': i}
            for i in mentions_day_publisher['candidate'].unique()],
        value = mentions_day_publisher['candidate'].unique()
            ),

    dcc.DatePickerRange(
        id = 'date_range',
        start_date = dt(2020, 3, 1),
        end_date_placeholder_text = 'Select the end date'
            ),

    html.H1(children =
            'MONITORING MEDIA COVERAGE OF THE PRESIDENTIAL PRIMARY',
            style = {
                'textAlign': 'center',
                'color': colors['text']
            }),

    html.Div(children =
             'Data from Breitbart, NBC, Fox News, the New York Times, AP, the Washington Times, Politico, and Buzzfeed',
             style={
                 'textAlign': 'center',
                 'color': colors['text']
             }),

    dcc.Graph(
        id = 'total_mentions_by_publisher',
        figure = {
            'data': [{
                'x': mentions_day_publisher['candidate'],
                'y': mentions_day_publisher['count'],
                'type': 'bar',
                'name': 'Chart 1'}
            ],
            'layout': {
                'title': 'Total Candidate Mentions (by Publisher)',
                'plot_bgcolor': colors['background_color'],
                'paper_bgcolor': colors['background_color'],
                'font': {
                    'color': colors['text']}
            }}),

    dcc.Graph(
        id = 'mentions_per_day',
        figure = {
            'data': [
                go.Scatter(
                    x = mentions_per_day['date'],
                    y = mentions_per_day['count'],
                    showlegend = True,
                    mode = 'lines',
                    name = i)
                    for i in mentions_per_day['candidates'].unique()],
            'layout': go.Layout(
                title = 'Candidate Mentions Over Time',
                yaxis = {'title': 'Count'})
                })

])

app.run_server()
import sys
path = '/Users/marinabennett/Desktop/Hertie/1._Spring_2020/Hertie-NLP-Python-Project/py_scripts/dashBoard'
sys.path.append(path)

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/

import plotly.express as px

from dashDataPrep import DashData


# initialize data
mentions_day_publisher = DashData().mentions_day_publisher()
# sentiment_day_publisher = DashData().sentiment_day_publisher()

# layout colors
colors = {
    'text': '#ffffff',
    'background_color': '#696969'
}

# initialize app
app = dash.Dash()

# layout
app.layout = html.Div([

    dcc.Dropdown(
        id = 'publisher_choice',
        options = [
            {'label': i, 'value': i}
            for i in mentions_day_publisher['publisher'].unique()],
        value = 'AP'
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
        min_date_allowed=mentions_day_publisher['date'].iloc[0],
        max_date_allowed=mentions_day_publisher['date'].iloc[-1],
        start_date=mentions_day_publisher['date'].iloc[0],
        end_date=mentions_day_publisher['date'].iloc[-1]
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

    html.Div(id='mentions_pub'),

    html.Div(id='mentions_day')

])

@app.callback(
    Output(component_id='mentions_pub', component_property='children'),
    [Input(component_id='publisher_choice', component_property='value'),
     Input(component_id='candidate_choice', component_property='value'),
     Input(component_id='date_range', component_property='start_date'),
     Input(component_id='date_range', component_property='end_date')]
)

@app.callback(
    Output(component_id='mentions_day', component_property='children'),
    [Input(component_id='publisher_choice', component_property='value'),
     Input(component_id='candidate_choice', component_property='value'),
     Input(component_id='date_range', component_property='start_date'),
     Input(component_id='date_range', component_property='end_date')]
)

def update_mentions_pub(publisher_choice, candidate_choice, start_date, end_date):

    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    mentions_day_publisher = DashData().mentions_day_publisher()

    mask = (start <= mentions_day_publisher['date']) & \
           (mentions_day_publisher['date'] <= end) & \
           (mentions_day_publisher['publisher'] == publisher_choice) & \
           (mentions_day_publisher['candidate'].isin(candidate_choice))
    dat_fig_mentions_pub = mentions_day_publisher.loc[mask]
    dat_fig_mentions_pub = dat_fig_mentions_pub.groupby('candidate').sum().reset_index()

    fig_mentions_pub = px.bar(dat_fig_mentions_pub,
                              x='candidate',
                              y='count',
                              title='Total Mentions By Outlet')

    return dcc.Graph(id ='total_mentions_by_publisher', figure = fig_mentions_pub)


def update_mentions_day(publisher_choice, candidate_choice, start_date, end_date):

    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    mentions_day_publisher = DashData().mentions_day_publisher()

    mask = (start <= mentions_day_publisher['date']) & \
           (mentions_day_publisher['date'] <= end) & \
           (mentions_day_publisher['publisher'] == publisher_choice) & \
           (mentions_day_publisher['candidate'].isin(candidate_choice))
    dat_fig_mentions_day = mentions_day_publisher.loc[mask]
    dat_fig_mentions_day = dat_fig_mentions_day.groupby(['candidate', 'date']).sum().reset_index()

    fig_mentions_day = px.line(dat_fig_mentions_day,
                               x="date",
                               y="count",
                               color="candidate",
                               line_group="candidate",
                               hover_name="candidate")

    return dcc.Graph(id ='total_mentions_per_day', figure = fig_mentions_day)


app.run_server()

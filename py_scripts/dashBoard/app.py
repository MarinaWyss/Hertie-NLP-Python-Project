import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px


# initialize and prep data
path = '/Users/marinabennett/Desktop/Hertie/1._Spring_2020/Hertie-NLP-Python-Project/data/'

mentions_day_publisher = pd.read_csv(path + 'mentions_data.csv')
mentions_day_publisher['date'] = pd.to_datetime(mentions_day_publisher['date'])

sentiment_day_publisher = pd.read_csv(path + 'sentiment_data.csv')
sentiment_day_publisher['date'] = pd.to_datetime(sentiment_day_publisher['date'])
sentiment_day_publisher['candidate'] = sentiment_day_publisher['candidate'].str.capitalize()

# initialize app
app = dash.Dash(
    external_stylesheets=[dbc.themes.GRID],
    assets_folder="/Users/marinabennett/Desktop/Hertie/1._Spring_2020/Hertie-NLP-Python-Project/py_scripts/dashBoard/assets")

# layout
app.layout = html.Div(
    className="container scalable",
    children=[
        html.Div(
            id="banner",
            className="banner",
            children=[
                html.H3("MONITORING MEDIA COVERAGE OF THE 2020 U.S. PRESIDENTIAL PRIMARY",
                        style={'text-align': 'center'}),
                html.H6("Data from the AP, Breitbart, Buzzfeed, Fox, NBC, the New York Times, Politico, and the Washington Times",
                        style={'text-align': 'center'})
            ],
            style={'padding': 10}
        ),
        html.Div(
            className="app_main_content",
            children=[
                dbc.Row(
                    id="dropdown-select-outer",
                    children=[
                        dbc.Col(
                            [
                                html.P("Select Date Range"),
                                dcc.DatePickerRange(
                                    id='date_range',
                                    min_date_allowed=mentions_day_publisher['date'].iloc[0],
                                    max_date_allowed=mentions_day_publisher['date'].iloc[-1],
                                    start_date=mentions_day_publisher['date'].iloc[0],
                                    end_date=mentions_day_publisher['date'].iloc[-1]
                                ),
                            ],
                            className="selector",
                        ),
                        dbc.Col(
                            [
                                html.P("Select A Publisher"),
                                dcc.Dropdown(
                                    id='publisher_choice',
                                    options=[
                                        {'label': i, 'value': i}
                                        for i in mentions_day_publisher['publisher'].unique()],
                                    value=mentions_day_publisher['publisher'].unique(),
                                    multi=True
                                ),
                            ],
                            className="selector",
                        ),
                        dbc.Col(
                            [
                                html.P("Select Candidate(s)"),
                                dcc.Dropdown(
                                    id='candidate_choice',
                                    options=[
                                        {'label': i, 'value': i}
                                        for i in mentions_day_publisher['candidate'].unique()],
                                    value=mentions_day_publisher['candidate'].unique(),
                                    multi=True
                                ),
                            ],
                            className="selector",
                        )
                    ]
                ),
                dbc.Row(
                    id="first-row",
                    className="row",
                    children=[
                        dbc.Col(id='mentions_pub'),
                        dbc.Col(id='sentiment_pub'),
                    ],
                    style={'padding': 10},
                ),
                dbc.Row(
                    id="second-row",
                    className="row",
                    children=[
                        dbc.Col(id='mentions_day'),
                    ],
                    style={'padding': 10},
                ),
                dbc.Row(
                    id="last-row",
                    className="row",
                    children=[
                        dbc.Col(id='sentiment_day'),
                    ],
                    style={'padding': 10},
                ),
            ],
        ),
    ],
)

@app.callback(
    Output(component_id='mentions_day', component_property='children'),
    [Input(component_id='publisher_choice', component_property='value'),
     Input(component_id='candidate_choice', component_property='value'),
     Input(component_id='date_range', component_property='start_date'),
     Input(component_id='date_range', component_property='end_date')]
)

def update_mentions_day(publisher_choice, candidate_choice, start_date, end_date):

    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    mask = (start <= mentions_day_publisher['date']) & \
           (mentions_day_publisher['date'] <= end) & \
           (mentions_day_publisher['publisher'].isin(publisher_choice)) & \
           (mentions_day_publisher['candidate'].isin(candidate_choice))
    dat_fig_mentions_day = mentions_day_publisher.loc[mask]
    dat_fig_mentions_day = dat_fig_mentions_day.groupby(['candidate', 'date']).sum().reset_index()

    fig_mentions_day = px.line(dat_fig_mentions_day,
                               x="date",
                               y="count",
                               color="candidate",
                               line_group="candidate",
                               hover_name="candidate",
                               title="Total Mentions Per Day",
                               template='plotly_dark')

    fig_mentions_day.update_yaxes(title_text=' ')
    fig_mentions_day.update_xaxes(tickangle=45, title_text=' ')

    return dcc.Graph(id ='total_mentions_per_day', figure = fig_mentions_day)


@app.callback(
    Output(component_id='mentions_pub', component_property='children'),
    [Input(component_id='publisher_choice', component_property='value'),
     Input(component_id='candidate_choice', component_property='value'),
     Input(component_id='date_range', component_property='start_date'),
     Input(component_id='date_range', component_property='end_date')]
)

def update_mentions_pub(publisher_choice, candidate_choice, start_date, end_date):

    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    mask = (start <= mentions_day_publisher['date']) & \
           (mentions_day_publisher['date'] <= end) & \
           (mentions_day_publisher['publisher'].isin(publisher_choice)) & \
           (mentions_day_publisher['candidate'].isin(candidate_choice))
    dat_fig_mentions_pub = mentions_day_publisher.loc[mask]
    dat_fig_mentions_pub = dat_fig_mentions_pub.groupby('candidate').sum().reset_index()

    fig_mentions_pub = px.bar(dat_fig_mentions_pub,
                              x='candidate',
                              y='count',
                              color="candidate",
                              title='Total Mentions Overall',
                              template='plotly_dark')

    fig_mentions_pub.update_yaxes(title_text=' ')
    fig_mentions_pub.update_xaxes(tickangle=45, title_text=' ')
    fig_mentions_pub.update_layout(showlegend=False)

    return dcc.Graph(id ='total_mentions_by_publisher', figure = fig_mentions_pub)


@app.callback(
    Output(component_id='sentiment_pub', component_property='children'),
    [Input(component_id='publisher_choice', component_property='value'),
     Input(component_id='candidate_choice', component_property='value'),
     Input(component_id='date_range', component_property='start_date'),
     Input(component_id='date_range', component_property='end_date')]
)

def update_sentiment_pub(publisher_choice, candidate_choice, start_date, end_date):

    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    mask = (start <= sentiment_day_publisher['date']) & \
           (sentiment_day_publisher['date'] <= end) & \
           (sentiment_day_publisher['publisher'].isin(publisher_choice)) & \
           (sentiment_day_publisher['candidate'].isin(candidate_choice))
    dat_fig_sentiment_pub = sentiment_day_publisher.loc[mask]
    dat_fig_sentiment_pub = dat_fig_sentiment_pub.loc[dat_fig_sentiment_pub['sentiment'] != 0, ]
    dat_fig_sentiment_pub = dat_fig_sentiment_pub.groupby('candidate').mean().reset_index()

    fig_sentiment_pub = px.bar(dat_fig_sentiment_pub,
                              x='candidate',
                              y='sentiment',
                              color="candidate",
                              title='Mean Sentiment Score Overall',
                              template='plotly_dark')

    fig_sentiment_pub.update_yaxes(title_text=' ')
    fig_sentiment_pub.update_xaxes(tickangle=45, title_text=' ')
    fig_sentiment_pub.update_layout(showlegend=False)

    return dcc.Graph(id ='mean_sentiment', figure = fig_sentiment_pub)


@app.callback(
    Output(component_id='sentiment_day', component_property='children'),
    [Input(component_id='publisher_choice', component_property='value'),
     Input(component_id='candidate_choice', component_property='value'),
     Input(component_id='date_range', component_property='start_date'),
     Input(component_id='date_range', component_property='end_date')]
)

def update_sentiment_day(publisher_choice, candidate_choice, start_date, end_date):

    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    mask = (start <= sentiment_day_publisher['date']) & \
           (sentiment_day_publisher['date'] <= end) & \
           (sentiment_day_publisher['publisher'].isin(publisher_choice)) & \
           (sentiment_day_publisher['candidate'].isin(candidate_choice))
    dat_fig_sentiment_day = sentiment_day_publisher.loc[mask]
    dat_fig_sentiment_day = dat_fig_sentiment_day.groupby(['candidate', 'date']).mean().reset_index()

    fig_sentiment_day = px.line(dat_fig_sentiment_day,
                               x="date",
                               y="sentiment",
                               color="candidate",
                               line_group="candidate",
                               hover_name="candidate",
                               title="Mean Sentiment Per Day",
                               template='plotly_dark')

    fig_sentiment_day.update_yaxes(title_text=' ')
    fig_sentiment_day.update_xaxes(tickangle=45, title_text=' ')

    return dcc.Graph(id ='sentiment_by_day', figure = fig_sentiment_day)


# app.run_server()

if __name__ == '__main__':
    app.run_server(debug=True)

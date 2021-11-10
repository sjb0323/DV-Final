# -*- coding: utf-8 -*-
from flask import Flask
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

import time
import pandas as pd
import datetime as dt 
import plotly.express as px
import plotly.graph_objs as go
from plotly.graph_objects import Layout

server = Flask(__name__)
app = dash.Dash(__name__, server=server,external_stylesheets=[dbc.themes.FLATLY])

daterange = pd.date_range(start=dt.datetime(2000, 1, 1)+ dt.timedelta(hours=9),end=dt.datetime(2000, 1, 2)+ dt.timedelta(hours=9),freq='S')

def unixTimeMillis(dt):
    ''' Convert datetime to unix timestamp '''
    return int(time.mktime(dt.timetuple()))

def unixToDatetime(unix):
    ''' Convert unix timestamp to datetime. '''
    return pd.to_datetime([unix],unit='s').time[0]

def getMarks(start, end, Nth=100):
    ''' Returns the marks for labeling. 
        Every Nth value will be used.
    '''

    result = {}
    for i, date in enumerate(daterange):
        if(i%Nth == 1):
            # Append value to dict
            result[unixTimeMillis(date)] = str(date.strftime('%Y-%m-%d'))
    return result

df = pd.read_csv('data/concat.csv')
userInfo_df = pd.read_csv('data/user_info.csv')

app.layout = html.Div([
    dbc.Row(
        dbc.Col(
            html.H3("Dashboard", className = "m-2"), style = {"color":"white"}
        ), className="navbar navbar-expand-lg navbar-dark bg-primary"
    ),

    dbc.Row([
        dbc.Col([
            dbc.Row(dbc.Col(html.Div(["chart1",
            dcc.Graph(id='main-graph')]),width = 12, style = {"background":"red"})),
            dbc.Row(dbc.Col(html.Div(["chart2",
            dcc.Graph(id='second-graph')]),width = 12, style = {"background":"pink"})),
        ], width = 9),

        dbc.Col([
            html.H1("Options"),
            html.H3("Selected Apps"),
            html.Div([
                dbc.Input(id="input", placeholder="Search application...", type="text"),
                html.Br(),
                html.P(id="output"),
            ]),
            
            html.H3("Selected User Traits"),
            html.H5("Gender"),
            html.Div([
                    dbc.RadioItems(
                        id="radios",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Male", "value": 1},
                            {"label": "Female", "value": 2},
                        ],
                        value=1,
                    ),
                    #html.Div(id="output"),
                ],
                className="radio-group",
            ),

            
            # html.Div(
            #     dbc.ButtonGroup(
            #         [dbc.Button("Male", id = "Male-Button"), dbc.Button("Female")]
            #     ),
            # ),

            html.H5("Neuroticism"),
            html.Div(
                dbc.ButtonGroup(
                    [dbc.Button("High"), dbc.Button("Middle"), dbc.Button("Low")]
                ),
            ),
            html.H5("Extraversion"),
            html.Div(
                dbc.ButtonGroup(
                    [dbc.Button("High"), dbc.Button("Middle"), dbc.Button("Low")]
                ),
            ),html.H5("Openness"),
            html.Div(
                dbc.ButtonGroup(
                    [dbc.Button("High"), dbc.Button("Middle"), dbc.Button("Low")]
                ),
            ),html.H5("Conscientiousness"),
            html.Div(
                dbc.ButtonGroup(
                    [dbc.Button("High"), dbc.Button("Middle"), dbc.Button("Low")]
                ),
            ),html.H5("Agreeableness"),
            html.Div(
                dbc.ButtonGroup(
                    [dbc.Button("High"), dbc.Button("Middle"), dbc.Button("Low")]
                ),
            )], width = 3, style = {"background":"blue"}
        )
    ], className ="g-2"),

    dbc.Row([
        dbc.Col(html.Div(["chart3",
        dcc.Graph(id='third-graph')]), width = 3, style = {"background":"red"}),
        dbc.Col(html.Div(["chart4",
        dcc.Graph(id='fourth-graph')]), width = 6, style = {"background":"red"}),
        dbc.Col(html.Div(["chart5",
        dcc.Graph(id='fifth-graph')]), width = 3, style = {"background":"red"}),
    ]),
    
    html.Div([
    dcc.Graph(
        id="scatter-plot",
        hoverData={'points': [{'hovertext': 'P0701'}]}
        ), 
    ],style={'width': '500px'},
    ),
    html.Div(
        [
            html.Label('From 00:00:00 to 23:59:59', id='time-range-label'),
            dcc.RangeSlider(
                id='time_slider',
                min = unixTimeMillis(daterange.min()),
                max = unixTimeMillis(daterange.max()),
                value = [unixTimeMillis(daterange.min()),
                         unixTimeMillis(daterange.max())],
            ),
        ],
        style={'margin-top': '20', 'width': '500px'}
    ),
    html.Div(
        [
            html.Label('USER ID', id='user-id-label'),
        ],
        style={'margin-top': '20', 'width': '500px'}
    ),
    html.Hr(),
    html.Div([
    dcc.Graph(
        id="polar-plot",
        ), 
    ],style={'width': '500px'},
    )
])


@app.callback(dash.dependencies.Output("output", "children"), [dash.dependencies.Input("radios", "value")])
def display_value(value):
    return f"Selected value: {value}"

#@app.callback(
    #Output(component_id="Male_button", "children"),
    #Input("component_id="Male_button")
#)
# def on_button_click(n):
#     if n is None:
#         return "Not clicked."
#     else:
#         return "Clicked {n} times."
@app.callback(
    dash.dependencies.Output('polar-plot', 'figure'),
    [dash.dependencies.Input('scatter-plot', 'hoverData')])
def update_user_Id(hoverData):
    userId=hoverData['points'][0]['hovertext']
    userNumb=int(userId[1:])

    polar_df=pd.DataFrame()

    polar_df['theta']= ['Openness','Conscientiousness','Neuroticism','Extraversion','Agreeableness']

    data_df=userInfo_df.loc[userInfo_df['UID']==userNumb]
    data=[]

    for i in range(1,6,1):
        data.append(data_df.iloc[0][i])

    polar_df['data']=data

    fig=px.line_polar(polar_df, r="data", theta="theta", range_r=[0,15], line_close=True)
    
    
    return fig


@app.callback(
    dash.dependencies.Output('user-id-label', 'children'),
    [dash.dependencies.Input('scatter-plot', 'hoverData')])
def update_user_Id(hoverData):
    userId=hoverData['points'][0]['hovertext']
    return 'user id : {}'.format(userId)
    
@app.callback(
    dash.dependencies.Output('time-range-label', 'children'),
    [dash.dependencies.Input('time_slider', 'value')])
def _update_time_range_label(year_range):
    low, high = year_range
    low=low%86400+32400
    high=(high-1)%86400+32400

    return 'From {} to {}. {}~{}'.format(unixToDatetime(year_range[0]),
                                  unixToDatetime(year_range[1]),low,high)

@app.callback(
    dash.dependencies.Output("scatter-plot", "figure"), 
    [dash.dependencies.Input("time_slider", "value")])
def update_chart(slider_range):
    low, high = slider_range
    low=low%86400
    high=(high-1)%86400
    mask = (df['timestamp'] > low) & (df['timestamp'] < high)
    scatter_df=df[mask]

    layout = Layout(plot_bgcolor='rgba(0,0,0,0)')

    fig = go.Figure(layout = layout)
    unique_y=scatter_df['name'].unique()
    fig=px.scatter(
    scatter_df,
    x=scatter_df.convertTime,          
    y=scatter_df.name,
    hover_name=scatter_df.ID
    )
    fig.update_traces(
        marker = dict(
        size = 7, 
        color = 'black', 
        symbol='line-ns',
        opacity = 0.2,
        line = dict(
            color='red',
            width=2
        )
    )
    )
    fig.update_layout(plot_bgcolor = 'rgba(0,0,0,0)')
    fig.update_yaxes(showline=True, gridwidth=7, gridcolor="#eee")

    return fig

    

if __name__ == '__main__':
    app.run_server(debug=True)

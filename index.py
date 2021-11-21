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

# Time Convert Function
def unixTimeMillis(dt):
    ''' Convert datetime to unix timestamp '''
    return int(time.mktime(dt.timetuple()))

def unixToDatetime(unix):
    ''' Convert unix timestamp to datetime. '''
    return pd.to_datetime([unix],unit='s').time[0]


# Read The Data
df = pd.read_csv('data/concat.csv')
userInfo_df = pd.read_csv('data/user_info.csv')


# Order 
# openness
# conscientiousness
# neuroticism
# extraversion
# agreeableness
Trait = [0,0,0,0,0]


app.layout = html.Div([
    dbc.Row(
        dbc.Col(
            html.H3("Dashboard", className = "m-2"), style = {"color":"white"}
        ), className="navbar navbar-expand-lg navbar-dark bg-primary"
    ),

    dbc.Row([
        dbc.Col([
            dbc.Row(
                dbc.Col(
                    html.Div(["",
                    html.Label('Selected time range : 00:00:00 ~ 23:59:59', id='time-range-label'),
                    dcc.RangeSlider(
                        id='time_slider',
                        min = unixTimeMillis(daterange.min()),
                        max = unixTimeMillis(daterange.max()),
                        value = [unixTimeMillis(daterange.min()),
                                unixTimeMillis(daterange.max())],
                        marks={
                            unixTimeMillis(daterange.min()): {'label': '0H'},
                            unixTimeMillis(daterange.min()) + 3600 * 2: {'label': '2H'},
                            unixTimeMillis(daterange.min()) + 3600 * 4: {'label': '4H'},
                            unixTimeMillis(daterange.min()) + 3600 * 6: {'label': '6H'},
                            unixTimeMillis(daterange.min()) + 3600 * 8: {'label': '8H'},
                            unixTimeMillis(daterange.min()) + 3600 * 10: {'label': '10H'},
                            unixTimeMillis(daterange.min()) + 3600 * 12: {'label': '12H'},
                            unixTimeMillis(daterange.min()) + 3600 * 14: {'label': '14H'},
                            unixTimeMillis(daterange.min()) + 3600 * 16: {'label': '16H'},
                            unixTimeMillis(daterange.min()) + 3600 * 18: {'label': '18H'},
                            unixTimeMillis(daterange.min()) + 3600 * 20: {'label': '20H'},
                            unixTimeMillis(daterange.min()) + 3600 * 22: {'label': '22H'},
                            unixTimeMillis(daterange.max()): {'label': '24H'},
                        }
                    ),
                    dcc.Graph(id='main-graph')
                    ]),
                width = 12, style = {"background":"white"}
                )
            ),
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

            html.H5("Openness"),
            html.Div(
                dbc.ButtonGroup(
                    [dbc.Button("High", id="o_h"), dbc.Button("Middle", id="o_m"), dbc.Button("Low", id="o_l")]
                ),
            ),html.H5("Conscientiousness"),
            html.Div(
                dbc.ButtonGroup(
                    [dbc.Button("High", id="c_h"), dbc.Button("Middle", id="c_m"), dbc.Button("Low", id="c_l")]
                ),
            ),html.H5("Neuroticism"),
            html.Div(
                dbc.ButtonGroup(
                    [dbc.Button("High", id="n_h"), dbc.Button("Middle", id="n_m"), dbc.Button("Low", id="n_l")]
                ),
            ),
            html.H5("Extraversion"),
            html.Div(
                dbc.ButtonGroup(
                    [dbc.Button("High", id="e_h"), dbc.Button("Middle", id="e_m"), dbc.Button("Low", id="e_l")]
                ),
            ),html.H5("Agreeableness"),
            html.Div(
                dbc.ButtonGroup(
                    [dbc.Button("High", id="a_h"), dbc.Button("Middle", id="a_m"), dbc.Button("Low", id="a_l")]
                ),
            )], width = 3, style = {"background":"blue"}
        )
    ], className ="g-2"),

    dbc.Row([
        dbc.Col(html.Div(["",
        #Pie Chart
            html.H3("Used App Time Proportion"),
            html.Div(
            [
                dcc.Graph(
                    id="pie-plot",
                ),
            ], style={'width' :'100%', 'padding' : '0'}) 
         ]), width = 3, style = {"background":"white"}),

        dbc.Col(html.Div([
        #Interaction Mark
            html.H3("Interaction Marsk in Apps by Time"),
            html.P("Each marks are results of user's interaction with package, such as response to notification"),
            html.P("Please hover at the mark to check User ID and App Name"),
            dcc.Graph(
                id="interaction-mark",
                hoverData={'points': [{'hovertext': 'P0701'}]}
            )]), width = 6),

        dbc.Col(html.Div(["",
        #Polar Chart
            html.H3("Trait of User in the Mark"),
            html.P("Hover over the line if you want more"),
            html.Div([
                html.Label('USER ID', id='user-id-label')
            ]),
            html.Div(
            [
                dbc.Button("Apply Trait to Dashboard", id='user_trait_to_dashboard')
            ]
            ),
            html.Div(
            [
                dcc.Graph(
                    id="polar-plot",
                ),
            ], style={'width' :'100%', 'padding' : '0'}), 
        ]), width = 3,  style = {"background":"white"}),
    ]),
    html.Div(
    # Time range selection part

    ),

    html.Hr(),
'''    html.Div([
    #User trait display part
        html.Div(
            [
                html.Label('USER ID', id='user-id-label'),
            ],
            style={'margin-top': '20', 'width': '500px'}
        ),
        dcc.Graph(
            id="polar-plot",
        ), 
        ],style={'width': '500px'},
    )'''
])

#
@app.callback(dash.dependencies.Output("output", "children"), [dash.dependencies.Input("radios", "value")])
def display_value(value):
    return f"Selected value: {value}"

@app.callback(
    dash.dependencies.Output('pie-plot', 'figure'),
    [dash.dependencies.Input("radios", "value")])
def update_pie(value):
    df = px.data.tips()
    fig = px.pie(df, values='tip', names='day')
    return fig

# Update polar chart based on User ID
@app.callback(
    dash.dependencies.Output('polar-plot', 'figure'),
    [dash.dependencies.Input('interaction-mark', 'hoverData')])
def update_user_Id(hoverData):
    userId=hoverData['points'][0]['hovertext']
    userNumb=int(userId[1:])

    polar_df=pd.DataFrame()

    polar_df['Trait']= ['O','C','N','E','A']

    data_df=userInfo_df.loc[userInfo_df['UID']==userNumb]
    data=[]

    for i in range(1,6,1):
        data.append(data_df.iloc[0][i])

    polar_df['Score']=data
    polar_df['Detail'] = ['openness', 'conscientiousness', 'neuroticism', 'extraversion',' agreeableness']
    polar_df['Description'] = ['openness', 'conscientiousness', 'neuroticism', 'extraversion',' agreeableness']

    fig=px.line_polar(
        polar_df, 
        r="Score", 
        theta="Trait", 
        range_r=[0,15], 
        line_close=True,
        text="Score",
        hover_data={
            'Score' : True,
            'Trait' : False,
            'Detail' : True,
        }
    )
    fig.update_traces(textposition='top center', fill='toself')
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[0,15]
            )
        ),
    )    
    
    return fig

#Update User ID from Interaction Mark Hover 
@app.callback(
    dash.dependencies.Output('user-id-label', 'children'),
    [dash.dependencies.Input('interaction-mark', 'hoverData')])
def update_user_Id(hoverData):
    userId=hoverData['points'][0]['hovertext']
    return 'This trait is from user id "{}"'.format(userId)
    
#Time Slider
@app.callback(
    dash.dependencies.Output('time-range-label', 'children'),
    [dash.dependencies.Input('time_slider', 'value')])
def _update_time_range_label(year_range):
    low, high = year_range
    low=low%86400+32400
    high=(high-1)%86400+32400

    return 'Selected time range : {} ~ {}'.format(unixToDatetime(year_range[0]),
                                  unixToDatetime(year_range[1]))

#Interaction mark
@app.callback(
    dash.dependencies.Output("interaction-mark", "figure"), 
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
    
    scatter_copy=pd.DataFrame()
    scatter_copy['Time']=scatter_df['convertTime']
    scatter_copy['App Name']=scatter_df['name']

    fig=px.scatter(
        scatter_copy,
        x=scatter_copy['Time'],          
        y=scatter_copy['App Name'],
        hover_name=scatter_df.ID,
        hover_data={
            'Time' : '|%H:%M',
            'App Name' : True
        }
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
        ),
    )
    fig.update_layout(
        plot_bgcolor = 'rgba(0,0,0,0)'
    )
    
    fig.update_yaxes(showline=True, gridwidth=7, gridcolor="#eee")

    return fig




if __name__ == '__main__':
    app.run_server(debug=True)

# -*- coding: utf-8 -*-
from dash.exceptions import PreventUpdate
from flask import Flask
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import time
from numpy import NaN
import pandas as pd
import datetime as dt 
import plotly.express as px
import plotly.graph_objs as go
import json
from plotly.graph_objects import Layout

server = Flask(__name__)
stylesheets = [dbc.themes.FLATLY, dbc.icons.BOOTSTRAP,"/static/style.css"]
app = dash.Dash(__name__, server=server, external_stylesheets = stylesheets)

applist = ["KaKaotalk", "Facebook", "Instagram", "NAVER", "Chrome", "Youtube", "Messenger"] 
AppColorDict = {"KaKaotalk" : "yellow", "Facebook" : "Blue", "Instagram" : "Pink", "NAVER" : "green", "Chrome" : "white", "Youtube" : "red", "Messenger" : "black"}

daterange = pd.date_range(start=dt.datetime(2000, 1, 1)+ dt.timedelta(hours=9),end=dt.datetime(2000, 1, 2)+ dt.timedelta(hours=9),freq='S')

selectedApp = []
k = []


def make_button(value):
    t = html.Div(children = [
                dbc.Button([
                    value, html.I(className="bi bi-x-octagon m-2")], value = value, n_clicks = 0, style = { "color" : "white", "background": AppColorDict.get(value, "white"), "margin": "5px"}
                    )], id = "{}closebutton".format(value), style= {"display" : "none"})
    return t

for a in AppColorDict.keys():
    k.append(make_button(a))

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

#적용할 애들
applyUserInfo = userInfo_df

# Order 
# openness
# conscientiousness
# neuroticism
# extraversion
# agreeableness
global user_trait 
global recent_trait 
user_trait = [0,0,0,0,0,0,'','']
recent_trait = [0,0,0,0,0,0,'','']

o_button = ['Low','Low','Low','Low','Low','Low','Low','Low','Low','Mid','Mid','Mid','High','High','High','High']
c_button = ['Low','Low','Low','Low','Low','Low','Low','Low','Low','Mid','Mid','Mid','High','High','High','High']
n_button = ['Low','Low','Low','Low','Low','Low','Mid','Mid','Mid','Mid','High','High','High','High','High','High']
e_button = ['Low','Low','Low','Low','Low','Low','Low','Low','Mid','Mid','Mid','High','High','High','High','High']
a_button = ['Low','Low','Low','Low','Low','Low','Low','Low','Low','Low','Mid','Mid','High','High','High','High']

#Button
o_dict = { 'Low' : True , 'Mid' : True, 'High' : True}
c_dict = { 'Low' : True , 'Mid' : True, 'High' : True}
n_dict = { 'Low' : True , 'Mid' : True, 'High' : True}
e_dict = { 'Low' : True , 'Mid' : True, 'High' : True}
a_dict = { 'Low' : True , 'Mid' : True, 'High' : True}
g_dict = { 'Male' : True , 'Female' : True}


app.layout = html.Div([ 
    html.Div([
        html.Div([                   
            dbc.Row(
                dbc.Col(
                    html.H3("Dashboard", className = "m-2"), style = {"color":"white"}
                ), className="navbar navbar-expand-lg navbar-dark bg-primary"
            ),
            dbc.Row(dbc.Col(html.Div(["chart2",
            dcc.Graph(id='second-graph')]),width = 12, style = {"background":"pink"})),
        ], width = 9),

        dbc.Col([
            html.H1("Options"),
            html.H3("Selected Apps"),
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        options=[
                            {'label': i, 'value': i} for i in applist
                        ],
                        id = 'searchinput',
                        placeholder = 'Select Apps...',
                        clearable = False,
                        multi = True
                    ),
                    html.Div(id='searchoutput', children = k)
                ])
            ]),

            #Time Range
            dbc.Row([
                dbc.Col([
                    dbc.Row(
                        dbc.Col(
                            html.Div(["",
                            html.H5("Select Time"),
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
                            html.Label('Selected time range : 00:00:00 ~ 23:59:59', id='time-range-label'),
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
                    
                    #Search
                    html.H3("Selected Apps"),
                    html.Div([
                        html.Div([
                            dcc.Dropdown(
                                options=[
                                    {'label': i, 'value': i} for i in applist
                                ],
                                id = 'searchinput',
                                placeholder = 'Select Apps...',
                                clearable = False,
                                multi = True
                            ),
                            html.Div(id='searchoutput', children = k)
                        ])
                    ]),                  
                      
                    html.H5("Selected User Traits"),
                    html.Div([
                        dbc.Button("Select All", id='select-all', n_clicks=0),
                    ]),
                    html.H5("Gender"),
                    html.Div([
                        dbc.Checklist(
                            id="checklist-G",
                            options=[
                                {"label": "Male", "value": "Male"},
                                {"label": "Female", "value": "Female"},
                            ],
                            labelStyle={"display": "block"},
                            value=["Male","Female"],
                            inline=True,
                        ),
                    ]),

                    
                    # html.Div(
                    #     dbc.ButtonGroup(
                    #         [dbc.Button("Male", id = "Male-Button"), dbc.Button("Female")]
                    #     ),
                    # ),

                    html.Br(),
                    html.H5("Openness"),
                    html.Div(
                        dbc.Checklist(
                            id="checklist-O",
                            options=[
                                {"label": "High", "value": "High"},
                                {"label": "Middle", "value": "Mid"},
                                {"label": "Low", "value": "Low"},
                            ],
                            labelStyle={"display": "block"},
                            value=["High","Mid","Low"],
                            inline=True,
                        ),
                    ),
                    html.Br(),
                    html.H5("Conscientiousness"),
                    html.Div(
                        dbc.Checklist(
                            id="checklist-C",
                            options=[
                                {"label": "High", "value": "High"},
                                {"label": "Middle", "value": "Mid"},
                                {"label": "Low", "value": "Low"},
                            ],
                            labelStyle={"display": "block"},
                            value=["High","Mid","Low"],
                            inline=True,
                        ),
                    ),
                    html.Br(),
                    html.H5("Neuroticism"),
                    html.Div(
                        dbc.Checklist(
                            id="checklist-N",
                            options=[
                                {"label": "High", "value": "High"},
                                {"label": "Middle", "value": "Mid"},
                                {"label": "Low", "value": "Low"},
                            ],
                            labelStyle={"display": "block"},
                            value=["High","Mid","Low"],
                            inline=True,
                        ),    
                    ),
                    html.Br(),
                    html.H5("Extraversion"),
                    html.Div(
                        dbc.Checklist(
                            id="checklist-E",
                            options=[
                                {"label": "High", "value": "High"},
                                {"label": "Middle", "value": "Mid"},
                                {"label": "Low", "value": "Low"},
                            ],
                            labelStyle={"display": "block"},
                            value=["High","Mid","Low"],
                            inline=True,
                        ),
                    ),
                    html.Br(),
                    html.H5("Agreeableness"),
                    html.Div(
                        dbc.Checklist(
                            id="checklist-A",
                            options=[
                                {"label": "High", "value": "High"},
                                {"label": "Middle", "value": "Mid"},
                                {"label": "Low", "value": "Low"},
                            ],
                            labelStyle={"display": "block"},
                            value=["High","Mid","Low"],
                            inline=True,
                        ),                
                    ),
                    html.Br(),
                    html.Div([
                        html.Label('## Number of users will be displayed', id='user-number-label')
                    ]),
                    html.Div(
                    [
                        dbc.Button("Apply Trait to Dashboard", id='apply_button', n_clicks=0),
                    ]
                    )], width = 3, style = {"max-width" : "277px", "background":"white"}
                )
            ], className ="g-2"),

            dbc.Row([
                dbc.Col(html.Div(["",
                #Pie Chart
                    html.H5("Used App Time Proportion"),
                    html.Div(
                    [
                        dcc.Graph(
                            id="pie-plot",
                        ),
                    ], style={'width' :'100%', 'padding' : '0'}) 
                ]), width = 3, style = {"background":"white"}),
                
                dbc.Col(html.Div([
                #Interaction Mark
                    html.H5("Interaction Marsk in Apps by Time"),
                    html.P(["Each marks are results of user's with package, such as response to notification"]),
                    html.P("Please hover over the mark to check User ID and App Name"),
                    dcc.Graph(
                        id="interaction-mark",
                        hoverData={'points': [{'hovertext': 'P0701'}]}
                    )]), width = 6),

                dbc.Col(html.Div(["",
                #Polar Chart
                    html.H5("Trait of User in the Mark"),
                    html.P("Hover over the line if you want more"),
                    html.Div([
                        html.Label('USER ID', id='user-id-label')
                    ]),
                    html.Br(),                    
                    html.Div(
                    [
                        dbc.Button("Apply Trait to Option", id='trait_apply_button', n_clicks=0)
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
        ], style={'max-width' : '1400px', 'display' : 'flex', 'flex-direction' : 'column', 'align-self' : 'center'})
    ], style={'width' : 'device-width', 'display' : 'flex', 'flex-direction' : 'column', 'align-item' : 'center'}),
])


# @app.callback(dash.Output('facebookclosebutton', 'style'), [dash.Input('searchinput','value'),dash.Input('facebookclosebutton','n_clicks')])
# def destroy_searchoutput1(value, n_clicks):
#     global k
#     changed_id = [p for p in dash.callback_context.triggered[0]['prop_id'].split(".")]
    
#     print(value)
#     if 'facebookclosebutton' in changed_id:
#         return {"display" : "none"}
#     if "facebook" in value:
#         return {"display" : "inline-block"}
#     return {"display" : "none"}


applist = ["KaKaotalk", "Facebook", "Instagram", "NAVER", "Chrome", "Youtube", "Messenger"] 

@app.callback(dash.Output('KaKaotalkclosebutton', 'style'), [dash.Input('searchinput','value'),dash.Input('KaKaotalkclosebutton','n_clicks')])
def destroy_searchoutput2(value, n_clicks):
    global selectedApp
    changed_id = [p for p in dash.callback_context.triggered[0]['prop_id'].split(".")]
    if 'KaKaotalkclosebutton' in changed_id:
        return {"display" : "none"}
    if 'KaKaotalk' in value:
        selectedApp = value
        return {"display" : "inline-block"}
    return {"display" : "none"}

@app.callback(dash.Output('Facebookclosebutton', 'style'), [dash.Input('searchinput','value'),dash.Input('Facebookclosebutton','n_clicks')])
def destroy_searchoutput2(value, n_clicks):
    global selectedApp
    changed_id = [p for p in dash.callback_context.triggered[0]['prop_id'].split(".")]
    if 'Facebookclosebutton' in changed_id:
        return {"display" : "none"}
    if 'Facebook' in value:
        selectedApp = value
        return {"display" : "inline-block"}
    return {"display" : "none"}

@app.callback(dash.Output('Instagramclosebutton', 'style'), [dash.Input('searchinput','value'),dash.Input('Instagramclosebutton','n_clicks')])
def destroy_searchoutput2(value, n_clicks):
    global selectedApp
    changed_id = [p for p in dash.callback_context.triggered[0]['prop_id'].split(".")]
    if 'Instagramclosebutton' in changed_id:
        return {"display" : "none"}
    if 'Instagram' in value:
        selectedApp = value
        return {"display" : "inline-block"}
    return {"display" : "none"}

@app.callback(dash.Output('NAVERclosebutton', 'style'), [dash.Input('searchinput','value'),dash.Input('NAVERclosebutton','n_clicks')])
def destroy_searchoutput2(value, n_clicks):
    global selectedApp
    changed_id = [p for p in dash.callback_context.triggered[0]['prop_id'].split(".")]
    if 'NAVERclosebutton' in changed_id:
        return {"display" : "none"}
    if 'NAVER' in value:
        selectedApp = value
        return {"display" : "inline-block"}
    return {"display" : "none"}

@app.callback(dash.Output('Chromeclosebutton', 'style'), [dash.Input('searchinput','value'),dash.Input('Chromeclosebutton','n_clicks')])
def destroy_searchoutput2(value, n_clicks):
    global selectedApp
    changed_id = [p for p in dash.callback_context.triggered[0]['prop_id'].split(".")]
    if 'Chromeclosebutton' in changed_id:
        return {"display" : "none"}
    if 'Chrome' in value:
        selectedApp = value
        return {"display" : "inline-block"}
    return {"display" : "none"}

@app.callback(dash.Output('Youtubeclosebutton', 'style'), [dash.Input('searchinput','value'),dash.Input('Youtubeclosebutton','n_clicks')])
def destroy_searchoutput2(value, n_clicks):
    global selectedApp
    changed_id = [p for p in dash.callback_context.triggered[0]['prop_id'].split(".")]
    if 'Youtubeclosebutton' in changed_id:
        return {"display" : "none"}
    if 'Youtube' in value:
        selectedApp = value
        return {"display" : "inline-block"}
    return {"display" : "none"}

@app.callback(dash.Output('Messengerclosebutton', 'style'), [dash.Input('searchinput','value'),dash.Input('Messengerclosebutton','n_clicks')])
def destroy_searchoutput2(value, n_clicks):
    global selectedApp
    changed_id = [p for p in dash.callback_context.triggered[0]['prop_id'].split(".")]
    if 'Messengerclosebutton' in changed_id:
        return {"display" : "none"}
    if 'Messenger' in value:
        selectedApp = value
        return {"display" : "inline-block"}
    return {"display" : "none"}



@app.callback(dash.Output('searchinput','value'), [dash.Input('KaKaotalkclosebutton','n_clicks'), dash.Input('Facebookclosebutton','n_clicks'), dash.Input('Instagramclosebutton','n_clicks'), dash.Input('NAVERclosebutton','n_clicks'), dash.Input('Chromeclosebutton','n_clicks'), dash.Input('Youtubeclosebutton','n_clicks'), dash.Input('Messengerclosebutton','n_clicks')])
def destroy_searchoutput2(n_clicks1, n_clicks2, n_clicks3, n_clicks4, n_clicks5, n_clicks6, n_clicks7):
    changed_id = [p for p in dash.callback_context.triggered[0]['prop_id'].split(".")]
    if n_clicks1 == 0 and n_clicks2 == 0 and n_clicks3 == 0 and n_clicks4 == 0 and n_clicks5 == 0 and n_clicks6 == 0 and n_clicks7 == 0:
        raise PreventUpdate
    if 'KaKaotalkclosebutton' in changed_id:
        selectedApp.remove("KaKaotalk")
    elif 'Facebookclosebutton' in changed_id:
        selectedApp.remove("Facebook")
    elif 'Instagramclosebutton' in changed_id:
        selectedApp.remove("Instagram")
    elif 'NAVERclosebutton' in changed_id:
        selectedApp.remove("NAVER")
    elif 'Chromeclosebutton' in changed_id:
        selectedApp.remove("Chrome")
    elif 'Youtubeclosebutton' in changed_id:
        selectedApp.remove("Youtube")
    elif 'Messengerclosebutton' in changed_id:
        selectedApp.remove("Messenger")
    return selectedApp

# @app.callback(dash.dependencies.Output("output", "children"), [dash.dependencies.Input("radios", "value")])
# def display_value(value):
#     return f"Selected value: {value}"

@app.callback(
    dash.dependencies.Output('pie-plot', 'figure'),
    [dash.dependencies.Input("checklist-G", "value")])
def update_pie(value):
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    df = px.data.tips()
    fig = px.pie(df, values='tip', names='day')
    fig.update_layout(
        margin=dict(b=0, l=0, r=0, t=80)
    )        
    return fig

# Update polar chart based on User ID
@app.callback(
    dash.dependencies.Output('polar-plot', 'figure'),
    [dash.dependencies.Input('interaction-mark', 'hoverData')])
def update_user_Id(hoverData):
    global recent_trait
    
    userId=hoverData['points'][0]['hovertext']
    userNumb=int(userId[1:])

    polar_df=pd.DataFrame()

    polar_df['Trait']= ['O','C','N','E','A']

    data_df=userInfo_df.loc[userInfo_df['UID']==userNumb]
    data=[]

    for i in range(0,8,1):
        data.append(data_df.iloc[0][i])

    polar_df['Score']=data[1:6]
    recent_trait=data

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
        margin=dict(b=100, l=20, r=20, t=20)
    )    
    
    return fig

#Update User ID from Interaction Mark Hover 
@app.callback(
    dash.dependencies.Output('user-id-label', 'children'),
    [dash.dependencies.Input('interaction-mark', 'hoverData')])
def update_user_Id(hoverData):
    userId=hoverData['points'][0]['hovertext']
    return 'This trait is from user id : {}'.format(userId)
    
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
        plot_bgcolor = 'rgba(0,0,0,0)',
        margin=dict(b=100, l=20, r=20, t=0)
    )
    
    fig.update_yaxes(showline=True, gridwidth=7, gridcolor="#eee")

    return fig



#Connect to O
global check_click
global select_check
global select_all
check_click=0
select_check=0
select_all= [0,0,0,0,0,0]
@app.callback(
    dash.dependencies.Output("checklist-O", "value"),
    dash.dependencies.Input("select-all", "n_clicks"),
    dash.dependencies.Input("trait_apply_button", "n_clicks"))
def change_values(alls,n_clicks):
    global user_trait
    global recent_trait
    global check_click
    global select_all
    if(n_clicks == 0 ) : return ["High","Low","Mid"]

    if(alls > select_all[0]) : 
        select_all[0]=alls
        return ["High","Low","Mid"]

    if(n_clicks > check_click ) :
        user_trait=recent_trait
        check_click=n_clicks
    print(recent_trait)
    print(user_trait)
    if( user_trait[1]<=9 ) : 

        return ["Low"]
    elif( user_trait[1]<=11 ) :

        return ["Mid"]
    else :

        return ["High"]

#Connect to C
@app.callback(
    dash.dependencies.Output("checklist-C", "value"), 
    dash.dependencies.Input("select-all", "n_clicks"),
    dash.dependencies.Input("trait_apply_button", "n_clicks"))
def change_values(alls, n_clicks):
    global user_trait
    global recent_trait
    global check_click
    global select_all
    if(n_clicks == 0 ) : return ["High","Low","Mid"]

    if(alls > select_all[1]) : 
        select_all[1]=alls
        return ["High","Low","Mid"]

    if(n_clicks > check_click ) :
        user_trait=recent_trait
        check_click=n_clicks
    print(recent_trait)
    print(user_trait)
    if( user_trait[2]<=9 ) : 

        return ["Low"]
    elif( user_trait[2]<=11 ) :

        return ["Mid"]
    else :

        return ["High"]

#Connect to N
@app.callback(
    dash.dependencies.Output("checklist-N", "value"), 
    dash.dependencies.Input("select-all", "n_clicks"),
    dash.dependencies.Input("trait_apply_button", "n_clicks"))
def change_values(alls, n_clicks):
    global user_trait
    global recent_trait
    global check_click
    global select_all
    if(n_clicks == 0 ) : return ["High","Low","Mid"]

    if(alls >  select_all[2]) : 
        select_all[2]=alls
        return ["High","Low","Mid"]

    if(n_clicks > check_click ) :
        user_trait=recent_trait
        check_click=n_clicks
    print(recent_trait)
    print(user_trait)
    if( user_trait[3]<=6 ) : 

        return ["Low"]
    elif( user_trait[3]<=9 ) :

        return ["Mid"]
    else :

        return ["High"]
        
#Connect to E
@app.callback(
    dash.dependencies.Output("checklist-E", "value"), 
    dash.dependencies.Input("select-all", "n_clicks"),
    dash.dependencies.Input("trait_apply_button", "n_clicks"))
def change_values(alls, n_clicks):
    global user_trait
    global recent_trait
    global check_click
    global select_all
    if(n_clicks == 0 ) : return ["High","Low","Mid"]

    if(alls > select_all[3]) : 
        select_all[3]=alls
        return ["High","Low","Mid"]

    if(n_clicks > check_click ) :
        user_trait=recent_trait
        check_click=n_clicks
    print(recent_trait)
    print(user_trait)
    if( user_trait[4]<=7 ) : 

        return ["Low"]
    elif( user_trait[4]<=10 ) :

        return ["Mid"]
    else :

        return ["High"]
        
#Connect to A
@app.callback(
    dash.dependencies.Output("checklist-A", "value"), 
    dash.dependencies.Input("select-all", "n_clicks"),
    dash.dependencies.Input("trait_apply_button", "n_clicks"))
def change_values(alls, n_clicks):
    global user_trait
    global recent_trait
    global check_click
    global select_all
    if(n_clicks == 0 ) : return ["High","Low","Mid"]

    if(alls > select_all[4]) : 
        select_all[4]=alls
        return ["High","Low","Mid"]

    if(n_clicks > check_click ) :
        user_trait=recent_trait
        check_click=n_clicks
    print(recent_trait)
    print(user_trait)
    
    if( user_trait[5]<=9 ) : 

        return ["Low"]
    elif( user_trait[5]<=11 ) :

        return ["Mid"]
    else :

        return ["High"]

#Connect to Gender
@app.callback(
    dash.dependencies.Output("checklist-G", "value"), 
    dash.dependencies.Input("select-all", "n_clicks"),
    dash.dependencies.Input("trait_apply_button", "n_clicks"))
def change_values(alls, n_clicks):
    global user_trait
    global recent_trait
    global check_click
    global select_all
    if(n_clicks == 0 ) : return ["Male","Female"]

    if(alls > select_all[5]) : 
        select_all[5]=alls
        return ["High","Low","Mid"]

    print(recent_trait)
    print(user_trait)
    
    if( user_trait[7]=='M' ) : 

        return ["Male"]
    else :

        return ["Female"]



@app.callback(
    dash.dependencies.Output("user-number-label", "children"),
    dash.dependencies.Input("apply_button", "n_clicks"),
    dash.dependencies.Input("checklist-O", "value"),
    dash.dependencies.Input("checklist-C", "value"),
    dash.dependencies.Input("checklist-N", "value"),
    dash.dependencies.Input("checklist-E", "value"),
    dash.dependencies.Input("checklist-A", "value"),
    dash.dependencies.Input("checklist-G", "value"),
    dash.dependencies.Input("select-all", "n_clicks"))
def change_values(n_clicks, o, c, n, e, a, g, s_n_clicks):
    global user_trait
    global recent_trait
    global applyUserInfo
    global check_click
    global select_check
    global o_dict
    global c_dict
    global n_dict
    global e_dict
    global a_dict
    global g_dict
    print(1)
    if(s_n_clicks > select_check ) :
        o_dict = { 'Low' : True , 'Mid' : True, 'High' : True}
        c_dict = { 'Low' : True , 'Mid' : True, 'High' : True}
        n_dict = { 'Low' : True , 'Mid' : True, 'High' : True}
        e_dict = { 'Low' : True , 'Mid' : True, 'High' : True}
        a_dict = { 'Low' : True , 'Mid' : True, 'High' : True}
        g_dict = { 'Male' : True , 'Female' : True}
        select_check=s_n_clicks
        print(o_dict)
    else :
        for i in ["Low","Mid","High"] :
            if i in o :
                o_dict[i]=True
            else : 
                o_dict[i]=False
        
        for i in ["Low","Mid","High"] :
            if i in c :
                c_dict[i]=True
            else : 
                c_dict[i]=False

        for i in ["Low","Mid","High"] :
            if i in n :
                n_dict[i]=True
            else : 
                n_dict[i]=False

        for i in ["Low","Mid","High"] :
            if i in e :
                e_dict[i]=True
            else : 
                e_dict[i]=False

        for i in ["Low","Mid","High"] :
            if i in a :
                a_dict[i]=True
            else : 
                a_dict[i]=False

        for i in ["Male","Female"] :
            if i in g :
                g_dict[i]=True
            else : 
                g_dict[i]=False
                
            

    filter=pd.DataFrame(columns=['UID',	'Openness',	'Conscientiousness',	'Neuroticism',	'Extraversion',	'Agreeableness',	'Age', 'Gender'])

    for  index, row in userInfo_df.iterrows() :
        o1=o_button[row['Openness']]
        c1=c_button[row['Conscientiousness']]
        n1=n_button[row['Neuroticism']]
        e1=e_button[row['Extraversion']]
        a1=a_button[row['Agreeableness']]
        if(o_dict[o1] and c_dict[c1] and n_dict[n1] and e_dict[e1] and a_dict[a1]) :
            row_series = pd.Series(list(row), index=filter.columns)
            filter = filter.append(row_series, ignore_index=True)
 
    if(n_clicks > check_click ) :
        applyUserInfo=filter
        user_trait=recent_trait
        check_click=n_clicks

    print(len(applyUserInfo))
    print(len(filter))
    return "{} users will be displayed".format(len(filter))


########
#Search#

@app.callback(dash.Output('KaKaotalkclosebutton', 'style'), [dash.Input('searchinput','value'),dash.Input('KaKaotalkclosebutton','n_clicks')])
def destroy_searchoutput2(value, n_clicks):
    global selectedApp
    changed_id = [p for p in dash.callback_context.triggered[0]['prop_id'].split(".")]
    if 'KaKaotalkclosebutton' in changed_id:
        return {"display" : "none"}
    if 'KaKaotalk' in value:
        selectedApp = value
        return {"display" : "inline-block"}
    return {"display" : "none"}

@app.callback(dash.Output('Facebookclosebutton', 'style'), [dash.Input('searchinput','value'),dash.Input('Facebookclosebutton','n_clicks')])
def destroy_searchoutput2(value, n_clicks):
    global selectedApp
    changed_id = [p for p in dash.callback_context.triggered[0]['prop_id'].split(".")]
    if 'Facebookclosebutton' in changed_id:
        return {"display" : "none"}
    if 'Facebook' in value:
        selectedApp = value
        return {"display" : "inline-block"}
    return {"display" : "none"}

@app.callback(dash.Output('Instagramclosebutton', 'style'), [dash.Input('searchinput','value'),dash.Input('Instagramclosebutton','n_clicks')])
def destroy_searchoutput2(value, n_clicks):
    global selectedApp
    changed_id = [p for p in dash.callback_context.triggered[0]['prop_id'].split(".")]
    if 'Instagramclosebutton' in changed_id:
        return {"display" : "none"}
    if 'Instagram' in value:
        selectedApp = value
        return {"display" : "inline-block"}
    return {"display" : "none"}

@app.callback(dash.Output('NAVERclosebutton', 'style'), [dash.Input('searchinput','value'),dash.Input('NAVERclosebutton','n_clicks')])
def destroy_searchoutput2(value, n_clicks):
    global selectedApp
    changed_id = [p for p in dash.callback_context.triggered[0]['prop_id'].split(".")]
    if 'NAVERclosebutton' in changed_id:
        return {"display" : "none"}
    if 'NAVER' in value:
        selectedApp = value
        return {"display" : "inline-block"}
    return {"display" : "none"}

@app.callback(dash.Output('Chromeclosebutton', 'style'), [dash.Input('searchinput','value'),dash.Input('Chromeclosebutton','n_clicks')])
def destroy_searchoutput2(value, n_clicks):
    global selectedApp
    changed_id = [p for p in dash.callback_context.triggered[0]['prop_id'].split(".")]
    if 'Chromeclosebutton' in changed_id:
        return {"display" : "none"}
    if 'Chrome' in value:
        selectedApp = value
        return {"display" : "inline-block"}
    return {"display" : "none"}

@app.callback(dash.Output('Youtubeclosebutton', 'style'), [dash.Input('searchinput','value'),dash.Input('Youtubeclosebutton','n_clicks')])
def destroy_searchoutput2(value, n_clicks):
    global selectedApp
    changed_id = [p for p in dash.callback_context.triggered[0]['prop_id'].split(".")]
    if 'Youtubeclosebutton' in changed_id:
        return {"display" : "none"}
    if 'Youtube' in value:
        selectedApp = value
        return {"display" : "inline-block"}
    return {"display" : "none"}

@app.callback(dash.Output('Messengerclosebutton', 'style'), [dash.Input('searchinput','value'),dash.Input('Messengerclosebutton','n_clicks')])
def destroy_searchoutput2(value, n_clicks):
    global selectedApp
    changed_id = [p for p in dash.callback_context.triggered[0]['prop_id'].split(".")]
    if 'Messengerclosebutton' in changed_id:
        return {"display" : "none"}
    if 'Messenger' in value:
        selectedApp = value
        return {"display" : "inline-block"}
    return {"display" : "none"}



@app.callback(dash.Output('searchinput','value'), [dash.Input('KaKaotalkclosebutton','n_clicks'), dash.Input('Facebookclosebutton','n_clicks'), dash.Input('Instagramclosebutton','n_clicks'), dash.Input('NAVERclosebutton','n_clicks'), dash.Input('Chromeclosebutton','n_clicks'), dash.Input('Youtubeclosebutton','n_clicks'), dash.Input('Messengerclosebutton','n_clicks')])
def destroy_searchoutput2(n_clicks1, n_clicks2, n_clicks3, n_clicks4, n_clicks5, n_clicks6, n_clicks7):
    changed_id = [p for p in dash.callback_context.triggered[0]['prop_id'].split(".")]
    if n_clicks1 == 0 and n_clicks2 == 0 and n_clicks3 == 0 and n_clicks4 == 0 and n_clicks5 == 0 and n_clicks6 == 0 and n_clicks7 == 0:
        raise PreventUpdate
    if 'KaKaotalkclosebutton' in changed_id:
        selectedApp.remove("KaKaotalk")
    elif 'Facebookclosebutton' in changed_id:
        selectedApp.remove("Facebook")
    elif 'Instagramclosebutton' in changed_id:
        selectedApp.remove("Instagram")
    elif 'NAVERclosebutton' in changed_id:
        selectedApp.remove("NAVER")
    elif 'Chromeclosebutton' in changed_id:
        selectedApp.remove("Chrome")
    elif 'Youtubeclosebutton' in changed_id:
        selectedApp.remove("Youtube")
    elif 'Messengerclosebutton' in changed_id:
        selectedApp.remove("Messenger")
    return selectedApp






if __name__ == '__main__':
    app.run_server(debug=True)

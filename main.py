# -*- coding: utf-8 -*-
from flask import Flask
from dash.exceptions import PreventUpdate
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import time
import numpy as np
from numpy import NaN
import pandas as pd
import datetime as dt 
import plotly.express as px
import plotly.graph_objs as go
from plotly.graph_objects import Layout

server = Flask(__name__)
stylesheets = [dbc.themes.FLATLY, dbc.icons.BOOTSTRAP,"/static/style.css"]
app = dash.Dash(__name__, server=server, external_stylesheets = stylesheets)

AppColorDict = {"KaKaotalk" : ["darkorange","white"], "Facebook" : ["dodgerBlue","white"], "Instagram" : ["BlueViolet","white"], "NAVER" : ["forestgreen","white"], "Chrome" : ["darkslategrey","white"], "Youtube" : ["red","white"], "Messenger" : ["fuchsia","white"]}

daterange = pd.date_range(start=dt.datetime(2000, 1, 1)+ dt.timedelta(hours=9),end=dt.datetime(2000, 1, 2)+ dt.timedelta(hours=9),freq='S')

abcde=1
selectedApp = list(AppColorDict.keys())
k = []


def make_button(value):
    t = html.Div(children = [
                dbc.Button([
                    value, html.I(className="bi bi-x-octagon m-2")], value = value, n_clicks = 0, style = { "font-size":"0.5em","color" : AppColorDict.get(value, "white")[1], "background": AppColorDict.get(value, "white")[0], "margin": "5px"}
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

print("-")
print("-")
print("-")
print("-")
print(unixTimeMillis(daterange.min()))
print(unixTimeMillis(daterange.max()))
print("-")
print("-")
print("-")
print("-")
# Read The Data

userInfo_df = pd.read_csv('data/user_info.csv')
final_df = pd.read_csv('data/Final Data.csv')

global interaction_df
interaction_df = final_df.loc[final_df['is_interaction']==True]
interaction_df['time_id'] = pd.to_datetime(interaction_df.time_id)
interaction_df['second'] = interaction_df.time_id.values.astype(np.int64)/1000000000%86400
interaction_df['pid'] = interaction_df['pid'].map(lambda x: x.lstrip('P'))
interaction_df['pid']=pd.to_numeric(interaction_df['pid'])

final_df['time_id'] = pd.to_datetime(final_df.time_id)
final_df['second'] = final_df.time_id.values.astype(np.int64)/1000000000%86400


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
                    html.H3("App Usage Data by Time, Interaction and Trait", className = "m-2"), style = {"color":"white"}
                ), className="navbar navbar-expand-lg navbar-dark bg-primary"
            ),

            #Time Range
            dbc.Row([
                dbc.Col([
                    dbc.Row(
                        dbc.Col(
                            html.Div(["",
                            html.Br(),
                            html.H5("Select Time"),
                            dcc.RangeSlider(
                                id='time_slider',
                                min = 0,
                                max = 86400,
                                value = [0,86400],
                                marks={
                                    0: {'label': '0H'},
                                    0 + 3600 * 2: {'label': '2H'},
                                    0 + 3600 * 4: {'label': '4H'},
                                    0 + 3600 * 6: {'label': '6H'},
                                    0 + 3600 * 8: {'label': '8H'},
                                    0 + 3600 * 10: {'label': '10H'},
                                    0 + 3600 * 12: {'label': '12H'},
                                    0 + 3600 * 14: {'label': '14H'},
                                    0 + 3600 * 16: {'label': '16H'},
                                    0 + 3600 * 18: {'label': '18H'},
                                    0 + 3600 * 20: {'label': '20H'},
                                    0 + 3600 * 22: {'label': '22H'},
                                    86400: {'label': '24H'},
                                }
                            ),
                            html.Label('Selected time range : 00:00:00 ~ 23:59:59', id='time-range-label'),
                            html.Br(),
                            html.Hr(),
                            html.Br(),
                            html.H5('Overall Application Uses'),
                            dcc.Graph(id='main-graph')
                            ]),
                        width = 12, style = {"background":"white"}
                        )
                    ),
                    dbc.Row(dbc.Col(html.Div([
                    html.Br(),
                    html.Br(),
                    html.H5('Stacked Application Uses (5 minute interval'),
                    dcc.Graph(id='second-graph')]),width = 12, style = {"background":"white"})),
                ], width = 9),

                dbc.Col([
                    html.Br(),
                    
                    html.H3("Options"),
                    
                    #Search
                    html.H5("Selected Apps"),
                    html.Div([
                        html.Div([
                            dcc.Dropdown(
                                options=[
                                    {'label': i, 'value': i} for i in AppColorDict.keys()
                                ],
                                id = 'searchinput',
                                value = list(AppColorDict.keys()),
                                placeholder = 'Select Apps...',
                                clearable = False,
                                multi = True
                            ),
                            html.Div(id='searchoutput', children = k, style={"height" : "200px"})
                        ])
                    ]),
                    html.Hr(),                  
                    html.Div([  
                        html.H5("Selected User Traits"),                    
                        dbc.Button("Select All", id='select-all', n_clicks=0),
                    ]),
                    html.Br(),
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

            html.Br(),
            html.Hr(),
            html.Br(),
            dbc.Row([
                dbc.Col(html.Div(["",
                #Pie Chart
                    html.H5("Used App Time Proportion"),
                    html.P(["Proportion of app uses in the selected time interval"]),
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
                    html.P(["Marks are trace of user's interaction with package, such as response to notification"]),
                    html.P("Hover over the mark to check User ID and App Name"),
                    dcc.Graph(
                        id="interaction-mark",
                        hoverData={'points': [{'hovertext': '701'}]}
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
@app.callback(
    dash.dependencies.Output('main-graph', 'figure'),[dash.dependencies.Input("searchinput", "value"), dash.dependencies.Input("apply_button", "n_clicks"),dash.dependencies.Input("time_slider", "value")]
)
def update_main(value, n_clicks, slider_range):
    global applyUserInfo
    df_data = final_df.copy()
    low, high = slider_range
    low=low%86400
    high=(high-1)%86400

    if('KaKaotalk' in value):
        value[value.index('KaKaotalk')] = '카카오톡'
    if ('Youtube' in value):
        value[value.index('Youtube')] = 'YouTube'

    df_data = df_data.loc[df_data['appName'].isin(value)]

    mask = (df_data['second'] > low) & (df_data['second'] < high)
    df_data=df_data[mask]


    df_data = df_data[df_data['is_interaction'] == False]
    df_data['pid'] = pd.to_numeric(df_data['pid'].str[1:])
    df_data = df_data.loc[df_data["pid"].isin(applyUserInfo['UID'].unique())] 
    print("applyUserInfo-1")
    print(applyUserInfo['UID'].unique())

    df_data.sort_values('time_id', inplace=True)
    df_data['appName'].unique()
    df_grouped = df_data.groupby(['appName', 'time_id']).count()
    df_grouped.reset_index(inplace=True)


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_grouped[df_grouped['appName'] == 'Chrome']['time_id'], y=df_grouped[df_grouped['appName'] == 'Chrome']['pid'],
                        mode='lines',
                        name='Chrome',
                        marker_color=AppColorDict['Chrome'][0]))
    fig.add_trace(go.Scatter(x=df_grouped[df_grouped['appName'] == 'YouTube']['time_id'], y=df_grouped[df_grouped['appName'] == 'YouTube']['pid'],
                        mode='lines',
                        name='YouTube',
                        marker_color=AppColorDict['Youtube'][0]))
    fig.add_trace(go.Scatter(x=df_grouped[df_grouped['appName'] == '카카오톡']['time_id'], y=df_grouped[df_grouped['appName'] == '카카오톡']['pid'],
                        mode='lines',
                        name='KaKaoTalk',
                        marker_color=AppColorDict['KaKaotalk'][0]))
    fig.add_trace(go.Scatter(x=df_grouped[df_grouped['appName'] == 'Facebook']['time_id'], y=df_grouped[df_grouped['appName'] == 'Facebook']['pid'],
                        mode='lines',
                        name='Facebook',
                        marker_color=AppColorDict['Facebook'][0]))
    fig.add_trace(go.Scatter(x=df_grouped[df_grouped['appName'] == 'Instagram']['time_id'], y=df_grouped[df_grouped['appName'] == 'Instagram']['pid'],
                        mode='lines',
                        name='Instagram',
                        marker_color=AppColorDict['Instagram'][0]))
    fig.add_trace(go.Scatter(x=df_grouped[df_grouped['appName'] == 'Messenger']['time_id'], y=df_grouped[df_grouped['appName'] == 'Messenger']['pid'],
                        mode='lines',
                        name='Messenger',
                        marker_color=AppColorDict['Messenger'][0]))
    fig.add_trace(go.Scatter(x=df_grouped[df_grouped['appName'] == 'NAVER']['time_id'], y=df_grouped[df_grouped['appName'] == 'NAVER']['pid'],
                        mode='lines',
                        name='NAVER',
                        marker_color=AppColorDict['NAVER'][0]))
    fig.update_layout(
        yaxis_title="Number of Users",
        margin=dict(b=20, l=20, r=160, t=20),
        height = 385
    )

    return fig

@app.callback(
    dash.dependencies.Output('second-graph', 'figure'),[dash.dependencies.Input("searchinput", "value"),dash.dependencies.Input("apply_button", "n_clicks"), dash.dependencies.Input("time_slider", "value")]
)
def update_second(value, n_clicks, slider_range):
    global applyUserInfo
    df_data = final_df.copy()
    low, high = slider_range
    low=low%86400
    high=(high-1)%86400


    if('KaKaotalk' in value):
        value[value.index('KaKaotalk')] = '카카오톡'
    if ('Youtube' in value):
        value[value.index('Youtube')] = 'YouTube'
        
    mask = (df_data['second'] > low) & (df_data['second'] < high)
    df_data=df_data[mask]


    df_data = df_data.loc[df_data['appName'].isin(value)]
    df_data['pid'] = pd.to_numeric(df_data['pid'].str[1:])
    df_data = df_data.loc[df_data["pid"].isin(applyUserInfo['UID'].unique())] 
    print("applyUserInfo-2")
    print(applyUserInfo['UID'].unique())
    df_data.sort_values('time_id', inplace=True)
    df_data['appName'].unique()
    df_grouped = df_data.groupby(['appName', 'time_id']).count()
    df_grouped.reset_index(inplace=True)


    fig = go.Figure(data=[
        go.Bar(name='Chrome', x=df_grouped[df_grouped['appName'] == 'Chrome']['time_id'], y=df_grouped[df_grouped['appName'] == 'Chrome']['pid'], marker_color=AppColorDict['Chrome'][0]),
        go.Bar(name='YouTube', x=df_grouped[df_grouped['appName'] == 'YouTube']['time_id'], y=df_grouped[df_grouped['appName'] == 'YouTube']['pid'], marker_color=AppColorDict['Youtube'][0]),
        go.Bar(name='KakaoTalk', x=df_grouped[df_grouped['appName'] == '카카오톡']['time_id'], y=df_grouped[df_grouped['appName'] == '카카오톡']['pid'], marker_color=AppColorDict['KaKaotalk'][0]),
        go.Bar(name='Facebook', x=df_grouped[df_grouped['appName'] == 'Facebook']['time_id'], y=df_grouped[df_grouped['appName'] == 'Facebook']['pid'], marker_color=AppColorDict['Facebook'][0]),
        go.Bar(name='Instagram', x=df_grouped[df_grouped['appName'] == 'Instagram']['time_id'], y=df_grouped[df_grouped['appName'] == 'Instagram']['pid'], marker_color=AppColorDict['Instagram'][0]),
        go.Bar(name='Messenger', x=df_grouped[df_grouped['appName'] == 'Messenger']['time_id'], y=df_grouped[df_grouped['appName'] == 'Messenger']['pid'], marker_color=AppColorDict['Messenger'][0]),
        go.Bar(name='NAVER', x=df_grouped[df_grouped['appName'] == 'NAVER']['time_id'], y=df_grouped[df_grouped['appName'] == 'NAVER']['pid'], marker_color=AppColorDict['NAVER'][0])            
    ])

    fig.update_layout(barmode='stack')
    fig.update_layout(
        yaxis_title="Cumulative Number of Users",
        margin=dict(b=20, l=20, r=160, t=20),
        height = 385
    )
    return fig



#Interaction mark
@app.callback(
    dash.dependencies.Output("interaction-mark", "figure"), 
    [dash.dependencies.Input("searchinput", "value"),dash.dependencies.Input("apply_button", "n_clicks"),dash.dependencies.Input("time_slider", "value")])
def update_chart(value,a,slider_range):
    df_data = interaction_df.copy()
    low, high = slider_range
    low=low%86400
    high=(high-1)%86400
    
    filtered= pd.DataFrame()
 

    if('KaKaotalk' in value):
            value[value.index('KaKaotalk')] = '카카오톡'
    if ('Youtube' in value):
        value[value.index('Youtube')] = 'YouTube'
    
    
    df_data = interaction_df.copy()
    df_data = interaction_df.copy()
    df_data = interaction_df.copy()
    df_data = interaction_df.copy()
    df_data = interaction_df.copy()
    df_data = interaction_df.copy()
    df_data = interaction_df.copy()
    df_data = interaction_df.copy()
    df_data = interaction_df.copy()
    df_data = interaction_df.copy()
    df_data = interaction_df.copy()
    print("!!!!!")
    print(df_data['pid'].unique())
    filtered= df_data.loc[df_data["pid"].isin(applyUserInfo['UID'].unique())]
    filtered = filtered.loc[filtered['appName'].isin(value)]
    
    mask = (filtered['second'] > low) & (filtered['second'] < high)
    scatter_df=filtered[mask]

    layout = Layout(plot_bgcolor='rgba(0,0,0,0)')

    fig = go.Figure(layout = layout)
    
    scatter_copy=pd.DataFrame()
    scatter_copy['Time']=scatter_df['time_id']
    scatter_copy['App Name']=scatter_df['appName']
    fig=px.scatter(
        scatter_copy,
        x=scatter_copy['Time'],          
        y=scatter_copy['App Name'],
        hover_name=scatter_df.pid,
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


@app.callback(
    dash.dependencies.Output('pie-plot', 'figure'),
    [dash.dependencies.Input("searchinput", "value") ,dash.dependencies.Input("time_slider", "value")])
def update_pie(value,slider_range):
    df_data = final_df.copy()
    low, high = slider_range
    low=low%86400
    high=(high-1)%86400

    if('KaKaotalk' in value):
        value[value.index('KaKaotalk')] = '카카오톡'
    if ('Youtube' in value):
        value[value.index('Youtube')] = 'YouTube'

    df_data = df_data.loc[df_data['appName'].isin(value)]

    mask = (df_data['second'] > low) & (df_data['second'] < high)
    df_data=df_data[mask]


    df_data = df_data[df_data['is_interaction'] == False]
    df_data['pid'] = pd.to_numeric(df_data['pid'].str[1:])
    df_data = df_data.loc[df_data["pid"].isin(applyUserInfo['UID'].unique())] 

    df_data.sort_values('time_id', inplace=True)
    df_data['appName'].unique()
    df_grouped = df_data.groupby(['appName']).count()
    df_grouped.reset_index(inplace=True)


    
    df = px.data.tips()
    fig = px.pie(df_grouped, values='pid', names='appName', color='appName',
                 color_discrete_map={"카카오톡" : "darkorange", 
                                     "Facebook" : "dodgerBlue", 
                                     "Instagram" : "BlueViolet", 
                                     "NAVER" : "forestgreen", 
                                     "Chrome" : "darkslategrey", 
                                     "YouTube" : "red", 
                                     "Messenger" : "fuchsia"})
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.update_layout(
        showlegend = False,
        margin=dict(b=0, l=0, r=0, t=80)
    )        
    return fig
b=1

# Update polar chart based on User ID
@app.callback(
    dash.dependencies.Output('polar-plot', 'figure'),
    [dash.dependencies.Input('interaction-mark', 'hoverData'),
     dash.dependencies.Input('user-id-label', 'children')])
def update_user_Id(hoverData, value1):
    global recent_trait
    a=value1
    userId=0
    userId=hoverData['points'][0]['hovertext']
    userNumb=int(userId)

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
    print(year_range)
    low, high = year_range
    low=low%86400+32400
    high=(high-1)%86400+32400

    return 'Selected time range : {} ~ {}'.format(unixToDatetime(year_range[0]),
                                  unixToDatetime(year_range[1]))

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
    if(s_n_clicks > select_check ) :
        o_dict = { 'Low' : True , 'Mid' : True, 'High' : True}
        c_dict = { 'Low' : True , 'Mid' : True, 'High' : True}
        n_dict = { 'Low' : True , 'Mid' : True, 'High' : True}
        e_dict = { 'Low' : True , 'Mid' : True, 'High' : True}
        a_dict = { 'Low' : True , 'Mid' : True, 'High' : True}
        g_dict = { 'Male' : True , 'Female' : True}
        select_check=s_n_clicks
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
    app.server(host='0.0.0.0', port=8080, debug=True)


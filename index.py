# -*- coding: utf-8 -*-
from flask import Flask
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

server = Flask(__name__)
app = dash.Dash(__name__, server=server,external_stylesheets=[dbc.themes.FLATLY])




app.layout = html.Div([
    dbc.Row(
        dbc.Col(
            html.H3("Dashboard", className = "m-2"), style = {"color":"white"}
        ), className="navbar navbar-expand-lg navbar-dark bg-primary"
    ),

    dbc.Row([
        dbc.Col([
            dbc.Row(dbc.Col(html.Div("chart1"), width = 12, style = {"background":"red"})),
            dbc.Row(dbc.Col(html.Div("chart2"), width = 12, style = {"background":"pink"})),
        ]),

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
            html.Div(
                dbc.ButtonGroup(
                    [dbc.Button("Male"), dbc.Button("Female")]
                ),
            ),
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
        dbc.Col(html.Div("chart3"), width = 3, style = {"background":"red"}),
        dbc.Col(html.Div("chart4"), width = 6, style = {"background":"red"}),
        dbc.Col(html.Div("chart5"), width = 3, style = {"background":"red"}),
    ])

])
 


    

if __name__ == '__main__':
    app.run_server(debug=True)

# -*- coding: utf-8 -*-
from flask import Flask
from dash import dash, html, Input, Output, callback_context
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
    ])
])


@app.callback(Output("output", "children"), [Input("radios", "value")])
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

    

if __name__ == '__main__':
    app.run_server(debug=True)

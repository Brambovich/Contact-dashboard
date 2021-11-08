# pip install dash networkx pandas 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import networkx as nx
import plotly.graph_objs as go
import re
import pandas as pd
from colour import Color
from datetime import datetime
from textwrap import dedent as d
from classes import person, matchedperson, match
from classes import createclasses

import json
import ast



# import the css template, and pass the css template into dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Transaction Network"

ACCOUNT = "Thomas"
STARTDATE = "2020-05-26"
ENDDATE = "2020-05-27"
TIME = [0, 16]
YEAR = 2020


##############################################################################################################################################################
def network_graph(timerange, AccountToSearch, start_date, end_date):
    
    persons = createclasses()

    #edge1 = pd.read_csv('edge1.csv')
    #node1 = pd.read_csv('node1.csv')

    edge1 = pd.DataFrame(columns = ["from", "to", "value"])
    node1 = pd.DataFrame(columns = ["ID", "Name", "contacts"])    
    
    
    datestring = [None] * 2

    
    datestring[0] = datetime.strptime((str(start_date) + ":" + str(timerange[0])), '%Y-%m-%d:%H')
    
    datestring[1] = datetime.strptime((str(end_date) + ":" + str(timerange[1])), '%Y-%m-%d:%H')

    for person in persons.items():
        Name = person[0]
        
        for personmet in persons[Name].matchedpersons.items():
            personmetname = personmet[0]
            if not (((edge1['from'] == personmetname) & (edge1['to'] == Name)).any()):
                noofmatches = 0
                #matchdatetime = datetime.strptime(edge1['Date'][index], '%d/%m/%Y')
                #print("\n",persons[Name].matchedpersons[personmetname].matches.keys())
                for match in persons[Name].matchedpersons[personmetname].matches.items():
                    date = match[0]
                    matchdatetime = datetime.strptime(date, '%d/%m/%Y:%H.%M')
                    #print("date of match:", matchdatetime, "no of matches:", noofmatches)
                    #print((datestring[0] < matchdatetime)," EN ", (matchdatetime < datestring[1]))
                    if (datestring[0] < matchdatetime) & (matchdatetime < datestring[1]):
                        #print("             date of match:", matchdatetime, "no of matches:", noofmatches)
                        noofmatches += 1
                
                if noofmatches >= 1:
                    edge1 = edge1.append({'from': Name, 'to': personmetname, 'value': noofmatches}, ignore_index=True)  
                    
    accountSet=set()
    accountSet.update(edge1['from'].tolist())
    accountSet.update(edge1['to'].tolist())
    count = 0
    for account in accountSet:
        noofcontacts = 0
        for personmet in persons[account].matchedpersons.keys():
            noofcontacts += len(persons[account].matchedpersons[personmet].matches)
        node1 = node1.append({'ID':count, 'Name':account, 'contacts':noofcontacts}, ignore_index=True)
        print("name:", account, "ID:", count)
        count += 1
    
    

    # filter the record by datetime, to enable interactive control through the input box

    # to define the centric point of the networkx layout
    shells=[]
    shell1=[]
    shell1.append(AccountToSearch)
    shells.append(shell1)
    shell2=[]
    for ele in accountSet:
        if ele!=AccountToSearch:
            shell2.append(ele)
    shells.append(shell2)


    G = nx.from_pandas_edgelist(edge1, 'from', 'to', ['from', 'to', 'value'], create_using=nx.MultiDiGraph())
    print("SET INDEX: ", node1.set_index('Name')['contacts'].to_dict())
    
    nx.set_node_attributes(G, node1.set_index('Name')['contacts'].to_dict(), 'contacts')


    #print("Nodes:",G.nodes['Bram']['contacts'])
    # pos = nx.layout.spring_layout(G)
    # pos = nx.layout.circular_layout(G)
    # nx.layout.shell_layout only works for more than 3 nodes
    if len(shell2)>1:
        pos = nx.drawing.layout.shell_layout(G, shells)
    else:
        pos = nx.drawing.layout.spring_layout(G)
    
    for node in G.nodes:

        G.nodes[node]['pos'] = list(pos[node])


    if len(shell2)==0:
        traceRecode = []  # contains edge_trace, node_trace, middle_node_trace

        node_trace = go.Scatter(x=tuple([1]), y=tuple([1]), text=tuple([str(AccountToSearch)]), textposition="bottom center",
                                mode='markers+text',
                                marker={'size': 50, 'color': 'lightcoral'})
        traceRecode.append(node_trace)

        node_trace1 = go.Scatter(x=tuple([1]), y=tuple([1]),
                                mode='markers',
                                marker={'size': 50, 'color': 'lightcoral'},
                                opacity=0)
        traceRecode.append(node_trace1)

        figure = {
            "data": traceRecode,
            "layout": go.Layout(title='Interactive Contact Visualization', showlegend=False,
                                margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
                                xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                                yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                                height=600
                                )}
        return figure


    traceRecode = []  # contains edge_trace, node_trace, middle_node_trace
    ############################################################################################################################################################
    colors = list(Color('lightcoral').range_to(Color('darkred'), len(G.edges())))
    colors = ['rgb' + str(x.rgb) for x in colors]

    index = 0
    for edge in G.edges:
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        weight = float(G.edges[edge]['value']) / max(edge1['value']) * 10
        trace = go.Scatter(x=tuple([x0, x1, None]), y=tuple([y0, y1, None]),
                           mode='lines',
                           line={'width': weight},
                           marker={'color': 'lightcoral'},
                           line_shape='linear',
                           opacity=1)
        traceRecode.append(trace)
        index = index + 1
    ###############################################################################################################################################################
    coughcolors = []
    for node in G.nodes():
        print("  ---  ", node, "  ---")
        coughedcounter = 0
        for matchname in persons[node].matchedpersons.keys():
            print("   ",matchname)
            for matchtime in persons[node].matchedpersons[matchname].matches.keys():
                print("           ", matchtime, ": ", persons[node].matchedpersons[matchname].matches[matchtime].coughed)
                matchdatetime = datetime.strptime(matchtime, '%d/%m/%Y:%H.%M')
                if (datestring[0] < matchdatetime) & (matchdatetime < datestring[1]):
                    print("            dates match!!")
                    print("            coughed: ", persons[node].matchedpersons[matchname].matches[matchtime].coughed)
                    if (persons[node].matchedpersons[matchname].matches[matchtime].coughed) == True:
                        
                        coughedcounter = coughedcounter + 1
                        print("Counter = ", coughedcounter)
        coughcolors.append(coughedcounter)

    node_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers+text', textposition="bottom center",
    hoverinfo="text", marker={'size': 50, 'color': coughcolors, 'colorscale': 'Reds'})
    print(coughcolors)

    index = 0
    for node in G.nodes():
        
        
        x, y = G.nodes[node]['pos']
        hovertext = "Name: " + str(node) + "<br>" + "No of contacts: "
        for matched in persons[str(node)].matchedpersons.keys():
            hovertext += "<br>" + 'with ' + str(matched) + ' ' + str(len(persons[str(node)].matchedpersons[matched].matches)) + ' times'
        hovertext += "<br>" + 'Coughed: ' + str(coughcolors[index]) + ' times.'
        text = node


        
        print("COUGHED TIMES: ", coughedcounter)
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['hovertext'] += tuple([hovertext])
        node_trace['text'] += tuple([text])
        index = index + 1
        


    traceRecode.append(node_trace)
    ################################################################################################################################################################
    middle_hover_trace = go.Scatter(x=[], y=[], hovertext=[], mode='markers', hoverinfo="text",
                                    marker={'size': 20, 'color': 'LightSkyBlue'},
                                    opacity=0)

    index = 0
    for edge in G.edges:
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        hovertext = "from: " + str(G.edges[edge]['from']) + "<br>" + "To: " + str(
            G.edges[edge]['to']) + "<br>" + "value: " + str(
            G.edges[edge]['value'])
        middle_hover_trace['x'] += tuple([(x0 + x1) / 2])
        middle_hover_trace['y'] += tuple([(y0 + y1) / 2])
        middle_hover_trace['hovertext'] += tuple([hovertext])
        index = index + 1

    traceRecode.append(middle_hover_trace)
    #################################################################################################################################################################
    figure = {
        "data": traceRecode,
        "layout": go.Layout(title='Interactive Transaction Visualization', showlegend=False, hovermode='closest',
                            margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
                            xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                            yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                            height=600,
                            clickmode='event+select',
                            annotations=[
                                dict(
                                    ax=(G.nodes[edge[0]]['pos'][0] + G.nodes[edge[1]]['pos'][0]) / 2,
                                    ay=(G.nodes[edge[0]]['pos'][1] + G.nodes[edge[1]]['pos'][1]) / 2, axref='x', ayref='y',
                                    x=(G.nodes[edge[1]]['pos'][0] * 3 + G.nodes[edge[0]]['pos'][0]) / 4,
                                    y=(G.nodes[edge[1]]['pos'][1] * 3 + G.nodes[edge[0]]['pos'][1]) / 4, xref='x', yref='y',
                                    showarrow=True,
                                    arrowhead=1,
                                    arrowsize=1,
                                    arrowwidth=1,
                                    opacity=0
                                ) for edge in G.edges]
                            )}
    return figure
######################################################################################################################################################################
# styles: for right side hover/click component
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([
    #style={'textAlign': "center", 'margin-left': "300px", 'margin-right': "300px"}),
    #########################Title
    html.Div([html.H1("Contact Network Graph")],
             className="row",
             style={'textAlign': "center"}),
    #############################################################################################define the row
    html.Div(
        className="row",
        children=[
            html.Div(
                className="row",
                style={'textAlign': "center",'margin-left': "200px", 'margin-right': "200px"},
                children=[
                    dcc.Markdown(d("""
                            **Date selection**

                            Select 2 dates to make a selection.
                            """)),
                    html.Div(
                        
                        [
                        dcc.DatePickerRange(
                            id='my-date-picker-range',
                            minimum_nights = 0,
                            min_date_allowed=datetime(2020, 1, 1),
                            max_date_allowed=datetime(2020, 12, 31),
                            initial_visible_month=datetime(2020, 5, 26),
                            start_date=datetime(2020, 5, 26).date(),
                            end_date=datetime(2020, 5, 28).date()
                        ),
                        html.Div(id='output-container-date-picker-range')
                    ]),
                    dcc.Markdown(d("""
                            **Time Range To Visualize**

                            Slide the bar to define the range of times on the two seperate days.
                            """)),
                    html.Div(
                        className="twelve columns",
                        
                        children=[
                            dcc.RangeSlider(
                                id='my-range-slider',
                                min=0,
                                max=23.98,
                                step=1,
                                value=[9, 16],
                                marks={
                                    0: {'label': '0'},
                                    2: {'label': '2'},
                                    4: {'label': '4'},
                                    6: {'label': '6'},
                                    8: {'label': '8'},
                                    10: {'label': '10'},
                                    12: {'label': '12'},
                                    14: {'label': '14'},
                                    16: {'label': '16'},
                                    18: {'label': '18'},
                                    20: {'label': '20'},
                                    22: {'label': '22'},
                                    24: {'label': '24'}
                                }

                                
                            ),
                            html.Br(),
                            html.Div(id='output-container-range-slider')
                        ],
                        style={'height': '100px', 
                            'textAlign': "center",
                            }
                    ),
                ]
            ),
            ############################################middle graph component
            html.Div(
                id = 'output-graph',
                #className="twelve columns",
                children=[dcc.Graph(id="my-graph", figure=network_graph(TIME, ACCOUNT, STARTDATE, ENDDATE))],
            )
        ]
    )
])

@app.callback(
    dash.dependencies.Output('output-graph', 'children'),
    [dash.dependencies.Input('my-range-slider', 'value'),
     dash.dependencies.Input('my-graph', 'clickData'),
     dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')]
)
def update_date(value, clickData, start_date, end_date):
    TIME = value
    STARTDATE = start_date
    ENDDATE = end_date
    #ACCOUNT = 'Thomas'
    if clickData is not None:
        ACCOUNT = clickData["points"][0]['text']
    else:
        ACCOUNT = ''
    return dcc.Graph(id="my-graph", figure=network_graph(TIME, ACCOUNT, STARTDATE, ENDDATE))

#@app.callback(
#    dash.dependencies.Output('output-graph', 'children'),
#    [dash.dependencies.Input('output-graph', 'clickData')])
#def update_account(clickData):
#    if clickData is not None:
#        ACCOUNT = clickedPerson = clickData["points"][0]['text']
#    return dcc.Graph(id="my-graph", figure=network_graph(TIME, ACCOUNT, STARTDATE, ENDDATE))
#@app.callback(
#    Output(component_id='output-graph', component_property='children'),
#    [Input(component_id='input', component_property='value')]
#)
#def update_value(input_data):

if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    

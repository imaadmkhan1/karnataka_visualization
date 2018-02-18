import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import pandas as pd
import numpy as np
import plotly

app = dash.Dash(__name__)
server = app.server
app.title = 'Karnataka 2013 Elections'

app.scripts.config.serve_locally = True
# app.css.config.serve_locally = True


df = pd.read_csv('karnataka.csv')
df = df.drop('sl_no',1)
df.loc[0:20]
const_type = df['constituency_type'].unique()
const_type_list = [const_type[i] for i in range(len(const_type))]
parties = df['party'].unique()
parties_list = [parties[i] for i in range(len(parties))]
district_names = df['district_name'].unique()
district_names_list = [district_names[i] for i in range(len(district_names))]

app.layout = html.Div([
    html.H3('Karnataka 2013 Election Results Visualization', style={'text-align': 'center', 'width': '100%'},),
    html.A(html.Button('Add me on LinkedIn'),href='https://www.linkedin.com/in/imaad-mohamed-khan-218b3999/'),
    html.Label('This table contains the following columns:', style={'font-weight': 'bold'}),
    html.Label('Constituency Name, District, Winning Candidate and other columns'),
    html.Label('Constituency types:'+' '+", ".join(const_type_list)),
    html.Label('Parties:'+' '+", ".join(parties_list)), 
    html.Label('District Names:'+' '+", ".join(district_names_list)),
    dt.DataTable(
        rows=df.to_dict('records'),
        column_widths=[150,120,150,50,50,70,100, 200, 200],

        # optional - sets the order of columns
        columns=df.columns,

        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id='datatable-df'
    ),
    html.Div(id='selected-indexes'),
    dcc.Graph(
        id='graph-df'
    ),
], className="container")


@app.callback(
    Output('datatable-df', 'selected_row_indices'),
    [Input('graph-df', 'clickData')],
    [State('datatable-df', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(
    Output('graph-df', 'figure'),
    [Input('datatable-df', 'rows'),
     Input('datatable-df', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    fig = plotly.tools.make_subplots(
        rows=4, cols=1,
        subplot_titles=('Age', 'Candidate Vote Share', 'Candidate Votes','Winning Margin'),
        shared_xaxes=True)

    y = dff['party']
    color = np.array(['rgb(255,255,255)']*y.shape[0])
    #saffron
    color[y == 'BJP']='rgb(244,196, 48)'
    #purple
    color[y == 'INC']='rgb(208,156,217)'
    #black
    color[y == 'BSRCP'] = 'rgb(0,0,0)'
    #blue
    color[y == 'IND'] = 'rgb(51,153,255)'
    #brown
    color[y == 'KJP'] = 'rgb(121,64,68)'
    #green
    color[y == 'JD(S)'] = 'rgb(0,128,0)'
    #salmon
    color[y == 'KMP'] = 'rgb(250,128,114)'
    #red
    color[y == 'SP'] = 'rgb(255,64,64)'
    #yellow
    color[y == 'SKP'] = 'rgb(255,255,0)'


    #marker = {'color': ['#0084A9']*len(dff)}
 
    for i in (selected_row_indices or []):
        marker['color'][i] = '#AB821B'
    fig.append_trace({
        'x': dff['winning_candidate'],
        'y': dff['age'],
        'type': 'bar',
        'marker': dict(color=color.tolist()) 	
    }, 1, 1)
    fig.append_trace({
        'x': dff['winning_candidate'],
        'y': dff['candidate_vote_share'],
        'type': 'bar',
        'marker': dict(color=color.tolist()) 
    }, 2, 1)
    fig.append_trace({
        'x': dff['winning_candidate'],
        'y': dff['candidate_votes'],
        'type': 'bar',
        'marker': dict(color=color.tolist()) 
    }, 3, 1)
    fig.append_trace({
        'x': dff['winning_candidate'],
        'y': dff['winning_margin'],
        'type': 'bar',
        'marker': dict(color=color.tolist())
    }, 4, 1)
    fig['layout']['showlegend'] = False
    fig['layout']['height'] = 900
    fig['layout']['margin'] = {
        'l': 30,
        'r': 5,
        't': 60,
        'b': 200
    }
    fig['layout']['yaxis3']['type'] = 'log'
    return fig


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
from dash.dependencies import Input, Output
from categoryplot import dfPokemon, getPlot

color_set = ['#000000','#FCE63D']
esti_func = {
    'Count': len,
    'Sum': sum,
    'Average': np.mean,
    'Standard Deviation': np.std
}

disabledEsti = {
    'Count': True,
    'Sum': False,
    'Average': False,
    'Standard Deviation': False
}

app = dash.Dash(__name__)

def generate_table(dataframe, max_rows=10) :
    return html.Table(
         # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(str(dataframe[col][i])) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app.title = 'Dashboard Pokemon'

app.layout = html.Div(children=[
    html.H1(children='Dashboard Pokemon (dari Bronson)',className='titleDashboard'),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Pokemon Dataset', value='tab-1',children=[
            html.Div([
                html.H1('Data Pokemon', className='h1'),
                generate_table(dfPokemon)
            ])
        ]),
        dcc.Tab(label='Scatter Plot', value='tab-2',children=[
            html.Div([
                html.H1('Scatter Plot Pokemon', className='h1'),
                dcc.Graph(
                    id='scatterPlot',
                    figure={
                        'data': [
                            go.Scatter(
                                x=dfPokemon[dfPokemon['Legendary'] == col]['Attack'],
                                y=dfPokemon[dfPokemon['Legendary'] == col]['Defense'],
                                mode='markers',
                                marker=dict(color=color_set[i], size=10, line=dict(width=0.5, color='white')),
                                name=str(col)
                            ) for col, i in zip(dfPokemon['Legendary'].unique(), range(2))
                        ],
                        'layout': go.Layout(
                            xaxis= dict(title='Attack'),
                            yaxis={'title': 'Defense'},
                            margin={ 'l': 40, 'b': 40, 't': 10, 'r': 10 },
                            hovermode='closest'
                        )
                    }
                )
            ])
        ]),
        dcc.Tab(label='Categorical Plot', value='tab-3',children=[
            html.Div([
                html.H1('Categorical Plot Pokemon', className='h1'),
                html.Div(children=[
                    html.Div([
                        dcc.Dropdown(
                            id='jenisPlot',
                            options=[{'label': i.capitalize(), 'value': i} for i in ['bar','box','violin']],
                            value='bar'
                        )
                    ],className='col-6')
                ],className='row'),
                dcc.Graph(
                    id='categoricalPlot'
                )
            ])
        ]),
        dcc.Tab(label='Pie Chart', value='tab-4',children=[
            html.Div([
                html.H1('Pie Chart Pokemon', className='h1'),
                html.Div(children=[
                    html.Div([
                        html.P('Category :'),
                        dcc.Dropdown(
                            id='catFilterPie',
                            options=[{'label': i.capitalize(), 'value': i} for i in ['Generation','Legendary']],
                            value='Generation'
                        )
                    ],className='col-4'),
                    html.Div([
                        html.P('Estimator :'),
                        dcc.Dropdown(
                            id='estiFilterPie',
                            options=[{'label': i, 'value': i} for i in ['Count','Sum','Average','Standard Deviation']],
                            value='Count'
                        )
                    ],className='col-4'),
                    html.Div([
                        html.P('Column :'),
                        dcc.Dropdown(
                            id='colFilterPie',
                            options=[{'label': i, 'value': i} for i in dfPokemon.describe().drop(['#','Generation'],axis=1).columns],
                            value='Total'
                        )
                    ],className='col-4')
                ],className='row'),
                dcc.Graph(
                    id='pieChart'
                )
            ])
        ])
    ], style={
        'fontFamily': 'system-ui'
    }, content_style={
        'fontFamily': 'Arial',
        'borderBottom': '1px solid #d6d6d6',
        'borderLeft': '1px solid #d6d6d6',
        'borderRight': '1px solid #d6d6d6',
        'padding': '44px'
    })
], style={
    'maxWidth': '1200px',
    'margin': '0 auto'
})

@app.callback(
    Output(component_id='categoricalPlot', component_property='figure'),
    [Input(component_id='jenisPlot', component_property='value')]
)
def update_graph_categorical(jenisPlot):
    return {
        'data': getPlot(jenisPlot),
        'layout': go.Layout(
                    xaxis={'title': 'Generation'},
                    yaxis={'title': 'Total Stat'},
                    margin=dict(l=40,b=40,t=10,r=10),
                    # legend=dict(x=0,y=1), 
                    hovermode='closest',
                    boxmode='group',violinmode='group'
                )
    }

@app.callback(
    Output(component_id='pieChart', component_property='figure'),
    [Input(component_id='catFilterPie', component_property='value'),
    Input(component_id='estiFilterPie', component_property='value'),
    Input(component_id='colFilterPie', component_property='value')]
)
def update_graph_pie(cat,esti,col):
    listLabel = list(dfPokemon[cat].unique())
    listLabel.sort()
    return {
        'data': [
            go.Pie(
                labels=listLabel,
                values=[esti_func[esti](dfPokemon[dfPokemon[cat] == item][col]) for item in listLabel],
                textinfo='value',
                hoverinfo='label+percent',
                marker=dict(
                    # colors=color_set[hue], 
                    line=dict(color='black', width=2)
                ),
                sort=False
            )
        ],
        'layout': go.Layout(
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1}
        )
    }

@app.callback(
    Output('colFilterPie', 'disabled'),
    [Input('estiFilterPie','value')]
)
def update_ddl_col(esti) :
    return disabledEsti[esti]

if __name__ == '__main__':
    app.run_server(debug=True,port=1997)
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

dfPokemon = pd.read_csv('dataPokemon.csv')
color_set = ['#000000','#FCE63D']

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
                                marker=dict(color=color_set[i], size=10, line={'width':0.5,'color': 'white'}),
                                name=str(col)
                            ) for col, i in zip(dfPokemon['Legendary'].unique(), range(2))
                        ],
                        'layout': go.Layout(
                            xaxis= {'title': 'Attack'},
                            yaxis={'title': 'Defense'},
                            margin={ 'l': 40, 'b': 40, 't': 10, 'r': 10 },
                            hovermode='closest'
                        )
                    }
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

if __name__ == '__main__':
    app.run_server(debug=True,port=1997)
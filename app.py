import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
from plotly import tools
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

subplots_hist = {
    'All': [1,1],
    'Generation': [3,2],
    'Legendary': [1,2]
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
        ]),
        dcc.Tab(label='Histogram', value='tab-5',children=[
            html.Div([
                html.H1('Histogram Pokemon', className='h1'),
                html.Div(children=[
                    html.Div([
                        html.P('Column :'),
                        dcc.Dropdown(
                            id='colFilterHist',
                            options=[{'label': i, 'value': i} for i in dfPokemon.columns[4:11]],
                            value=dfPokemon.columns[4]
                        )
                    ],className='col-4'),
                    html.Div([
                        html.P('Category :'),
                        dcc.Dropdown(
                            id='catFilterHist',
                            options=[{'label': i, 'value': i} for i in ['All', 'Generation', 'Legendary']],
                            value='All'
                        )
                    ],className='col-4')
                ],className='row'),
                dcc.Graph(
                    id='histogramPlot'
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

@app.callback(
    Output('histogramPlot', 'figure'),
    [Input('colFilterHist','value'),
    Input('catFilterHist','value')]
)
def update_fig_hist(col,cat) :
    jmlrow,jmlcol = subplots_hist[cat][0],subplots_hist[cat][1]
    subtitles = ['All']
    if(cat != 'All') :
        subtitles = []
        for item in dfPokemon[cat].unique() :
            subtitles.append(str(item))

    fig = tools.make_subplots(rows=jmlrow, 
                            cols=jmlcol,
                            subplot_titles=subtitles)
    r,c = 1,1;
    if(cat == 'All'):
        fig.append_trace(
             go.Histogram(
                    x=dfPokemon[
                        (dfPokemon[col] > (dfPokemon[col].mean() - 2 * dfPokemon[col].std()))
                        & (dfPokemon[col] < (dfPokemon[col].mean() + 2 * dfPokemon[col].std()))
                    ][col],
                    marker=dict(
                        color="green"
                    ),
                    name="Normal " + col,
                    opacity=0.7
                ),1,1
        )
        fig.append_trace(
             go.Histogram(
                x=dfPokemon[
                    (dfPokemon[col] < (dfPokemon[col].mean() - 2 * dfPokemon[col].std()))
                    | (dfPokemon[col] > (dfPokemon[col].mean() + 2 * dfPokemon[col].std()))
                ][col],
                marker=dict(
                    color="red"
                ),
                name="Outlier " + col,
                opacity=0.7
            ),1,1
        )
        fig['layout']['xaxis'+str(1)].update(title=col.capitalize())
        fig['layout']['yaxis'+str(1)].update(title='Total Pokemon')
    else :
        for item,index in zip(dfPokemon[cat].unique(), range(1, dfPokemon[cat].nunique()+1)) :
            fig.append_trace(
                go.Histogram(
                        x=dfPokemon[
                            (dfPokemon[cat] == item)
                            & (dfPokemon[col] > (dfPokemon[col].mean() - 2 * dfPokemon[col].std()))
                            & (dfPokemon[col] < (dfPokemon[col].mean() + 2 * dfPokemon[col].std()))
                        ][col],
                        marker=dict(
                            color="green"
                        ),
                        name="Normal " + str(item) + " " + col,
                        opacity=0.7
                    ),r,c
            )
            fig.append_trace(
                go.Histogram(
                    x=dfPokemon[
                        (dfPokemon[cat] == item)
                        & ((dfPokemon[col] < (dfPokemon[col].mean() - 2 * dfPokemon[col].std()))
                        | (dfPokemon[col] > (dfPokemon[col].mean() + 2 * dfPokemon[col].std())))
                    ][col],
                    marker=dict(
                        color="red"
                    ),
                    name="Outlier " + str(item) + " " + col,
                    opacity=0.7
                ),r,c
            )
            fig['layout']['xaxis'+str(index)].update(title=col.capitalize())
            fig['layout']['yaxis'+str(index)].update(title='Total Pokemon')
            c += 1;
            # sLegend = False;
            if(c > jmlcol) :
                c = 1;
                r += 1;
    if(cat == 'Generation') :
        fig['layout'].update(height=700, width=1000,
                            title='Histogram ' + col.capitalize())
    else :
        fig['layout'].update(height=450, width=1000,
                            title='Histogram ' + col.capitalize())
    return fig

if __name__ == '__main__':
    app.run_server(debug=True,port=1997)
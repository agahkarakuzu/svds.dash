import plotly.graph_objs as go
from operator import itemgetter

def get_figure(svds,**kwargs):

    traces = []


    if 'index' in kwargs:
        idx = kwargs['index']
    else:
        idx = 0

    # List indexing here is temp. To be made more elegant
    # There is index ID and many other details to be dealt with later.

    xLabel = [svds.Correlation.Pearson.Required[idx]['xLabel'][0]][0]
    yLabel = [svds.Correlation.Pearson.Required[idx]['yLabel'][0]][0]
    xData =  [svds.Correlation.Pearson.Required[idx]['xData']][0]
    yData =  [svds.Correlation.Pearson.Required[idx]['yData']][0]

    traceName = '<b>' + xLabel + ' vs ' + yLabel + '</b>'
    xFitLine = itemgetter(*[0,1])([svds.Correlation.Pearson.Required[idx]['fitLine']][0])
    yFitLine = itemgetter(*[0,1])([svds.Correlation.Pearson.Required[idx]['fitLine']][0])

    # Deal with other cases later. load_svds may need to be modified.

    # Required field traces ------------------------------------------

    # fitLine
    traces.append(go.Scatter(
                    mode = 'lines',
                    x = xFitLine,
                    y = yFitLine,
                    line= dict(
                    color = ('rgb(255,0,0)'),
                    width = 4 ),
                    showlegend=False))
    # Scatter
    traces.append(go.Scatter(
        x= xData,
        y= yData,
        mode='markers',
        opacity=0.7,
        marker={
            'size': 20,
            'line': {'width': 0.5, 'color': 'white'},
            'color': 'blue',
        },
        name= traceName))

    # Optional field traces ------------------------------------------

    if svds.Correlation.Pearson.Optional:

        if svds.Correlation.Pearson.Optional[idx]['CILine1']:

            traces.append(go.Scatter(
            mode = 'lines',
            x = itemgetter(*[0,1])([svds.Correlation.Pearson.Optional[idx]['CILine1']][0]),
            y = itemgetter(*[2,3])(svds.Correlation.Pearson.Optional[idx]['CILine1']),
            fill = None,
            line= dict(
                color = ('rgb(0,0,0)'),
                width = 2,),
            showlegend=False
            ))

            traces.append(go.Scatter(
            mode = 'lines',
            x = itemgetter(*[0,1])([svds.Correlation.Pearson.Optional[idx]['CILine2']][0]),
            y = itemgetter(*[2,3])([svds.Correlation.Pearson.Optional[idx]['CILine2']][0]),
            fill = 'tonexty',
            fillcolor = 'rgba(0,200,0,0.2)',
            line= dict(
                color = ('rgb(0,0,0)'),
                width = 2,),
            showlegend=False
            ))


    figure={
        'data': traces,

        'layout': go.Layout(
            xaxis={'title': xLabel},
            yaxis={'title': yLabel},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

    return figure

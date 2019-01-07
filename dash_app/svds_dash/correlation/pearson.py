import plotly.graph_objs as go
from operator import itemgetter
from svds.iop_svds import update as update_dict

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
            title = 'Something here',
            xaxis={'title': xLabel},
            yaxis={'title': yLabel},
            width = 600,
            height = 600,
            autosize = False,
            showlegend = False,
            #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            #legend={'x': 0, 'y': 1},
            hovermode='closest',
            plot_bgcolor = 'rgba(240,240,240,0.95)'
        )
    }

    return figure

def get_splom_figure(svds,**kwargs):
# To get splom there are some requirements:
# i)  Have more than two vars
# ii) Segmented if available by some partition that is present in svds.Tag

    if 'partition' in kwargs and 'index' in kwargs:

        partition = kwargs['partition']
        idx = kwargs['index']

    else:
        # deal with this later
        idx = 0

    if [svds.Correlation.Pearson.Tag[0][partition]]:
        parts = set([d['SegmentID'][0] for d in svds.Correlation.Pearson.Tag])

        # Find dictionaries containing data for the idx segment
        if idx in parts:
            idxs = [i for i,_ in enumerate(svds.Correlation.Pearson.Tag) if _[partition] == [idx]]

    # Loop through idxs to get a unique list of all vectors along with their labels for splom
    dicto = {}

    for ii in idxs:
        dicto = update_dict(dicto,{svds.Correlation.Pearson.Required[ii]['xLabel'][0]:svds.Correlation.Pearson.Required[ii]['xData']})
        dicto = update_dict(dicto,{svds.Correlation.Pearson.Required[ii]['yLabel'][0]:svds.Correlation.Pearson.Required[ii]['yData']})

    splomdims = [{'label':k,'values':dicto[k]} for k in dicto]

    trace = go.Splom(dimensions = splomdims)

    trace['diagonal'].update(visible=False)
    trace['showupperhalf'] = False

    layout = go.Layout(
            title = str(partition) + ' ' + str(idx),
            dragmode = 'select',
            width = 600,
            height = 600,
            autosize = False,
            hovermode = 'closest',
            plot_bgcolor = 'rgba(240,240,240,0.95)'
            )

    axis = dict(showline=True, gridcolor="#fff", zeroline = False)

    # Had to hack here
    for ii in range(len(splomdims)):
        exec('layout.xaxis' + str(ii+1) + '= axis')
        exec('layout.yaxis' + str(ii+1) + '= axis')

    figure = dict(data=[trace],layout=layout)

    return figure

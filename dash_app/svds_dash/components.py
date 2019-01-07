def get_svds_div(svds,name):

    if name == 'Pearson.json':
        return html.Div(
        className = "row",
        children = [
        html.Div(
        className = "four columns",
        children = [dcc.Graph(
        id='pearson-scatter',
        figure=[]),

        dcc.Slider(
            id='pearson-slider',
            min=1,
            max=30,
            value=1,
            updatemode='drag',
            marks = {1:'1',10:'10',20:'20',30:'30'})
        ])
    ])


    

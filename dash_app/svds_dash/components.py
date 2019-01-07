import dash_html_components as html
import dash_core_components as dcc

def get_svds_div(svds,name):

    if name == 'Pearson.json':

        return html.Div(
        className = "row",
        children = [
        # one div
        html.Div(
        className = "two columns",
        children = [dcc.Graph(
        id='pearson-scatter',
        figure=[]),
        ]),

        # another
        html.Div(
        className = "two columns",
        children = [html.H3('Something here')]
        ),

        # another div
        html.Div(
        className = "two columns",
        children = [dcc.Graph(
        id='pearson-splom',
        figure=[]),]
        ),
        # another div
        html.Div(
        className = 'row',
        children = html.Div(
        className = 'twelve columns u-full-width',
        children = [dcc.Slider(
            id='pearson-slider',
            min=1,
            max=30,
            value=1,
            updatemode='drag',
            marks = {1:'1',10:'10',20:'20',30:'30'}),

        html.Div(
            style = {'margin-top':'40px'},
            children = [dcc.Slider(
            id='pearson-slider-2',
            min=1,
            max=10,
            value=1,
            updatemode='drag',
            marks = {1:'Seg1',5:'Seg5',10:'Seg10'})])

            ])
        )

    ])

import base64
import os
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from svds.iop_svds import load_svds
from svds.validation import SVDSValidator
import plotly.graph_objs as go
from operator import itemgetter

# To be changed.
UPLOAD_DIRECTORY = "/Users/Agah/Desktop/KuzuHub/svds.dash/dash_app/data"

# Create upload directory if not available
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Development server.
server = Flask(__name__)
app = dash.Dash(server=server)

# Serve a file from the upload directory.
@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

app.config['suppress_callback_exceptions']=True

tabs_styles = {
    'height': '44px',
    'color': '#242331',
    'text-align': 'center',
    'font-weight': 'bold',
    'box-shadow': '0px 2px 2px rgba(34,34,34,0.6)'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#242331',
    'color': 'white',
    'padding': '6px'
}


# Main.
app.layout = html.Div([
    # Div for upload component
    html.Div(
    className = 'row',

    children = [dcc.Upload(
    className = "two columns",
    id = "upload-data",
    children= html.Div(
            ["Upload"]
    ),
    style={"clear":"both",
            "position":"absolute",
            "top":"1",
            "height":"100px",
            "width":"17.2%",
            "lineHeight":"100px",
            "text-align":"center",
            "text-weight": "bold",
            "border-bottom":"solid #fbdeda 10px",
            "background-color":"rgba(255,255,255,0.5)",
            "color":"#242331",
            'background-image': 'url(https://github.com/agahkarakuzu/svds/blob/master/svds2.png?raw=true)',
            'background-size': 'contain',
            'background-repeat': 'no-repeat',
            'background-position': 'center'},
    multiple=True,

    )]),
    # Div for file check list
    html.Div(
    className = "row",
    children = [
        html.Div(className = "two columns",
        style={"margin-top":"8%",
                "width":"17.2%",
                "border-bottom":"solid #fbdeda 10px",
                "background-color":"rgba(255,255,255,0.5)",
                "color":"#242331"},
        children = [
        html.H3("File List"),
        dcc.Checklist(
            id = "check-me",
            options =[],
            values=[])
        ])
    ]),
    # Div for the tabs
    html.Div(
    className = "row",
    children = [html.Div(
    className = "offset-by-two ten columns",
    style={"position":"absolute","top":"1"},
    children = [
    dcc.Tabs(id="my-tabs",value=[],children=[],style=tabs_styles),
    html.Div(id='tab-output',
             style= {"margin-right":"5px"}
                            )
    ])
    ])
                    ])


# Decode and store a file uploaded with Plotly Dash.
def save_file(name, content):
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

# List the files in the upload directory.
def uploaded_files():
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path) and filename != '.DS_Store':
            files.append(filename)
    return files

def file_download_link(filename):
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)

# This callback is to list files loaded by dcc.Upload
# Only SVDS valid files are going to be displayed in checkbox list.
@app.callback(
    Output("check-me", "options"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return {'label':'No files yet!','value':"Empty"}
    else:
        svds_names = load_svds(UPLOAD_DIRECTORY)[0]
        return [{'label':filename,'value':filename} for filename in svds_names]

# Dynamically populate dcc.Tabs each time a file is selected.
@app.callback(
    Output('my-tabs','children'),
    [Input('check-me','values')]
)
def update_tabs(value):
    if value:
        return [dcc.Tab(label=x,value = x,style=tab_style, selected_style=tab_selected_style) for x in value]
    else:
        return dcc.Tab(label = 'Welcome to qMRLab Dash! Please upload your files to start.',
        value = 'idle',style=tab_style, selected_style=tab_selected_style)

# Fill out tab content depending on its SVDS family::type
@app.callback(Output('tab-output', 'children'),
              [Input('my-tabs', 'value')])
def render_content(tab):
    svds_content = load_svds(UPLOAD_DIRECTORY)[1]
    if tab == 'idle':
        return html.Div(
            children=[html.Iframe(src = "https://qmrlab.org",width="100%",height="550px",style={'border':'0'})]
        )
    elif tab == 'Pearson.json':
        return get_svds_div(svds_content,'Pearson.json')


# Select welcome tab if no SVDS is chosen,
@app.callback(Output('my-tabs', 'value'),
              [Input('my-tabs', 'children')])
def render_content(tab):
    # The only case where tab is dict is when no file is chosen
    # Otherwise tab is always a list of dicts
    if isinstance(tab, dict):
        return 'idle'


def get_svds_div(svds,name):

    if name == 'Pearson.json':
        return html.Div([dcc.Graph(
        id='pearson-scatter',
        figure=[],
    ),
    dcc.Slider(
        id='pearson-slider',
        min=1,
        max=30,
        value=1,
        updatemode='drag',
        marks = {1:'1',10:'10',20:'20',30:'30'},

    )])

@app.callback(
Output('pearson-scatter','figure'),
[Input('pearson-slider','value')]
)
def update_lan(value):
    val = value-1
    svds = load_svds(UPLOAD_DIRECTORY)[1]
    figure={
        'data': [

            go.Scatter(
            mode = 'lines',
            x = itemgetter(*[0,1])(svds.Correlation.Pearson.Required[val]['fitLine']),
            y = itemgetter(*[2,3])(svds.Correlation.Pearson.Required[val]['fitLine']),
            name = 'dede',
            line= dict(
                color = ('rgb(255,0,0)'),
                width = 4,
            )),
            go.Scatter(
            mode = 'lines',
            x = itemgetter(*[0,1])(svds.Correlation.Pearson.Optional[val]['CILine1']),
            y = itemgetter(*[2,3])(svds.Correlation.Pearson.Optional[val]['CILine1']),
            fill = None,
            name = 'dede',
            line= dict(
                color = ('rgb(0,0,0)'),
                width = 2,)
            ),
            go.Scatter(
            mode = 'lines',
            x = itemgetter(*[0,1])(svds.Correlation.Pearson.Optional[val]['CILine2']),
            y = itemgetter(*[2,3])(svds.Correlation.Pearson.Optional[val]['CILine2']),
            fill = 'tonexty',
            fillcolor = 'rgba(0,200,0,0.2)',
            name = 'dede',
            line= dict(
                color = ('rgb(0,0,0)'),
                width = 2,)
            ),
            go.Scatter(
                x= svds.Correlation.Pearson.Required[val]['xData'],
                y= svds.Correlation.Pearson.Required[val]['yData'],
                text= ['agah'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 20,
                    'line': {'width': 0.5, 'color': 'white'},
                    'color': 'blue',
                },
                name= 'dede'
            )

        ],
        'layout': go.Layout(
            xaxis={'title': svds.Correlation.Pearson.Required[val]['xLabel'][0]},
            yaxis={'title': svds.Correlation.Pearson.Required[val]['yLabel'][0]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }
    return figure




if __name__ == "__main__":
    app.run_server(debug=True, port=8888)

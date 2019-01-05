# Data driven callbacks 
# Instead of this you can have a slider and chart interact with each other as well.as

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from flask import Flask
import pandas as pd

import base64
import os
from urllib.parse import quote as urlquote

import dash_core_components as dcc
from dash.dependencies import Input, Output

UPLOAD_DIRECTORY = "/Users/Agah/Desktop/DOcean/dash_app/data"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

server = Flask(__name__)


app = dash.Dash(name='agah',server=server,csrf_protect=False)

app.layout = html.Div([

        dcc.Upload(
            id="upload-data",
            children=html.Div(
                [" "]
            ),
            style={
                "width": "300px",
                "color": "#fff",
                "height": "300px",
                "lineHeight": "60px",
                "borderWidth": "4px",
                "borderStyle": "none",
                "borderRadius": "50%",
                "margin": "10% 20% 0% 40%",
                "textAlign": "center",
                "background": "#fbdeda",
                
            },
            multiple=False,
        ),
        html.H2(" "),
        html.Ul(id="file-list")

])



def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))
        
def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files
    
def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)


@app.callback(
     Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]





if __name__ == '__main__':
    app.run_server(debug=True)
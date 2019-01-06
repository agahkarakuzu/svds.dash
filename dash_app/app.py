import base64
import os
from urllib.parse import quote as urlquote

from flask import Flask, send_from_directory
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

UPLOAD_DIRECTORY = "/Users/Agah/Desktop/KuzuHub/svds.dash/dash_app/data"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

server = Flask(__name__)
app = dash.Dash(server=server)

@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

app.config['suppress_callback_exceptions']=True

app.layout = html.Div([
    html.Div(
    className = "footer",
    children = [
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select SVDS files."]
            ),
            style={
                "width": "100%",
                "height": "80px",
                "lineHeight": "200px",
                "textIndent": "10px",
                "textAlign": "center",
                "margin": "10px",
                'background-image': 'url(https://github.com/agahkarakuzu/svds/blob/master/svds2.png?raw=true)',
                'background-size': 'contain',
                'background-repeat': 'no-repeat',
                'background-position': 'center'
            },
            multiple=True,
        ),
    ],
    style={"max-width": "500px"}),
    html.Div(
    className = "row",
    children = [
    html.Div(className = "six columns",
    style={"fontColor":"blue","marginTop":"5%","marginLeft":"15px"},
    children = [
    html.H3("File List"),
    dcc.Checklist(id = "check-me",options =[],values=[])
    ])])
    ],
)



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
        if os.path.isfile(path) and filename != '.DS_Store':
            files.append(filename)
    return files

def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)

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
        return [{'label':filename,'value':filename} for filename in files]



if __name__ == "__main__":
    app.run_server(debug=True, port=8888)

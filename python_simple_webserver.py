import http.server
import socketserver
import os
import subprocess
import html
import json
from urllib.parse import unquote, quote

PORT = 8000
DIRECTORY = "/app/gpx"
WEB_DIRECTORY = "/gpx"

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def translate_path(self, path):
        path = unquote(path)
        return super().translate_path(path)

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            gpx_files = [f for f in os.listdir(DIRECTORY) if f.endswith('.gpx')]
            html_content = f"""
            <!DOCTYPE html>
            <html lang="de">
            <head>
                <title>Komoot GPX Downloads</title>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: sans-serif; }}
                    ul {{ list-style-type: none; padding: 0; }}
                    li {{ margin-bottom: 0.5em; }}
                    a {{ text-decoration: none; color: #007bff; }}
                    a:hover {{ text-decoration: underline; }}
                    .button-container {{
                        display: flex;
                        gap: 10px;
                        margin-top: 10px;
                    }}
                    .button {{
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 10px 20px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        cursor: pointer;
                        border-radius: 5px;
                    }}
                    .json-button {{
                        background-color: #007bff;
                    }}
                </style>
            </head>
            <body>
                <h1>Komoot GPX Downloads</h1>
                <p>Hier sind die heruntergeladenen GPX-Dateien:</p>
                <ul>
                    {''.join(f'<li><a href="{quote(f)}">{html.escape(f)}</a></li>' for f in gpx_files)}
                </ul>
                <div class="button-container">
                    <form method="post" action="/refresh">
                        <button type="submit" class="button">GPX-Dateien aktualisieren</button>
                    </form>
                    <button class="button json-button" onclick="window.location.href='/list'">GPX-Liste (JSON)</button>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
        elif self.path == '/list':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            gpx_files = [f for f in os.listdir(DIRECTORY) if f.endswith('.gpx')]
            json_data = json.dumps([{"name": f, "url": quote(f)} for f in gpx_files], indent=4) # WEB_DIRECTORY entfernt
            self.wfile.write(json_data.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/refresh':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            try:
                result = subprocess.run(['./refresh_gpx.sh'], capture_output=True, text=True, check=True, encoding='utf-8')
                output = result.stdout
                error = result.stderr
            except subprocess.CalledProcessError as e:
                output = ""
                error = f"Fehler beim Aktualisieren der GPX-Dateien: {e}"

            html_content = f"""
            <!DOCTYPE html>
            <html lang="de">
            <head>
                <title>Komoot GPX Aktualisierung</title>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: sans-serif; }}
                    .output-box {{
                        border: 1px solid #ccc;
                        padding: 10px;
                        margin-top: 20px;
                        white-space: pre-wrap;
                        font-family: monospace;
                    }}
                    .error-box {{
                        background-color: #f8d7da;
                        color: #721c24;
                        border: 1px solid #f5c6cb;
                        padding: 10px;
                        margin-top: 10px;
                    }}
                    .button {{
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 10px 20px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        cursor: pointer;
                        border-radius: 5px;
                    }}
                </style>
            </head>
            <body>
                <h1>Komoot GPX Aktualisierung</h1>
                <p>Aktualisiere GPX-Dateien...</p>
                {'<div class="output-box">Ausgabe:<br>' + html.escape(output) + '</div>' if output else ''}
                {'<div class="error-box">Fehler:<br>' + html.escape(error) + '</div>' if error else ''}
                <a href="/" class="button">Zurück zur Dateiliste</a>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b"404 Not Found")


Handler = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT} from directory {DIRECTORY}")
    httpd.serve_forever()
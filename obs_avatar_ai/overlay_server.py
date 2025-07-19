from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

PORT = 8765
web_dir = os.path.dirname(__file__)
os.chdir(web_dir)

print(f"Overlay server running at http://localhost:{PORT}")
print("Add this to OBS as a browser source.")

httpd = HTTPServer(("localhost", PORT), SimpleHTTPRequestHandler)
httpd.serve_forever()

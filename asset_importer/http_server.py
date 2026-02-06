from http.server import BaseHTTPRequestHandler

imported_asset = ""

class AssetHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        global imported_asset
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode()
        imported_asset = body
        print("POST recibido:", body)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(b"OK")
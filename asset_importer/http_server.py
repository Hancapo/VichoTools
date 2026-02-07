from http.server import BaseHTTPRequestHandler
from urllib.parse import unquote

imported_asset = ""
asset_category = ""

class AssetHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global imported_asset, asset_category

        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8", errors="replace")

        left, sep, right = raw.partition(";")
        imported_asset = unquote(left) if left else ""
        asset_category = unquote(right) if sep else ""

        print("POST received:", imported_asset)
        print("Category(s):", asset_category)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(b"OK")
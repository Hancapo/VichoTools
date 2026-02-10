from http.server import BaseHTTPRequestHandler
from urllib.parse import unquote
from .helper import set_asset_name, set_category_name, get_asset_name, get_category_name


class AssetHandler(BaseHTTPRequestHandler):
    def do_POST(self):

        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8", errors="replace")

        left, sep, right = raw.partition(";")
        set_asset_name(unquote(left) if left else "")
        set_category_name(unquote(right) if sep else "")

        print("POST received:", get_asset_name())
        print("Category(s):", get_category_name())

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(b"OK")
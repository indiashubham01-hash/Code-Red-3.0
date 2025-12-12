from http.server import HTTPServer, BaseHTTPRequestHandler
class S(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello")
httpd = HTTPServer(('0.0.0.0', 8005), S)
print("Serving...")
httpd.serve_forever()

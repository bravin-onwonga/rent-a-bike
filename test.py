#!/usr/bin/env python

from http.server import HTTPServer, BaseHTTPRequestHandler
import logging

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = bytes("Hello", "utf-8")
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

def start_server():
    logging.basicConfig(level=logging.INFO)
    server = HTTPServer(("localhost", 0), HelloHandler)

    # Import ngrok here to avoid circular import issues
    import ngrok
    ngrok.listen(server)

    server.serve_forever()

if __name__ == "__main__":
    start_server()

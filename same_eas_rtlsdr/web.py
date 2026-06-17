from http.server import BaseHTTPRequestHandler, HTTPServer
import time

STREAM_FILE = "/tmp/noaa_stream.mp3"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            html = """
            <html>
              <body style="font-family: sans-serif; padding: 20px;">
                <h2>SAME/EAS RTL-SDR</h2>
                <p>NOAA Weather Radio Audio Stream</p>
                <audio controls autoplay src="/stream"></audio>
              </body>
            </html>
            """
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())
            return

        if self.path == "/stream":
            self.send_response(200)
            self.send_header("Content-Type", "audio/mpeg")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()

            with open(STREAM_FILE, "rb") as f:
                while True:
                    chunk = f.read(4096)
                    if chunk:
                        self.wfile.write(chunk)
                    else:
                        time.sleep(0.25)
            return

        self.send_response(404)
        self.end_headers()

HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()

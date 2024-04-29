import http.server
import socketserver
import subprocess
import html

PORT = 55555
# simple example of a web server
# Handler = http.server.SimpleHTTPRequestHandler

# with socketserver.TCPServer(("", PORT), Handler) as httpd:
#     print("serving at port", PORT)
#     httpd.serve_forever()


class myHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):

        # Run the cgi script for the fibonacci sequence
        output = subprocess.check_output(["python", "next_fibonacci.py"])
        # sanitized_output = html.escape(output.decode("utf-8"))
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(output)

PORT = 55555
with socketserver.TCPServer(("", PORT), myHTTPRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()

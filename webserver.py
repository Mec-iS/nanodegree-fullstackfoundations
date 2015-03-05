__author__ = 'lorenzo'

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>Server is Running</body></html>"
                self.wfile.write(output)
                print output
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

        pass


def main():
    try:
        port = 8080
        server = HTTPServer(('localhost', port), webserverHandler)
        print "Server Running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "server stopping"
        server.socket.close()

if __name__ == '__main__':
    main()

__author__ = 'lorenzo'

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy.orm import sessionmaker, Query
from database_setup import engine, Base, Restaurant, MenuItem


def start_session(eng):
    """This method starts an SQLAlchemy session"""
    Base.metadata.bind = eng
    DBSession = sessionmaker(bind=eng)
    session = DBSession()
    return session


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                session = start_session(engine)

                for q in session.query(Restaurant).all():
                    output += "<ul><li>" + q.name + "</li>"
                    output += "<li><a href=\"#\">Edit</a></li>"
                    output += "<li><a href=\"#\">Delete</a></li>"
                    output += "</ul><br/><br/>"

                output += "</ul></body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

                output = ""
                output += "<html><body>"
                output += "<h2> Ok, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]

                output += """<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>"""
                output += "</html></body>"
                self.wfile.write(output)
                return

        except:
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


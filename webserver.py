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


def insert_restaurant(ssn, name):
    """CREATE Restaurant"""
    restaurant = Restaurant(name=name)
    ssn.add(restaurant)
    try:
        ssn.commit()
    except:
        raise IOError


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

                output += "<p><a href=\"/restaurants/new\">Make a new Restaurant</a></p>"

                for q in session.query(Restaurant).all():
                    output += "<ul><li>" + q.name + "</li>"
                    output += "<li><a href=\"#\">Edit</a></li>"
                    output += "<li><a href=\"#\">Delete</a></li>"
                    output += "</ul><br/><br/>"

                output += "</ul></body></html>"
                session.close()
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"

                output += "<h2>New Restaurant's name: </h2>"
                output += """<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name="restaurant" type="text" ><input type="submit" value="Submit"> </form>"""

                output += "</ul></body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        if self.path.endswith("/restaurants/new"):
            print "here"
            try:
                self.send_response(301)
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant')
                    name = messagecontent[0]
                    print name

                    session = start_session(engine)
                    try:
                        insert_restaurant(session, name)
                    except IOError as e:
                        raise e

                    output = ""
                    output += "<html><body>"
                    output += "New Restaurant %s inserted" % name
                    output += "</ul></body></html>"
                    session.close()
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


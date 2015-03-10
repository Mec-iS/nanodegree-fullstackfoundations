__author__ = 'lorenzo'

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from libs.database_setup import engine, Restaurant
from libs.dbSession import start_session


def insert_restaurant(ssn, name):
    """CREATE Restaurant"""
    restaurant = Restaurant(name=name)
    ssn.add(restaurant)
    try:
        ssn.commit()
    except:
        raise IOError


def query_filter_by(ssn, name=None, item_id=None):
    """ Filters by name or by id if name is None"""
    if name:
        return ssn.query(Restaurant).filter_by(name=name)
    elif item_id:
        return ssn.query(Restaurant).filter_by(id=item_id).one()
    else:
        raise AttributeError


def update_restaurant_name(ssn, res_id, new_name):
    """updates resource name filtering by id"""
    try:
        res = ssn.query(Restaurant).filter_by(id=res_id).one()
        res.name = new_name
        ssn.add(res)
        return ssn.commit()
    except:
        raise IOError


def delete_restaurant(ssn, res_id):
    """delete a resource by id"""
    try:
        res = ssn.query(Restaurant).filter_by(id=res_id).one()
        ssn.delete(res)
        return ssn.commit()
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
                    output += "<li><a href=\"/restaurants/" + str(q.id) + "/edit\">Edit</a></li>"
                    output += "<li><a href=\"/restaurants/" + str(q.id) + "/delete\">Delete</a></li>"
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

            if self.path.endswith("/edit"):
                p = self.path
                pos2 = p.rfind("/edit")
                print p[13:pos2]
                restaurant_id = p[13:pos2]

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                session = start_session(engine)

                restaurant = query_filter_by(session, name=None, item_id=int(restaurant_id))

                output += """<form method='POST' enctype='multipart/form-data' action='/restaurants/""" + str(restaurant.id) + """/edit'>
                <input name="restaurant" type="text" placeholder='""" + restaurant.name + """'><input type="submit" value="Submit"> </form>"""

                output += "</ul></body></html>"
                session.close()
                self.wfile.write(output)
                return

            if self.path.endswith("/delete"):
                p = self.path
                pos2 = p.rfind("/delete")
                print p[13:pos2]
                restaurant_id = p[13:pos2]

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                session = start_session(engine)

                restaurant = query_filter_by(session, name=None, item_id=int(restaurant_id))

                output += """Are you sure you want to delete """ + restaurant.name + """?<br/>
                 <form method='POST' enctype='multipart/form-data' action='/restaurants/""" + str(restaurant.id) + """/delete'>
                 <input type="submit" value="Delete"> </form>"""

                output += "</ul></body></html>"
                session.close()
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant')
                    name = messagecontent[0]

                    session = start_session(engine)
                    try:
                        insert_restaurant(session, name)
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        # self.send_header('Location', '/restaurants') # automatic redirect
                        self.end_headers()
                    except IOError as e:
                        raise e

                    output = ""
                    output += "<html><body>"
                    output += "New Restaurant %s inserted" % name
                    output += "<br><a href=\"/restaurants\">Back</a>"
                    output += "</ul></body></html>"
                    session.close()
                    self.wfile.write(output)
                    return
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant')
                    new_name = messagecontent[0]

                    p = self.path
                    pos2 = p.rfind("/edit")
                    restaurant_id = p[13:pos2]

                    session = start_session(engine)

                    try:
                        update_restaurant_name(session, res_id=int(restaurant_id), new_name=new_name)
                    except IOError as e :
                        raise e

                    session.close()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')  # automatic redirect
                    self.end_headers()
                    self.wfile.write("<html><body></body></html>")
                    return

            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    p = self.path
                    pos2 = p.rfind("/delete")
                    restaurant_id = p[13:pos2]

                    session = start_session(engine)

                    try:
                        delete_restaurant(session, res_id=int(restaurant_id))
                    except IOError as e :
                        raise e

                    session.close()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')  # automatic redirect
                    self.end_headers()
                    self.wfile.write("<html><body></body></html>")
                    return

        except Exception:
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


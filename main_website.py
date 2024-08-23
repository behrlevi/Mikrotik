import cherrypy
import custom_api as ca

class MyWebApp(object):
    @cherrypy.expose
    def index(self):
        # HTML content with a button
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Execute Function</title>
        </head>
        <body>
            <body>
            <form method="get" action="apicall">
              <button type="submit">Show interface</button>
            </form>
            <br>
            <div class="select">
            <label for="language">Select a Command:</label>
            <select name="command" id="command">
            <option value="">JavaScript</option>
            <option value="python">Python</option>
            <option value="c++">C++</option>
            <option value="java">Java</option>
            </select>
            <button onclick="apicall">Execute</button>
        </div>
        </body>
        <script>
        function apicall()</script>
        </html>
        """
    @cherrypy.expose
    def apicall(self):
        r = ca.Mapi('192.168.2.214','admin', '1')
        result = r.login()
        return result
    
    @cherrypy.expose
    def display(self):
        return cherrypy.session['result']

if __name__ == '__main__':
    cherrypy.quickstart(MyWebApp())

import cherrypy
import custom_api as ca

class MyWebApp(object):
    @cherrypy.expose
    def index(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Execute Function</title>
        </head>
        <body>
            <form method="get" action="apicall">
                <label for="ip">IP Address:</label>
                <input type="text" id="ip" name="ip"><br><br>
                <label for="username">Username:</label>
                <input type="text" id="username" name="username"><br><br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password"><br><br>
                <label>Select a Command:</label>
                <select name="command" id="command">
                    <option value="wg">WG config</option>
                    <option value="other">Other config</option>
                </select>
                <button type="submit" value="Submit">Execute</button>
            </form>
            <br>
        </body>

        <script>
        const selection = document.getElementById('command');
        const selected = selection.value;
        console.log('Selected command:', selected);
        </script>

        </html>
        """
    
    @cherrypy.expose
    def apicall(self, ip, username, password, command):
        r = ca.Mapi(ip, username, password)
        result = r.login()
        return result
    
    @cherrypy.expose
    def display(self):
        return cherrypy.session['result']

if __name__ == '__main__':
    cherrypy.quickstart(MyWebApp())
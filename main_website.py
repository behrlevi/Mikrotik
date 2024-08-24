import cherrypy
import custom_api as ca
import json
import os

class MyWebApp(object):
    @cherrypy.expose
    def index(self):
        result = cherrypy.session.pop('result', None)
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Execute Function</title>
            <style>
                .form-group {{
                    display: flex;
                    align-items: center;
                    margin-bottom: 10px;
                }}
                .form-group label {{
                    width: 150px;
                }}
                .form-group input, .form-group select {{
                    width: 150px;
                }}
                button[type="submit"] {{
                    display: block;
                    margin-left: 150px;
                    background-color: red;
                    color: white;
                    cursor: pointer;
                    font-weight: bold;
                }}
            </style>
            <script>
                window.onload = function() {{
                    var result = {json.dumps(result)};
                    if (result) {{
                        alert(result);
                    }}
                }};
            </script>
        </head>
        <body>
            <h1>Mikrotik Management Tools</h1>
            <form method="get" action="apicall">
                <div class="form-group">
                    <label for="ip">IP Address:</label>
                    <input type="text" id="ip" name="ip">
                </div>
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username">
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password">
                </div>
                <div class="form-group">
                    <label for="command">Select a Command:</label>
                    <select name="command" id="command">
                        <option value="wg">Quick WG</option>
                        <option value="other">Other config</option>
                    </select>
                </div>
                <button type="submit" value="Submit">Execute</button>
            </form>
            <br>
        </body>

        </html>
        """
    
    @cherrypy.expose
    def apicall(self, ip, username, password, command):
        try:
            call = ca.Mapi(ip, username, password)
            if command == 'wg':
                config_path = call.wg()
                if os.path.exists(config_path):
                    return cherrypy.lib.static.serve_file(config_path, "application/x-download", "attachment", os.path.basename(config_path))
            elif command == 'other':
                result = "Other config"
            cherrypy.session['result'] = result
        except Exception as e:
            cherrypy.session['result'] = f"Error: {str(e)}"
        raise cherrypy.HTTPRedirect('/')
    
    """
    @cherrypy.expose
    def display(self):
        return cherrypy.session['result']
    """

if __name__ == '__main__':
    cherrypy.quickstart(MyWebApp(), '/', {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080,
            'tools.sessions.on': True,
            'tools.sessions.storage_type': 'ram'
        }
    })
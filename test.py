from custom_api import *

s = None
dst = "192.168.2.214"
user = "admin"
passw = "1"
secure = False
port = 0

apiros = ApiRos(s)
if apiros.login(user, passw):
    response = apiros.execute_command(["/interface/print"])
    print(response)
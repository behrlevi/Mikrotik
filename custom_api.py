import routeros_api

class Mapi:
    def __init__(self,ip,usr,passw):
        self.ip = ip
        self.usr = usr
        self.passw = passw
    
    def login(self):
        connection = routeros_api.RouterOsApiPool(self.ip, username=self.usr, password=self.passw, plaintext_login=True)
        api = connection.get_api()
        interfaces = api.get_resource('/interface')
        interface_list = interfaces.get()
        addr=interface_list[1]['default-name']
        return addr

r = Mapi('192.168.2.214','admin', '1')
r.login()


"""
connection = routeros_api.RouterOsApiPool('192.168.2.214', username='admin', password='1', plaintext_login=True)
api = connection.get_api()

api = connection.get_api()
#response = api.get_binary_resource('/').call('ping', { 'address': b'192.168.56.1', 'count': b'4' })
#print(response)

interfaces = api.get_resource('/interface')
interface_list = interfaces.get()

for interface in interface_list:
    print(interface)

resp = api.get_resource('/ip/address/').get()
address = resp[0]['address']
print (address)
"""

#connection.disconnect()
import routeros_api
import textwrap
import subprocess

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
    
    def wg(self):
        # Generate public key
        private_key = subprocess.check_output(['wg', 'genkey']).strip()
        public_key = subprocess.check_output(['wg', 'pubkey'], input=private_key).strip()
        
        #Decode keys to string
        public_key_str = public_key.decode('utf-8')
        private_key_str = private_key.decode('utf-8')

        # Generate WireGuard configuration content
        wg_config_content = textwrap.dedent(f"""
        [Interface]
        PrivateKey = {private_key_str}
        Address = 10.0.0.1/24

        [Peer]
        PublicKey = {public_key_str}
        AllowedIPs = 0.0.0.0/0
        Endpoint = {self.ip}:51820
        """).strip()

        # Save the configuration to a temporary file
        config_path = '/tmp/wg_config.conf'
        with open(config_path, 'w') as config_file:
            config_file.write(wg_config_content)


        # Add public key to WireGuard interface
        connection = routeros_api.RouterOsApiPool(self.ip, username=self.usr, password=self.passw, plaintext_login=True)
        api = connection.get_api()
        interfaces = api.get_resource('/interface/wireguard')
        interfaces.add(name='Vajer Gabor')
        peers = api.get_resource('/interface/wireguard/peers')
        peers.add(interface='Vajer Gabor', public_key=public_key_str)
            
        connection.disconnect()
        
        return config_path
"""
r = Mapi('192.168.2.214','admin', '1')
r.login()
"""


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
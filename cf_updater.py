import requests
import socket
import time
import json
import os
import re

# Read .env variables 
def dot_env(file_path=".env"):
    env_vars = {}
    if os.path.exists(file_path):
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    value = re.sub(r'^["\'<]*(.*?)["\'>]*$', r'\1', value)
                    env_vars[key] = value
    return env_vars

env_vars = dot_env()

CF_API_TOKEN = os.getenv("CF_API_TOKEN") or env_vars.get("CF_API_TOKEN")
CF_API_KEY = os.getenv("CF_API_KEY") or env_vars.get("CF_API_KEY")
CF_EMAIL = os.getenv("CF_EMAIL") or env_vars.get("CF_EMAIL")
HOSTNAME = os.getenv("HOSTNAME") or env_vars.get("HOSTNAME")

CONFIG = {
    "CLOUDFLARE": {
        "EMAIL": CF_EMAIL, # Cloudflare account email address here
        "API_TOKEN": CF_API_TOKEN, # Cloudflare API token here (this one can be generated through the dashboard)
        "API_KEY": CF_API_KEY, # Your Cloudflare global API key here
        "LOCATION_NAME": "Default Location" # The Cloudflare ZT Gateway location name
    },
    "HOSTNAME": HOSTNAME,
}

def main():
    cf_account_id = ""
    location_uuid = ""
    location_name = ""
    location_is_default = False
    network = ""
    
    try:
        req = requests.get(
            f"https://api.cloudflare.com/client/v4/accounts",
            headers={
                "Content-Type": "application/json",
                "Authorizarion": "Bearer " + str(CONFIG['CLOUDFLARE']['API_TOKEN']),
                "X-Auth-Key": str(CONFIG['CLOUDFLARE']['API_KEY']),
                "X-Auth-Email": str(CONFIG['CLOUDFLARE']['EMAIL'])
            }
        )
        res = json.loads(req.text)
        cf_account_id = res['result'][0]['id'] # usually the first element of the array, However that's still not the best practice. Change the index if necessary
    except Exception as e:
        print(e)
        return

    try:
        req = requests.get(
            f"https://api.cloudflare.com/client/v4/accounts/{cf_account_id}/gateway/locations",
            headers={
                "Authorizarion": "Bearer " + str(CONFIG['CLOUDFLARE']['API_TOKEN']),
                "X-Auth-Key": str(CONFIG['CLOUDFLARE']['API_KEY']),
                "X-Auth-Email": str(CONFIG['CLOUDFLARE']['EMAIL'])
            }
        )
        res = json.loads(req.text)
        for location in res['result']:
            if location['name'].strip() == CONFIG['CLOUDFLARE']['LOCATION_NAME'].strip():
                location_uuid = location['id']
                location_name = location['name']
                location_is_default = location['client_default']

        networks = res['result'][0]['networks']
        for network_info in networks:
            network = network_info['network'].split('/')[0]
            break
    except Exception as e:
        print(e)
        return

    daip = socket.gethostbyname(CONFIG['HOSTNAME'])
	
    if daip == network:
        print("ip address has not changed")
        return
    
    try:
        req = requests.put(
            f"https://api.cloudflare.com/client/v4/accounts/{cf_account_id}/gateway/locations/{location_uuid}",
            headers={
                "Authorizarion": "Bearer " + str(CONFIG['CLOUDFLARE']['API_TOKEN']),
                "X-Auth-Key": str(CONFIG['CLOUDFLARE']['API_KEY']),
                "X-Auth-Email": str(CONFIG['CLOUDFLARE']['EMAIL'])
            },
            json={
                "name": location_name,
                "networks": [
                    {
                        "network": str(socket.gethostbyname(CONFIG['HOSTNAME'])) + "/32"
                    }
                ],
                "client_default": location_is_default,
                "ecs_support": True
            }
        )
        if json.loads(req.text)['success'] == True:
            print("successfully synced the gateway location")
    except Exception as e:
        print(e)
        return
        

if __name__ == '__main__':
    main()

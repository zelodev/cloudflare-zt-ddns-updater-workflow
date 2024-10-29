# cloudflare-zt-ddns-updater-workflow
Automatically sync your Cloudflare Zero Trust Gateway location with the IP address of a hostname (No-IP, etc) using github actions

important:

you must create the following actions secrets in your repository's settings:

- CF_API_KEY
- CF_API_TOKEN
- CF_EMAIL
- HOSTNAME

i feel the values of which are self explanatory

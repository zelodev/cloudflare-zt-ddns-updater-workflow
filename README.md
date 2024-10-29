# cloudflare-zt-ddns-updater-workflow
Automatically sync your Cloudflare Zero Trust Gateway location with the IP address of a hostname (No-IP, etc) using github actions

when set up, this will run every 20 minutes, so account for that in your monthly usage. you may change this value/behavior via the workflow's schedule cron

important:

you must create the following actions secrets in your repository's settings:

- CF_API_KEY
- CF_API_TOKEN
- CF_EMAIL
- HOSTNAME

i feel the values of which are self explanatory

you may also want to change the value of LOCATION_NAME in cf_updater.py if you use anything other than Default Location

if forking this repository, then remember to enable workflows via the actions tab.

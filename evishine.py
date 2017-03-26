import requests

# PANEL_ID = {1: 36976, 11: 37392, 13: 31487, 23: 31468, 25: 31470, }
PANEL_ID = {1: 36976, 11: 37392}

client = requests.session()

res = client.get('https://evishine.dk/data/json_data/17249/37392')
json = res.json()


import requests

client = requests.session()

res = client.get('https://evishine.dk/data/json_data/17249/37392')
json = res.json()


import requests
import datetime
import numpy

# URLs
DAILY_PRODUCTION_URL = 'https://evishine.dk/data/statistics_list/17249/%s?timestamp=%s'

# Panels
# PANEL_ID = {1: 36976, 11: 37392, 13: 31487, 23: 31468, 25: 31470, }
PANEL_IDS = {1: 36976, 11: 37392}

# Start and end times (end time not inclusive)
start_time = datetime.datetime(2016, 12, 01, 0, 0)
end_time = datetime.datetime(2017, 01, 01, 0, 0)

# Prepare datastructure for data collection
number_of_days = (end_time - start_time).days
# Keep x (day number after start_time) and y (energy production) values for each panel for the given number of days
energy_production = {}
for apartment_number in PANEL_IDS.keys():
    energy_production[apartment_number] = numpy.zeros((2, number_of_days))

client = requests.session()

current_time = start_time
while current_time < end_time:
    timestamp = current_time.strftime('%s') + '000'
    # print timestamp
    for apartment_number, id in PANEL_IDS.iteritems():

        url = DAILY_PRODUCTION_URL % (str(id), timestamp)
        # TODO: catch exception, check status code
        response = client.get(url)
        json = response.json()

        # Extract relevant data from JSON
        # TODO: refactor
        data_list = json['statisticsList'][0]['data']  # List like [{'name': '0', 'value': 1729},...]
        daily_production = 0.001*sum([d['value'] for d in data_list])  # kWh
        day_number = (current_time - start_time).days
        energy_production[apartment_number][0][day_number] = day_number
        energy_production[apartment_number][1][day_number] = daily_production

    current_time += datetime.timedelta(days=1)

with open('/home/andreas/Dropbox/administration/privat/solceller/production.dat', 'w') as f:
    f.write('Dato;Nr 11; Nr 1\n')
    for i in range(number_of_days):
        f.write(str(energy_production[11][0][i] + 1) + ';' + str(energy_production[11][1][i]) + ';' + str(energy_production[1][1][i]) + '\n')
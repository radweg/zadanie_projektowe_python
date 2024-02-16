import requests


def get_data_from_api():
    headers = {
        'Content-Type': 'application/json',
        'apikey': 'rLQBboGtHjaphGBF6iA1ppK2rV8pxzUx'
    }
    response = requests.get(url="https://airapi.airly.eu/v2/measurements/point?lat=50.1022&lng=18.5463",
                            headers=headers)

    data = response.json()
    data = data['current']

    result = {}
    result['fromDateTime'] = data['fromDateTime']
    result['tillDateTime'] = data['tillDateTime']

    for item in data['values']:
        result[item['name']] = item['value']

    result['AIRLY_CAQI'] = data['indexes'][0]['value']
    result['level'] = data['indexes'][0]['level']
    result['description'] = data['indexes'][0]['description']
    result['WHO'] = {
        'PM25': data['standards'][0]['percent'],
        'PM10': data['standards'][1]['percent']
    }
    return result

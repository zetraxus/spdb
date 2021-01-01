import requests


def search_for_coords(address):
    url = ' https://nominatim.openstreetmap.org/search'
    params = {'q': address, 'format': 'json', 'addressdetails': '1'}
    data = requests.get(url=url, params=params).json()
    return data[0]['lat'], data[0]['lon']


def filter_results(query_results, coords, distance):
    URL_high_acc = 'https://routing.openstreetmap.de/routed-foot/route/v1/driving/'
    # URL_low_acc = 'http://router.project-osrm.org/route/v1/driving/'
    start = coords[1] + ',' + coords[0]

    nearby_results = []
    for result in query_results:
        meta = str(result[8]) + ',' + str(result[7])
        data = requests.get(URL_high_acc + start + ';' + meta).json()
        if data['routes'][0]['distance'] < distance:
            result_with_dist = result + (data['routes'][0]['distance'],)
            nearby_results.append(result_with_dist)
    return nearby_results


def sort_results(results, order):
    if order == 'price':
        return sorted(results, key=lambda x: x[9])
    if order == 'rating':
        return sorted(results, key=lambda x: -x[6])
    if order == 'distance':
        return sorted(results, key=lambda x: x[20])

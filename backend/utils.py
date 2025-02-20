import math
import requests
import mysql.connector as mysql
from backend.config import host, user, passwd, database


def search_for_coords(address):
    url = ' https://nominatim.openstreetmap.org/search'
    params = {'q': address, 'format': 'json', 'addressdetails': '1'}
    data = requests.get(url=url, params=params).json()
    return data[0]['lat'], data[0]['lon']


def filter_results(query_results, coords, max_distance):
    URL_high_acc = 'https://routing.openstreetmap.de/routed-foot/route/v1/driving/'
    # URL_low_acc = 'http://router.project-osrm.org/route/v1/driving/'
    start = coords[1] + ',' + coords[0]

    nearby_results = []
    for result in query_results:
        meta = str(result[8]) + ',' + str(result[7])
        data = requests.get(URL_high_acc + start + ';' + meta).json()
        distance = data['routes'][0]['distance']
        if distance < max_distance:
            result_with_dist = result + (round(distance / 1000, 1),)
            nearby_results.append(result_with_dist)
    return nearby_results


def calc_popularity(results):
    max_rev_cnt = max(results, key=lambda item: item[4])
    max_rev_cnt = max_rev_cnt[4]
    for i in range(len(results)):
        results[i] += (math.ceil(10 * results[i][4] / max_rev_cnt),)
    return results


def sort_results(results, order):
    if order == 'price':
        return sorted(results, key=lambda x: x[9])
    if order == 'rating':
        return sorted(results, key=lambda x: -x[6])
    if order == 'distance':
        return sorted(results, key=lambda x: x[20])
    if order == 'popularity':
        calc_popularity(results)
        return sorted(results, key=lambda x: -x[-1])


def db_query(query_builder):
    db = mysql.connect(host=host, user=user, passwd=passwd, database=database)
    query = query_builder.build_sql_query()
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results


def filter_address(query_builder, results):
    if query_builder.address:
        coords = search_for_coords(query_builder.address)
        return filter_results(results, coords, query_builder.distance)
    return results


def order(query_builder, results):
    if query_builder.order:
        if not (query_builder.order == 'distance' and not query_builder.address):
            return sort_results(results, query_builder.order)[:query_builder.results_cnt]
    return results[:query_builder.results_cnt]


def add_lp(results):
    for i in range(len(results)):
        results[i] += (i + 1,)
    return results

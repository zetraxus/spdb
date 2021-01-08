import mysql.connector as mysql
from flask import Flask, render_template, request

from backend.config import host, user, passwd, database
from backend.utils import search_for_coords, filter_results, calc_popularity
from backend.sql_query import SQLQuery
from backend.utils import sort_results

app = Flask(__name__)
db = mysql.connect(host=host, user=user, passwd=passwd, database=database)


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('query.html')


@app.route('/process', methods=['POST'])
def process():
    query_builder = SQLQuery(request)
    query = query_builder.build_sql_query()

    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    if query_builder.address:
        coords = search_for_coords(query_builder.address)
        results = filter_results(results, coords, query_builder.distance)

    if query_builder.order:
        if not (query_builder.order == 'distance' and not query_builder.address):
            results = sort_results(results, query_builder.order)

    results = results[:query_builder.results_cnt]
    if query_builder.order != 'popularność':
        calc_popularity(results)

    for i in range(len(results)):
        results[i] += (i + 1,)

    if query_builder.address:
        return render_template('response_with_dist.html', results=results)
    else:
        return render_template('response_base.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)

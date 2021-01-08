from flask import Flask, render_template, request
from backend.utils import calc_popularity, db_query, filter_address, order, add_lp
from backend.sql_query import SQLQuery

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('query.html')


@app.route('/process', methods=['POST'])
def process():
    query_builder = SQLQuery(request)
    results = db_query(query_builder)
    results = filter_address(query_builder, results)
    results = order(query_builder, results)
    results = calc_popularity(results)
    results = add_lp(results)

    if query_builder.address:
        return render_template('response_with_dist.html', results=results)
    else:
        return render_template('response_base.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)

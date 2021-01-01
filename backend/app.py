import mysql.connector as mysql
from flask import Flask, render_template, request

from backend.config import host, user, passwd, database
from backend.sql_query import SQLQuery

app = Flask(__name__)
db = mysql.connect(host=host, user=user, passwd=passwd, database=database)


@app.route('/')
def main():
    return render_template('query.html')


@app.route('/process', methods=['POST'])
def process():
    query_builder = SQLQuery(request)
    query = query_builder.build_sql_query()
    print(query)

    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    return render_template('response.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)

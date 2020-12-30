import mysql.connector as mysql
from flask import Flask, render_template, request

from backend.config import host, user, passwd, database

app = Flask(__name__)
db = mysql.connect(host=host, user=user, passwd=passwd, database=database)


@app.route('/')
def main():
    return render_template('query.html')


@app.route('/process', methods=['POST'])
def process():
    # get(attr) returns None if attr is not present
    _category = request.form.get('category')
    _longitude = request.form.get('longitude')
    _latitude = request.form.get('latitude')

    cursor = db.cursor()
    cursor.execute("(select * from restaurants_test where main_category = %s limit 10)", (_category,))
    results = cursor.fetchall()
    return render_template('response.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)

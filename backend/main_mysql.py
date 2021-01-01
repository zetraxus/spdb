import mysql.connector as mysql

from backend.config import host, user, passwd, database


def connect():
    return mysql.connect(host=host, user=user, passwd=passwd, database=database)


def select(db, query, params):
    cursor = db.cursor()
    cursor.execute(query, params)
    return cursor.fetchall()


def print_results(records):
    for record in records:
        print(record)


if __name__ == '__main__':
    db_conn = connect()
    # main_category = input('main category = ') Dance Clubs
    for i in range(10):
        query = input('query = ')
        cursor = db_conn.cursor()
        cursor.execute(query)
        print(cursor.fetchall())
    main_category = 'Dance Clubs'
    records = select(db_conn, "(select * from restaurants_test where main_category = %s limit 10)", (main_category,))
    print_results(records)

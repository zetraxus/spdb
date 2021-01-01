import mysql.connector as mysql

from backend.config import host, user, passwd, database

# for testing purposes
if __name__ == '__main__':
    db_conn = mysql.connect(host=host, user=user, passwd=passwd, database=database)
    for i in range(10):
        query = input('query = ')
        cursor = db_conn.cursor()
        cursor.execute(query)
        print(cursor.fetchall())

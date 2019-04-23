import psycopg2
import psycopg2.extras

try:
    connection = psycopg2.connect(
    "dbname='kurs_PDB' \
    user='kurs_user' \
    host='localhost' \
    password='123' \
    port='5433'"
    )
    connection.set_client_encoding('UTF8')
except psycopg2.Error as err:
    print("Unable to connect to database: {}".format(err))

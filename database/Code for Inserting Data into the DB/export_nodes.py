import mysql.connector
from mysql.connector import Error
from csv import reader
import csv
try:
    connection = mysql.connector.connect(host="localhost", database="geospatial_okan", user="root", password="Kashyap@1995")
    if connection.is_connected():
        db_Info = connection.get_server_info()
        cursor = connection.cursor(buffered=True)
        cursor.execute("select database();")
        record = cursor.fetchone()

        query = "select * from node;"
        cursor.execute(query)
        row = cursor.fetchall()

        fields = ['node_id','name','latitude','longitude','street_name','city_code','county_code','zipcode','sc_step']
        with open('nodes_export.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(row)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
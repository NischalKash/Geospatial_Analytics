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

        query = "select * from fm_lm_connections;"
        cursor.execute(query)
        row = cursor.fetchall()

        fields = ['connection_id','Origin_node_id','Dest_node_id','Commodity_id','Fewsion_unit_type','Fewsion_unit_value','Fewsion_dollar_value','Sc_step_fmlm','date_recorded','origin_county_code','destination_county_code']
        with open('fm_lm_connections_export.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(row)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
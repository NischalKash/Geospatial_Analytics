import mysql.connector
from mysql.connector import Error
from csv import reader

try:
    connection = mysql.connector.connect(host="localhost", database="geospatial_okan", user="root", password="Kashyap@1995")
    if connection.is_connected():
        db_Info = connection.get_server_info()
        cursor = connection.cursor(buffered=True)
        cursor.execute("select database();")
        record = cursor.fetchone()

        with open('fewsion_units.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                units_id = row[0]
                unit_name = row[1]
                unit_desc = row[2]
                query = "Insert into fewsion_units values('"+units_id+"','"+str(unit_name)+"','"+str(unit_desc)+"');"
                cursor.execute(query)

                connection.commit()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
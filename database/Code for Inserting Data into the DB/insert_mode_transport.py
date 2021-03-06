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

        with open('Mode_Of_Transport.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                mot_id = row[0]
                transport_type = row[1]
                query = "Insert into mode_of_transport values('"+str(mot_id)+"','"+str(transport_type)+"');"
                cursor.execute(query)

                connection.commit()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
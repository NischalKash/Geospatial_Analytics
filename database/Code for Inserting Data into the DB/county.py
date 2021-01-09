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

        with open('county.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                id = row[0]
                name = row[1]
                state_listing = row[2]
                query = "Insert into county values('"+str(id)+"','"+str(name)+"','"+str(state_listing)+"');"
                print(query)
                cursor.execute(query)

                connection.commit()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
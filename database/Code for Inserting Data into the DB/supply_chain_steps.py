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

        with open('supply_chain_steps.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                id = row[0]
                id_letter = row[1]
                id_description = row[2]
                query = "Insert into supply_chain_steps values('"+str(id)+"','"+str(id_letter)+"','"+str(id_description)+"');"
                cursor.execute(query)

                connection.commit()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
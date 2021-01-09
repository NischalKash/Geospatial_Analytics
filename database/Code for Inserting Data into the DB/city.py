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

        with open('city.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                id = row[0]
                county_code = row[3]
                name = row[1]
                city_flips = row[2]
                state_code = row[4]
                query = "Insert into city values('"+str(id)+"','"+str(name)+"','"+str(state_code)+"','"+str(county_code)+"','"+str(city_flips)+"');"
                cursor.execute(query)

                connection.commit()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
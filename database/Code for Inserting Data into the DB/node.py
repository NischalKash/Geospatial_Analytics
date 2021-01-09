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

        with open('nodes_weld_csv.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                node = row[0]
                node_name = row[1]
                latitude = row[2]
                longitude = row[3]
                address = row[4]
                city = row[5]
                county = row[6]
                zip_code = row[7]
                scm_step = row[8]
                query = "Insert into node values('"+str(node)+"','"+str(node_name)+"',"+latitude+","+longitude+",'"+str(address)+"','"+str(city)+"','"+str(county)+"','"+zip_code+"','"+str(scm_step)+"');"
                print(query)
                cursor.execute(query)

                connection.commit()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
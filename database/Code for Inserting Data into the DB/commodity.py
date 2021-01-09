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

        with open('commodity.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                commodity_id = row[0]
                few_sector = row[1]
                few_subsector = row[2]
                sctg_code = row[3]
                query = "Insert into commodity values('"+str(commodity_id)+"','"+str(few_sector)+"','"+str(few_subsector)+"','"+str(sctg_code)+"');"
                cursor.execute(query)

                connection.commit()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
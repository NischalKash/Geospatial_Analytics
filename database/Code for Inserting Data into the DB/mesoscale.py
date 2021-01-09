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

        with open('mesoscale.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                ms_id = row[0]
                origin_county = row[1]
                origin_sc_step = row[3]
                destination_county = row[4]
                destination_sc_step = row[6]
                commodity_id = row[7]
                fewsion_unit_type = row[8]
                fewsion_unit_value = row[9]
                fewsion_dollar_value = row[10]
                date_recorded = row[11]
                query = "Insert into mesoscale values('"+str(ms_id)+"','"+str(origin_county)+"','"+str(origin_sc_step)+"','"+str(destination_county)+"','"+str(destination_sc_step)+"','"+str(commodity_id)+"','"+str(fewsion_unit_type)+"','"+fewsion_unit_value+"','"+str(fewsion_dollar_value)+"','"+str(date_recorded)+"');"
                cursor.execute(query)

                connection.commit()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
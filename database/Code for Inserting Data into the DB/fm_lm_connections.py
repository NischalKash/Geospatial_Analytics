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

        with open('fm_weld_csv.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                conn_id = row[0]
                origin_id = row[1]
                destination_id = row[2]
                commodity = row[3]
                fewsion_unit_type = row[4]
                fewsion_unit_value = row[5]
                fewsion_unit_dollar = row[6]
                sc_step = row[7]
                date_recorded = row[8]

                origin_county_code = row[9]
                destination_county_code = row[10]
                '''query1 = "Select county_code from node where node_id = '"+str(origin_id)+"'"
                cursor.execute(query1)
                row = cursor.fetchone()
                if row:
                    origin_county_code = row[0]

                print(destination_id)
                query2 = "Select county_code from node where node_id = '" + str(destination_id)+"'"
                cursor.execute(query2)
                row = cursor.fetchone()
                if row:
                    destination_county_code = row[0]'''

                query = "Insert into fm_lm_connections values('"+str(conn_id)+"','"+str(origin_id)+"','"+str(destination_id)+"','"+str(commodity)+"','"+str(fewsion_unit_type)+"',"+str(fewsion_unit_value)+","+str(fewsion_unit_dollar)+",'"+str(sc_step)+"','"+str(date_recorded)+"','"+str(origin_county_code)+"','"+str(destination_county_code)+"');"
                print(query)
                cursor.execute(query)
                connection.commit()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
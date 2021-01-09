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

        query = "Select * from mesoscale;"
        cursor.execute(query)
        row = cursor.fetchall()

        row = row[1:]
        for i in row:
            meso_id = int(i[0])
            if meso_id<201003391:
                query = "Update mesoscale set data_source = 'phoenix_inflows_to_people_data' where ms_id = '"+str(meso_id)+"';"
                cursor.execute(query)
                connection.commit()
            elif meso_id<201006353:
                query = "Update mesoscale set data_source = 'phoenix_inflows_to_distribution_centers_data' where ms_id = '" + str(meso_id) + "';"
                cursor.execute(query)
                connection.commit()
            elif meso_id<201009314:
                query = "Update mesoscale set data_source = 'Phoenix_inflows_to_food_processors_data_refining' where ms_id = '" + str(meso_id) + "';"
                cursor.execute(query)
                connection.commit()
            elif meso_id<201010596:
                query = "Update mesoscale set data_source = 'flagstaff_inflows_to_distribution_centers_data' where ms_id = '" + str(meso_id) + "';"
                cursor.execute(query)
                connection.commit()
            elif meso_id<201011871:
                query = "Update mesoscale set data_source = 'flagstaff_inflows_to_food_processors_data' where ms_id = '" + str(meso_id) + "';"
                cursor.execute(query)
                connection.commit()
            else:
                query = "Update mesoscale set data_source = 'flagstaff_inflows_to_people_data' where ms_id = '" + str(meso_id) + "';"
                cursor.execute(query)
                connection.commit()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
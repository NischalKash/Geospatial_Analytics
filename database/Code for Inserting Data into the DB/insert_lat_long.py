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

        query = "select state_listing_id,state_name from state;"
        cursor.execute(query)
        state_info = cursor.fetchall()
        state_dict = {}
        for i in state_info[1:]:
            state_dict[i[1]] = i[0]

        state_dict['Alabama'] = "1"
        print(state_dict)
        with open('uscounties.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            a = []
            for row in csv_reader:
                a.append(row)
            a = a[1:]
            for data in a:
                county_name = data[1]+' County'
                state_name = data[2]
                latitude = data[7]
                longitude = data[6]

                if state_dict[state_name]== "72":
                    county_name=county_name+" "+"Municipio"
                    print(county_name)

                if state_dict[state_name] == "22":
                    county_name = county_name + " " + "Parish"
                    print(county_name)

                query = "update county set county.latitude = "+str(latitude)+" , county.longitude = "+str(longitude) + " where county_name = '"+str(county_name)+"' and state_listing_id = '"+str(state_dict[state_name])+"';"
                cursor.execute(query)
                connection.commit()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
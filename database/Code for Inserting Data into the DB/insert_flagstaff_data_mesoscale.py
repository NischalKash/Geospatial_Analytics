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

        query = "Select * from commodity;"
        cursor.execute(query)
        record = cursor.fetchall()

        dict_map = {}
        for i in record:
            dict_map[i[3]] = i[0]

        query = "Select * from mesoscale;"
        cursor.execute(query)
        record = cursor.fetchall()

        last_val = int(record[-1][0])
        print(last_val)
        next_val = last_val+1

        with open('flagstaff_inflows_to_distribution_centers_data_Refined.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                mesoscale_id = str(next_val+1)
                origin_county = str(row[0])
                origin_sc_step = '3'
                dest_county = row[2]
                dest_sc_step = '6'
                commodity_id = str(dict_map[row[4]])
                fewsion_unit_type = str(row[5])
                fewsion_unit_value = str(row[6])
                fewsion_dollar_value = str(row[7])
                next_val+=1

                query = "insert into mesoscale values('"+mesoscale_id+"','"+origin_county+"','"+origin_sc_step+"','"+dest_county+"','"+dest_sc_step+"','"+commodity_id+"','"+fewsion_unit_type+"','"+fewsion_unit_value+"','"+fewsion_dollar_value+"','Null');"
                print(query)
                cursor.execute(query)
                connection.commit()

        with open('flagstaff_inflows_to_food_processors_data_Refined.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                mesoscale_id = str(next_val + 1)
                origin_county = str(row[0])
                origin_sc_step = '3'
                dest_county = row[2]
                dest_sc_step = '6'
                commodity_id = str(dict_map[row[4]])
                fewsion_unit_type = str(row[5])
                fewsion_unit_value = str(row[6])
                fewsion_dollar_value = str(row[7])
                next_val+=1

                query = "insert into mesoscale values('" + mesoscale_id + "','" + origin_county + "','" + origin_sc_step + "','" + dest_county + "','" + dest_sc_step + "','" + commodity_id + "','" + fewsion_unit_type + "','" + fewsion_unit_value + "','" + fewsion_dollar_value + "','Null');"
                print(query)
                cursor.execute(query)
                connection.commit()

        with open('flagstaff_inflows_to_people_data_Refined.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                mesoscale_id = str(next_val + 1)
                origin_county = str(row[0])
                origin_sc_step = '3'
                dest_county = row[2]
                dest_sc_step = '6'
                commodity_id = str(dict_map[row[4]])
                fewsion_unit_type = str(row[5])
                fewsion_unit_value = str(row[6])
                fewsion_dollar_value = str(row[7])
                next_val+=1

                query = "insert into mesoscale values('" + mesoscale_id + "','" + origin_county + "','" + origin_sc_step + "','" + dest_county + "','" + dest_sc_step + "','" + commodity_id + "','" + fewsion_unit_type + "','" + fewsion_unit_value + "','" + fewsion_dollar_value + "','Null');"
                print(query)
                cursor.execute(query)
                connection.commit()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
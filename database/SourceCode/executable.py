import mysql.connector
from mysql.connector import Error

def check_path(source,fm_lm,meso,last_mile,origin):
    print(source)
    condition = False
    condition2 = False
    for i in fm_lm:
        if i[1]==source:
            condition = True
            print("Calling for ",i[2])
            output = str(i[1])+'->'+check_path(i[2],fm_lm,meso,last_mile,origin)
            print("Received Output Gamma")
    if condition==False:
        query = "SELECT county_code FROM node where node_id=" + str(source)
        cursor.execute(query)
        row = cursor.fetchone()[0]
        count1 = 0
        for i in meso:
            if row==i[1]:
                count2 = 0
                for j in last_mile:
                    query = "SELECT county_code FROM node where node_id=" + str(j[1])
                    cursor.execute(query)
                    row2 = cursor.fetchone()[0]
                    if row2==i[3]:
                        condition2 = True
                        print("Recursive Calling for ", j[1])
                        output = str(source) + '->' + check_path(j[1], fm_lm, meso, last_mile,origin)
                        print("Received Output Delta")
                    count2+=1
            count1+=1

    if condition2==False and condition==False:
        print("Alpha",source)
        return str(source)
    print("Beta",output)
    return output


try:
    connection = mysql.connector.connect(host="localhost",database="geospatial",user="root",password="Kashyap@1995")
    if connection.is_connected():
        db_Info = connection.get_server_info()
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        commodity_id = int(input("Please enter the commodity id you want to visualize"))
        #commodity_id = 1200
        query = "SELECT * FROM fm_lm_connections where Commodity_id="+str(commodity_id)
        cursor.execute(query)
        row = cursor.fetchone()
        values = []
        while row is not None:
            values.append(row)
            row = cursor.fetchone()
        first_mile = []
        last_mile = []

        query = "SELECT * FROM mesoscale where Commodity_id=" + str(commodity_id)
        cursor.execute(query)
        row = cursor.fetchone()
        values_meso = []
        while row is not None:
            values_meso.append(row)
            row = cursor.fetchone()
        for i in values:
            if i[7]=='fm':
                first_mile.append(i)
            else:
                last_mile.append(i)
        first_origin = []
        all_origin = []
        all_dest = []
        for i in first_mile:
            all_origin.append(i[1])
            all_dest.append(i[2])

        start_origin = []
        for i in all_origin:
            if i not in all_dest:
                start_origin.append(i)
        final_path = []

        for i in start_origin:
            path_name = ""
            path_string = check_path(i,values,values_meso,last_mile,all_origin)
            path_string = path_string.split('->')
            for i in path_string:
                query = "SELECT county_code FROM node where node_id=" + str(i)
                cursor.execute(query)
                row2 = cursor.fetchone()[0]
                query = "SELECT county_name FROM county where county_id=" + str(row2)
                cursor.execute(query)
                row3 = cursor.fetchone()[0]
                query = "SELECT name FROM node where node_id =" + str(i)
                cursor.execute(query)
                row4 = cursor.fetchone()[0]
                path_name += str(row4) + '(' + row3 + ')' + '->'
            final_path.append(path_name)
        for i in final_path:
            print("")
            print(i[0:len(i)-2])
            print("")

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
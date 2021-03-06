import mysql.connector
from mysql.connector import Error

#This function is used to find the last_mile aggregated data for each county for a commodity id!
def traverse_lastmile(lastmile):
    dict = {}

    #Iterate over the last_mile list
    for i in last_mile:
        #Find out the start_node,next_node to which it would go to! This is because the next node may differ and we may need to keep track of the two transfers!
        #Also find out the county ids for both the nodes!

        start_node = i[1]
        next_node = i[2]
        start_node_county = i[9]
        next_node_county = i[10]

        #Update the dictionaries with fewsion dollar values if key found else initialize!
        key_dict = str(start_node)+'-'+str(next_node)+'-'+str(start_node_county)+'-'+str(next_node_county)
        if key_dict not in dict:
            dict[key_dict] = i[6]

    new_dict = {}

    #The below code is written to aggregate it with respect to counties
    for i in dict:
        val = i.split('-')
        receiving_county_code = val[3]
        if receiving_county_code in new_dict:
            new_dict[receiving_county_code] += dict[i]
        else:
            new_dict[receiving_county_code]=dict[i]

    return new_dict

#This function is used to find the mesoscale aggregated data for each county for a commodity id!
def traverse_meso(mesoscale):
    sending_counties = {}
    receiving_counties = {}

    #Iterate over the mesoscale
    for i in mesoscale:
        #add the source for the commodity id to the sending_counties dictionary if not found! If found update it!
        if i[1] in sending_counties:
            sending_counties[i[1]]+=i[8]
        else:
            sending_counties[i[1]] = i[8]
        #add the destinations for the commodity id to the receiving_counties dictionary if not found! If found update it!
        if i[3] in receiving_counties:
            receiving_counties[i[3]]+=i[8]
        else:
            receiving_counties[i[3]] = i[8]

    #return both the dictionaries
    return [sending_counties,receiving_counties]

def find_last_node(start_node,commodity_id,diction):
    query = "SELECT Dest_node_id FROM fm_lm_connections where commodity_id=" + str(commodity_id) + " and Origin_node_id="+str(start_node) + " and Sc_step_fmlm = 'fm'"
    cursor.execute(query)
    row = cursor.fetchone()
    dest_nodes = []
    while row is not None:
        dest_nodes.append(row[0])
        row = cursor.fetchone()

    condition = False
    for i in dest_nodes:
        condition = True
        node_val = find_last_node(i,commodity_id,diction)
        if node_val[1]=="END":
            query = "SELECT Fewsion_dollar_value FROM fm_lm_connections where commodity_id=" + str(commodity_id) + " and Dest_node_id = " + str(i) + " and Sc_step_fmlm = 'fm'" + "and Origin_node_id = "+str(start_node)
            cursor.execute(query)
            row = cursor.fetchone()[0]
            diction[str(start_node)+'-'+str(i)+'-'+str(commodity_id)] = row

    if condition:
        return [diction, "Done"]
    else:
        return [{},"END"]

def find_values(first_mile,commodity_id):
    origin_node = []
    final_dict = {}
    node1 = []
    node2 = []
    for j in first_mile:
        node1.append(j[1])
        node2.append(j[2])
    for j in node1:
        if j not in node2:
            origin_node.append(j)

    for j in origin_node:
        diction = {}
        find_last_node(j,commodity_id,diction)
        for i in diction:
            find_county_val = i.split('-')
            start_node_val = find_county_val[0]
            dest_node_val = find_county_val[1]

            query = "SELECT dest_county_code FROM fm_lm_connections where commodity_id=" + str(commodity_id) + " and Dest_node_id = " + str(dest_node_val) + " and Sc_step_fmlm = 'fm'" + "and Origin_node_id = " + str(start_node_val)
            cursor.execute(query)
            row = cursor.fetchone()[0]

            if row not in final_dict:
                final_dict[row] = diction[i]
            else:
                final_dict[row] += diction[i]

    return final_dict

try:
    connection = mysql.connector.connect(host="localhost", database="geospatial", user="root", password="Kashyap@1995")
    if connection.is_connected():
        db_Info = connection.get_server_info()
        cursor = connection.cursor(buffered=True)
        cursor.execute("select database();")
        record = cursor.fetchone()
        commodity_id = int(input("Please enter the commodity id you want to visualize"))

        query = "SELECT * FROM fm_lm_connections where Commodity_id="+str(commodity_id)
        cursor.execute(query)
        row = cursor.fetchone()
        values = []
        while row is not None:
            values.append(row)
            row = cursor.fetchone()
        first_mile = []
        last_mile = []
        for i in values:
            if i[7] == 'fm':
                first_mile.append(i)
            else:
                last_mile.append(i)

        fm_dollar_values = find_values(first_mile,commodity_id)

        print("\nCommodity_ID = ",commodity_id)
        print("\nFM_LM_connections\n")
        print(fm_dollar_values)

        #retreives all the mesoscale data with respect to the commodity entered above
        query = "SELECT * FROM mesoscale where Commodity_id=" + str(commodity_id)
        cursor.execute(query)
        row = cursor.fetchone()

        #The returned data structure is one single object, in order to get all the rows, we iterate through
        values_meso = []
        while row is not None:
            values_meso.append(row)
            row = cursor.fetchone()

        #To find the aggregated values in mesoscale table
        values_meso = traverse_meso(values_meso)

        #Contains all the aggregated values for a particular if it is in the origin column, that is if it is the source!
        sending_counties = values_meso[0]

        # Contains all the aggregated values for a particular if it is in the destination column, that is if it is the destination!
        receiving_counties = values_meso[1]

        #Print the Mesoscale Data
        print("\nMesoscale Data\n")
        print("Sending Counties = ",sending_counties)
        print("Receiving Counties = ",receiving_counties)

        #Traversing Last Mile
        last_mile_values = traverse_lastmile(last_mile)

        #Printing the Last Mile Datas
        print("\nLast_Mile\n")
        print(last_mile_values)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()





import mysql.connector
from mysql.connector import Error
import networkx
import matplotlib.pyplot as plt
from operator import itemgetter

def plot(values_meso):
    option = int(input())
    if option == 1:
        print("The mapping for First Mile - Mesoscale for the Commodity ID : ", commodity_id)
    elif option == 2:
        transfer_data = values_meso[2]
        transfer_data = transfer_data[0:10]
        transfer_data = sorted(transfer_data, key=itemgetter(2), reverse=False)
        elarge = []
        esmall = []
        for i in transfer_data:
            if i[2] > 1:
                elarge.append((i[0], i[1]))
            else:
                esmall.append((i[0], i[1]))
        G = networkx.DiGraph()
        for i in transfer_data:
            if i[0] not in G:
                G.add_node(i[0])
            if i[1] not in G:
                G.add_node(i[1])
            G.add_edge(i[0], i[1], weight=i[2])
        pos = networkx.circular_layout(G)
        networkx.draw_networkx_nodes(G, pos, node_size=100)
        networkx.draw_networkx_edges(G, pos, edgelist=elarge, width=2)
        networkx.draw_networkx_edges(G, pos, edgelist=esmall, width=2, alpha=0.5, edge_color="b", style="dashed")
        networkx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
        labels = networkx.get_edge_attributes(G, 'weight')
        networkx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.show()
    elif option == 3:
        print(last_mile_values)

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
        receiving_county_code = val[2]
        if receiving_county_code in new_dict:
            new_dict[receiving_county_code] += dict[i]
        else:
            new_dict[receiving_county_code]=dict[i]
    return new_dict

#This function is used to find the mesoscale aggregated data for each county for a commodity id!
def traverse_meso(mesoscale):
    sending_counties = {}
    receiving_counties = {}
    transfer_data = []
    #Iterate over the mesoscale
    for i in mesoscale:
        if [i[1],i[3],i[8]] not in transfer_data:
            transfer_data.append([i[1],i[3],i[8]])

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
    return [sending_counties,receiving_counties,transfer_data]

def find_last_node(start_node,commodity_id,county):
    query = "SELECT Dest_node_id FROM fm_lm_connections where commodity_id=" + str(commodity_id) + " and Origin_node_id="+str(start_node)+" and origin_county_code="+str(county) + " and Sc_step_fmlm = 'fm'"
    cursor.execute(query)
    row = cursor.fetchone()
    if row:
        node_val = find_last_node(row[0],commodity_id,county)
        if node_val=="END":
            return row[0]
        else:
            return node_val
    else:
        return "END"

def find_counties(first_mile):
    glob = []
    for i in first_mile:
        if i[-1] not in glob:
            glob.append(i[-1])
    return glob

def find_values(first_mile,counties,commodity_id):
    dict = {}
    for i in counties:
        origin_node = []
        new_first_mile = []
        for j in first_mile:
            if j[-1]==i:
                new_first_mile.append(j)
        node1 = []
        node2 = []
        for j in new_first_mile:
            node1.append(j[1])
            node2.append(j[2])
        for j in node1:
            if j not in node2:
                origin_node.append(j)

        for j in origin_node:
            node_val = find_last_node(j,commodity_id,i)
            query = "SELECT Fewsion_dollar_value FROM fm_lm_connections where commodity_id=" + str(commodity_id) + " and Dest_node_id=" + str(node_val) + " and origin_county_code=" + str(i) + " and Sc_step_fmlm= 'fm'"
            cursor.execute(query)
            dollar_value = cursor.fetchone()[0]
            dict[str(i) + '-' + str(commodity_id) + '-' + str(node_val)] = dollar_value
    return dict

try:
    connection = mysql.connector.connect(host="localhost", database="geospatial_okan", user="root", password="Kashyap@1995")
    if connection.is_connected():
        db_Info = connection.get_server_info()
        cursor = connection.cursor(buffered=True)
        cursor.execute("select database();")
        record = cursor.fetchone()
        commodity_id = int(input("Please enter the commodity id you want to visualize"))

        query = "SELECT * FROM fm_lm_connections where Commodity_id='"+str(commodity_id)+"'"
        print(query)
        cursor.execute(query)
        row = cursor.fetchone()
        values = []
        while row is not None:
            values.append(row)
            row = cursor.fetchone()
        print(values)
        first_mile = []
        last_mile = []
        for i in values:
            if i[7] == 'fm':
                first_mile.append(i)
            else:
                last_mile.append(i)

        counties = find_counties(first_mile)
        fm_dollar_values = find_values(first_mile,counties,commodity_id)
        new_dict = {}
        for i in fm_dollar_values:
            a = i.split('-')
            county_code = a[0]
            if county_code not in new_dict:
                new_dict[county_code] = fm_dollar_values[i]
            else:
                new_dict[county_code] += fm_dollar_values[i]
        print("\nCommodity_ID = ",commodity_id)
        print("\nFM_LM_connections\n")
        print(new_dict)

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

        print("For viewing the mapping between Different domains, please select the respective numbers")
        print("1. First Mile - Mesoscale")
        print("2. Mesoscale - Mesoscale")
        print("3. Mesoscale - Last Mile")
        print("\n")
        plot(values_meso)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()





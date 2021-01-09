#Center for Geospatial Analytics
#Code Author - Nischal Badarinath Kashyap
#NC State University

from django.shortcuts import render
import mysql.connector
from mysql.connector import Error
from operator import itemgetter
import folium
import random
import os
from folium import plugins
import json

USER_SELECTION = 0
#Global variable which is used to decide which option user selects

COUNTY_CODE = None

#This function is used for data visualization
def plot(values_meso,last_mile_edges,first_mile_edges):
    #Create an instance of the map using Folium
    m = folium.Map(locations=[-112.48849364, 33.3596368342], zoom_start=12, tiles='OpenStreetMap', control_scale=True)

    #Used to insert Counties into the map
    data = [json.loads(line) for line in open('/Users/nischalkashyap/Downloads/Fall 2020/Research Assistant GIS/database/djangoapp/geospatial/visualization/templates/visualization/us_geoson.json', 'r')]
    folium.TopoJson(data[0], 'objects.us_counties_20m', name='topojson').add_to(m)

    #Based on user selection, project the necessary data onto the map
    #For First Mile to First Mile

    if USER_SELECTION == 'FM':
        #Used to keep track of all the nodes inserted onto the map
        marked_tracker = []
        for i in first_mile_edges:
            val = i.split('*')
            fewsion_dollar_value = float(val[6])
            edge = [[float(val[0]), float(val[1])], [float(val[3]), float(val[4])]]

            popup_source = '<strong>' + val[2] + '</strong>'
            popup_destination = '<strong>' + val[5] + '</strong>'
            tooltip = "Click for More Info"

            #Create markers on the map based on the nodes in the edge entity
            if val[0] + val[1] not in marked_tracker:
                folium.Marker([float(val[0]), float(val[1])], popup=popup_source, tooltip=tooltip,
                              icon=folium.Icon(icon='cloud', color='red')).add_to(m)
                marked_tracker.append(val[0] + val[1])

            if val[3] + val[4] not in marked_tracker:
                folium.Marker([float(val[3]), float(val[4])], popup=popup_destination, tooltip=tooltip,
                              icon=folium.Icon(icon='cloud', color='red')).add_to(m)
                marked_tracker.append(val[3] + val[4])

            #Make the edges size based on the fewsion dollar value of that particular edge
            if fewsion_dollar_value < 1:
                folium.PolyLine(edge, weight=1.0, color="green").add_to(m)
            elif fewsion_dollar_value >= 1 and fewsion_dollar_value < 2:
                folium.PolyLine(edge, weight=2.0, color="blue").add_to(m)
            else:
                folium.PolyLine(edge, weight=3.0, color="black").add_to(m)
    # For First Mile to Mesoscale
    elif USER_SELECTION == "FM-MESOSCALE":
        marked_tracker = []
        for i in first_mile_edges:
            val = i.split('*')
            fewsion_dollar_value = float(val[6])
            edge = [[float(val[0]), float(val[1])], [float(val[3]), float(val[4])]]

            popup_source = '<strong>' + val[2] + '</strong>'
            popup_destination = '<strong>' + val[5] + '</strong>'
            tooltip = "Click for More Info"

            if val[0] + val[1] not in marked_tracker:
                folium.Marker([float(val[0]), float(val[1])], popup=popup_source, tooltip=tooltip,
                              icon=folium.Icon(icon='cloud', color='red')).add_to(m)
                marked_tracker.append(val[0] + val[1])

            if val[3] + val[4] not in marked_tracker:
                folium.Marker([float(val[3]), float(val[4])], popup=popup_destination, tooltip=tooltip,
                              icon=folium.Icon(icon='cloud', color='red')).add_to(m)
                marked_tracker.append(val[3] + val[4])

            if fewsion_dollar_value < 1:
                folium.PolyLine(edge, weight=1.0, color="blue").add_to(m)
            elif fewsion_dollar_value >= 1 and fewsion_dollar_value < 2:
                folium.PolyLine(edge, weight=2.0, color="blue").add_to(m)
            else:
                folium.PolyLine(edge, weight=3.0, color="blue").add_to(m)

        transfer_data = values_meso[2]
        all_connections = {}
        #Logic to identify if any two entries are present which has same source node and destination node
        #If yes, we tend to aggregate the fewsion_dollar_value
        for i in transfer_data:
            if (i[0], i[1]) not in all_connections:
                all_connections[(i[0], i[1])] = float(i[2])
            else:
                all_connections[(i[0], i[1])] += float(i[2])
        #All Connections is a dictionary used to store the aggregated fewsion dollar values of two counties if present in the mesoscale data
        marked_tracker = []

        for i in all_connections:
            source_county = i[0]
            destination_county = i[1]

            #find Coordinates for the source county
            query = "select latitude,longitude,county_name from county where county_id = '" + str(source_county) + "';"
            cursor.execute(query)
            row = cursor.fetchone()

            #find Coordinates for the destination county
            query = "select latitude,longitude,county_name from county where county_id = '" + str(destination_county) + "';"
            cursor.execute(query)
            row_dest = cursor.fetchone()

            #Store the fewsion dollar value of the respective edge
            fewsion_dollar_value = all_connections[i]
            edge = [[row[0], row[1]], [row_dest[0], row_dest[1]]]

            popup_source = '<strong>' + row[2] + '</strong>'
            popup_destination = '<strong>' + row_dest[2] + '</strong>'
            tooltip = "Click for More Info"

            # Create markers on the map based on the nodes in the edge entity
            if source_county not in marked_tracker:
                folium.Marker([row[0], row[1]], popup=popup_source, tooltip=tooltip, icon=folium.Icon
                (icon='cloud', color='green')).add_to(m)
                marked_tracker.append(source_county)

            folium.Marker([row_dest[0], row_dest[1]], popup=popup_destination, tooltip=tooltip, icon=folium.Icon
            (icon='cloud', color='green')).add_to(m)
            marked_tracker.append(destination_county)

            # plugins.AntPath(edge).add_to(m) -> This code is for displaying flow
            # Make the edges size based on the fewsion dollar value of that particular edge
            if fewsion_dollar_value < 1:
                folium.PolyLine(edge, weight=1.0, color="black").add_to(m)
            elif fewsion_dollar_value >= 1 and fewsion_dollar_value < 2:
                folium.PolyLine(edge, weight=2.0, color="black").add_to(m)
            else:
                folium.PolyLine(edge, weight=3.0, color="black").add_to(m)
    # For Mesoscale to Mesoscale
    elif USER_SELECTION == "MESOSCALE INFLOWS" or USER_SELECTION=='MESOSCALE OUTFLOWS':
        transfer_data = values_meso[2]
        all_connections = {}
        for i in transfer_data:
            if (i[0],i[1]) not in all_connections:
                all_connections[(i[0],i[1])] = float(i[2])
            else:
                all_connections[(i[0], i[1])] += float(i[2])
        marked_tracker = []

        for i in all_connections:
            if i[0] == COUNTY_CODE or i[1]==COUNTY_CODE:
                source_county = i[0]
                destination_county = i[1]
                query = "select latitude,longitude,county_name from county where county_id = '"+str(source_county)+"';"
                cursor.execute(query)
                row = cursor.fetchone()
    
                query = "select latitude,longitude,county_name from county where county_id = '" + str(destination_county) + "';"
                cursor.execute(query)
                row_dest = cursor.fetchone()
    
                fewsion_dollar_value = all_connections[i]
                edge = [[row[0],row[1]],[row_dest[0],row_dest[1]]]

                popup_source = '<a href = "http://127.0.0.1:8000/" target="_blank">Google</a>'
                #popup_source = '<strong>'+row[2]+'</strong>'
                popup_destination = '<strong>'+row_dest[2]+'</strong>'
                tooltip = "Click for More Info"
    
                if source_county not in marked_tracker:
                    folium.Marker([row[0],row[1]],popup=popup_source,tooltip = tooltip,icon=folium.Icon
                    (icon='cloud',color='red')).add_to(m)
                    marked_tracker.append(source_county)
    
                folium.Marker([row_dest[0], row_dest[1]], popup=popup_destination,tooltip=tooltip,icon=folium.Icon
                (icon='cloud',color='green')).add_to(m)
                marked_tracker.append(destination_county)

                plugins.AntPath(edge).add_to(m)
                '''if fewsion_dollar_value<1:
                    folium.PolyLine(edge, weight=1.0, color="green").add_to(m)
                elif fewsion_dollar_value>=1 and fewsion_dollar_value<2:
                    folium.PolyLine(edge, weight=2.0, color="blue").add_to(m)
                else:
                    folium.PolyLine(edge, weight=3.0, color="black").add_to(m)'''
    # For Mesocale to Last Mile
    elif USER_SELECTION == "MESOSCALE-LM":
        marked_tracker = []
        for i in last_mile_edges:
            val = i.split('*')
            fewsion_dollar_value = float(val[6])
            edge = [[float(val[0]), float(val[1])], [float(val[3]), float(val[4])]]

            popup_source = '<strong>' + val[2] + '</strong>'
            popup_destination = '<strong>' + val[5] + '</strong>'
            tooltip = "Click for More Info"

            if val[0] + val[1] not in marked_tracker:
                folium.Marker([float(val[0]), float(val[1])], popup=popup_source, tooltip=tooltip,
                              icon=folium.Icon(icon='cloud', color='red')).add_to(m)
                marked_tracker.append(val[0] + val[1])

            if val[3] + val[4] not in marked_tracker:
                folium.Marker([float(val[3]), float(val[4])], popup=popup_destination, tooltip=tooltip,
                              icon=folium.Icon(icon='cloud', color='red')).add_to(m)
                marked_tracker.append(val[3] + val[4])

            if fewsion_dollar_value < 1:
                folium.PolyLine(edge, weight=1.0, color="green").add_to(m)
            elif fewsion_dollar_value >= 1 and fewsion_dollar_value < 2:
                folium.PolyLine(edge, weight=2.0, color="blue").add_to(m)
            else:
                folium.PolyLine(edge, weight=3.0, color="black").add_to(m)

        transfer_data = values_meso[2]
        all_connections = {}
        for i in transfer_data:
            if (i[0], i[1]) not in all_connections:
                all_connections[(i[0], i[1])] = float(i[2])
            else:
                all_connections[(i[0], i[1])] += float(i[2])
        marked_tracker = []

        for i in all_connections:
            source_county = i[0]
            destination_county = i[1]
            query = "select latitude,longitude,county_name from county where county_id = '" + str(source_county) + "';"
            cursor.execute(query)
            row = cursor.fetchone()

            query = "select latitude,longitude,county_name from county where county_id = '" + str(
                destination_county) + "';"
            cursor.execute(query)
            row_dest = cursor.fetchone()

            fewsion_dollar_value = all_connections[i]
            edge = [[row[0], row[1]], [row_dest[0], row_dest[1]]]

            popup_source = '<strong>' + row[2] + '</strong>'
            popup_destination = '<strong>' + row_dest[2] + '</strong>'
            tooltip = "Click for More Info"

            if source_county not in marked_tracker:
                folium.Marker([row[0], row[1]], popup=popup_source, tooltip=tooltip, icon=folium.Icon
                (icon='cloud', color='red')).add_to(m)
                marked_tracker.append(source_county)

            folium.Marker([row_dest[0], row_dest[1]], popup=popup_destination, tooltip=tooltip, icon=folium.Icon
            (icon='cloud', color='green')).add_to(m)
            marked_tracker.append(destination_county)

            plugins.AntPath(edge).add_to(m)
            '''if fewsion_dollar_value < 1:
                folium.PolyLine(edge, weight=1.0, color="green").add_to(m)
            elif fewsion_dollar_value >= 1 and fewsion_dollar_value < 2:
                folium.PolyLine(edge, weight=2.0, color="blue").add_to(m)
            else:
                folium.PolyLine(edge, weight=3.0, color="black").add_to(m)'''
    # For Last Mile to Last Mile
    elif USER_SELECTION == 'LM':
        marked_tracker = []
        for i in last_mile_edges:
            val = i.split('*')
            fewsion_dollar_value = float(val[6])
            edge = [[float(val[0]), float(val[1])], [float(val[3]), float(val[4])]]

            popup_source = '<strong>' + val[2] + '</strong>'
            popup_destination = '<strong>' + val[5] + '</strong>'
            tooltip = "Click for More Info"

            if val[0] + val[1] not in marked_tracker:
                folium.Marker([float(val[0]), float(val[1])], popup=popup_source, tooltip=tooltip,
                              icon=folium.Icon(icon='cloud', color='red')).add_to(m)
                marked_tracker.append(val[0] + val[1])

            if val[3] + val[4] not in marked_tracker:
                folium.Marker([float(val[3]), float(val[4])], popup=popup_destination, tooltip=tooltip,
                              icon=folium.Icon(icon='cloud', color='red')).add_to(m)
                marked_tracker.append(val[3] + val[4])

            if fewsion_dollar_value < 1:
                folium.PolyLine(edge, weight=1.0, color="green").add_to(m)
            elif fewsion_dollar_value >= 1 and fewsion_dollar_value < 2:
                folium.PolyLine(edge, weight=2.0, color="blue").add_to(m)
            else:
                folium.PolyLine(edge, weight=3.0, color="black").add_to(m)

    #Save the Map
    m.save('visualization/templates/visualization/map.html')

#This function queries to the database to find all the edges and the respective nodes positional cooridinates.
def find_edges(first_mile):

    first_mile_edges = []
    for i in first_mile:
        origin_node_id = i[1]
        destination_node_id = i[2]
        fewsion_dollar_value = i[6]

        query = "SELECT latitude,longitude,name FROM node where node_id='" + str(origin_node_id) + "';"
        cursor.execute(query)
        coordinates_start_node = cursor.fetchone()

        query = "SELECT latitude,longitude,name FROM node where node_id='" + str(destination_node_id) + "';"
        cursor.execute(query)
        coordinates_next_node = cursor.fetchone()

        #Stores the positional latitude longitude in a string format which will be retrieved later.
        edges = str(coordinates_start_node[0]) + '*' + str(coordinates_start_node[1]) + '*' + str(
            coordinates_start_node[2]) + '*' + str(coordinates_next_node[0]) + '*' + str(
            coordinates_next_node[1]) + '*' + str(coordinates_next_node[2]) + '*' + str(fewsion_dollar_value)

        first_mile_edges.append(edges)

    return first_mile_edges

#This function is used to find the first_mile aggregated data for each county for a commodity id!
def traverse_firstmile(first_mile):

    #This function is called to get the first mile edges traversed by the commodity in a particular county
    edges = find_edges(first_mile)
    original_nodes = []
    nonoriginal_nodes = []

    #Stores the source and destination nodes of all the rows of first mile data
    for i in first_mile:
        original_nodes.append(i[1])
        nonoriginal_nodes.append(i[2])

    #Finds the nodes or points at which the data forms the interface with mesoscale
    last_nodes = []
    for i in nonoriginal_nodes:
        if i not in original_nodes:
            last_nodes.append(i)

    #Finds all the edges whose destination points are in the last_nodes!
    last_edges_information = []
    for i in last_nodes:
        for j in first_mile:
            if j[2]==i:
                last_edges_information.append(j)

    return [last_edges_information,edges]

#This function is used to find the last_mile aggregated data for each county for a commodity id!
def traverse_lastmile(last_mile):
    dict = {}
    last_mile_edges = []
    #Iterate over the last_mile list
    for i in last_mile:
        #Find out the start_node,next_node to which it would go to! This is because the next node may differ and we may need to keep track of the two transfers!
        #Also find out the county ids for both the nodes!
        start_node = i[1]
        next_node = i[2]
        fewsion_dollar_value = i[6]
        start_node_county = i[9]
        next_node_county = i[10]

        #Update the dictionaries with fewsion dollar values if key found else initialize!
        key_dict = str(start_node)+'-'+str(next_node)+'-'+str(start_node_county)+'-'+str(next_node_county)+'-'+str(fewsion_dollar_value)
        if key_dict not in dict:
            dict[key_dict] = i[6]
        else:
            dict[key_dict] += i[6]

        query = "SELECT latitude,longitude,name FROM node where node_id='"+str(start_node)+"';"
        cursor.execute(query)
        coordinates_start_node = cursor.fetchone()

        query = "SELECT latitude,longitude,name FROM node where node_id='" + str(next_node) + "';"
        cursor.execute(query)
        coordinates_next_node = cursor.fetchone()

        edges = str(coordinates_start_node[0])+'*'+str(coordinates_start_node[1])+'*'+str(coordinates_start_node[2])+'*'+str(coordinates_next_node[0])+'*'+str(coordinates_next_node[1])+'*'+str(coordinates_next_node[2])+'*'+str(fewsion_dollar_value)
        last_mile_edges.append(edges)

    new_dict = {}
    #The below code is written to aggregate it with respect to counties
    for i in dict:
        val = i.split('-')
        receiving_county_code = val[2]
        if receiving_county_code in new_dict:
            new_dict[receiving_county_code] += dict[i]
        else:
            new_dict[receiving_county_code]=dict[i]
    return [new_dict,last_mile_edges]

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

#Base Functions which starts the whole web app
def home(request):
    #return render(request, "visualization/home.html")
    os.system('python3 populate_json.py')
    return render(request, "visualization/basepage.html")

def json_file(request):
    return render(request, "visualization/data.json")

def js_file(request):
    return render(request, "visualization/map.js")

#this function is called if the user chooses first mile to first mile
def visualization(request):
    if request.method == "POST":
        #receive county code and commodity_id from the user
        commodity_id = request.POST.get('commodity', "")
        commodity_id = '1103003'
        county_id = request.POST.get('county', "")
        global USER_SELECTION
        USER_SELECTION = request.POST.get('transfer', "")
        try:
            #Setup the database connection
            connection = mysql.connector.connect(host="localhost", database="geospatial_okan", user="root",
                                                 password="Kashyap@1995")
            if connection.is_connected():
                global cursor
                cursor = connection.cursor(buffered=True)
                cursor.execute("select database();")

                global COUNTY_CODE
                COUNTY_CODE = county_id

                #Query to retrive all the fm_lm_connections data
                query = "SELECT * FROM fm_lm_connections where Commodity_id='" + str(commodity_id) + "';"
                cursor.execute(query)
                row = cursor.fetchall()

                first_mile = []
                last_mile = []

                #This code is used to separate the first mile with last mile
                for i in row:
                    if i[7]=='FM':
                        if i[9]==COUNTY_CODE or i[10]==COUNTY_CODE:
                            first_mile.append(i)
                    else:
                        if i[9] == COUNTY_CODE or i[10] == COUNTY_CODE:
                            last_mile.append(i)

                #Send First mile data for visualization! Receive output in necessary format.
                first_mile_data = traverse_firstmile(first_mile)

                values_first_mile = first_mile_data[0]
                #Stores the row entities of first mile data

                #This part of the code is to determine the total amount of fewsion_dollar_value
                #for the last particular mesoscale interface point
                total_fewsion_values = {}
                for i in values_first_mile:
                    if i[10] not in total_fewsion_values:
                        total_fewsion_values[i[10]] = i[6]
                    else:
                        total_fewsion_values[i[10]] += i[6]

                #retreives all the mesoscale data with respect to the commodity entered above
                query = "SELECT * FROM mesoscale where Commodity_id='" + str(commodity_id)+"' and (origin_county = '" + str(COUNTY_CODE) + "' or dest_county = '" + str(COUNTY_CODE) + "');"
                cursor.execute(query)
                row = cursor.fetchall()

                # The returned data structure is one single object, in order to get all the rows, we iterate through
                values_meso = []
                for i in row:
                    if USER_SELECTION=='MESOSCALE INFLOWS' or USER_SELECTION=='FM-MESOSCALE':
                        if i[3]==COUNTY_CODE:
                            values_meso.append(i)
                    elif USER_SELECTION=='MESOSCALE OUTFLOWS' or USER_SELECTION=='MESOSCALE-LM':
                        if i[1]==COUNTY_CODE:
                            values_meso.append(i)

                # To find the aggregated values in mesoscale table
                values_meso = traverse_meso(values_meso)

                #Send last mile data for visualization! Receive output in necessary format.
                last_mile_values = traverse_lastmile(last_mile)
                last_mile_edges = last_mile_values[1]

                #This function is called to project the data onto the maps
                plot(values_meso,last_mile_edges,first_mile_data[1])

                return render(request, "visualization/map.html")
        except Error as e:
            return render(request, "visualization/databaseerror.html")
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()

def createmap(request):
    try:
        # Setup the database connection
        connection = mysql.connector.connect(host="localhost", database="geospatial_okan", user="root",
                                             password="Kashyap@1995")
        if connection.is_connected():
            global cursor
            cursor = connection.cursor(buffered=True)
            cursor.execute("select database();")

            m = folium.Map(locations=[-112.48849364, 33.3596368342], zoom_start=12, tiles='OpenStreetMap',control_scale=True)
            # Used to insert Counties into the map
            data = [json.loads(line) for line in open('/Users/nischalkashyap/Downloads/Fall 2020/Research Assistant GIS/database/djangoapp/geospatial/visualization/templates/visualization/us_geoson.json','r')]
            folium.TopoJson(data[0], 'objects.us_counties_20m', name='topojson').add_to(m)

            query = "Select * from county;"
            cursor.execute(query)
            rows = cursor.fetchall()

            query = "Select * from commodity;"
            cursor.execute(query)
            commodities = cursor.fetchall()

            for i in rows:
                query = "Select * from mesoscale where origin_county = '"+str(i[0])+"' or dest_county='"+str(i[0])+"';"
                cursor.execute(query)
                data = cursor.fetchall()
                commodity_values = []
                for j in data:
                    commodity_values.append(j[5])

                query = "Select * from fm_lm_connections where origin_county_code = '" + str(i[0]) + "' or destination_county_code='" + str(i[0]) + "';"
                cursor.execute(query)
                data = cursor.fetchall()
                for j in data:
                    commodity_values.append(j[5])

                popup_source = '<strong>'+str(i[1])+'</strong>'
                popup_source+='<form action="visualization" method="post">'
                popup_source+='<select name="commodity" id="commodity" class="form-control input-lg">'
                for comm in commodities:
                    if comm[0] in commodity_values:
                        popup_source+='<option value="'+str(comm[0])+'">'+str(comm[0])+'</option>'
                popup_source+='</select><br/>'
                popup_source += '<select name="county" id="county" class="form-control input-lg"><option value="'+str(i[0])+'">'+str(i[1])+'</option></select><br/>'
                popup_source += '<select name="transfer" id="transfer" class="form-control input-lg"><option value="FM">FM</option><option value="FM-MESOSCALE">FM-MS</option><option value="MESOSCALE INFLOWS">MSINF</option><option value="MESOSCALE OUTFLOWS">MSOUT</option><option value="MESOSCALE-LM">MS-LM</option><option value="LM">LM</option></select><br /><input type="submit" class="btn btn-primary my-2" value="Visualize"></form>'
                tooltip = "Click for More Info"

                popup = folium.Popup(popup_source,max_width=10000000)
                folium.Marker([i[3], i[4]], popup=popup, tooltip=tooltip, icon=folium.Icon(icon='cloud', color='blue')).add_to(m)

            m.save('visualization/templates/visualization/map.html')
            return render(request, "visualization/map.html")
    except Error as e:
        return render(request, "visualization/databaseerror.html")
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

import mysql.connector
from mysql.connector import Error
from csv import reader
import json

try:
    connection = mysql.connector.connect(host="localhost", database="geospatial_okan", user="root", password="Kashyap@1995")
    if connection.is_connected():
        db_Info = connection.get_server_info()
        cursor = connection.cursor(buffered=True)
        cursor.execute("select database();")
        record = cursor.fetchone()

        new_array = []
        new_array.append({'id': 'MESOSCALE OUTFLOWS', 'parent_id': 'select transfer'})
        new_array.append({'id': 'MESOSCALE INFLOWS', 'parent_id': 'select transfer'})
        new_array.append({'id': 'FM', 'parent_id': 'select transfer'})
        new_array.append({'id': 'LM', 'parent_id': 'select transfer'})


        query = "Select distinct(commodity_id) from mesoscale;"
        cursor.execute(query)
        rows = cursor.fetchall()

        commodity_numbers = []
        for i in rows:
            commodity_numbers.append(i[0])

        commodity_numbers_counties = {}
        for i in commodity_numbers:
            distinct_counties = []
            query = "select distinct(county_name),county_id from county full join mesoscale on county_id = mesoscale.dest_county where mesoscale.commodity_id='"+str(i)+"';"
            cursor.execute(query)
            rows = cursor.fetchall()
            for j in rows:
                if j[1] not in distinct_counties:
                    distinct_counties.append([j[1],j[0]])
            commodity_numbers_counties[i] = distinct_counties

        final_dict = {}
        for i in commodity_numbers_counties:
            state_county_mapping = {}
            for j in commodity_numbers_counties[i]:
                query = "Select state_listing_id from county where county_id='"+str(j[0])+"';"
                cursor.execute(query)
                row = cursor.fetchone()

                query = "Select state_name from state where state_listing_id='"+row[0]+"';"
                cursor.execute(query)
                row_state = cursor.fetchone()

                if row_state[0] in state_county_mapping:
                    state_county_mapping[row_state[0]].append([j[1]])
                else:
                    state_county_mapping[row_state[0]] = [j[1]]
            final_dict[i] = state_county_mapping

        for commodity in final_dict:
            if final_dict[commodity]!={}:
                temp_dict = {}
                temp_dict["id"] = commodity
                temp_dict["parent_id"] = 'MESOSCALE INFLOWS'
                new_array.append(temp_dict)
                for state in final_dict[commodity]:
                    temp_dict = {}
                    temp_dict["id"]=state
                    temp_dict["parent_id"] = commodity
                    temp_dict["sc_step"] = 'MESOSCALE INFLOWS'
                    new_array.append(temp_dict)
                    for county in final_dict[commodity][state]:
                        temp_dict = {}
                        temp_dict["id"] = county
                        temp_dict["parent_id"] = state
                        temp_dict["parent_commodity_id"] = commodity
                        temp_dict["sc_step"] = 'MESOSCALE INFLOWS'
                        new_array.append(temp_dict)

        query = "Select distinct(commodity_id) from mesoscale;"
        cursor.execute(query)
        rows = cursor.fetchall()

        commodity_numbers = []
        for i in rows:
            commodity_numbers.append(i[0])

        commodity_numbers_counties = {}
        for i in commodity_numbers:
            distinct_counties = []
            query = "select distinct(county_name),county_id from county full join mesoscale on county_id = mesoscale.origin_county where mesoscale.commodity_id='" + str(i) + "';"
            cursor.execute(query)
            rows = cursor.fetchall()
            for j in rows:
                if j[1] not in distinct_counties:
                    distinct_counties.append([j[1], j[0]])
            commodity_numbers_counties[i] = distinct_counties

        final_dict = {}
        for i in commodity_numbers_counties:
            state_county_mapping = {}
            for j in commodity_numbers_counties[i]:
                query = "Select state_listing_id from county where county_id='" + str(j[0]) + "';"
                cursor.execute(query)
                row = cursor.fetchone()

                query = "Select state_name from state where state_listing_id='" + row[0] + "';"
                cursor.execute(query)
                row_state = cursor.fetchone()

                if row_state[0] in state_county_mapping:
                    state_county_mapping[row_state[0]].append([j[1]])
                else:
                    state_county_mapping[row_state[0]] = [j[1]]
            final_dict[i] = state_county_mapping

        for commodity in final_dict:
            if final_dict[commodity] != {}:
                temp_dict = {}
                temp_dict["id"] = commodity
                temp_dict["parent_id"] = 'MESOSCALE OUTFLOWS'

                new_array.append(temp_dict)
                for state in final_dict[commodity]:
                    temp_dict = {}
                    temp_dict["id"] = state
                    temp_dict["parent_id"] = commodity
                    temp_dict["sc_step"] = 'MESOSCALE OUTFLOWS'
                    new_array.append(temp_dict)
                    for county in final_dict[commodity][state]:
                        temp_dict = {}
                        temp_dict["id"] = county
                        temp_dict["parent_id"] = state
                        temp_dict["parent_commodity_id"] = commodity
                        temp_dict["sc_step"] = 'MESOSCALE OUTFLOWS'
                        new_array.append(temp_dict)

        query = "Select distinct(commodity_id) from fm_lm_connections where Sc_step_fmlm='FM';"
        cursor.execute(query)
        rows = cursor.fetchall()

        commodity_numbers = []
        for i in rows:
            commodity_numbers.append(i[0])

        commodity_numbers_counties = {}
        for i in commodity_numbers:
            distinct_counties = []
            query = "select distinct(county_name),county_id from county full join fm_lm_connections on county_id = fm_lm_connections.destination_county_code where fm_lm_connections.commodity_id='" + str(i) + "' and Sc_step_fmlm='FM';"
            cursor.execute(query)
            rows = cursor.fetchall()
            for j in rows:
                if j[1] not in distinct_counties:
                    distinct_counties.append([j[1], j[0]])

            query = "select distinct(county_name),county_id from county full join fm_lm_connections on county_id = fm_lm_connections.origin_county_code where fm_lm_connections.commodity_id='" + str(i) + "' and Sc_step_fmlm='FM';"
            cursor.execute(query)
            rows = cursor.fetchall()

            for j in rows:
                if j[1] not in distinct_counties:
                    distinct_counties.append([j[1], j[0]])
            commodity_numbers_counties[i] = distinct_counties

        final_dict = {}
        for i in commodity_numbers_counties:
            state_county_mapping = {}
            for j in commodity_numbers_counties[i]:
                query = "Select state_listing_id from county where county_id='" + str(j[0]) + "';"
                cursor.execute(query)
                row = cursor.fetchone()

                query = "Select state_name from state where state_listing_id='" + row[0] + "';"
                cursor.execute(query)
                row_state = cursor.fetchone()

                if row_state[0] in state_county_mapping:
                    state_county_mapping[row_state[0]].append(j[1])
                else:
                    state_county_mapping[row_state[0]] = [j[1]]
            final_dict[i] = state_county_mapping

        for commodity in final_dict:
            if final_dict[commodity] != {}:
                temp_dict = {}
                temp_dict["id"] = commodity
                temp_dict["parent_id"] = 'FM'
                new_array.append(temp_dict)
                for state in final_dict[commodity]:
                    temp_dict = {}
                    temp_dict["id"] = state
                    temp_dict["parent_id"] = commodity
                    temp_dict["sc_step"] = 'FM'
                    new_array.append(temp_dict)
                    for county in final_dict[commodity][state]:
                        temp_dict = {}
                        temp_dict["id"] = county
                        temp_dict["parent_id"] = state
                        temp_dict["parent_commodity_id"] = commodity
                        temp_dict["sc_step"] = 'FM'
                        new_array.append(temp_dict)

        query = "Select distinct(commodity_id) from fm_lm_connections where Sc_step_fmlm='LM';"
        cursor.execute(query)
        rows = cursor.fetchall()

        commodity_numbers = []
        for i in rows:
            commodity_numbers.append(i[0])

        commodity_numbers_counties = {}
        for i in commodity_numbers:
            distinct_counties = []
            query = "select distinct(county_name),county_id from county full join fm_lm_connections on county_id = fm_lm_connections.destination_county_code where fm_lm_connections.commodity_id='" + str(i) + "' and Sc_step_fmlm='LM';"
            cursor.execute(query)
            rows = cursor.fetchall()
            for j in rows:
                if j[1] not in distinct_counties:
                    distinct_counties.append([j[1], j[0]])

            query = "select distinct(county_name),county_id from county full join fm_lm_connections on county_id = fm_lm_connections.origin_county_code where fm_lm_connections.commodity_id='" + str(i) + "' and Sc_step_fmlm='L';"
            cursor.execute(query)
            rows = cursor.fetchall()
            for j in rows:
                if j[1] not in distinct_counties:
                    distinct_counties.append([j[1], j[0]])
            commodity_numbers_counties[i] = distinct_counties

        final_dict = {}
        for i in commodity_numbers_counties:
            state_county_mapping = {}
            for j in commodity_numbers_counties[i]:
                query = "Select state_listing_id from county where county_id='" + str(j[0]) + "';"
                cursor.execute(query)
                row = cursor.fetchone()

                query = "Select state_name from state where state_listing_id='" + row[0] + "';"
                cursor.execute(query)
                row_state = cursor.fetchone()

                if row_state[0] in state_county_mapping:
                    state_county_mapping[row_state[0]].append(j[1])
                else:
                    state_county_mapping[row_state[0]] = [j[1]]

            final_dict[i] = state_county_mapping

        for commodity in final_dict:
            if final_dict[commodity] != {}:
                temp_dict = {}
                temp_dict["id"] = commodity
                temp_dict["parent_id"] = 'LM'
                new_array.append(temp_dict)
                for state in final_dict[commodity]:
                    temp_dict = {}
                    temp_dict["id"] = state
                    temp_dict["parent_id"] = commodity
                    temp_dict["sc_step"] = 'LM'
                    new_array.append(temp_dict)
                    for county in final_dict[commodity][state]:
                        temp_dict = {}
                        temp_dict["id"] = county
                        temp_dict["parent_id"] = state
                        temp_dict["parent_commodity_id"] = commodity
                        temp_dict["sc_step"] = 'LM'
                        new_array.append(temp_dict)

        json_object = json.dumps(new_array, indent=4)
        with open("data.json", "w") as outfile:
            outfile.write(json_object)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
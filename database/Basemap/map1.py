import folium

list1 = [[40.7127,-74.0059],[34.05,-118.25]]
list2 = [[49.895077,-97.138451],[33.359637,-112.488494]]
m = folium.Map(locations = [20,0],zoom_start=3.5,tiles = 'OpenStreetMap')
folium.PolyLine(list1).add_to(m)
folium.PolyLine(list2).add_to(m)
m.save('map.html')
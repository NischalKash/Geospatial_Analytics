from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from csv import reader

m = Basemap(projection='mill',llcrnrlat=25,llcrnrlon=-130,urcrnrlat=50,urcrnrlon=-60,resolution='l')
m.drawcoastlines()
m.drawcountries(linewidth=3)
m.drawstates(linewidth=1)
m.drawlsmask()
m.drawcounties()

nyclat = 40.7127
nyclong = -74.0059
xpt , ypt = m(nyclong,nyclat)
m.plot(xpt,ypt,'c.',markersize=10,label='New York')
plt.text(xpt,ypt,'New York',fontsize=10,ha='center',va='center',color='k')

lalat = 34.05
lalong = -118.25
xpt , ypt = m(lalong,lalat)
m.plot(xpt,ypt,'g.',markersize=10,label='Los Angeles')
plt.text(xpt,ypt,'Los Angeles',fontsize=10,ha='center',va='center',color='k')

m.drawgreatcircle(nyclong,nyclat,lalong,lalat,color='r',linewidth=3,label='Commodity Number = 121221')

state_mapping = []
with open('statelatlong.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    for row in csv_reader:
        state_mapping.append([row[1],row[2],row[0]])

state_mapping = state_mapping[1:]
for i in state_mapping:
    latitude = float(i[0])
    longitude = float(i[1])
    name = i[2]
    xpt, ypt = m(longitude, latitude)
    plt.text(xpt, ypt, name, fontsize=10, ha='center', va='center', color='k',fontstyle = 'italic',fontname='sans')

plt.legend(loc=4)
plt.title("US Map Visualization")
plt.show()
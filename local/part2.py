from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

pd_flights_not_cancelled = pd_flights[pd_flights['CANCELLED'] == 0]

def usa_map():
    map = Basemap(resolution='l',llcrnrlon=-180, urcrnrlon=-50,
              llcrnrlat=10, urcrnrlat=75, lat_0=0, lon_0=0,)
    map.drawcoastlines()  
    map.drawcountries(linewidth = 4)  
    map.drawstates()  
    map.drawcounties()
    map.fillcontinents(color = 'coral',alpha = .1) 
    map.drawmapboundary()
    return map

fig = plt.figure(figsize=(25,20))
map = usa_map()
plt.title('United States Map',fontsize=20)
plt.show()
plt.close()

## Airport Traffic
fig = plt.figure(figsize=(25,20))
map = usa_map()
log, lat = pd_airports['LONGITUDE'], pd_airports['LATITUDE']
log, lat = map(log, lat)
map.scatter(log, lat, s=15, c='red')
plt.title('United States Airport Location',fontsize=20)
plt.show()
plt.close()

USEFUL_FLIGHT_KEYS = ["MONTH","DAY","DAY_OF_WEEK","AIRLINE","ORIGIN_AIRPORT","DESTINATION_AIRPORT","DEPARTURE_TIME","DEPARTURE_DELAY","ARRIVAL_TIME","ARRIVAL_DELAY"]
pd_flights_short = pd_flights_not_cancelled[USEFUL_FLIGHT_KEYS]
USEFUL_AIRPORT_KEYS = ["IATA_CODE", "CITY", "STATE", "LATITUDE", "LONGITUDE"]
## Merge Origin Airport Information
pd_flights_short = pd_flights_short.merge(pd_airports[USEFUL_AIRPORT_KEYS], left_on="ORIGIN_AIRPORT", right_on="IATA_CODE").drop(columns="IATA_CODE")
pd_flights_short.rename(
    columns={
        "CITY": "ORI_CITY",
        "STATE": "ORI_STATE",
        "LATITUDE": "ORI_LATITUDE",
        "LONGITUDE": "ORI_LONGITUDE",
    },
    inplace=True)
## Merge Destination Airport Information
pd_flights_short = pd_flights_short.merge(pd_airports[USEFUL_AIRPORT_KEYS], left_on="DESTINATION_AIRPORT", right_on="IATA_CODE").drop(columns="IATA_CODE")
pd_flights_short.rename(
    columns={
        "CITY": "DES_CITY",
        "STATE": "DES_STATE",
        "LATITUDE": "DES_LATITUDE",
        "LONGITUDE": "DES_LONGITUDE",
    },
    inplace=True)


## Airport Traffic
pd_flights_short["COUNT_ORI_AIRPORT"] = pd_flights_short['AIRLINE'].groupby(pd_flights_short["ORIGIN_AIRPORT"]).transform('count')
pd_flights_short_ori_airport = pd_flights_short[["ORIGIN_AIRPORT", "ORI_STATE", "ORI_LATITUDE", "ORI_LONGITUDE", "COUNT_ORI_AIRPORT"]]
pd_flights_short_ori_airport.drop_duplicates(inplace=True) 

fig = plt.figure(figsize=(25,20))
map = usa_map()
log, lat = pd_flights_short_ori_airport['ORI_LONGITUDE'], pd_flights_short_ori_airport['ORI_LATITUDE']
log, lat = map(log, lat)
count_ori = pd_flights_short_ori_airport['COUNT_ORI_AIRPORT']
names = pd_flights_short_ori_airport['ORIGIN_AIRPORT']
for x,y,c,name in zip(log, lat, count_ori, names):
    map.scatter(x, y, s=c/300, c='green')
    if c>80000:
        plt.annotate(name, xy=(x, y),  xycoords='data', xytext=(x+0.8, y+0.8), textcoords='data', c='red', fontsize=10, fontweight="bold" )
plt.title('United States Airport Traffic Density',fontsize=20)
plt.show()
plt.close()


## State Traffic
pd_flights_short["COUNT_ORI_STATE"] = pd_flights_short['AIRLINE'].groupby(pd_flights_short["ORI_STATE"]).transform('count')
pd_flights_short_ori_state = pd_flights_short[["ORI_STATE", "COUNT_ORI_STATE"]]
pd_flights_short_ori_state.drop_duplicates(inplace=True) 



code_to_state = {'AK': 'Alaska','AL': 'Alabama','AR': 'Arkansas','AS': 'American Samoa','AZ': 'Arizona','CA': 'California','CO': 'Colorado','CT': 'Connecticut',
        'DC': 'District of Columbia','DE': 'Delaware','FL': 'Florida','GA': 'Georgia','GU': 'Guam','HI': 'Hawaii','IA': 'Iowa','ID': 'Idaho',
        'IL': 'Illinois','IN': 'Indiana','KS': 'Kansas','KY': 'Kentucky','LA': 'Louisiana','MA': 'Massachusetts','MD': 'Maryland','ME': 'Maine',
        'MI': 'Michigan','MN': 'Minnesota','MO': 'Missouri','MP': 'Northern Mariana Islands','MS': 'Mississippi','MT': 'Montana','NA': 'National',
        'NC': 'North Carolina','ND': 'North Dakota','NE': 'Nebraska','NH': 'New Hampshire','NJ': 'New Jersey','NM': 'New Mexico','NV': 'Nevada',
        'NY': 'New York','OH': 'Ohio','OK': 'Oklahoma','OR': 'Oregon','PA': 'Pennsylvania','PR': 'Puerto Rico','RI': 'Rhode Island',
        'SC': 'South Carolina','SD': 'South Dakota','TN': 'Tennessee','TX': 'Texas','UT': 'Utah','VA': 'Virginia','VI': 'Virgin Islands',
        'VT': 'Vermont','WA': 'Washington','WI': 'Wisconsin','WV': 'West Virginia','WY': 'Wyoming'}

from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

fig = plt.figure(figsize=(25,20))
map = usa_map()
map.readshapefile('st99_d00', name='states', drawbounds=True)

state_names = []
for shape_dict in map.states_info:
    state_names.append(shape_dict['NAME'])

## Color
colors = []
patches = []
cmap = plt.get_cmap('Blues')
vmax = pd_flights_short_ori_state["COUNT_ORI_STATE"].max()

ax = plt.gca()
for state_code, count in zip(pd_flights_short_ori_state["ORI_STATE"], pd_flights_short_ori_state["COUNT_ORI_STATE"]):
    if (state_code not in ["GU", "AS", "VI"]):
        color = cmap(count/float(vmax))
        colors.append(color)
        ## Hardcode since MI&MI has exceptions in indexing
        if state_code == "MI":
            idx = 106
        elif state_code == "WI":
            idx = state_names.index(code_to_state[state_code])+2
        else:
            idx = state_names.index(code_to_state[state_code])
        seg = map.states[idx]
        poly = Polygon(seg, facecolor=color,edgecolor=color)
        patches.append(poly)
        ax.add_patch(poly)

p = PatchCollection(patches, cmap=cmap)
p.set_array(np.array(colors))
p.set_clim([0, vmax])
plt.colorbar(p, shrink=0.53)


plt.title('United States State Traffic Density',fontsize=20)
plt.show()
plt.close()

## Flights Visualization
pd_flights_short["ROUTE"] = pd_flights_short["ORIGIN_AIRPORT"] + "-" + pd_flights_short["DESTINATION_AIRPORT"] 
pd_flights_short["COUNT_ROUTE"] = pd_flights_short['AIRLINE'].groupby(pd_flights_short["ROUTE"]).transform('count')
pd_flights_short_flights = pd_flights_short[["ORIGIN_AIRPORT", "ORI_LATITUDE", "ORI_LONGITUDE", "DESTINATION_AIRPORT", "DES_LATITUDE", "DES_LONGITUDE", "COUNT_ROUTE"]]
pd_flights_short_flights.drop_duplicates(inplace=True) 

from matplotlib.lines import Line2D
fig = plt.figure(figsize=(25,20))
map = usa_map()
## Airports
log, lat = pd_flights_short_ori_airport['ORI_LONGITUDE'], pd_flights_short_ori_airport['ORI_LATITUDE']
log, lat = map(log, lat)
count_ori = pd_flights_short_ori_airport['COUNT_ORI_AIRPORT']
for x,y,c in zip(log, lat, count_ori):
    map.scatter(x, y, s=c/300, c='green')
## Flights
log_ori, lat_ori = pd_flights_short_flights["ORI_LONGITUDE"], pd_flights_short_flights["ORI_LATITUDE"]
log_des, lat_des = pd_flights_short_flights["DES_LONGITUDE"], pd_flights_short_flights["DES_LATITUDE"]
count = pd_flights_short_flights["COUNT_ROUTE"]
colors = ["green", "blue", 'red']
def count_to_idx(c):
    if c<=5000:
        idx = 1
    elif c>5000 and c<=10000:
        idx = 2
    elif c>10000:
        idx = 3
    return idx

for x1, y1, x2, y2, c in zip(log_ori, lat_ori, log_des, lat_des, count):
    x1,y1 = map(x1,y1)
    x2,y2 = map(x2,y2)
    map.plot([x1,x2], [y1,y2], c=colors[count_to_idx(c)-1], linewidth=0.0001*c*count_to_idx(c))
## Legend and plot
lines = [Line2D([0], [0], color=colors[c], linewidth=(c+1), linestyle='-') for c in [0,1,2]]
labels = ["count<=5000", "5000<count<=10000", "10000<count"]
plt.legend(lines, labels,loc = 3,title='Number of flights')

plt.title('United States Flight Routes',fontsize=20)
plt.show()
plt.close()

## 10 Most Frequent Routine
pd_flights_short_flights_sort = pd_flights_short_flights.sort_values(by=["COUNT_ROUTE"],ascending=False)[:30]

# Remove duplicate routines
row_id = []
routes = {}
row_count = -1
for i,r in pd_flights_short_flights_sort.iterrows():
    if len(row_id)==10:
        break
    k1 = r["ORIGIN_AIRPORT"] + "-" + r["DESTINATION_AIRPORT"]
    k2 = r["DESTINATION_AIRPORT"] + "-" + r["ORIGIN_AIRPORT"]
    row_count += 1
    if k1 in routes or k2 in routes:
        continue
    else:
        row_id.append(i)
        routes[k1]=0
        routes[k2]=0
pd_flights_short_flights_top = pd_flights_short_flights_sort[pd_flights_short_flights_sort.index.isin(row_id)].sort_values(by=["COUNT_ROUTE"], ascending=False)



fig = plt.figure(figsize=(25,20))
map = usa_map()
## Airports
log, lat = pd_flights_short_ori_airport['ORI_LONGITUDE'], pd_flights_short_ori_airport['ORI_LATITUDE']
log, lat = map(log, lat)
count_ori = pd_flights_short_ori_airport['COUNT_ORI_AIRPORT']
for x,y,c in zip(log, lat, count_ori):
    map.scatter(x, y, s=c/300, c='green')
## Flights
log_ori, lat_ori = pd_flights_short_flights_top["ORI_LONGITUDE"], pd_flights_short_flights_top["ORI_LATITUDE"]
log_des, lat_des = pd_flights_short_flights_top["DES_LONGITUDE"], pd_flights_short_flights_top["DES_LATITUDE"]
count = pd_flights_short_flights_top["COUNT_ROUTE"]

for i, (x1, y1, x2, y2, c) in enumerate(zip(log_ori, lat_ori, log_des, lat_des, count)):
    x1,y1 = map(x1,y1)
    x2,y2 = map(x2,y2)
    if i==0:
        color = "red"
    else:
        color = "blue"
    map.plot([x1,x2], [y1,y2], c=color, linewidth=0.0004*c)

plt.title('United States - 10 Most Frequent Routes',fontsize=20)
plt.show()
plt.close()


## Flights Visualization by time. To simply, include all flights in that time region
# Late Night from 0:00 - 6:00
pd_flights_short_night = pd_flights_short[((pd_flights_short["DEPARTURE_TIME"]>=0)&(pd_flights_short["DEPARTURE_TIME"]<600))|((pd_flights_short["ARRIVAL_TIME"]>=0)&(pd_flights_short["ARRIVAL_TIME"]<600))]
# Morning from 6:00 - 12:00
pd_flights_short_morning = pd_flights_short[((pd_flights_short["DEPARTURE_TIME"]>=600)&(pd_flights_short["DEPARTURE_TIME"]<1200))|((pd_flights_short["ARRIVAL_TIME"]>=600)&(pd_flights_short["ARRIVAL_TIME"]<1200))]
# Afternoon from 12:00 - 18:00
pd_flights_short_afternoon = pd_flights_short[((pd_flights_short["DEPARTURE_TIME"]>=1200)&(pd_flights_short["DEPARTURE_TIME"]<1800))|((pd_flights_short["ARRIVAL_TIME"]>=1200)&(pd_flights_short["ARRIVAL_TIME"]<1800))]
# Evening from 18:00 - 24:00
pd_flights_short_evening = pd_flights_short[((pd_flights_short["DEPARTURE_TIME"]>=1800)&(pd_flights_short["DEPARTURE_TIME"]<2400))|((pd_flights_short["ARRIVAL_TIME"]>=1800)&(pd_flights_short["ARRIVAL_TIME"]<2400))]


pd_flights_short_night["ROUTE"] = pd_flights_short_night["ORIGIN_AIRPORT"] + "-" + pd_flights_short_night["DESTINATION_AIRPORT"] 
pd_flights_short_night["COUNT_ROUTE"] = pd_flights_short_night['AIRLINE'].groupby(pd_flights_short_night["ROUTE"]).transform('count')
pd_flights_short_night_flights = pd_flights_short_night[["ORIGIN_AIRPORT", "ORI_LATITUDE", "ORI_LONGITUDE", "DESTINATION_AIRPORT", "DES_LATITUDE", "DES_LONGITUDE", "COUNT_ROUTE"]]
pd_flights_short_night_flights.drop_duplicates(inplace=True) 


pd_flights_short_morning["ROUTE"] = pd_flights_short_morning["ORIGIN_AIRPORT"] + "-" + pd_flights_short_morning["DESTINATION_AIRPORT"] 
pd_flights_short_morning["COUNT_ROUTE"] = pd_flights_short_morning['AIRLINE'].groupby(pd_flights_short_morning["ROUTE"]).transform('count')
pd_flights_short_morning_flights = pd_flights_short_morning[["ORIGIN_AIRPORT", "ORI_LATITUDE", "ORI_LONGITUDE", "DESTINATION_AIRPORT", "DES_LATITUDE", "DES_LONGITUDE", "COUNT_ROUTE"]]
pd_flights_short_morning_flights.drop_duplicates(inplace=True) 


pd_flights_short_afternoon["ROUTE"] = pd_flights_short_afternoon["ORIGIN_AIRPORT"] + "-" + pd_flights_short_afternoon["DESTINATION_AIRPORT"] 
pd_flights_short_afternoon["COUNT_ROUTE"] = pd_flights_short_afternoon['AIRLINE'].groupby(pd_flights_short_afternoon["ROUTE"]).transform('count')
pd_flights_short_afternoon_flights = pd_flights_short_afternoon[["ORIGIN_AIRPORT", "ORI_LATITUDE", "ORI_LONGITUDE", "DESTINATION_AIRPORT", "DES_LATITUDE", "DES_LONGITUDE", "COUNT_ROUTE"]]
pd_flights_short_afternoon_flights.drop_duplicates(inplace=True) 


pd_flights_short_evening["ROUTE"] = pd_flights_short_evening["ORIGIN_AIRPORT"] + "-" + pd_flights_short_evening["DESTINATION_AIRPORT"] 
pd_flights_short_evening["COUNT_ROUTE"] = pd_flights_short_evening['AIRLINE'].groupby(pd_flights_short_evening["ROUTE"]).transform('count')
pd_flights_short_evening_flights = pd_flights_short_evening[["ORIGIN_AIRPORT", "ORI_LATITUDE", "ORI_LONGITUDE", "DESTINATION_AIRPORT", "DES_LATITUDE", "DES_LONGITUDE", "COUNT_ROUTE"]]
pd_flights_short_evening_flights.drop_duplicates(inplace=True) 


from matplotlib.lines import Line2D
fig = plt.figure(figsize=(25,20))
map = usa_map()
## Airports
log, lat = pd_flights_short_ori_airport['ORI_LONGITUDE'], pd_flights_short_ori_airport['ORI_LATITUDE']
log, lat = map(log, lat)
count_ori = pd_flights_short_ori_airport['COUNT_ORI_AIRPORT']
for x,y,c in zip(log, lat, count_ori):
    map.scatter(x, y, s=c/300, c='green')
## Flights
log_ori, lat_ori = pd_flights_short_night_flights["ORI_LONGITUDE"], pd_flights_short_night_flights["ORI_LATITUDE"]
log_des, lat_des = pd_flights_short_night_flights["DES_LONGITUDE"], pd_flights_short_night_flights["DES_LATITUDE"]
count = pd_flights_short_night_flights["COUNT_ROUTE"]
colors = ["green", "blue", 'red']
def count_to_idx(c):
    if c<=2000:
        idx = 1
    elif c>2000 and c<=4000:
        idx = 2
    elif c>4000:
        idx = 3
    return idx

for x1, y1, x2, y2, c in zip(log_ori, lat_ori, log_des, lat_des, count):
    x1,y1 = map(x1,y1)
    x2,y2 = map(x2,y2)
    map.plot([x1,x2], [y1,y2], c=colors[count_to_idx(c)-1], linewidth=0.0001*c*count_to_idx(c))
## Legend and plot
lines = [Line2D([0], [0], color=colors[c], linewidth=(c+1), linestyle='-') for c in [0,1,2]]
labels = ["count<=2000", "2000<count<=4000", "4000<count"]
plt.legend(lines, labels,loc = 3,title='Number of flights')

plt.title('United States Flight Traffic in Late Night(0:00-6:00)',fontsize=20)
plt.show()
plt.close()


from matplotlib.lines import Line2D
fig = plt.figure(figsize=(25,20))
map = usa_map()
## Airports
log, lat = pd_flights_short_ori_airport['ORI_LONGITUDE'], pd_flights_short_ori_airport['ORI_LATITUDE']
log, lat = map(log, lat)
count_ori = pd_flights_short_ori_airport['COUNT_ORI_AIRPORT']
for x,y,c in zip(log, lat, count_ori):
    map.scatter(x, y, s=c/300, c='green')
## Flights
log_ori, lat_ori = pd_flights_short_morning_flights["ORI_LONGITUDE"], pd_flights_short_morning_flights["ORI_LATITUDE"]
log_des, lat_des = pd_flights_short_morning_flights["DES_LONGITUDE"], pd_flights_short_morning_flights["DES_LATITUDE"]
count = pd_flights_short_morning_flights["COUNT_ROUTE"]
colors = ["green", "blue", 'red']
def count_to_idx(c):
    if c<=2000:
        idx = 1
    elif c>2000 and c<=4000:
        idx = 2
    elif c>4000:
        idx = 3
    return idx

for x1, y1, x2, y2, c in zip(log_ori, lat_ori, log_des, lat_des, count):
    x1,y1 = map(x1,y1)
    x2,y2 = map(x2,y2)
    map.plot([x1,x2], [y1,y2], c=colors[count_to_idx(c)-1], linewidth=0.0001*c*count_to_idx(c))
## Legend and plot
lines = [Line2D([0], [0], color=colors[c], linewidth=(c+1), linestyle='-') for c in [0,1,2]]
labels = ["count<=2000", "2000<count<=4000", "4000<count"]
plt.legend(lines, labels,loc = 3,title='Number of flights')

plt.title('United States Flight Traffic in Morning (6:00-12:00)',fontsize=20)
plt.show()
plt.close()


from matplotlib.lines import Line2D
fig = plt.figure(figsize=(25,20))
map = usa_map()
## Airports
log, lat = pd_flights_short_ori_airport['ORI_LONGITUDE'], pd_flights_short_ori_airport['ORI_LATITUDE']
log, lat = map(log, lat)
count_ori = pd_flights_short_ori_airport['COUNT_ORI_AIRPORT']
for x,y,c in zip(log, lat, count_ori):
    map.scatter(x, y, s=c/300, c='green')
## Flights
log_ori, lat_ori = pd_flights_short_afternoon_flights["ORI_LONGITUDE"], pd_flights_short_afternoon_flights["ORI_LATITUDE"]
log_des, lat_des = pd_flights_short_afternoon_flights["DES_LONGITUDE"], pd_flights_short_afternoon_flights["DES_LATITUDE"]
count = pd_flights_short_afternoon_flights["COUNT_ROUTE"]
colors = ["green", "blue", 'red']
def count_to_idx(c):
    if c<=2000:
        idx = 1
    elif c>2000 and c<=4000:
        idx = 2
    elif c>4000:
        idx = 3
    return idx

for x1, y1, x2, y2, c in zip(log_ori, lat_ori, log_des, lat_des, count):
    x1,y1 = map(x1,y1)
    x2,y2 = map(x2,y2)
    map.plot([x1,x2], [y1,y2], c=colors[count_to_idx(c)-1], linewidth=0.0001*c*count_to_idx(c))
## Legend and plot
lines = [Line2D([0], [0], color=colors[c], linewidth=(c+1), linestyle='-') for c in [0,1,2]]
labels = ["count<=2000", "2000<count<=4000", "4000<count"]
plt.legend(lines, labels,loc = 3,title='Number of flights')

plt.title('United States Flight Traffic in Afternoon (12:00-18:00)',fontsize=20)
plt.show()
plt.close()


from matplotlib.lines import Line2D
fig = plt.figure(figsize=(25,20))
map = usa_map()
## Airports
log, lat = pd_flights_short_ori_airport['ORI_LONGITUDE'], pd_flights_short_ori_airport['ORI_LATITUDE']
log, lat = map(log, lat)
count_ori = pd_flights_short_ori_airport['COUNT_ORI_AIRPORT']
for x,y,c in zip(log, lat, count_ori):
    map.scatter(x, y, s=c/300, c='green')
## Flights
log_ori, lat_ori = pd_flights_short_evening_flights["ORI_LONGITUDE"], pd_flights_short_evening_flights["ORI_LATITUDE"]
log_des, lat_des = pd_flights_short_evening_flights["DES_LONGITUDE"], pd_flights_short_evening_flights["DES_LATITUDE"]
count = pd_flights_short_evening_flights["COUNT_ROUTE"]
colors = ["green", "blue", 'red']
def count_to_idx(c):
    if c<=2000:
        idx = 1
    elif c>2000 and c<=4000:
        idx = 2
    elif c>4000:
        idx = 3
    return idx

for x1, y1, x2, y2, c in zip(log_ori, lat_ori, log_des, lat_des, count):
    x1,y1 = map(x1,y1)
    x2,y2 = map(x2,y2)
    map.plot([x1,x2], [y1,y2], c=colors[count_to_idx(c)-1], linewidth=0.0001*c*count_to_idx(c))
## Legend and plot
lines = [Line2D([0], [0], color=colors[c], linewidth=(c+1), linestyle='-') for c in [0,1,2]]
labels = ["count<=2000", "2000<count<=4000", "4000<count"]
plt.legend(lines, labels,loc = 3,title='Number of flights')

plt.title('United States Flight Traffic in Evening (18:00-24:00)',fontsize=20)
plt.show()
plt.close()

for begin in range(24):
    print("Time {}:00-{}:00".format(begin, begin+1))
    pd_flights_short_time = pd_flights_short[((pd_flights_short["DEPARTURE_TIME"]>=begin*100)&(pd_flights_short["DEPARTURE_TIME"]<(begin+1)*100))|((pd_flights_short["ARRIVAL_TIME"]>=begin*100)&(pd_flights_short["ARRIVAL_TIME"]<(begin+1)*100))]
    pd_flights_short_time["ROUTE"] = pd_flights_short_time["ORIGIN_AIRPORT"] + "-" + pd_flights_short_time["DESTINATION_AIRPORT"] 
    pd_flights_short_time["COUNT_ROUTE"] = pd_flights_short_time['AIRLINE'].groupby(pd_flights_short_time["ROUTE"]).transform('count')
    pd_flights_short_time_flights = pd_flights_short_time[["ORIGIN_AIRPORT", "ORI_LATITUDE", "ORI_LONGITUDE", "DESTINATION_AIRPORT", "DES_LATITUDE", "DES_LONGITUDE", "COUNT_ROUTE"]]
    pd_flights_short_time_flights.drop_duplicates(inplace=True) 

    from matplotlib.lines import Line2D
    fig = plt.figure(figsize=(25,20))
    map = usa_map()
    ## Airports
    log, lat = pd_flights_short_ori_airport['ORI_LONGITUDE'], pd_flights_short_ori_airport['ORI_LATITUDE']
    log, lat = map(log, lat)
    count_ori = pd_flights_short_ori_airport['COUNT_ORI_AIRPORT']
    for x,y,c in zip(log, lat, count_ori):
        map.scatter(x, y, s=c/300, c='green')
    ## Flights
    log_ori, lat_ori = pd_flights_short_time_flights["ORI_LONGITUDE"], pd_flights_short_time_flights["ORI_LATITUDE"]
    log_des, lat_des = pd_flights_short_time_flights["DES_LONGITUDE"], pd_flights_short_time_flights["DES_LATITUDE"]
    count = pd_flights_short_time_flights["COUNT_ROUTE"]
    colors = ["green", "blue", 'red']
    def count_to_idx(c):
        if c<=1000:
            idx = 1
        elif c>1000 and c<=1500:
            idx = 2
        elif c>1500:
            idx = 3
        return idx

    for x1, y1, x2, y2, c in zip(log_ori, lat_ori, log_des, lat_des, count):
        x1,y1 = map(x1,y1)
        x2,y2 = map(x2,y2)
        map.plot([x1,x2], [y1,y2], c=colors[count_to_idx(c)-1], linewidth=0.0005*c*count_to_idx(c))
    ## Legend and plot
    lines = [Line2D([0], [0], color=colors[c], linewidth=(c+1), linestyle='-') for c in [0,1,2]]
    labels = ["count<=1000", "1000<count<=1500", "1500<count"]
    plt.legend(lines, labels,loc = 3,title='Number of flights')

    plt.title('United States Flight Traffic in {:02d}:00-{:02d}:00)'.format(begin, begin+1),fontsize=20)
    plt.savefig("time-{:02d}.png".format(begin))
    plt.close()
    del pd_flights_short_time_flights


Airline_Select = "B6"
pd_flights_short_airline = pd_flights_short[pd_flights_short["AIRLINE"]==Airline_Select]
pd_flights_short_airline["ROUTE"] = pd_flights_short_airline["ORIGIN_AIRPORT"] + "-" + pd_flights_short_airline["DESTINATION_AIRPORT"] 
pd_flights_short_airline["COUNT_ROUTE"] = pd_flights_short_airline['AIRLINE'].groupby(pd_flights_short_airline["ROUTE"]).transform('count')
pd_flights_short_airline_flights = pd_flights_short_airline[["ORIGIN_AIRPORT", "ORI_LATITUDE", "ORI_LONGITUDE", "DESTINATION_AIRPORT", "DES_LATITUDE", "DES_LONGITUDE", "COUNT_ROUTE"]]
pd_flights_short_airline_flights.drop_duplicates(inplace=True) 

from matplotlib.lines import Line2D
fig = plt.figure(figsize=(25,20))
map = usa_map()
## Airports
log, lat = pd_flights_short_ori_airport['ORI_LONGITUDE'], pd_flights_short_ori_airport['ORI_LATITUDE']
log, lat = map(log, lat)
count_ori = pd_flights_short_ori_airport['COUNT_ORI_AIRPORT']
for x,y,c in zip(log, lat, count_ori):
    map.scatter(x, y, s=c/300, c='green')
## Flights
log_ori, lat_ori = pd_flights_short_airline_flights["ORI_LONGITUDE"], pd_flights_short_airline_flights["ORI_LATITUDE"]
log_des, lat_des = pd_flights_short_airline_flights["DES_LONGITUDE"], pd_flights_short_airline_flights["DES_LATITUDE"]
count = pd_flights_short_airline_flights["COUNT_ROUTE"]
colors = ["green", "blue", 'red']
def count_to_idx(c):
    if c<=1000:
        idx = 1
    elif c>1000 and c<=1500:
        idx = 2
    elif c>1500:
        idx = 3
    return idx

for x1, y1, x2, y2, c in zip(log_ori, lat_ori, log_des, lat_des, count):
    x1,y1 = map(x1,y1)
    x2,y2 = map(x2,y2)
    map.plot([x1,x2], [y1,y2], c="blue", linewidth=0.0002*c) 

plt.title(pd_airlines[pd_airlines["IATA_CODE"]==Airline_Select]["AIRLINE"].item(),fontsize=20)
plt.show()
plt.close()



Sample_Cities = ["SFO", "SEA", "JFK", "ATL", "DFW"]
Airport_Select = Sample_Cities[4]
pd_flights_short_airport = pd_flights_short[pd_flights_short["ORIGIN_AIRPORT"]==Airport_Select]
pd_flights_short_airport["ROUTE"] = pd_flights_short_airport["ORIGIN_AIRPORT"] + "-" + pd_flights_short_airport["DESTINATION_AIRPORT"] 
pd_flights_short_airport["COUNT_ROUTE"] = pd_flights_short_airport['AIRLINE'].groupby(pd_flights_short_airport["ROUTE"]).transform('count')
pd_flights_short_airport_flights = pd_flights_short_airport[["ORIGIN_AIRPORT", "ORI_LATITUDE", "ORI_LONGITUDE", "DESTINATION_AIRPORT", "DES_LATITUDE", "DES_LONGITUDE", "COUNT_ROUTE"]]
pd_flights_short_airport_flights.drop_duplicates(inplace=True) 

from matplotlib.lines import Line2D
fig = plt.figure(figsize=(25,20))
map = usa_map()
## Airports
log, lat = pd_flights_short_ori_airport['ORI_LONGITUDE'], pd_flights_short_ori_airport['ORI_LATITUDE']
log, lat = map(log, lat)
count_ori = pd_flights_short_ori_airport['COUNT_ORI_AIRPORT']
for x,y,c in zip(log, lat, count_ori):
    map.scatter(x, y, s=c/300, c='green')
## Flights
log_ori, lat_ori = pd_flights_short_airport_flights["ORI_LONGITUDE"], pd_flights_short_airport_flights["ORI_LATITUDE"]
log_des, lat_des = pd_flights_short_airport_flights["DES_LONGITUDE"], pd_flights_short_airport_flights["DES_LATITUDE"]
count = pd_flights_short_airport_flights["COUNT_ROUTE"]
colors = ["green", "blue", 'red']
def count_to_idx(c):
    if c<=1000:
        idx = 1
    elif c>1000 and c<=1500:
        idx = 2
    elif c>1500:
        idx = 3
    return idx

for x1, y1, x2, y2, c in zip(log_ori, lat_ori, log_des, lat_des, count):
    x1,y1 = map(x1,y1)
    x2,y2 = map(x2,y2)
    map.plot([x1,x2], [y1,y2], c="blue", linewidth=0.0002*c) 

plt.title("{} Destinations".format(Airport_Select),fontsize=20)
plt.show()
plt.close()



Sample_Cities = ["SFO", "SEA", "JFK", "ATL", "DFW"]
Airport_Select = Sample_Cities[4]
pd_flights_short_airport = pd_flights_short[pd_flights_short["ORIGIN_AIRPORT"]==Airport_Select]
pd_flights_short_airport["ROUTE"] = pd_flights_short_airport["ORIGIN_AIRPORT"] + "-" + pd_flights_short_airport["DESTINATION_AIRPORT"] 
pd_flights_short_airport["COUNT_ROUTE"] = pd_flights_short_airport['AIRLINE'].groupby(pd_flights_short_airport["ROUTE"]).transform('count')
pd_flights_short_airport_flights = pd_flights_short_airport[["ORIGIN_AIRPORT", "ORI_LATITUDE", "ORI_LONGITUDE", "DESTINATION_AIRPORT", "DES_LATITUDE", "DES_LONGITUDE", "COUNT_ROUTE"]]
pd_flights_short_airport_flights.drop_duplicates(inplace=True) 

from matplotlib.lines import Line2D
fig = plt.figure(figsize=(25,20))
map = usa_map()
## Airports
log, lat = pd_flights_short_ori_airport['ORI_LONGITUDE'], pd_flights_short_ori_airport['ORI_LATITUDE']
log, lat = map(log, lat)
count_ori = pd_flights_short_ori_airport['COUNT_ORI_AIRPORT']
for x,y,c in zip(log, lat, count_ori):
    map.scatter(x, y, s=c/300, c='green')
## Flights
log_ori, lat_ori = pd_flights_short_airport_flights["ORI_LONGITUDE"], pd_flights_short_airport_flights["ORI_LATITUDE"]
log_des, lat_des = pd_flights_short_airport_flights["DES_LONGITUDE"], pd_flights_short_airport_flights["DES_LATITUDE"]
count = pd_flights_short_airport_flights["COUNT_ROUTE"]
colors = ["green", "blue", 'red']
def count_to_idx(c):
    if c<=1000:
        idx = 1
    elif c>1000 and c<=1500:
        idx = 2
    elif c>1500:
        idx = 3
    return idx

for x1, y1, x2, y2, c in zip(log_ori, lat_ori, log_des, lat_des, count):
    x1,y1 = map(x1,y1)
    x2,y2 = map(x2,y2)
    map.plot([x1,x2], [y1,y2], c="blue", linewidth=0.0002*c) 

plt.title("{} Destinations".format(Airport_Select),fontsize=20)
plt.show()
plt.close()

Sample_Cities = ["SFO", "SEA", "JFK", "ATL", "DFW"]
Airport_Select = Sample_Cities[4]
pd_flights_short_airport = pd_flights_short[pd_flights_short["ORIGIN_AIRPORT"]==Airport_Select]
pd_flights_short_airport["ROUTE"] = pd_flights_short_airport["ORIGIN_AIRPORT"] + "-" + pd_flights_short_airport["DESTINATION_AIRPORT"] 
pd_flights_short_airport["COUNT_ROUTE"] = pd_flights_short_airport['AIRLINE'].groupby(pd_flights_short_airport["ROUTE"]).transform('count')
pd_flights_short_airport_flights = pd_flights_short_airport[["ORIGIN_AIRPORT", "ORI_LATITUDE", "ORI_LONGITUDE", "DESTINATION_AIRPORT", "DES_LATITUDE", "DES_LONGITUDE", "COUNT_ROUTE"]]
pd_flights_short_airport_flights.drop_duplicates(inplace=True) 

from matplotlib.lines import Line2D
fig = plt.figure(figsize=(25,20))
map = usa_map()
## Airports
log, lat = pd_flights_short_ori_airport['ORI_LONGITUDE'], pd_flights_short_ori_airport['ORI_LATITUDE']
log, lat = map(log, lat)
count_ori = pd_flights_short_ori_airport['COUNT_ORI_AIRPORT']
for x,y,c in zip(log, lat, count_ori):
    map.scatter(x, y, s=c/300, c='green')
## Flights
log_ori, lat_ori = pd_flights_short_airport_flights["ORI_LONGITUDE"], pd_flights_short_airport_flights["ORI_LATITUDE"]
log_des, lat_des = pd_flights_short_airport_flights["DES_LONGITUDE"], pd_flights_short_airport_flights["DES_LATITUDE"]
count = pd_flights_short_airport_flights["COUNT_ROUTE"]
colors = ["green", "blue", 'red']
def count_to_idx(c):
    if c<=1000:
        idx = 1
    elif c>1000 and c<=1500:
        idx = 2
    elif c>1500:
        idx = 3
    return idx

for x1, y1, x2, y2, c in zip(log_ori, lat_ori, log_des, lat_des, count):
    x1,y1 = map(x1,y1)
    x2,y2 = map(x2,y2)
    map.plot([x1,x2], [y1,y2], c="blue", linewidth=0.0002*c) 

plt.title("{} Destinations".format(Airport_Select),fontsize=20)
plt.show()
plt.close()




import sklearn.cluster

pd_airports_notna = pd_airports.dropna()
n_clusters = 10
cluster = sklearn.cluster.KMeans(n_clusters=n_clusters, init='k-means++', n_init=10, max_iter=3000, tol=0.0001, precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1)
cluster.fit(pd_airports_notna[["LONGITUDE","LATITUDE"]])

cluster.cluster_centers_


from matplotlib.lines import Line2D

fig = plt.figure(figsize=(25,20))
map = usa_map()
log, lat = pd_flights_short_ori_airport['ORI_LONGITUDE'], pd_flights_short_ori_airport['ORI_LATITUDE']
log, lat = map(log, lat)
count_ori = pd_flights_short_ori_airport['COUNT_ORI_AIRPORT']
for x,y,c in zip(log, lat, count_ori):
    map.scatter(x, y, s=c/1200, c='green')
cen_log, cen_lat = map(cluster.cluster_centers_[:,0],cluster.cluster_centers_[:,1])
for x,y in zip(cen_log, cen_lat):
    map.scatter(x, y, s=300, c='red')

lines = [Line2D([0], [0], marker='o', color='w', label='Scatter',
                          markerfacecolor='g', markersize=10),
         Line2D([0], [0], marker='o', color='w', label='Scatter',
                          markerfacecolor='r', markersize=20)]
labels = ["Airports", "Centroids"]
plt.legend(lines, labels,loc = 3)

plt.title('United States Airports Centroids by K-means',fontsize=20)
plt.show()
plt.close()

pd_airports_notna["CLUSTER_ID"] = cluster.labels_


USEFUL_FLIGHT_KEYS = ["ORIGIN_AIRPORT","DESTINATION_AIRPORT"]
pd_flights_short_cluster = pd_flights_not_cancelled[USEFUL_FLIGHT_KEYS]
USEFUL_AIRPORT_KEYS = ["IATA_CODE", "CITY", "STATE", "LATITUDE", "LONGITUDE", "CLUSTER_ID"]
## Merge Origin Airport Information
pd_flights_short_cluster = pd_flights_short_cluster.merge(pd_airports_notna[USEFUL_AIRPORT_KEYS], left_on="ORIGIN_AIRPORT", right_on="IATA_CODE").drop(columns=["IATA_CODE","CITY","STATE"])
pd_flights_short_cluster.rename(
    columns={
        "LATITUDE": "ORI_LATITUDE",
        "LONGITUDE": "ORI_LONGITUDE",
        "CLUSTER_ID": "ORI_CLUSTER_ID"
    },
    inplace=True)
## Merge Destination Airport Information
pd_flights_short_cluster = pd_flights_short_cluster.merge(pd_airports_notna[USEFUL_AIRPORT_KEYS], left_on="DESTINATION_AIRPORT", right_on="IATA_CODE").drop(columns=["IATA_CODE","CITY","STATE"])
pd_flights_short_cluster.rename(
    columns={
        "LATITUDE": "DES_LATITUDE",
        "LONGITUDE": "DES_LONGITUDE",
        "CLUSTER_ID": "DES_CLUSTER_ID"
    },
    inplace=True)


## Flights within Cluster
pd_flights_short_cluster["ROUTE"] = pd_flights_short_cluster["ORIGIN_AIRPORT"] + "-" + pd_flights_short_cluster["DESTINATION_AIRPORT"] 
pd_flights_short_cluster["COUNT_ROUTE"] = pd_flights_short_cluster['ORI_LATITUDE'].groupby(pd_flights_short_cluster["ROUTE"]).transform('count')
pd_flights_short_cluster_flights = pd_flights_short_cluster[["ORIGIN_AIRPORT", "ORI_LATITUDE", "ORI_LONGITUDE", "ORI_CLUSTER_ID", "DESTINATION_AIRPORT", "DES_LATITUDE", "DES_LONGITUDE", "DES_CLUSTER_ID", "COUNT_ROUTE"]]
pd_flights_short_cluster_flights.drop_duplicates(inplace=True) 



fig = plt.figure(figsize=(25,20))
map = usa_map()
## Airports
log, lat = pd_flights_short_ori_airport['ORI_LONGITUDE'], pd_flights_short_ori_airport['ORI_LATITUDE']
log, lat = map(log, lat)
count_ori = pd_flights_short_ori_airport['COUNT_ORI_AIRPORT']
for x,y,c in zip(log, lat, count_ori):
    map.scatter(x, y, s=c/1200, c='green')
cen_log, cen_lat = map(cluster.cluster_centers_[:,0],cluster.cluster_centers_[:,1])
for x,y in zip(cen_log, cen_lat):
    map.scatter(x, y, s=300, c='red')
## Flights Within Each Cluster
log_ori, lat_ori = pd_flights_short_cluster_flights["ORI_LONGITUDE"], pd_flights_short_cluster_flights["ORI_LATITUDE"]
log_des, lat_des = pd_flights_short_cluster_flights["DES_LONGITUDE"], pd_flights_short_cluster_flights["DES_LATITUDE"]
count = pd_flights_short_cluster_flights["COUNT_ROUTE"]
ori_id, des_id = pd_flights_short_cluster_flights["ORI_CLUSTER_ID"],pd_flights_short_cluster_flights["DES_CLUSTER_ID"]
colors = ["green", "blue", 'red', 'black', 'aqua', 'orange', 'yellow', 'teal', 'brown', 'purple']

for x1, y1, x2, y2, c, id1, id2 in zip(log_ori, lat_ori, log_des, lat_des, count, ori_id, des_id):
    if id1 == id2:
        x1,y1 = map(x1,y1)
        x2,y2 = map(x2,y2)
        map.plot([x1,x2], [y1,y2], c=colors[id1], linewidth=0.0004*c)

plt.title('US Airports Centroid -- Flights within Clusters',fontsize=20)
plt.show()
plt.close()

pd_flights_short_cluster["ROUTE2"] = pd_flights_short_cluster["ORI_CLUSTER_ID"].apply(str) + "-" + pd_flights_short_cluster["DES_CLUSTER_ID"].apply(str)
pd_flights_short_cluster["COUNT_ROUTE2"] = pd_flights_short_cluster['ORI_LATITUDE'].groupby(pd_flights_short_cluster["ROUTE2"]).transform('count')
pd_flights_short_cluster_flights2 = pd_flights_short_cluster[["ORI_CLUSTER_ID", "DES_CLUSTER_ID", "COUNT_ROUTE2"]]
pd_flights_short_cluster_flights2.drop_duplicates(inplace=True) 

pd_flights_short_cluster_flights2.sort_values(by = ["COUNT_ROUTE2"])

from matplotlib.lines import Line2D
fig = plt.figure(figsize=(25,20))
map = usa_map()
## Airports
log, lat = pd_flights_short_ori_airport['ORI_LONGITUDE'], pd_flights_short_ori_airport['ORI_LATITUDE']
log, lat = map(log, lat)
count_ori = pd_flights_short_ori_airport['COUNT_ORI_AIRPORT']
for x,y,c in zip(log, lat, count_ori):
    map.scatter(x, y, s=c/1200, c='green')
cen_log, cen_lat = map(cluster.cluster_centers_[:,0],cluster.cluster_centers_[:,1])
for x,y in zip(cen_log, cen_lat):
    map.scatter(x, y, s=300, c='red')
## Flights Between Each Cluster
count = pd_flights_short_cluster_flights2["COUNT_ROUTE2"]
ori_id, des_id = pd_flights_short_cluster_flights2["ORI_CLUSTER_ID"],pd_flights_short_cluster_flights2["DES_CLUSTER_ID"]
colors = ["green", "blue", 'red']
def count_to_idx(c):
    if c<=100000:
        idx = 1
    elif c>100000 and c<=300000:
        idx = 2
    elif c>300000:
        idx = 3
    return idx

for c, id1, id2 in zip(count, ori_id, des_id):
    if id1 != id2:
        x1,y1 = map(cluster.cluster_centers_[id1,0],cluster.cluster_centers_[id1,1])
        x2,y2 = map(cluster.cluster_centers_[id2,0],cluster.cluster_centers_[id2,1])
        map.plot([x1,x2], [y1,y2], c=colors[count_to_idx(c)-1], linewidth=0.000008*c*count_to_idx(c))

## Legend and plot
lines = [Line2D([0], [0], color=colors[c], linewidth=(c+1), linestyle='-') for c in [0,1,2]]
labels = ["count<=100000", "100000<count<=300000", "300000<count"]
plt.legend(lines, labels,loc = 3, title='Number of flights')

plt.title('US Airports Centroid -- Flights Between Clusters',fontsize=20)
plt.show()
plt.close()




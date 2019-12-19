import pandas as pd
import numpy as np
import warnings

FLIGHTS_DATA_PATH = "flights.csv"
pd_flights = pd.read_csv(FLIGHTS_DATA_PATH, low_memory=False)
pd_flights_not_cancelled = pd_flights[pd_flights['CANCELLED'] == 0]
warnings.filterwarnings('ignore')

def enable_plotly_in_cell(): ## Needs it to shown fig in notebooks
  import IPython
  from plotly.offline import init_notebook_mode
  display(IPython.core.display.HTML('''
        <script src="/static/components/requirejs/require.js"></script>
  '''))
  init_notebook_mode(connected=False)

  # Use features MONTH, DAY_OF_WEEK, AIRLINE, ORIGIN_AIRPORT and SCHEDULED_DEPARTURE
def time_period(time):
    if 0 <= time and time < 600:
        return 'night'
    elif 600 <= time and time < 1200:
        return 'morning'
    elif 1200 <= time and time < 1800:
        return 'afternoon'
    elif 1800 <= time and time < 2400:
        return 'evening'

def create_df_delay(df):
    df1 = df[['MONTH','DAY_OF_WEEK','AIRLINE','ORIGIN_AIRPORT','SCHEDULED_DEPARTURE', 'DEPARTURE_DELAY']]
    df1.dropna(how = 'any', inplace = True)
    #____________________
    # delete unknown airports data
    df1['ORIGIN_AIRPORT'] = df1['ORIGIN_AIRPORT'].apply(lambda x:x if x[0].isalpha() else np.nan)
    df1.dropna(how = 'any', inplace = True)
    #_________________
    # formating times
    df1['DEPARTURE_PERIOD'] = df1['SCHEDULED_DEPARTURE'].apply(time_period)
    return df1

df = create_df_delay(pd_flights_not_cancelled)
print(df.shape)



# Avg delay by origin airport(top 15)
delay_by_airport = df.groupby('ORIGIN_AIRPORT')[['DEPARTURE_DELAY']].mean()\
.sort_values(by='DEPARTURE_DELAY', ascending=False).round(2)
delay_by_airport = delay_by_airport[:15]

enable_plotly_in_cell()

trace = go.Scatter(
    x=delay_by_airport.index.tolist(),
    y=delay_by_airport.DEPARTURE_DELAY.tolist(),
    mode='markers',
    marker=dict(
        sizemode = 'diameter',
        sizeref = 1,
        size = 15,
        color = delay_by_airport.DEPARTURE_DELAY.tolist(),
        colorscale='viridis',
        showscale=True
    )
)

data = [trace]
layout = go.Layout(
    title='Average Delay by Departure Airport - Top 15', 
    yaxis = dict(title = 'Avg Delay'), 
    xaxis = dict(title = 'Departure Airport')
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)




# Avg delay by airline
delay_by_airline = df.groupby('AIRLINE')[['DEPARTURE_DELAY']].mean()\
.sort_values(by='DEPARTURE_DELAY', ascending=False).round(2)

enable_plotly_in_cell()

trace = go.Scatter(
    x=delay_by_airline.index.tolist(),
    y=delay_by_airline.DEPARTURE_DELAY.tolist(),
    mode='markers',
    marker=dict(
        sizemode = 'diameter',
        sizeref = 1,
        size = 15,
        color = delay_by_airline.DEPARTURE_DELAY.tolist(),
        colorscale='viridis',
        showscale=True
    )
)

data = [trace]
layout = go.Layout(
    title='Average Delay by Airline', 
    yaxis = dict(title = 'Avg Delay'), 
    xaxis = dict(title = 'Airline')
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)



# Avg delay by month
month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', \
         6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

delay_by_month = df.groupby('MONTH')[['DEPARTURE_DELAY']].mean()\
.sort_values(by='DEPARTURE_DELAY', ascending=False).round(2)
delay_by_month.index = delay_by_month.index.map(month)

enable_plotly_in_cell()

trace = go.Scatter(
    x=delay_by_month.index.tolist(),
    y=delay_by_month.DEPARTURE_DELAY.tolist(),
    mode='markers',
    marker=dict(
        sizemode = 'diameter',
        sizeref = 1,
        size = 15,
        color = delay_by_month.DEPARTURE_DELAY.tolist(),
        colorscale='viridis',
        showscale=True
    )
)

data = [trace]
layout = go.Layout(
    title='Average Delay by Month', 
    yaxis = dict(title = 'Avg Delay'), 
    xaxis = dict(title = 'Month')
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)



# Avg delay by weekday
dayOfWeek={1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday', 7:'Sunday'}

delay_by_weekday = df.groupby('DAY_OF_WEEK')[['DEPARTURE_DELAY']].mean()\
.sort_values(by='DEPARTURE_DELAY', ascending=False).round(2)
delay_by_weekday.index = delay_by_weekday.index.map(dayOfWeek)

enable_plotly_in_cell()

trace = go.Scatter(
    x=delay_by_weekday.index.tolist(),
    y=delay_by_weekday.DEPARTURE_DELAY.tolist(),
    mode='markers',
    marker=dict(
        sizemode = 'diameter',
        sizeref = 1,
        size = 15,
        color = delay_by_weekday.DEPARTURE_DELAY.tolist(),
        colorscale='viridis',
        showscale=True
    )
)

data = [trace]
layout = go.Layout(
    title='Average Delay by Day of Week', 
    yaxis = dict(title = 'Avg Delay'), 
    xaxis = dict(title = 'Day of Week')
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)



# Avg delay by scheduled departure time period
delay_by_period = df.groupby('DEPARTURE_PERIOD')[['DEPARTURE_DELAY']].mean()\
.sort_values(by='DEPARTURE_DELAY', ascending=False).round(2)

enable_plotly_in_cell()

trace = go.Scatter(
    x=delay_by_period.index.tolist(),
    y=delay_by_period.DEPARTURE_DELAY.tolist(),
    mode='markers',
    marker=dict(
        sizemode = 'diameter',
        sizeref = 1,
        size = 15,
        color = delay_by_period.DEPARTURE_DELAY.tolist(),
        colorscale='viridis',
        showscale=True
    )
)

data = [trace]
layout = go.Layout(
    title='Average Delay by Scheduled Departure Period', 
    yaxis = dict(title = 'Avg Delay'), 
    xaxis = dict(title = 'Scheduled Departure Period')
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

pd_flights_not_cancelled = pd_flights[pd_flights['CANCELLED'] == 0]
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


## Airport Delay
pd_flights_short["AVG_DELAY_ORI_AIRPORT"] = pd_flights_short['DEPARTURE_DELAY'].groupby(pd_flights_short["ORIGIN_AIRPORT"]).transform('mean')
pd_flights_short_avg_delay_ori_airport = pd_flights_short[["ORIGIN_AIRPORT", "ORI_STATE", "ORI_LATITUDE", "ORI_LONGITUDE", "AVG_DELAY_ORI_AIRPORT"]]
pd_flights_short_avg_delay_ori_airport.drop_duplicates(inplace=True) 


import math
fig = plt.figure(figsize=(25,20))
map = usa_map()
log, lat = pd_flights_short_avg_delay_ori_airport['ORI_LONGITUDE'], pd_flights_short_avg_delay_ori_airport['ORI_LATITUDE']
log, lat = map(log, lat)
avg_delay = pd_flights_short_avg_delay_ori_airport['AVG_DELAY_ORI_AIRPORT']
names = pd_flights_short_avg_delay_ori_airport['ORIGIN_AIRPORT']
for x,y,c,name in zip(log, lat, avg_delay, names):
    map.scatter(x, y, s=0 if c<=0 else 1.3**c, c='green')
    if c>20:
        plt.annotate(name+"({:.1f})min".format(c), xy=(x, y),  xycoords='data', xytext=(x+0.8, y+0.8), textcoords='data', c='red', fontsize=10, fontweight="bold" )
plt.title('United States Airport Delay Situation',fontsize=20)
plt.show()
plt.close()

## State Delay
pd_flights_short["AVG_DELAY_STATE"] = pd_flights_short['DEPARTURE_DELAY'].groupby(pd_flights_short["ORI_STATE"]).transform('mean')
pd_flights_short_avg_delay_state = pd_flights_short[["ORI_STATE", "AVG_DELAY_STATE"]]
pd_flights_short_avg_delay_state.drop_duplicates(inplace=True) 


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
vmax = pd_flights_short_avg_delay_state["AVG_DELAY_STATE"].max()

ax = plt.gca()
for state_code, delay in zip(pd_flights_short_avg_delay_state["ORI_STATE"], pd_flights_short_avg_delay_state["AVG_DELAY_STATE"]):
    if (state_code not in ["GU", "AS", "VI"]):
        if delay<0: delay = 0
        color = cmap(delay/float(vmax))
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


plt.title('United States State Delay Situation(in min)',fontsize=20)
plt.show()
plt.close()

## Flights Delay Visualization
pd_flights_short["ROUTE"] = pd_flights_short["ORIGIN_AIRPORT"] + "-" + pd_flights_short["DESTINATION_AIRPORT"] 
pd_flights_short["AVG_DELAY_ROUTE"] = pd_flights_short['DEPARTURE_DELAY'].groupby(pd_flights_short["ROUTE"]).transform('mean')
pd_flights_short_delay_flights = pd_flights_short[["ORIGIN_AIRPORT", "ORI_LATITUDE", "ORI_LONGITUDE", "DESTINATION_AIRPORT", "DES_LATITUDE", "DES_LONGITUDE", "AVG_DELAY_ROUTE"]]
pd_flights_short_delay_flights.drop_duplicates(inplace=True) 

from matplotlib.lines import Line2D
fig = plt.figure(figsize=(25,20))
map = usa_map()
## Airports
log, lat = pd_flights_short_delay_flights['ORI_LONGITUDE'], pd_flights_short_delay_flights['ORI_LATITUDE']
log, lat = map(log, lat)
for x,y in zip(log, lat):
    map.scatter(x, y, s=10, c='green')
## Flights
log_ori, lat_ori = pd_flights_short_delay_flights["ORI_LONGITUDE"], pd_flights_short_delay_flights["ORI_LATITUDE"]
log_des, lat_des = pd_flights_short_delay_flights["DES_LONGITUDE"], pd_flights_short_delay_flights["DES_LATITUDE"]
delay = pd_flights_short_delay_flights["AVG_DELAY_ROUTE"]
colors = ["green", "blue", 'red']
def delay_to_idx(c):
    if c<=30:
        idx = 1
    elif c>30 and c<=60:
        idx = 2
    elif c>60:
        idx = 3
    return idx

for x1, y1, x2, y2, c in zip(log_ori, lat_ori, log_des, lat_des, delay):
    x1,y1 = map(x1,y1)
    x2,y2 = map(x2,y2)
    map.plot([x1,x2], [y1,y2], c=colors[delay_to_idx(c)-1], linewidth=0.01*c*delay_to_idx(c))
## Legend and plot
lines = [Line2D([0], [0], color=colors[c], linewidth=(c+1), linestyle='-') for c in [0,1,2]]
labels = ["delay<=30min", "30min<delay<=60min", "60min<delay"]
plt.legend(lines, labels,loc = 3,title='Avg delay in min')

plt.title('United States Flight Routes Delay',fontsize=20)
plt.show()
plt.close()

## 10 Most Delay Routine
pd_flights_short_delay_flights_sort = pd_flights_short_delay_flights.sort_values(by=["AVG_DELAY_ROUTE"],ascending=False)[:30]

# Remove duplicate routines
row_id = []
routes = {}
row_count = -1
for i,r in pd_flights_short_delay_flights_sort.iterrows():
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
pd_flights_short_delay_flights_top = pd_flights_short_delay_flights_sort[pd_flights_short_delay_flights_sort.index.isin(row_id)].sort_values(by=["AVG_DELAY_ROUTE"], ascending=False)

fig = plt.figure(figsize=(25,20))
map = usa_map()
## Airports
log, lat = pd_flights_short_delay_flights_top['ORI_LONGITUDE'], pd_flights_short_delay_flights_top['ORI_LATITUDE']
log, lat = map(log, lat)
for x,y in zip(log, lat):
    map.scatter(x, y, s=30, c='green')
## Flights
log_ori, lat_ori = pd_flights_short_delay_flights_top["ORI_LONGITUDE"], pd_flights_short_delay_flights_top["ORI_LATITUDE"]
log_des, lat_des = pd_flights_short_delay_flights_top["DES_LONGITUDE"], pd_flights_short_delay_flights_top["DES_LATITUDE"]
delay = pd_flights_short_delay_flights_top["AVG_DELAY_ROUTE"]

names_ori = pd_flights_short_delay_flights_top['ORIGIN_AIRPORT']
names_des = pd_flights_short_delay_flights_top['DESTINATION_AIRPORT']
        
for i, (x1, y1, x2, y2, n1, n2, c) in enumerate(zip(log_ori, lat_ori, log_des, lat_des, names_ori, names_des, delay)):
    x1,y1 = map(x1,y1)
    x2,y2 = map(x2,y2)
    if i==0:
        color = "red"
    else:
        color = "blue"
    map.plot([x1,x2], [y1,y2], c=color, linewidth=0.01*c)
    plt.annotate(n1, xy=(x1, y1),  xycoords='data', xytext=(x1+0.3, y1+0.3), textcoords='data', c='red', fontsize=10, fontweight="bold" )
    plt.annotate(n2, xy=(x2, y2),  xycoords='data', xytext=(x2+0.3, y2+0.3), textcoords='data', c='red', fontsize=10, fontweight="bold" )

plt.title('United States - 10 Most Delay Routes',fontsize=20)
plt.show()
plt.close()






## Do basic data preprocessing and dataset spliting here. Remember to only use uncancelled data. We don't train for cancellation.
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
import warnings
import datetime
import json

FLIGHTS_DATA_PATH = "flights.csv"
pd_flights = pd.read_csv(FLIGHTS_DATA_PATH, low_memory=False)
pd_flights_not_cancelled = pd_flights[pd_flights['CANCELLED'] == 0]
warnings.filterwarnings('ignore')

# Use features MONTH, DAY_OF_WEEK, AIRLINE, ORIGIN_AIRPORT and SCHEDULED_DEPARTURE
def time_period(time):
    if 0 <= time and time < 600:
        return 'night'
    elif 600 <= time and time < 1200:
        return 'morning'
    elif 1200 <= time and time < 1800:
        return 'afternoon'
    elif 1800 <= time and time < 2400:
        return 'evening'

def create_df(df):
    df1 = df[['MONTH','DAY_OF_WEEK','AIRLINE','ORIGIN_AIRPORT','SCHEDULED_DEPARTURE', 'DEPARTURE_DELAY']]
    df1.dropna(how = 'any', inplace = True)
    #____________________
    # delete delays > 1h
    df1['DEPARTURE_DELAY'] = df1['DEPARTURE_DELAY'].apply(lambda x:x if x < 60 else np.nan)
    df1.dropna(how = 'any', inplace = True)
    #____________________
    # delete unknown airports data
    df1['ORIGIN_AIRPORT'] = df1['ORIGIN_AIRPORT'].apply(lambda x:x if x[0].isalpha() else np.nan)
    df1.dropna(how = 'any', inplace = True)
    #_________________
    # formating times
    df1['DEPARTURE_PERIOD'] = df1['SCHEDULED_DEPARTURE'].apply(time_period)
    return df1

df = create_df(pd_flights_not_cancelled)
del(pd_flights)
del(pd_flights_not_cancelled)
print(df.shape)
print(df[0:5])


# Convert airports whose counts are not in first 100 order and whose avg delay are not in first 100 order to "OTHER" to decrease feature levels
def get_stats(group):
    return {'min': group.min(), 'max': group.max(),
            'count': group.count(), 'mean': group.mean()}

check_airports = df['DEPARTURE_DELAY'].groupby(
                         df['ORIGIN_AIRPORT']).apply(get_stats).unstack()
check_airports.sort_values('count', ascending = False, inplace = True)
first_airports = check_airports[:100].index.tolist()

def get_stats(group):
    return {'min': group.min(), 'max': group.max(),
            'count': group.count(), 'mean': group.mean(), 'absmean': abs(group.mean())}

check_airports = df['DEPARTURE_DELAY'].groupby(
                         df['ORIGIN_AIRPORT']).apply(get_stats).unstack()
check_airports.sort_values('absmean', ascending = False, inplace = True)

first_airports.extend(check_airports[:100].index.tolist())

df['ORIGIN_AIRPORT'] = df['ORIGIN_AIRPORT'].apply(lambda x:x if x in first_airports else 'OTHER')
del(check_airports)
del(first_airports)


# Encoding airports, airline and departure_period
label_encoder = LabelEncoder()
onehot_encoder = OneHotEncoder(sparse=False)
PATH = 'drive/My Drive/bigdata_project/data/'

months_encoded = label_encoder.fit_transform(df['MONTH'])
'''
zipped = zip(df['MONTH'], months_encoded)
label_months = list(set(list(zipped)))
label_months.sort(key = lambda x:x[1])
months_json = {}
for month, index in label_months:
    months_json[str(month)] = str(index)
with open(PATH+'month.txt', 'w') as outfile:
    json.dump(months_json, outfile)
'''
months_encoded = months_encoded.reshape(len(months_encoded), 1)
onehot_encoded1 = onehot_encoder.fit_transform(months_encoded)
print(onehot_encoded1.shape[1])

weekdays_encoded = label_encoder.fit_transform(df['DAY_OF_WEEK'])
'''
zipped = zip(df['DAY_OF_WEEK'], weekdays_encoded)
label_weekdays = list(set(list(zipped)))
label_weekdays.sort(key = lambda x:x[1])
weekdays_json = {}
for weekday, index in label_weekdays:
    weekdays_json[str(weekday)] = str(index)
with open(PATH+'weekday.txt', 'w') as outfile:
    json.dump(weekdays_json, outfile)
'''
weekdays_encoded = weekdays_encoded.reshape(len(weekdays_encoded), 1)
onehot_encoded2 = onehot_encoder.fit_transform(weekdays_encoded)
print(onehot_encoded2.shape[1])

airports_encoded = label_encoder.fit_transform(df['ORIGIN_AIRPORT'])
'''
zipped = zip(df['ORIGIN_AIRPORT'], airports_encoded)
label_airports = list(set(list(zipped)))
label_airports.sort(key = lambda x:x[1])
airports_json = {}
for airport, index in label_airports:
    airports_json[airport] = str(index)
with open(PATH+'airport.txt', 'w') as outfile:
    json.dump(airports_json, outfile)
'''
airports_encoded = airports_encoded.reshape(len(airports_encoded), 1)
onehot_encoded3 = onehot_encoder.fit_transform(airports_encoded)
print(onehot_encoded3.shape[1])

airlines_encoded = label_encoder.fit_transform(df['AIRLINE'])
'''
zipped = zip(df['AIRLINE'], airlines_encoded)
label_airlines = list(set(list(zipped)))
label_airlines.sort(key = lambda x:x[1])
airlines_json = {}
for airline, index in label_airlines:
    airlines_json[airline] = str(index)
with open(PATH+'airline.txt', 'w') as outfile:
    json.dump(airlines_json, outfile)
'''
airlines_encoded = airlines_encoded.reshape(len(airlines_encoded), 1)
onehot_encoded4 = onehot_encoder.fit_transform(airlines_encoded)
print(onehot_encoded4.shape[1])

periods_encoded = label_encoder.fit_transform(df['DEPARTURE_PERIOD'])
'''
zipped = zip(df['DEPARTURE_PERIOD'], periods_encoded)
label_periods = list(set(list(zipped)))
label_periods.sort(key = lambda x:x[1])
periods_json = {}
for period, index in label_periods:
    periods_json[period] = str(index)
with open(PATH+'period.txt', 'w') as outfile:
    json.dump(periods_json, outfile)
'''
periods_encoded = periods_encoded.reshape(len(periods_encoded), 1)
onehot_encoded5 = onehot_encoder.fit_transform(periods_encoded)
print(onehot_encoded5.shape[1])

Y = np.array(df['DEPARTURE_DELAY'])
Y = Y.reshape(len(Y), 1)
print(Y.shape)
X = np.hstack((onehot_encoded1, onehot_encoded2, onehot_encoded3, onehot_encoded4, onehot_encoded5))
print(X.shape)

del(months_encoded)
del(onehot_encoded1)
del(weekdays_encoded)
del(onehot_encoded2)
del(airports_encoded)
del(onehot_encoded3)
del(airlines_encoded)
del(onehot_encoded4)
del(periods_encoded)
del(onehot_encoded5)


# Train and test dataset
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
print(X_test.shape)

'''
# Train and validation dataset
X_train, X_val, Y_train, Y_val = train_test_split(X_split, Y_split, test_size=0.2)
print(X_train.shape)
print(X_val.shape)
'''
del(X)
del(Y)


# Linear Regression
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import pickle

lm = LinearRegression()
lm.fit(X_train,Y_train)
filename = 'drive/My Drive/bigdata_project/data/linear.sav'
pickle.dump(lm, open(filename, 'wb'))

loaded_model = pickle.load(open(filename, 'rb'))
predictions = loaded_model.predict(X_train)
print("MSE =", metrics.mean_squared_error(predictions, Y_train))

icount = 0
for i, val in enumerate(Y_train):
    if abs(val-predictions[i]) > 15: icount += 1
print('{:.2f}%'.format(icount / len(predictions) * 100))

loaded_model = pickle.load(open(filename, 'rb'))
predictions = loaded_model.predict(X_test)
print("MSE =", metrics.mean_squared_error(predictions, Y_test))

icount = 0
for i, val in enumerate(Y_test):
    if abs(val-predictions[i]) > 15: icount += 1
print('{:.2f}%'.format(icount / len(predictions) * 100))

# Ridge regression
from sklearn.linear_model import Ridge
from sklearn import metrics
import pickle

ridgereg = Ridge(alpha=0.3,normalize=True)
ridgereg.fit(X_train, Y_train)

filename = 'drive/My Drive/bigdata_project/data/ridge.sav'
pickle.dump(ridgereg, open(filename, 'wb'))

loaded_model = pickle.load(open(filename, 'rb'))
predictions = loaded_model.predict(X_train)
print("MSE =", metrics.mean_squared_error(predictions, Y_train))

icount = 0
for i, val in enumerate(Y_train):
    if abs(val-predictions[i]) > 15: icount += 1
print('{:.2f}%'.format(icount / len(predictions) * 100))

loaded_model = pickle.load(open(filename, 'rb'))
predictions = loaded_model.predict(X_test)
print("MSE =", metrics.mean_squared_error(predictions, Y_test))

icount = 0
for i, val in enumerate(Y_test):
    if abs(val-predictions[i]) > 15: icount += 1
print('{:.2f}%'.format(icount / len(predictions) * 100))

from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics

regr = RandomForestRegressor(max_depth=10, random_state=0, n_estimators=10)
regr.fit(X_train, Y_train)
predictions = regr.predict(X_train)
print("MSE =", metrics.mean_squared_error(predictions, Y_train))

icount = 0
for i, val in enumerate(Y_train):
    if abs(val-predictions[i]) > 15: icount += 1
print('{:.2f}%'.format(icount / len(predictions) * 100))

















































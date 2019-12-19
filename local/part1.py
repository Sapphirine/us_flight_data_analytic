import pandas as pd
import plotly.graph_objs as go
from plotly.offline import iplot,init_notebook_mode
import cufflinks
cufflinks.go_offline(connected=True)

AIRPORTS_DATA_PATH = "airports.csv"
AIRLINES_DATA_PATH = "airlines.csv"
FLIGHTS_DATA_PATH = "flights.csv"
pd_flights = pd.read_csv(FLIGHTS_DATA_PATH, low_memory=False)
pd_airports = pd.read_csv(AIRPORTS_DATA_PATH)
pd_airlines = pd.read_csv(AIRLINES_DATA_PATH)

def enable_plotly_in_cell(): ## Needs it to shown fig in notebooks
  import IPython
  from plotly.offline import init_notebook_mode
  display(IPython.core.display.HTML('''
        <script src="/static/components/requirejs/require.js"></script>
  '''))
  init_notebook_mode(connected=False)


count_states = pd_airports['STATE'].value_counts()
enable_plotly_in_cell()
count_states.iplot(kind='bar', xTitle='State', yTitle='Count', title='Airport Location Distribution')

pd_airports['CITY_STATE'] = pd_airports['CITY'] + "," + pd_airports['STATE']
count_city = pd_airports['CITY_STATE'].value_counts()[:20]
enable_plotly_in_cell()
count_city.iplot(kind='bar', xTitle='City', yTitle='Count', title='Airport Location Distribution')

pd_flights_not_cancelled = pd_flights[pd_flights['CANCELLED'] == 0]
count_flights_origin = pd_flights_not_cancelled['ORIGIN_AIRPORT'].value_counts()[:20][::-1]
enable_plotly_in_cell()
count_flights_origin.iplot(kind='barh', xTitle='Count', yTitle='Airports', title='Origin Airport Distribution')

count_flights_arrival = pd_flights_not_cancelled['DESTINATION_AIRPORT'].value_counts()[:20][::-1]
enable_plotly_in_cell()
count_flights_arrival.iplot(kind='barh', xTitle='Count', yTitle='Airports', title='Arrival Airport Distribution')

pd_flights_airports_origin = pd_flights_not_cancelled.set_index('ORIGIN_AIRPORT').join(pd_airports.set_index('IATA_CODE'))
pd_flights_airports_origin['CITY_STATE'] = pd_flights_airports_origin['CITY'] + ',' + pd_flights_airports_origin['STATE']
count_cities_origin = pd_flights_airports_origin['CITY_STATE'].value_counts()[:20][::-1]
enable_plotly_in_cell()
count_cities_origin.iplot(kind='barh', xTitle='Count', yTitle='Cities', title='Origin City Distribution')

pd_flights_airports_arrival = pd_flights_not_cancelled.set_index('DESTINATION_AIRPORT').join(pd_airports.set_index('IATA_CODE'))
pd_flights_airports_arrival['CITY_STATE'] = pd_flights_airports_arrival['CITY'] + ',' + pd_flights_airports_arrival['STATE']
count_cities_arrival = pd_flights_airports_arrival['CITY_STATE'].value_counts()[:20][::-1]
enable_plotly_in_cell()
count_cities_origin.iplot(kind='barh', xTitle='Count', yTitle='Cities', title='Arrival City Distribution')

pd_airlines_count = pd_flights_not_cancelled.set_index('AIRLINE').join(pd_airlines.set_index('IATA_CODE'))['AIRLINE'].value_counts()[:10][::-1]
enable_plotly_in_cell()
trace = go.Bar(
    x=pd_airlines_count.index,
    y=pd_airlines_count.values,
    marker=dict(
        color = pd_airlines_count.values,
        colorscale='Jet',
        showscale=True)
)
data = [trace]
layout = go.Layout(xaxis=dict(tickangle=15),
    title='Airline distribution', 
                   yaxis = dict(title = 'Count'))
fig = go.Figure(data=data, layout=layout)
iplot(fig)

enable_plotly_in_cell()
label = pd_airlines_count.index
size = pd_airlines_count.values
colors = ['blue', 'yellow', 'green', 'grey', 'gold', 'orange', 'red', 
          'purple','lightgreen','aqua']
trace = go.Pie(labels=label, values=size, marker=dict(colors=colors),hole = .1)

data = [trace]
layout = go.Layout(
    title='Airline Distribution'
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)



pd_flights_not_cancelled['ROUTES'] = pd_flights_not_cancelled['ORIGIN_AIRPORT'] + '->' + pd_flights_not_cancelled['DESTINATION_AIRPORT']
pd_flights_routes_count = pd_flights_not_cancelled['ROUTES'].value_counts()[:20][::-1]
enable_plotly_in_cell()
trace = go.Bar(
    x=pd_flights_routes_count.index,
    y=pd_flights_routes_count.values,
    marker=dict(
        color = pd_flights_routes_count.values,
        colorscale='Magma',
        showscale=True)
)
data = [trace]
layout = go.Layout(xaxis=dict(tickangle=20),
    title='Air Routes distribution', 
                   yaxis = dict(title = 'Count'))
fig = go.Figure(data=data, layout=layout)
iplot(fig)

pd_flights_month_count = pd_flights_not_cancelled['MONTH'].value_counts()[:20][::-1].sort_index()
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
enable_plotly_in_cell()
trace = go.Bar(
    x=MONTHS,
    y=pd_flights_month_count.values,
    marker=dict(
        color = pd_flights_month_count.values,
        colorscale='Viridis',
        showscale=True)
)
data = [trace]
layout = go.Layout(xaxis=dict(tickangle=20),
    title='Air Flights by Month', 
                   yaxis = dict(title = 'Count'))
fig = go.Figure(data=data, layout=layout)
iplot(fig)


pd_flights_weekday_count = pd_flights_not_cancelled['DAY_OF_WEEK'].value_counts()[:20][::-1].sort_index()
WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
enable_plotly_in_cell()
trace = go.Bar(
    x=WEEKDAYS,
    y=pd_flights_weekday_count.values,
    marker=dict(
        color = pd_flights_weekday_count.values,
        colorscale='Cividis',
        showscale=True)
)
data = [trace]
layout = go.Layout(xaxis=dict(tickangle=20),
    title='Air Flights by Weekdays', 
                   yaxis = dict(title = 'Count'))
fig = go.Figure(data=data, layout=layout)
iplot(fig)

pd_flights_not_cancelled['SPEED'] = (pd_flights_not_cancelled['DISTANCE'] / pd_flights_not_cancelled['AIR_TIME'] ) * 60
pd_flights_airlines_speed = pd_flights_not_cancelled.set_index('AIRLINE').join(pd_airlines.set_index('IATA_CODE')).groupby('AIRLINE')['SPEED'].mean().sort_values(ascending=False)[:20]

enable_plotly_in_cell()
trace = go.Scatter(
    x=pd_flights_airlines_speed.index,
    y=pd_flights_airlines_speed.values,
    mode='markers',
    marker=dict(
        size=20,
        color = pd_flights_airlines_speed.values,
        colorscale='Rdbu',
        showscale=True)
)
data = [trace]
layout = go.Layout(xaxis=dict(tickangle=20),
    title='Airlines Speed Distribution', 
                   yaxis = dict(title = 'Speed (miles/h)'))
fig = go.Figure(data=data, layout=layout)
iplot(fig)

# Number of cancelled flights
print("Number of Cancelled flights:", pd_flights[pd_flights.CANCELLED==1].shape[0])
print("Percentage of Cancelled flights:",float(pd_flights[pd_flights.CANCELLED==1].shape[0]) / pd_flights.shape[0])

# Cancelled flight count by airline
cancelled_count_by_airlines = pd_flights[pd_flights.CANCELLED==1]['AIRLINE'].value_counts().reset_index()\
.sort_values(by='AIRLINE', ascending=False)
cancelled_count_by_airlines.columns = ['airline', 'counts']
enable_plotly_in_cell()

trace = go.Bar(
    x=cancelled_count_by_airlines.airline,
    y=cancelled_count_by_airlines.counts,
    marker=dict(
        color = cancelled_count_by_airlines.counts,
        colorscale='Blues',
        showscale=True)
)

data = [trace]
layout = go.Layout(
    title='# of Cancelled Flights by Airline', 
    yaxis = dict(title = '# of Flights'), 
    xaxis = dict(title = 'Airline')
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)

# Cancelled flight rate by airline
cancelled_rate_by_airlines = pd_flights.groupby('AIRLINE')[['CANCELLED']].mean()\
.sort_values(by='CANCELLED', ascending=False).round(3)
cancelled_rate_by_airlines = pd.DataFrame({'airline': cancelled_rate_by_airlines.index, 'rate': cancelled_rate_by_airlines.CANCELLED})
enable_plotly_in_cell()

trace = go.Scatter(
    x=cancelled_rate_by_airlines.airline,
    y=cancelled_rate_by_airlines.rate,
    mode='markers',
    marker=dict(
        sizemode = 'diameter',
        sizeref = 1,
        size = 15,
        color = cancelled_rate_by_airlines.rate.values,
        colorscale='Blues',
        showscale=True
    )
)

data = [trace]
layout = go.Layout(
    title='Cancellation Rate by Airline', 
    yaxis = dict(title = 'Cancellation Rate'), 
    xaxis = dict(title = 'Airline')
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)



# Cancelled flight count by departure airport
cancelled_count_by_airport = pd_flights[pd_flights.CANCELLED==1]['ORIGIN_AIRPORT'].value_counts().reset_index()\
.sort_values(by='ORIGIN_AIRPORT', ascending=False)[:15]
cancelled_count_by_airport.columns = ['airport', 'counts']
enable_plotly_in_cell()

trace = go.Bar(
    x=cancelled_count_by_airport.airport,
    y=cancelled_count_by_airport.counts,
    marker=dict(
        color = cancelled_count_by_airport.counts,
        colorscale='Greens',
        showscale=True)
)

data = [trace]
layout = go.Layout(
    title='# of Cancelled Flights by Departure Airport - Top 15', 
    yaxis = dict(title = '# of Flights'), 
    xaxis = dict(title = 'Departure Airport')
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)



# Cancelled flight rate by departure city
cancelled_rate_by_airport = pd_flights.groupby('ORIGIN_AIRPORT')[['CANCELLED']].mean()\
.sort_values(by='CANCELLED', ascending=False).round(3)
cancelled_rate_by_airport = pd.DataFrame({'airport': cancelled_rate_by_airport.index, 'rate': cancelled_rate_by_airport.CANCELLED})[:15]
enable_plotly_in_cell()

trace = go.Scatter(
    x=cancelled_rate_by_airport.airport,
    y=cancelled_rate_by_airport.rate,
    mode='markers',
    marker=dict(
        sizemode = 'diameter',
        sizeref = 1,
        size = 15,
        color = cancelled_rate_by_airport.rate.values,
        colorscale='Greens',
        showscale=True
    )
)

data = [trace]
layout = go.Layout(
    title='Cancellation Rate by Departure Airport - Top 15', 
    yaxis = dict(title = 'Cancellation Rate'), 
    xaxis = dict(title = 'Departure City')
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)



# Cancelled flight count by weekday
dayOfWeek={1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday', 7:'Sunday'}
cancelled_count_by_weekday = pd_flights[pd_flights.CANCELLED==1]['DAY_OF_WEEK'].value_counts().reset_index()\
.sort_values(by='DAY_OF_WEEK', ascending=False)
cancelled_count_by_weekday.columns = ['weekday', 'cancelled']
cancelled_count_by_weekday.weekday = cancelled_count_by_weekday.weekday.map(dayOfWeek)
enable_plotly_in_cell()

trace = go.Bar(
    x=cancelled_count_by_weekday.weekday,
    y=cancelled_count_by_weekday.cancelled, 
    marker=dict(
        color = cancelled_count_by_weekday.cancelled,
        colorscale='Oranges',
        showscale=True)
)

data = [trace]
layout = go.Layout(
    title='# of Cancelled Flights by Day of Week', 
    yaxis = dict(title = '# of Flights'), 
    xaxis = dict(title = 'Day of Week')
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)



# Cancelled flight rate by weekday
dayOfWeek={1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday', 7:'Sunday'}
cancelled_rate_by_weekday = pd_flights.groupby('DAY_OF_WEEK')[['CANCELLED']].mean()\
.sort_values(by='CANCELLED', ascending=False).round(3)
cancelled_rate_by_weekday = pd.DataFrame({'weekday': cancelled_rate_by_weekday.index, 'rate': cancelled_rate_by_weekday.CANCELLED})
cancelled_rate_by_weekday.weekday = cancelled_rate_by_weekday.weekday.map(dayOfWeek)
enable_plotly_in_cell()

trace = go.Scatter(
    x=cancelled_rate_by_weekday.weekday,
    y=cancelled_rate_by_weekday.rate,
    mode='markers',
    marker=dict(
        sizemode = 'diameter',
        sizeref = 1,
        size = 15,
        color = cancelled_rate_by_weekday.rate.values,
        colorscale='Oranges',
        showscale=True
    )
)

data = [trace]
layout = go.Layout(
    title='Cancellation Rate by Day of Week', 
    yaxis = dict(title = 'Cancellation Rate'), 
    xaxis = dict(title = 'Day of Week')
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)


# Cancelled flight count by month
month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', \
         6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
cancelled_count_by_month = pd_flights[pd_flights.CANCELLED==1]['MONTH'].value_counts().reset_index()\
.sort_values(by='MONTH', ascending=False)
cancelled_count_by_month.columns = ['month', 'cancelled']
cancelled_count_by_month.month = cancelled_count_by_month.month.map(month)
enable_plotly_in_cell()

trace = go.Bar(
    x=cancelled_count_by_month.month,
    y=cancelled_count_by_month.cancelled, 
    marker=dict(
        color = cancelled_count_by_month.cancelled,
        colorscale='PuRd',
        showscale=True)
)

data = [trace]
layout = go.Layout(
    title='# of Cancelled Flights by Month', 
    yaxis = dict(title = '# of Flights'), 
    xaxis = dict(title = 'Month')
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)



# Cancelled flight rate by month
month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', \
         6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
cancelled_rate_by_month = pd_flights.groupby('MONTH')[['CANCELLED']].mean()\
.sort_values(by='CANCELLED', ascending=False).round(3)
cancelled_rate_by_month = pd.DataFrame({'month': cancelled_rate_by_month.index, 'rate': cancelled_rate_by_month.CANCELLED})
cancelled_rate_by_month.month = cancelled_rate_by_month.month.map(month)
enable_plotly_in_cell()

trace = go.Scatter(
    x=cancelled_rate_by_month.month,
    y=cancelled_rate_by_month.rate,
    mode='markers',
    marker=dict(
        sizemode = 'diameter',
        sizeref = 1,
        size = 15,
        color = cancelled_rate_by_month.rate.values,
        colorscale='PuRd',
        showscale=True
    )
)

data = [trace]
layout = go.Layout(
    title='Cancellation Rate by Month', 
    yaxis = dict(title = 'Cancellation Rate'), 
    xaxis = dict(title = 'Month')
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)



# Cancellation Reason
pd_flights[pd_flights.CANCELLED == 1].CANCELLATION_REASON.unique()


# Cancellation reason by airline
reasons = {'A':'Airline/Carrier', 'B':'Weather', 'C':'National Air System', 'D':'Security'}
enable_plotly_in_cell()

pd_cancelled_flights = pd_flights[pd_flights.CANCELLED == 1]
pd_cancelled_flights.CANCELLATION_REASON = pd_cancelled_flights.CANCELLATION_REASON.map(reasons)

d = pd_cancelled_flights[pd_cancelled_flights.CANCELLATION_REASON=='Airline/Carrier'].AIRLINE.value_counts()
d = d.to_frame().sort_index()

trace1 = go.Bar(
    x=d.index,
    y=d.AIRLINE,
    name='Airline/Carrier',
    marker=dict(
        color = 'lightcoral'
    )
)

d = pd_cancelled_flights[pd_cancelled_flights.CANCELLATION_REASON=='Weather'].AIRLINE.value_counts()
d = d.to_frame().sort_index()

trace2 = go.Bar(
    x=d.index,
    y=d.AIRLINE,
    name = 'Weather',
    marker=dict(
        color = 'skyblue'
    )
)

d = pd_cancelled_flights[pd_cancelled_flights.CANCELLATION_REASON=='National Air System'].AIRLINE.value_counts()
d = d.to_frame().sort_index()

trace3 = go.Bar(
    x=d.index,
    y=d.AIRLINE,
    name='National Air System',
    marker=dict(
        color = 'gold'
    )
)

d = pd_cancelled_flights[pd_cancelled_flights.CANCELLATION_REASON=='Security'].AIRLINE.value_counts()
d = d.to_frame().sort_index()

trace4 = go.Bar(
    x=d.index,
    y=d.AIRLINE,
    name='Security',
    marker=dict(
        color = 'limegreen'
    )
)

data = [trace1,trace2,trace3, trace4]
layout = go.Layout(
    title='Cancellation Reasons by Airline', 
    yaxis = dict(title = '# of Flights'),
    xaxis = dict(title = 'Airline')
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)





# Cancellation reason by departure airport
pd_cancelled_flights_airport =  pd_cancelled_flights[pd_cancelled_flights.ORIGIN_AIRPORT.isin(cancelled_rate_by_airport.airport.unique())]
enable_plotly_in_cell()

d = pd_cancelled_flights_airport[pd_cancelled_flights_airport.CANCELLATION_REASON=='Airline/Carrier'].ORIGIN_AIRPORT.value_counts()
d = d.to_frame().sort_index()

trace1 = go.Bar(
    x=d.index,
    y=d.ORIGIN_AIRPORT,
    name='Airline/Carrier',
    marker=dict(
        color = 'lightcoral'
    )
)

d = pd_cancelled_flights_airport[pd_cancelled_flights_airport.CANCELLATION_REASON=='Weather'].ORIGIN_AIRPORT.value_counts()
d = d.to_frame().sort_index()

trace2 = go.Bar(
    x=d.index,
    y=d.ORIGIN_AIRPORT,
    name = 'Weather',
    marker=dict(
        color = 'skyblue'
    )
)

d = pd_cancelled_flights_airport[pd_cancelled_flights_airport.CANCELLATION_REASON=='National Air System'].ORIGIN_AIRPORT.value_counts()
d = d.to_frame().sort_index()

trace3 = go.Bar(
    x=d.index,
    y=d.ORIGIN_AIRPORT,
    name='National Air System',
    marker=dict(
        color = 'gold'
    )
)

d = pd_cancelled_flights_airport[pd_cancelled_flights_airport.CANCELLATION_REASON=='Security'].ORIGIN_AIRPORT.value_counts()
d = d.to_frame().sort_index()

trace4 = go.Bar(
    x=d.index,
    y=d.ORIGIN_AIRPORT,
    name='Security',
    marker=dict(
        color = 'limegreen'
    )
)

data = [trace1,trace2,trace3, trace4]
layout = go.Layout(
    title='Cancellation Reasons by Departure Airport - top 15', 
    yaxis = dict(title = '# of Flights'),
    xaxis = dict(title = 'Departure Airport')
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)



# Cancellation reason by weekday
enable_plotly_in_cell()

d = pd_cancelled_flights[pd_cancelled_flights.CANCELLATION_REASON=='Airline/Carrier'].DAY_OF_WEEK.value_counts()
d = d.to_frame().sort_index()
d.index = d.index.map(dayOfWeek)

trace1 = go.Bar(
    x=d.index,
    y=d.DAY_OF_WEEK,
    name='Airline/Carrier',
    marker=dict(
        color = 'lightcoral'
    )
)

d = pd_cancelled_flights[pd_cancelled_flights.CANCELLATION_REASON=='Weather'].DAY_OF_WEEK.value_counts()
d = d.to_frame().sort_index()
d.index = d.index.map(dayOfWeek)

trace2 = go.Bar(
    x=d.index,
    y=d.DAY_OF_WEEK,
    name = 'Weather',
    marker=dict(
        color = 'skyblue'
    )
)

d = pd_cancelled_flights[pd_cancelled_flights.CANCELLATION_REASON=='National Air System'].DAY_OF_WEEK.value_counts()
d = d.to_frame().sort_index()
d.index = d.index.map(dayOfWeek)

trace3 = go.Bar(
    x=d.index,
    y=d.DAY_OF_WEEK,
    name='National Air System',
    marker=dict(
        color = 'gold'
    )
)

d = pd_cancelled_flights[pd_cancelled_flights.CANCELLATION_REASON=='Security'].DAY_OF_WEEK.value_counts()
d = d.to_frame().sort_index()
d.index = d.index.map(dayOfWeek)

trace4 = go.Bar(
    x=d.index,
    y=d.DAY_OF_WEEK,
    name='Security',
    marker=dict(
        color = 'limegreen'
    )
)

data = [trace1,trace2,trace3, trace4]
layout = go.Layout(
    title='Cancellation Reasons by Day of Week', 
    yaxis = dict(title = '# of Flights'),
    xaxis = dict(title = 'Day of Week')
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)



# Cancellation reason by month
enable_plotly_in_cell()

d = pd_cancelled_flights[pd_cancelled_flights.CANCELLATION_REASON=='Airline/Carrier'].MONTH.value_counts()
d = d.to_frame().sort_index()
d.index = d.index.map(month)

trace1 = go.Bar(
    x=d.index,
    y=d.MONTH,
    name='Airline/Carrier',
    marker=dict(
        color = 'lightcoral'
    )
)

d = pd_cancelled_flights[pd_cancelled_flights.CANCELLATION_REASON=='Weather'].MONTH.value_counts()
d = d.to_frame().sort_index()
d.index = d.index.map(month)

trace2 = go.Bar(
    x=d.index,
    y=d.MONTH,
    name = 'Weather',
    marker=dict(
        color = 'skyblue'
    )
)

d = pd_cancelled_flights[pd_cancelled_flights.CANCELLATION_REASON=='National Air System'].MONTH.value_counts()
d = d.to_frame().sort_index()
d.index = d.index.map(month)

trace3 = go.Bar(
    x=d.index,
    y=d.MONTH,
    name='National Air System',
    marker=dict(
        color = 'gold'
    )
)

d = pd_cancelled_flights[pd_cancelled_flights.CANCELLATION_REASON=='Security'].MONTH.value_counts()
d = d.to_frame().sort_index()
d.index = d.index.map(month)

trace4 = go.Bar(
    x=d.index,
    y=d.MONTH,
    name='Security',
    marker=dict(
        color = 'limegreen'
    )
)

data = [trace1,trace2,trace3, trace4]
layout = go.Layout(
    title='Cancellation Reasons by Month', 
    yaxis = dict(title = '# of Flights'),
    xaxis = dict(title = 'Month')
)

fig = go.Figure(data=data, layout=layout)
iplot(fig)
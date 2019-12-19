from django.http import HttpResponse
from django.shortcuts import render
import pandas_gbq
from google.oauth2 import service_account
import math
import json
import numpy as np
import pickle
from sklearn import metrics
import warnings

# Make sure you have installed pandas-gbq at first;
# You can use the other way to query BigQuery.
# please have a look at
# https://cloud.google.com/bigquery/docs/reference/libraries#client-libraries-install-nodejs
# To get your credential

credentials = service_account.Credentials.from_service_account_file('./credentials/BigData-d79e8ed11c92.json')
Project_id = "bigdata-252821"
state_json_path = "./static/data/us-states.json"
data_path = "./static/data/"

def home(request):
    return render(request, 'home.html')

def predict(request):
    data = {}
    data['month'] = {'month': request.GET.get('month',False)}
    data['weekday'] = {'weekday': request.GET.get('weekday',False)}
    data['airport'] = {'airport': request.GET.get('airport',False)}
    data['airline'] = {'airline': request.GET.get('airline',False)}
    data['period'] = {'period': request.GET.get('period',False)}
    
    if data['month']['month']:
        months = []
        with open(data_path+'month.txt') as json_file:
            month = json.load(json_file)
            month_a = np.zeros((len(month),), dtype=int)
            month_a[int(month[data['month']['month']])] = 1
            months = month_a

    if data['weekday']['weekday']:
        weekdays = []
        with open(data_path+'weekday.txt') as json_file:
            weekday = json.load(json_file)
            weekday_a = np.zeros((len(weekday),), dtype=int)
            weekday_a[int(weekday[data['weekday']['weekday']])] = 1
            weekdays = weekday_a

    if data['airport']['airport']:
        airports = []
        with open(data_path+'airport.txt') as json_file:
            airport = json.load(json_file)
            airport_a = np.zeros((len(airport),), dtype=int)
            airport_input = data['airport']['airport']
            if airport_input not in airport.keys():
              airport_input = 'OTHER'
            airport_a[int(airport[airport_input])] = 1
            airports = airport_a

    if data['airline']['airline']:
        airlines = []
        with open(data_path+'airline.txt') as json_file:
            airline = json.load(json_file)
            airline_a = np.zeros((len(airline),), dtype=int)
            airline_a[int(airline[data['airline']['airline']])] = 1
            airlines = airline_a

    if data['period']['period']:
        periods = []
        with open(data_path+'period.txt') as json_file:
            period = json.load(json_file)
            period_a = np.zeros((len(period),), dtype=int)
            period_a[int(period[data['period']['period']])] = 1
            periods = period_a

        X = np.hstack((months, weekdays, airports, airlines, periods))
        X_test = np.reshape(X, (-1, len(X)))
        filename = data_path+'linear.sav'
        warnings.filterwarnings('ignore')
        loaded_model = pickle.load(open(filename, 'rb'))
        prediction = loaded_model.predict(X_test)

        data['predict_delay'] = {'predict_delay': str(round(prediction[0][0], 2))}

    return render(request, 'predict.html', data)

## State Code to Name
code_to_state = {'AK': 'Alaska','AL': 'Alabama','AR': 'Arkansas','AS': 'American Samoa','AZ': 'Arizona','CA': 'California','CO': 'Colorado','CT': 'Connecticut',
                 'DC': 'District of Columbia','DE': 'Delaware','FL': 'Florida','GA': 'Georgia','GU': 'Guam','HI': 'Hawaii','IA': 'Iowa','ID': 'Idaho',
                 'IL': 'Illinois','IN': 'Indiana','KS': 'Kansas','KY': 'Kentucky','LA': 'Louisiana','MA': 'Massachusetts','MD': 'Maryland','ME': 'Maine',
                 'MI': 'Michigan','MN': 'Minnesota','MO': 'Missouri','MP': 'Northern Mariana Islands','MS': 'Mississippi','MT': 'Montana','NA': 'National',
                 'NC': 'North Carolina','ND': 'North Dakota','NE': 'Nebraska','NH': 'New Hampshire','NJ': 'New Jersey','NM': 'New Mexico','NV': 'Nevada',
                 'NY': 'New York','OH': 'Ohio','OK': 'Oklahoma','OR': 'Oregon','PA': 'Pennsylvania','PR': 'Puerto Rico','RI': 'Rhode Island',
                 'SC': 'South Carolina','SD': 'South Dakota','TN': 'Tennessee','TX': 'Texas','UT': 'Utah','VA': 'Virginia','VI': 'Virgin Islands',
                 'VT': 'Vermont','WA': 'Washington','WI': 'Wisconsin','WV': 'West Virginia','WY': 'Wyoming'}
not_use_state = ["PR", "VI", "GU", "AS"] # Omit Puerto Rico/Virgin Island/GUAM/American Samoa due to visualization problems

def map(request):
    pandas_gbq.context.credentials = credentials
    pandas_gbq.context.project = Project_id

    data = {}
    ## For State and Count
    SQL1 = """
               SELECT AR.STATE, COUNT(*) as COUNT
               FROM us_flight.flights as F JOIN us_flight.airports AR ON F.ORIGIN_AIRPORT = AR.IATA_CODE
               GROUP BY AR.STATE
               ORDER BY COUNT DESC;
           """
    df1 = pandas_gbq.read_gbq(SQL1)
    '''
        Format of data:
        ## State and Count. Dict with each STATE_CODE as key, each value is still a dict
        data['State'] = {'Texas': {'State_Abv':TX, 'Count': 11000},"California": {'State_Abv': "CA", 'Count':10000},...}
    '''
    states = {}
    for ind, r in df1.iterrows():
        if r["STATE"] not in not_use_state:
            result = {}
            result['State_Abv'] = r["STATE"]
            result["Count"] = r["COUNT"]
            states[code_to_state[r["STATE"]]] = result
    states["Max_Count"] = df1["COUNT"].iloc[0]

    ## For Airport and Count
    SQL2 = """
               WITH A AS(
                   SELECT F.ORIGIN_AIRPORT, COUNT(*) as COUNT
                   FROM us_flight.flights as F JOIN us_flight.airports AR ON F.ORIGIN_AIRPORT = AR.IATA_CODE
                   GROUP BY F.ORIGIN_AIRPORT
                   ORDER BY COUNT DESC)
               SELECT AR.IATA_CODE, AR.AIRPORT, AR.CITY, AR.STATE, AR.LATITUDE, AR.LONGITUDE, A.COUNT
               FROM A JOIN us_flight.airports AR ON A.ORIGIN_AIRPORT = AR.IATA_CODE
               ORDER BY A.COUNT DESC;
           """
    df2 = pandas_gbq.read_gbq(SQL2)
    '''
        Format of data:
        ## Airport and Count. List of many dicts
        data['Airport'] = [{'Name':"Los Angeles Airport", 'Code': "LAX", 'City': "Los Angeles", 'State_Abv': "CA", 'State_Name': "California", 'Latitude':51.22 ,'Longitude': -151.22, 'Count':1000},,... ]
    '''
    airports = []
    for ind, r in df2.iterrows():
        if math.isnan(r["LATITUDE"]) or math.isnan(r["LONGITUDE"]) or r["STATE"] in not_use_state:
            continue
        n = {}
        n["Name"] = r["AIRPORT"]
        n["Code"] = r["IATA_CODE"]
        n["City"] = r["CITY"]
        n['State_Abv'] = r["STATE"]
        n["State_Name"] = code_to_state[r["STATE"]]
        n['Latitude'] = r["LATITUDE"]
        n['Longitude'] = r["LONGITUDE"]
        n["Count"] = r["COUNT"]
        airports.append(n)

    ## For flight routes from different Airport
    SQL3 = """
              WITH B AS(
                  WITH A AS(
                      SELECT F.ORIGIN_AIRPORT,F.DESTINATION_AIRPORT, COUNT(*) as COUNT
                      FROM us_flight.flights as F JOIN us_flight.airports AR ON F.ORIGIN_AIRPORT = AR.IATA_CODE
                      GROUP BY F.ORIGIN_AIRPORT, F.DESTINATION_AIRPORT
                      ORDER BY COUNT DESC)
                  SELECT A.ORIGIN_AIRPORT, AR.STATE AS ORI_STATE, AR.LATITUDE AS ORI_LATITUDE, AR.LONGITUDE AS ORI_LONGITUDE, A.DESTINATION_AIRPORT, A.COUNT
                  FROM A JOIN us_flight.airports AR ON A.ORIGIN_AIRPORT = AR.IATA_CODE)
              SELECT B.ORIGIN_AIRPORT, B.ORI_STATE, B.ORI_LATITUDE, B.ORI_LONGITUDE, B.DESTINATION_AIRPORT, AR.STATE AS DES_STATE, AR.LATITUDE AS DES_LATITUDE, AR.LONGITUDE AS DES_LONGITUDE, B.COUNT
              FROM B JOIN us_flight.airports AR ON B.DESTINATION_AIRPORT = AR.IATA_CODE
              ORDER BY ORIGIN_AIRPORT, COUNT DESC;
           """
    df3 = pandas_gbq.read_gbq(SQL3)
    '''
        Format of data:
        ## Route: Origin Airport and its Destinations with Count. Dict with each ORI_AIRPORT_CODE as key.
        ## Each value is still a dict. The destination in value is a list. Only keeps valuable informations
        ## MaxCount is used to scale the line width.
        data['Routes'] = {"LAX": ["Max_Count":3000, "Destination:"{"Code":..}{"Code":...}], ...}
        data['Routes']["LAX"]["Destination"] = [{"Code": "SFO", 'Ori_Latitude':51.22 ,'Ori_Longitude': -151.22, 'Des_Latitude':22.22 ,'Des_Longitude': -151.22,"Count"=1000,"Max_Count":3000},....]
    '''
    routes = {}
    for ind, r in df3.iterrows():
        ## Remove invalid routes
        if r["ORI_STATE"] in not_use_state or r["DES_STATE"] in not_use_state or math.isnan(r["ORI_LATITUDE"]) or math.isnan(r["ORI_LONGITUDE"]) or math.isnan(r["DES_LATITUDE"]) or math.isnan(r["DES_LONGITUDE"]):
            continue
        ## Init a origin airport
        if r["ORIGIN_AIRPORT"] not in routes.keys():
            routes[r["ORIGIN_AIRPORT"]] = {}
            routes[r["ORIGIN_AIRPORT"]]["Destination"] = []
            routes[r["ORIGIN_AIRPORT"]]["Max_Count"] = r["COUNT"]
        ## Append a destination airport
        des_airport = {}
        des_airport["Code"] = r["DESTINATION_AIRPORT"]
        des_airport["Ori_Latitude"] = r["ORI_LATITUDE"]
        des_airport["Ori_Longitude"] = r["ORI_LONGITUDE"]
        des_airport["Des_Latitude"] = r["DES_LATITUDE"]
        des_airport["Des_Longitude"] = r["DES_LONGITUDE"]
        des_airport["Count"] = r["COUNT"]
        des_airport["Max_Count"] = routes[r["ORIGIN_AIRPORT"]]["Max_Count"]
        routes[r["ORIGIN_AIRPORT"]]["Destination"].append(des_airport)

    ## For each airlines routes
    SQL4 = """
              WITH B AS(
                  WITH A AS(
                      SELECT F.AIRLINE AS CODE, F.ORIGIN_AIRPORT,F.DESTINATION_AIRPORT, COUNT(*) as COUNT
                      FROM us_flight.flights as F JOIN us_flight.airports AR ON F.ORIGIN_AIRPORT = AR.IATA_CODE
                      GROUP BY F.AIRLINE, F.ORIGIN_AIRPORT, F.DESTINATION_AIRPORT
                      ORDER BY COUNT DESC)
                  SELECT A.CODE, A.ORIGIN_AIRPORT, AR.STATE AS ORI_STATE, AR.LATITUDE AS ORI_LATITUDE, AR.LONGITUDE AS ORI_LONGITUDE, A.DESTINATION_AIRPORT, A.COUNT
                  FROM A JOIN us_flight.airports AR ON A.ORIGIN_AIRPORT = AR.IATA_CODE)
              SELECT B.CODE, B.ORIGIN_AIRPORT, B.ORI_STATE, B.ORI_LATITUDE, B.ORI_LONGITUDE, B.DESTINATION_AIRPORT, AR.STATE AS DES_STATE, AR.LATITUDE AS DES_LATITUDE, AR.LONGITUDE AS DES_LONGITUDE, B.COUNT
              FROM B JOIN us_flight.airports AR ON B.DESTINATION_AIRPORT = AR.IATA_CODE
              ORDER BY CODE, COUNT DESC, ORIGIN_AIRPORT;
           """
    df4 = pandas_gbq.read_gbq(SQL4)
    SQL5 = """
                SELECT *
                FROM us_flight.airlines;
           """
    df5 = pandas_gbq.read_gbq(SQL5)
    '''
        Format of data:
        ## Airline_Route: Different airlines's different Origin Airport and its Destinations with Count. Dict with each AIRLINE_CODE as key.
        ## Each value is still a dict. The destination in value is a list. Only keeps valuable informations
        ## MaxCount is used to scale the line width.
        data['Airline_Routes'] = {"UA": ["Max_Count":3000, "Routes:"{"Code":..}{"Code":...}], ...}
        data['Airline_Routes']["UA"]["Routes"] = [{'Ori_Latitude':51.22 ,'Ori_Longitude': -151.22, 'Des_Latitude':22.22 ,'Des_Longitude': -151.22,"Count"=1000,"Max_Count":3000},....]
    '''
    airline_routes = {}
    for ind, r in df4.iterrows():
        ## Remove invalid routes
        if r["ORI_STATE"] in not_use_state or r["DES_STATE"] in not_use_state or math.isnan(r["ORI_LATITUDE"]) or math.isnan(r["ORI_LONGITUDE"]) or math.isnan(r["DES_LATITUDE"]) or math.isnan(r["DES_LONGITUDE"]):
            continue
        ## Init a origin airport
        if r["CODE"] not in airline_routes.keys():
            airline_routes[r["CODE"]] = {}
            airline_routes[r["CODE"]]["Routes"] = []
            airline_routes[r["CODE"]]["Max_Count"] = r["COUNT"]
        ## Append a destination airport
        route = {}
        route["Ori_Latitude"] = r["ORI_LATITUDE"]
        route["Ori_Longitude"] = r["ORI_LONGITUDE"]
        route["Des_Latitude"] = r["DES_LATITUDE"]
        route["Des_Longitude"] = r["DES_LONGITUDE"]
        route["Count"] = r["COUNT"]
        route["Max_Count"] = airline_routes[r["CODE"]]["Max_Count"]
        airline_routes[r["CODE"]]["Routes"].append(route)

    airlines = []
    for ind, r in df5.iterrows():
        airline = {}
        airline["Code"] = r["IATA_CODE"]
        airline["Name"] = r["AIRLINE"]
        airlines.append(airline)

    ## For time. We only consider the first week in the year. Otherwise too many data.
    SQL6 = """
            WITH B AS(
              WITH A AS(
                SELECT F.ORIGIN_AIRPORT,F.DESTINATION_AIRPORT, F.DEPARTURE_TIME, F.ARRIVAL_TIME
                FROM us_flight.flights F JOIN us_flight.airports AR ON F.ORIGIN_AIRPORT = AR.IATA_CODE
                LIMIT 20000)
              SELECT A.ORIGIN_AIRPORT, AR.STATE AS ORI_STATE, AR.LATITUDE AS ORI_LATITUDE, AR.LONGITUDE AS ORI_LONGITUDE, A.DESTINATION_AIRPORT, A.DEPARTURE_TIME, A.ARRIVAL_TIME
              FROM A JOIN us_flight.airports AR ON A.ORIGIN_AIRPORT = AR.IATA_CODE)
            SELECT B.ORIGIN_AIRPORT, B.ORI_STATE, B.ORI_LATITUDE, B.ORI_LONGITUDE, B.DESTINATION_AIRPORT, AR.STATE AS DES_STATE, AR.LATITUDE AS DES_LATITUDE, AR.LONGITUDE AS DES_LONGITUDE, B.DEPARTURE_TIME, B.ARRIVAL_TIME
            FROM B JOIN us_flight.airports AR ON B.DESTINATION_AIRPORT = AR.IATA_CODE;
           """
    df6 = pandas_gbq.read_gbq(SQL6)
    '''
        Format of data:
        ## Time_Route: A list of flights given DEPARTURE_TIME and ARRIVAL_TIME
        data['Time_Routes'] = [{"ORI_LATITUDE":xx, "ORI_LONGITUDE":xx, "DES_LATITUDE":xx, "DES_LONGITUDE":xx,}...]
    '''
    time_routes = []
    for ind, r in df6.iterrows():
        ## Remove invalid routes
        if r["ORI_STATE"] in not_use_state or r["DES_STATE"] in not_use_state or math.isnan(r["ORI_LATITUDE"]) or math.isnan(r["ORI_LONGITUDE"]) or math.isnan(r["DES_LATITUDE"]) or math.isnan(r["DES_LONGITUDE"]) or math.isnan(r["DEPARTURE_TIME"]) or math.isnan(r["ARRIVAL_TIME"]):
            continue
        route = {}
        route["Ori_Latitude"] = r["ORI_LATITUDE"]
        route["Ori_Longitude"] = r["ORI_LONGITUDE"]
        route["Des_Latitude"] = r["DES_LATITUDE"]
        route["Des_Longitude"] = r["DES_LONGITUDE"]
        route["Dep_Time"] = r["DEPARTURE_TIME"]
        route["Arr_Time"] = r["ARRIVAL_TIME"]
        time_routes.append(route)

    data['state'] = states
    data['airport'] = airports
    data['route'] = routes
    data["airline_route"] = airline_routes
    data["airline"] = airlines
    data["time_route"] = time_routes
    with open(state_json_path) as json_file:
        data['state_json'] = json.load(json_file)
    return render(request, 'map.html', data)

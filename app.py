import streamlit as st
import requests
from shapely.geometry import Point, Polygon
import geopandas as gpd
import pandas as pd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import datetime

'''
# TaxiFareModel front
'''

d = st.date_input(
    "Set the day",
    datetime.date(2019, 7, 6))
t = st.time_input("Set the time", datetime.time(8, 45))
st.write(d,t)
passenger = st.number_input('Insert the number of passengers', format= "%d", step=1)


address = st.text_input("Pickup location", "JFK airport")
geolocator = Nominatim(user_agent="GTA Lookup")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
location = geolocator.geocode(address)
pick_lat = location.latitude
pick_long = location.longitude

map_data = pd.DataFrame({"lat": [pick_lat], "lon": [pick_long]})

address = st.text_input("Dropoff location", "Madison Square Park")
geolocator = Nominatim(user_agent="GTA Lookup")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
location = geolocator.geocode(address)
drop_lat = location.latitude
drop_long = location.longitude
drop=pd.DataFrame({
    "lat": [drop_lat],
    "lon": [drop_long]
})
map_data=map_data.append(drop)
st.map(map_data)

url = 'https://taxifare.lewagon.ai/predict'


pickup_datetime = f'{d} {t}'
# build X ⚠️ beware to the order of the parameters ⚠️
parameters = {
    "pickup_datetime":pickup_datetime,
    "pickup_longitude":pick_long,
    "pickup_latitude":pick_lat,
    "dropoff_longitude":drop_long,
    "dropoff_latitude":drop_lat,
    "passenger_count":passenger}

response = requests.get(url,params=parameters).json()

st.write('The estimated fare cost is:' ,response['prediction'])
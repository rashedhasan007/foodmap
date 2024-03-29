import streamlit as st
from streamlit_folium import folium_static
import folium
import json
import folium
import pandas as pd
import base64
from folium import IFrame

import streamlit as st

import warnings
warnings.filterwarnings('ignore')
import os

import codecs
import geocoder
g = geocoder.ip('me')

import requests
import json

send_url = "http://api.ipstack.com/check?access_key=e51d5b9649f03344146d8e72e8779eb2"
geo_req = requests.get(send_url)
geo_json = json.loads(geo_req.text)
latitude = geo_json['latitude']
longitude = geo_json['longitude']
city = geo_json['city']

f="""

"""


def getLatLon(allStations):
    res = []
    resNames = []
    latitudes = allStations['latitude']
    longitudes = allStations['longitude']
    names = allStations['name']
    for latitude, longitude, name in zip(latitudes,longitudes, names):
        res.append((latitude, longitude))
        resNames.append(name)
    return res, resNames

stations = pd.read_csv("austin_bikeshare_stations.csv", delimiter=',', skiprows=0, low_memory=False)
activeStations = stations[stations.status == 'active']
movedStations = stations[stations.status == 'moved']
closedStations = stations[stations.status == 'closed']
ACLStations = stations[stations.status == 'ACL only']

latlonActive, namesStationsActive = getLatLon(activeStations)
latlonMoved, namesStationsMoved = getLatLon(movedStations)
latlonClosed, namesStationsClosed = getLatLon(closedStations)
latlonACL, namesStationsACL = getLatLon(ACLStations)
#24.408649220141122, 88.60869992741216
mapStations = folium.Map( location=[latitude,longitude], zoom_start=18 )
for latlon, names, color in zip((latlonActive, latlonMoved, latlonClosed, latlonACL),
                                 (namesStationsActive, namesStationsMoved,
                                  namesStationsClosed, namesStationsACL),
                                ('green', 'blue', 'red', 'purple')):
    i=0
    for coord in latlon:
        #folium.Marker( location=[ coord[0], coord[1]], icon=folium.Icon(color=color),
                      #popup=names[i]).add_to( mapStations )

        encoded = base64.b64encode(open('icons8-burger-60.png', 'rb').read())
        html = '<h1>Onupom Store</h1><p>Amchottor,Rajshahi</p><p1>Total cokacol</p1><h1>8</h1><img src="data:image/png;base64,{}" style="width:300px;height:300px;">'.format

        iframe = IFrame(html(encoded.decode('UTF-8')), width=400, height=350)
        popup = folium.Popup(iframe, max_width=400)
        icon = folium.features.CustomIcon('icons8-burger-60.png', icon_size=(30, 30))

        folium.Marker(location=[ coord[0], coord[1]], tooltip=html, popup=popup,
                      icon=icon).add_to(mapStations)
        i += 1
#mapStations



folium.Circle([latitude,longitude],
                    radius=40
                   ).add_to(mapStations)
folium_static(mapStations)
st.title("rashed")
st.sidebar.button('hey')
html1="""
<!DOCTYPE html>
<html>
<head>

</head>
<body>

<h1>The border-radius Property</h1>

<p>Rounded corners for an element with a specified background color:</p>
<p style="border-radius: 25px;background: #73AD21;padding: 20px; width: 200px;height: 150px;">Rounded corners!</p>
</body>
</html>


"""
st.sidebar.markdown(html1.format(),unsafe_allow_html=True)
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

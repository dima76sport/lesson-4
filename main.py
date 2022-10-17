import json
import requests
from geopy import distance
import folium
from flask import Flask


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


def mapGen():
    with open("index.html") as file:
        return file.read()


apikey = 'c3d9fb00-6be4-45a2-b66a-550bdf888bdc'
yourPlace = input("Ваше местоположение? : ")
yourPlaceCoords = fetch_coordinates(apikey, yourPlace)
print("Ваши координаты : ")
print(yourPlaceCoords)


with open("coffee.json", "r", encoding="CP1251") as my_json:
    file_contents = my_json.read()

file_contents = json.loads(file_contents)

CoffeeShopList = []


for elem in file_contents:
    CoffeeShopInfo = {}
    CoffeeShopInfo["title"] = elem["Name"]
    CoffeeShopInfo["distance"] = distance.distance(yourPlaceCoords, (elem["Latitude_WGS84"], elem["Longitude_WGS84"])).km
    CoffeeShopInfo["latitude"] = elem["Latitude_WGS84"]
    CoffeeShopInfo["longitude"] = elem["Longitude_WGS84"]
    CoffeeShopList.append(CoffeeShopInfo)
nearestCoffeeShops = sorted(CoffeeShopList, key=lambda d: d['distance'])
nearestCoffeeShops = nearestCoffeeShops[0:5]


for index in range(1, len(nearestCoffeeShops)):
    CoffeeShop = nearestCoffeeShops[index]
    CoffeeShop2 = nearestCoffeeShops[index-1]
    if CoffeeShop["latitude"] == CoffeeShop["latitude"]:
        CoffeeShop["latitude"] = str(float(CoffeeShop["latitude"])+0.000150)
        CoffeeShop["longitude"] = str(float(CoffeeShop["longitude"])+0.000150)


Map = folium.Map(location=yourPlaceCoords, zoom_start=12)

folium.Marker(
    location=yourPlaceCoords,
    popup=yourPlace,
    icon=folium.Icon(color="red", icon="info-sign")).add_to(Map),
tooltip = "Click me"


for dictionary in nearestCoffeeShops:
    folium.Marker([dictionary["latitude"], dictionary["longitude"]], popup=f"<i>{dictionary['title']}</i>", tooltip=tooltip).add_to(Map)


Map.save("index.html")
tiles = 'Mapbox',
API_key = 'c3d9fb00-6be4-45a2-b66a-550bdf888bdc'

#---
#This code was changed by qanqanqan :)
#---


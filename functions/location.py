from dotenv import load_dotenv
from functions import authorizationKey
import json
import requests

def getLocation(office):
    if office['latitude'] and office['longitude']:
        coordinates = [float(office['latitude']), float(office['longitude'])]
    else:
        coordinates = [0,0]
    return {"type":"Point","coordinates":coordinates}

def invertCoordinates(collection):
    for e in collection.find():
        invert = lambda x,y: [y,x]
        print(e['location']['coordinates'])
        collection.update_one(e,{'$set':{'lat&long':e['location']['coordinates'],
                                         'location.coordinates':invert(*e['location']['coordinates'])}})

# https://api.opencagedata.com/geocode/v1/json?q=LAT+LNG&key=YOUR-API-KEY
def reverseGeocoding(lat,lng):
    load_dotenv()
    authToken = authorizationKey('GEO_TOKEN')
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lng}&key={authToken}"
    return requests.get(url)

def findCityFromCoords(office):
    res = reverseGeocoding(*office['location']['coordinates']).json()
    if res['total_results'] == 0:
        return 'Unknown'
    components = res['results'][0]['components']
    return components.get('city','Unknown')

def formatPlaceName(address,zip_code,city):
    address = (lambda a: a if a != None else '')(address)
    zip_code = (lambda a: a if a != None else '')(zip_code)   
    return '+'.join([address.replace(' ','+'), zip_code ,city.replace(' ','+')])
    
def forwardGeocoding(place_name):
    load_dotenv()
    authToken = authorizationKey('GEO_TOKEN')
    url = f"https://api.opencagedata.com/geocode/v1/json?q={place_name}&key={authToken}"
    return requests.get(url)

def findCoordsFromCity(office):
    place_name = formatPlaceName(office.get('address',''),office.get('zip_code',''),office.get('city',''))
    res = forwardGeocoding(place_name).json()
    if res['total_results'] == 0:
        return 'Unknown'
    coords = res['results'][0]['geometry']
    #[latitude, longitude]
    return {'type':'Point','coordinates':[*coords.values()]}
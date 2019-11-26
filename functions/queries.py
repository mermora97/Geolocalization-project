import os 
import requests
from dotenv import load_dotenv
load_dotenv()

def authorizationKey(key):
    authToken = os.getenv(key)
    if not authToken:
        raise ValueError('A key token is neeeded')
    else:
        print("We have a github token: ", authToken[0:4])
    return authToken

def getDocFromGoogleQuery(doc,city):
    coords = [*doc['geometry']['location'].values()]
    return {
        'address':doc['formatted_address'],
        'city':city,
        'location':{'type':'Point',
        'coordinates':coords[::-1]},
        'rating':doc['rating']
    }

def getDataFromGoogleQuery(jsonResponse,city):
    docs = []
    for r in jsonResponse['results']:
        docs.append(getDocFromGoogleQuery(r,city))
    return docs

def googleQuery(query,pagetoken = None):
    authToken = authorizationKey('GOOGLE_TOKEN')
    url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}'
    if pagetoken:
        url += f'&pagetoken={pagetoken}'
        print('pagetoken')
    return requests.get(url+f'&key={authToken}')


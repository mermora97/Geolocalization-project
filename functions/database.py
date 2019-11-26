import pandas as pd
from bson import ObjectId
from pymongo import MongoClient
from functions.location import getLocation

def createOfficeDoc(company,office):
    office.update({'company':company['_id']})
    office.update({'location':getLocation(office)})
    del office['latitude']
    del office['longitude']
    return office

def officeDictionary(dictionary):
    #Converts the dictionary coordinates attribute in a list
    dictionary['location'] = [dictionary['location']]
    return dictionary

def initializeDictionary():
    #Initial empty dataframe
    return pd.DataFrame(columns=[])

def officesDataFrame(db,query):
    df = initializeDictionary()
    for company in db['companies'].find(query):
        for office in db['offices'].find({'company':ObjectId(company['_id'])}):
            df = df.append(pd.DataFrame(officeDictionary(office)), ignore_index=True, sort=False)
    return df


def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll
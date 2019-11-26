import pymongo

sphericalQuery = lambda long,lat,radius:{'location': {'$geoWithin': {'$centerSphere':[[long,lat], radius/6371]}}}

def findMinDistance(col,office):
    #Find closest school and starbucks
    c = office['location']['coordinates']
    meters = 0
    found = 0
    while meters < 1000 and not found:
        meters += 5
        found = len(list(col.find(sphericalQuery(c[0],c[1],meters/1000))))
    return meters

def findTenStartups(col,office):
    #Find 10 surrounding startups
    c = office['location']['coordinates']
    meters = 0
    found = False
    while meters < 1000 and not found:
        meters += 5
        found = len(list(col.find(sphericalQuery(c[0],c[1],meters/1000)))) >= 10
    return meters
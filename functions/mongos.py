from functions import googleQuery,getDocFromGoogleQuery

def insertSchoolToMongo(db,dic):
    prop=dic['properties']
    db['schools'].insert_one({
        'type':'Feature',
        'campus_address':prop['campus_address'],
        'campus_name':prop['campus_name'],
        'grade_range':prop['grade_range'],
        'category':prop['category'],
        'location':dic['geometry']
    })

def insertStartUpToMongo(database,serie):
    db['startups'].insert_one({'name':serie.Name, 
                               'Number of employees':serie.Employees, 
                               'Total raised':s['Total Raised']})
    res = googleQuery(serie.Name + ' San Francisco').json()
    if not(res['status'] == 'ZERO_RESULTS'):
        doc = getDocFromGoogleQuery(res['results'][0],'San Francisco')
        db['startups'].update_one({'name':serie.Name},{'$set':doc})
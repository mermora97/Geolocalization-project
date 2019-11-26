import os 

def authorizationKey(key):
    authToken = os.getenv(key)
    if not authToken:
        raise ValueError('A key token is neeeded')
    else:
        print("We have a github token: ", authToken[0:4])
    return authToken
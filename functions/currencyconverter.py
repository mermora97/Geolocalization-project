import requests
import re
import json

multiplyBy = {'M':1, 'B':1000, 'k':1/1000, '':0}
currency = {'$':'USD', '€':'EUR', '£':'GBP', 'C$':'CAD', '¥':'JPY', 'kr':'SEK'}

def currencyConverter(base='EUR',other='USD'):
    url = f'https://api.exchangeratesapi.io/latest?base={base}'
    res = requests.get(url).json()
    return res['rates'][other]
        
def moneyConverter(s):
    multiplier = 1
    currencyConversion = 1
    
    m = re.findall('\D$',s)
    if m:
        multiplier = multiplyBy[m[0]]
        s = s[:-1]
    c = re.findall('^\D+',s)
    if c:
        if c[0] != '$':
            currencyConversion = currencyConverter(currency[c[0]])
        s = s.split(c[0])[1]
    return float(s)*multiplier*currencyConversion
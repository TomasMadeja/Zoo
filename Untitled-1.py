
import requests

API_KEY='dda1cac41829b7815e21389023a25cff'

headers = {'x-api-key' : API_KEY}

USAGE = "https://api.packettotal.com/v1/usage"
URL = "https://api.packettotal.com/v1/search?query={}"
URL_ANALYSIS = "https://api.packettotal.com/v1/pcaps/{}/analysis?accuracy=high"


rr = requests.get(USAGE, headers=headers)

r = requests.get(URL.format('Malicious Activity'), headers=headers)

r_a = requests.get(URL_ANALYSIS.format(_id), headers=headers)
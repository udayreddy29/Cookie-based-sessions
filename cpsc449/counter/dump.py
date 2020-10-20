import sys
import requests
url = sys.argv[1]
details = requests.get(url + '/getDetails')
for key in details.json():
    value = {
        key: details.json().get(key)
    }
    print(value)

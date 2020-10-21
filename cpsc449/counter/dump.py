import sys
import requests


def get_key(url):
    keyValue = requests.get(url)
    return keyValue

url = sys.argv[1]
details = requests.get(url)
keys = details.json().get('keys')
for key in keys:
    requestUrl = url + '/' + key
    p = get_key(requestUrl)
    print(p.json())
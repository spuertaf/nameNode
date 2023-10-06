import requests

url = "http://3.86.15.74:80/list"

body = {
    "payload" : ""
}

response = requests.get(url, json=body)

print(response.text)
import requests

url = "http://3.86.15.74:80/put"

body = {
    "payload" : "/env/data/customer.csv"
}

response = requests.get(url, json=body)

print(response.text)
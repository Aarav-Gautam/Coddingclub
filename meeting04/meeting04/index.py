import requests

api_key = "bf865602931cca9b2264b25aea627389"  # put your regenerated key here
phone = "+9779702433591"

url = f"http://apilayer.net/api/validate?access_key={api_key}&number={phone}"

response = requests.get(url)
data = response.json()

print(data)

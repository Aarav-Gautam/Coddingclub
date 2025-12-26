import requests
url="https://api.github.com/users/Aarav-gautam"
r=requests.get(url)
print(r.text)
with open("f.txt","w")as f:
    f.write(r.text)
# data = r.json()
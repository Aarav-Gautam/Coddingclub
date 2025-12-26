import phonenumbers
from phonenumbers import geocoder

number = phonenumbers.parse("+9779702433591", "NP")
location = geocoder.description_for_number(number, "en")

print("Approximate Region:", location)

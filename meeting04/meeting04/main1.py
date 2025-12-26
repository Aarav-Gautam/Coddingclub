import phonenumbers
from phonenumbers import geocoder, carrier

# Example phone number
number = "+9779702433591"

# Parse the number
phone_number = phonenumbers.parse(number)

# Get region
region = geocoder.description_for_number(phone_number, "en")
print("Region:", region)

# Get carrier
phone_carrier = carrier.name_for_number(phone_number, "en")
print("Carrier:", phone_carrier)

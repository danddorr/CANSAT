import requests
from datetime import datetime

#url = "http://38.242.151.128/set_data/"
url = "http://127.0.0.1:8000/set_data/"

# toto si nahrad svojim stringom
input_str = f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')} 25.0 1000.0 1000.0"

input_parsed = input_str.split()

data = {
    "date_time": input_parsed[0],
    "temperature": float(input_parsed[1]),
    "pressure": float(input_parsed[2]),
    "solar_radiation": float(input_parsed[3]),
    "latitude": 48.6211,
    "longitude": 18.3371,
    "altitude": 1000.0
}

print(data)

response = requests.post(url, data=data)

if response.status_code == 200:
    print("Data sent successfully!", response.text)
else:
    print("Failed to send data. Error:", response.text)
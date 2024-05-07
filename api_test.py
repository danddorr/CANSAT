import requests
from datetime import datetime
import random
from time import sleep

url = "http://127.0.0.1:8000/set_data/"

prev_values = {
    "date_time": "",
    "temperature": 0,
    "pressure": 0,
    "solar_radiation": 0,
    "latitude": 0,
    "longitude": 0,
    "altitude": 0
}
temp_range = (2000,3000)
pressure_range = (85000,105000)
solar_radiation_range = (105000,135000)
latitude_range = (486150,486250)
longitude_range = (183330,183430)
altitude_range = (20000,120000)

def relative_range(sensitivity_percent, range, prev_value):
    sensitivity = int((range[1] - range[0]) * sensitivity_percent / 100)
    new_value = prev_value + random.randint(-sensitivity, sensitivity)
    if new_value < range[0]:
        new_value = range[0]
    elif new_value > range[1]:
        new_value = range[1]
    return new_value

prev_values = {
    "date_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    "temperature": random.randint(temp_range[0], temp_range[1])*0.01,
    "pressure": random.randint(pressure_range[0], pressure_range[1])*0.01,
    "solar_radiation": random.randint(solar_radiation_range[0], solar_radiation_range[1])*0.01,
    "latitude": random.randint(latitude_range[0], latitude_range[1])*0.0001,
    "longitude": random.randint(longitude_range[0], longitude_range[1])*0.0001,
    "altitude": random.randint(altitude_range[0], altitude_range[1])*0.01
}

for i in range(10):
    data = {
        "date_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "temperature": relative_range(20, temp_range, prev_values["temperature"]*100)*0.01,
        "pressure": relative_range(8, pressure_range, prev_values["pressure"]*100)*0.01,
        "solar_radiation": relative_range(8, solar_radiation_range, prev_values["solar_radiation"]*100)*0.01,
        "latitude": relative_range(15, latitude_range, prev_values["latitude"]*10000)*0.0001,
        "longitude": relative_range(15, longitude_range, prev_values["longitude"]*10000)*0.0001,
        "altitude": relative_range(2, altitude_range, prev_values["altitude"]*100)*0.01
    }

    prev_values = data.copy()

    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("Data sent successfully!", response.text)
    else:
        print("Failed to send data. Error:", response.text)
    sleep(1)
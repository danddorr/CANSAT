import requests
from datetime import datetime
import random
from time import sleep

url = "http://127.0.0.1:8000/set_data/"

prev_values = {
    "date_time": "",
    "temperature": 0,
    "pressure": 0,
    "solar_radiation": 0
}
temp_range = (20,30)
pressure_range = (850,1050)
solar_radiation_range = (1050,1350)

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
    "temperature": random.randint(temp_range[0], temp_range[1]),
    "pressure": random.randint(pressure_range[0], pressure_range[1]),
    "solar_radiation": random.randint(solar_radiation_range[0], solar_radiation_range[1]),
}

for i in range(30):
    data = {
        "date_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "temperature": relative_range(20, temp_range, prev_values["temperature"]),
        "pressure": relative_range(8, pressure_range, prev_values["pressure"]),
        "solar_radiation": relative_range(8, solar_radiation_range, prev_values["solar_radiation"]),
    }

    prev_values = data.copy()

    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("Data sent successfully!", response.text)
    else:
        print("Failed to send data. Error:", response.text)
    sleep(1)
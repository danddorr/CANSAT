import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import requests
from matplotlib.dates import MinuteLocator

# Get data from the API
url = "http://38.242.151.128/charts_in_range/2024-05-09T12:15:10/2024-05-09T12:29:01/"

response = requests.get(url)

'''data = {
  "x_data": [
    "2024-05-09 10:35:15",
    "2024-05-09 10:35:13",
    "2024-05-09 10:35:12",
    "2024-05-09 10:35:11",
    "2024-05-09 10:35:10",
    "2024-05-09 10:35:09",
    "2024-05-09 10:35:08",
    "2024-05-09 10:35:06",
    "2024-05-09 10:35:05",
    "2024-05-09 10:35:04"
  ],
  "charts_data": [
    [27.35, 27.59, 26.22, 24.49, 22.84, 23.77, 21.82, 22.47, 20.91, 22.31],
    [980.58, 986.4, 972.3, 967.1, 969.37, 966.38, 959.04, 954.61, 943.29, 948.42],
    [1134.26, 1150.12, 1130.94, 1110.63, 1133.07, 1133.31, 1112.92, 1123.89, 1133.71, 1112.8],
    [334.1, 325.38, 319.73, 303.75, 305.8, 323.06, 328.46, 327.06, 313.08, 301.84]
  ],
  "coords": [
    [48.6159, 18.3391],
    [48.6159, 18.3391],
    [48.6153, 18.3397],
    [48.615, 18.3388],
    [48.6157, 18.3375],
    [48.6165, 18.3381],
    [48.6169, 18.3371],
    [48.6166, 18.3384],
    [48.6164, 18.3398],
    [48.6162, 18.3392]
  ]
}'''

data_response = response.json()

data = {
    "date_time": [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in data_response["x_data"]],
    "temperature": data_response["charts_data"][0],
    "pressure": data_response["charts_data"][1],
    "solar_radiation": data_response["charts_data"][2],
    "altitude": data_response["charts_data"][3],
    "latitude": [coord[0] for coord in data_response["coords"]],
    "longitude": [coord[1] for coord in data_response["coords"]]
}

"""print(sum(data["temperature"])/len(data["temperature"]))
print(sum(data["pressure"])/len(data["pressure"]))
print(sum(data["solar_radiation"])/len(data["solar_radiation"]))
exit()"""
# Create figure and subplots
fig, axs = plt.subplots(3, figsize=(10, 15))

# Plot altitude vs temperature, pressure, solar radiation
"""axs[0].plot(data["temperature"], data["altitude"], label="Temperature")
axs[0].plot(data["pressure"], data["altitude"], label="Pressure")
axs[0].plot(data["solar_radiation"], data["altitude"], label="Solar Radiation")
axs[0].set_xlabel("Altitude")
axs[0].legend()
axs[0].xaxis.set_tick_params(rotation=20)"""

# Plot time vs temperature, pressure, solar radiation
axs[0].plot(data["date_time"],data["temperature"], label="Temperature")
axs[0].set_xlabel("Time")
axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
axs[0].xaxis.set_major_locator(MinuteLocator(interval=1))  # Set major ticks every 10 minutes
axs[0].legend()
axs[0].xaxis.set_tick_params(rotation=20)

axs[1].plot(data["date_time"], data["pressure"], label="Pressure")
axs[1].set_xlabel("Time")
axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
axs[1].xaxis.set_major_locator(MinuteLocator(interval=1))  # Set major ticks every 10 minutes
axs[1].legend()
axs[1].xaxis.set_tick_params(rotation=20)

axs[2].plot(data["date_time"], data["solar_radiation"], label="Solar Radiation")
axs[2].set_xlabel("Time")
axs[2].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
axs[2].xaxis.set_major_locator(MinuteLocator(interval=1))  # Set major ticks every 10 minutes
axs[2].legend()
axs[2].xaxis.set_tick_params(rotation=20)

"""
# Plot time vs altitude
axs[2].plot(data["date_time"], data["altitude"])
axs[2].set_xlabel("Time")
axs[2].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
axs[2].xaxis.set_tick_params(rotation=20)
"""
# Save the figure as a PNG file
plt.savefig("graphs.png")
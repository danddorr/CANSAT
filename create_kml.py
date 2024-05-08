from xml.dom.minidom import Document
from datetime import datetime
import requests

def create_kml(coords, altitudes, times, output_file):
    doc = Document()

    # Create KML structure
    kml = doc.createElementNS('http://www.opengis.net/kml/2.2', 'kml')
    doc.appendChild(kml)
    document = doc.createElement('Document')
    kml.appendChild(document)

    # Create style for the points
    style = doc.createElement('Style')
    style.setAttribute('id', 'pointStyle')
    icon_style = doc.createElement('IconStyle')
    icon = doc.createElement('Icon')
    href = doc.createElement('href')
    # Set the URL to your custom icon image
    href_text = doc.createTextNode('https://cdn.discordapp.com/attachments/1195836694688178227/1225718419270402180/can_zeppelin_no_bg.png?ex=663b32bb&is=6639e13b&hm=41a021910473ecbb0a2cea827ece3d0f078f1ee537795f5e4d24c6e9d94500e1&')  # URL to custom icon image
    href.appendChild(href_text)
    icon.appendChild(href)
    icon_style.appendChild(icon)
    style.appendChild(icon_style)
    document.appendChild(style)

    initial_time = times[0]

    # Create points
    for coord, alt, time in zip(coords, altitudes, times):
        point = doc.createElement('Placemark')
        document.appendChild(point)
        
        # Add style for the point
        style_url = doc.createElement('styleUrl')
        style_url_text = doc.createTextNode('#pointStyle')
        style_url.appendChild(style_url_text)
        point.appendChild(style_url)
        
        # Convert time to elapsed seconds
        time_diff = datetime.strptime(initial_time, "%Y-%m-%dT%H:%M:%S") - datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
        time_seconds = int(time_diff.total_seconds())

        # Add name
        name = doc.createElement('name')
        name_text = doc.createTextNode(f"{time_seconds}s")
        name.appendChild(name_text)
        point.appendChild(name)
        
        # Add altitude
        altitude = doc.createElement('altitude')
        altitude_text = doc.createTextNode(str(alt))
        altitude.appendChild(altitude_text)
        point.appendChild(altitude)

        # Add altitude mode
        altitude_mode = doc.createElement('altitudeMode')
        altitude_mode_text = doc.createTextNode('absolute')
        altitude_mode.appendChild(altitude_mode_text)
        point.appendChild(altitude_mode)
        
        # Add timestamp
        timestamp = doc.createElement('TimeStamp')
        when = doc.createElement('when')
        when_text = doc.createTextNode(time)
        when.appendChild(when_text)
        timestamp.appendChild(when)
        point.appendChild(timestamp)

        # Add coordinates
        coords_elem = doc.createElement('Point')
        point.appendChild(coords_elem)
        altitudeMode = doc.createElement('altitudeMode')
        altitudeMode_text = doc.createTextNode('absolute')
        altitudeMode.appendChild(altitudeMode_text)
        coordinates = doc.createElement('coordinates')
        coordinates_text = doc.createTextNode(f"{coord[1]},{coord[0]},{alt}")  # Google Earth expects longitude,latitude
        coordinates.appendChild(coordinates_text)
        coords_elem.appendChild(altitudeMode)
        coords_elem.appendChild(coordinates)

    # Write to file
    with open(output_file, 'w') as f:
        f.write(doc.toprettyxml(indent="  "))

# Example usage
coords = [
    (48.6828, 17.6384),  # Starting point: Male Bielice, Slovakia
    (48.6830, 17.6390),
    (48.6832, 17.6395),
    (48.6834, 17.6400),
    (48.6836, 17.6405),
    (48.6838, 17.6410),
    (48.6840, 17.6415),
    (48.6842, 17.6420),
    (48.6844, 17.6425),
    (48.6846, 17.6430),
    (48.6848, 17.6435),
    (48.6850, 17.6440),
    (48.6852, 17.6445),
    (48.6854, 17.6450),
    (48.6856, 17.6455),
]  # List of (longitude, latitude) tuples
altitudes = [
    0,  # Starting altitude
    100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,  # Ascend to 1000 meters
    900, 800, 700, 600, 500, 400, 300, 200, 100, 0  # Descend back to ground
]  # List of altitudes
times = [
    "2024-05-07T08:00:00",  # Dummy time for start
    "2024-05-07T08:01:00",
    "2024-05-07T08:02:00",
    "2024-05-07T08:03:00",
    "2024-05-07T08:04:00",
    "2024-05-07T08:05:00",
    "2024-05-07T08:06:00",
    "2024-05-07T08:07:00",
    "2024-05-07T08:08:00",
    "2024-05-07T08:09:00",
    "2024-05-07T08:10:00",  # Dummy time for reaching max altitude
    "2024-05-07T08:11:00",
    "2024-05-07T08:12:00",
    "2024-05-07T08:13:00",
    "2024-05-07T08:14:00",
    "2024-05-07T08:15:00",
    "2024-05-07T08:16:00",
    "2024-05-07T08:17:00",
    "2024-05-07T08:18:00",
    "2024-05-07T08:19:00",
    "2024-05-07T08:20:00",  # Dummy time for end
]  # List of times

### Data from the Django app
def get_data():
    #url = "http://127.0.0.1:8000/get_charts_data/10/"
    url = "http://127.0.0.1:8000/charts_in_range/2024-05-08T00:05:00/2024-05-08T00:57:00/"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        times = data['x_data']
        times = [i.replace(' ', 'T') for i in times]

        altitudes = data['charts_data'][3]

        coords = data['coords']

        return coords, altitudes, times

output_file = 'flight_path.kml'  # Output file name

data = get_data()
#print(data)

create_kml(*data, output_file)
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from .models import RealTimeData
from datetime import datetime
#from plotly.offline import plot
#from plotly.graph_objs import Scatter

def index(request): 
    return render(request, "index.html")

def get_charts_data(request, amount):
    all_data = list(reversed(RealTimeData.objects.all().order_by('date_time')))[:amount]
    
    x_data = []
    y_data_temp = []
    y_data_pressure = []
    y_data_solar_radiation = []
    y_data_altitude = []
    data_gps = []

    for data in all_data:
        x_data.append(data.date_time.strftime('%Y-%m-%d %H:%M:%S'))
        y_data_temp.append(data.temperature)
        y_data_pressure.append(data.pressure)
        y_data_solar_radiation.append(data.solar_radiation/220)
        y_data_altitude.append(data.altitude)
        data_gps.append([data.latitude, data.longitude])

    return JsonResponse({'x_data': x_data, 'charts_data': [y_data_temp, y_data_pressure, y_data_solar_radiation, y_data_altitude], 'coords': data_gps})

def get_charts_data_in_range(request, start_date, end_date):
    all_data = list(reversed(RealTimeData.objects.filter(date_time__range=[start_date, end_date]).order_by('date_time')))
    
    x_data = []
    y_data_temp = []
    y_data_pressure = []
    y_data_solar_radiation = []
    y_data_altitude = []
    data_gps = []

    for data in all_data:
        x_data.append(data.date_time.strftime('%Y-%m-%d %H:%M:%S'))
        y_data_temp.append(data.temperature)
        y_data_pressure.append(data.pressure)
        y_data_solar_radiation.append(data.solar_radiation)
        y_data_altitude.append(data.altitude)
        data_gps.append([data.latitude, data.longitude])

    return JsonResponse({'x_data': x_data, 'charts_data': [y_data_temp, y_data_pressure, y_data_solar_radiation, y_data_altitude], 'coords': data_gps})


@csrf_exempt # disable csrf
def set_data(request):
    if request.method == 'POST':
        try:
            datetime_post = request.POST['date_time']
            temperature_post = request.POST['temperature']
            pressure_post = request.POST['pressure']
            solar_radiation_post = request.POST['solar_radiation']
            latitude_post = request.POST['latitude']
            longitude_post = request.POST['longitude']
            altitude_post = request.POST['altitude']
        except:
            print('Error getting POST data')
            return JsonResponse({'status': 'fail', 'error': 'Error getting POST data'})

        if not datetime_post or not temperature_post or not solar_radiation_post or not pressure_post or not latitude_post or not longitude_post or not altitude_post:
            print('Empty POST data')
            return JsonResponse({'status': 'fail', 'error': 'Empty POST data'})

        datetime_obj = datetime.strptime(datetime_post, '%Y-%m-%dT%H:%M:%S')

        temperature = float(temperature_post)
        pressure = float(pressure_post)
        solar_radiation = float(solar_radiation_post)
        latitude = float(latitude_post)
        longitude = float(longitude_post)
        altitude = float(altitude_post)

        RealTimeData.objects.create(date_time=datetime_obj, temperature=temperature, solar_radiation=solar_radiation, pressure=pressure, latitude=latitude, longitude=longitude, altitude=altitude)
        return JsonResponse({'status': 'success'})
    
    print('Not a POST request')
    return JsonResponse({'status': 'fail', 'error': 'Not a POST request'})
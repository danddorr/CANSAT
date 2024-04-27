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
    x_data = [data.date_time for data in all_data]
    y_data_temp = [data.temperature for data in all_data]
    y_data_humidity = [data.humidity for data in all_data]
    y_data_pressure = [data.pressure for data in all_data]

    x_data = [x.strftime('%Y-%m-%d %H:%M:%S') for x in x_data]

    return JsonResponse({'x_data': x_data, 'charts_data': [y_data_temp, y_data_humidity, y_data_pressure]})

@csrf_exempt # disable csrf
def set_data(request):
    if request.method == 'POST':
        try:
            datetime_post = request.POST['date_time']
            temperature_post = request.POST['temperature']
            humidity_post = request.POST['humidity']
            pressure_post = request.POST['pressure']
        except:
            print('Error getting POST data')
            return JsonResponse({'status': 'fail', 'error': 'Error getting POST data'})

        if not datetime_post or not temperature_post or not humidity_post or not pressure_post:
            print('Empty POST data')
            return JsonResponse({'status': 'fail', 'error': 'Empty POST data'})

        datetime_obj = datetime.strptime(datetime_post, '%Y-%m-%dT%H:%M:%S')

        temperature = float(temperature_post)
        humidity = float(humidity_post)
        pressure = float(pressure_post)

        RealTimeData.objects.create(date_time=datetime_obj, temperature=temperature, humidity=humidity, pressure=pressure)
        return JsonResponse({'status': 'success'})
    
    print('Not a POST request')
    return JsonResponse({'status': 'fail', 'error': 'Not a POST request'})
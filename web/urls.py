from django.urls import path
from .views import index, get_charts_data, set_data, get_charts_data_in_range

urlpatterns = [
    path('', index, name='index'),
    path('get_charts_data/<int:amount>/', get_charts_data, name='get_charts_data'),
    path('charts_in_range/<str:start_date>/<str:end_date>/', get_charts_data_in_range, name='get_charts_data_in_range'),
    path('set_data/', set_data, name='set_data'),
]
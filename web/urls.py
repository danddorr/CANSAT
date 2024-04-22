from django.urls import path
from .views import index, get_charts_data, set_data

urlpatterns = [
    path('', index, name='index'),
    path('get_charts_data/', get_charts_data, name='get_charts_data'),
    path('set_data/', set_data, name='set_data'),
]
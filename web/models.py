from django.db import models

class RealTimeData(models.Model):
    date_time = models.DateTimeField()
    temperature = models.FloatField(default = 0)
    pressure = models.FloatField(default = 0)
    solar_radiation = models.FloatField(default = 0)
    latitude = models.FloatField(default = 0)
    longitude = models.FloatField(default = 0)
    altitude = models.FloatField(default = 0)

    def __str__(self):
        return str(self.date_time) + ' ' + str(self.temperature)
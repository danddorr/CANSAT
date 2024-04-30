from django.db import models

class RealTimeData(models.Model):
    date_time = models.DateTimeField()
    temperature = models.FloatField(default = 0)
    pressure = models.FloatField(default = 0)
    solar_radiation = models.FloatField(default = 0)
    #altitude = models.FloatField()

    def __str__(self):
        return str(self.date_time) + ' ' + str(self.temperature)
from django.db import models


# Create your models here.
# Sensor 資料
class Sensor(models.Model):
    sensor_id = models.CharField(u'測點編號', max_length=50, unique=True)
    name = models.CharField(u'測點名稱', max_length=50)
    location = models.CharField(u'測點位置', max_length=100)
    type = models.CharField(u'感測器類型', max_length=50)
    SensorPM = models.CharField(u'懸浮微粒感測器型號', max_length=50)
    SensorEnv = models.CharField(u'溫溼度感測器型號', max_length=50)
    SensorCO2 = models.CharField(u'二氧化碳感測器型號', max_length=50)
    online = models.BooleanField()

    def __str__(self):  # __unicode__ for Python 2, use __str__ on Python 3
        return self.sensor_id

    class Meta:
        ordering = ['sensor_id', 'name', 'type', 'location']


class EnvironmentData(models.Model):
    sensor_id = models.ForeignKey(Sensor)
    name = models.CharField(u'感測器名稱', max_length=50, default="")
    date = models.DateField()
    time = models.TimeField()
    temperature = models.FloatField(u"攝氏溫度(°C)")
    humidity = models.FloatField(u"濕度(%)")
    HeatIndex = models.FloatField(u"熱指數")

    def __str__(self): # __unicode__ for Python 2, use __str__ on Python 3
        return self.name

    class Meta:
        ordering = ['sensor_id', 'date', 'time']


class CarbonDioxideData(models.Model):
    sensor_id = models.ForeignKey(Sensor)
    name = models.CharField(u'感測器名稱', max_length=50, default="")
    date = models.DateField()
    time = models.TimeField()
    concentration = models.FloatField(u"濃度(ppm)")

    def __str__(self):  # __unicode__ for Python 2, use __str__ on Python 3
        return self.name

    class Meta:
        ordering = ['sensor_id', 'date', 'time']


class ParticleMatterData(models.Model):
    sensor_id = models.ForeignKey(Sensor)
    name = models.CharField(u'感測器名稱', max_length=50, default="")
    date = models.DateField()
    time = models.TimeField()
    pm010_TSI = models.FloatField(u"標準顆粒 PM 1 濃度(ug/m3)")
    pm025_TSI = models.FloatField(u"標準顆粒 PM 2.5 濃度(ug/m3)")
    pm100_TSI = models.FloatField(u"標準顆粒 PM 10 濃度(ug/m3)")
    pm010_ATM = models.FloatField(u"大氣環境 PM 1 濃度(ug/m3)")
    pm025_ATM = models.FloatField(u"大氣環境 PM 2.5 濃度(ug/m3)")
    pm100_ATM = models.FloatField(u"大氣環境 PM 10 濃度(ug/m3)")

    def __str__(self):  # __unicode__ for Python 2, use __str__ on Python 3
        return self.name

    class Meta:
        ordering = ['sensor_id', 'date', 'time']


class ParticleNumberData(models.Model):
    sensor_id = models.ForeignKey(Sensor)
    name = models.CharField(u'感測器名稱', max_length=50, default="")
    date = models.DateField()
    time = models.TimeField()
    Diameter_003 = models.FloatField(u"粒徑 0.3μm(count)")
    Diameter_005 = models.FloatField(u"粒徑 0.5μm(count)")
    Diameter_010 = models.FloatField(u"粒徑 0.1μm(count)")
    Diameter_025 = models.FloatField(u"粒徑 2.5μm(count)")
    Diameter_050 = models.FloatField(u"粒徑 5.0μm(count)")
    Diameter_100 = models.FloatField(u"粒徑10.0μm(count)")

    def __str__(self):  # __unicode__ for Python 2, use __str__ on Python 3
        return self.name

    class Meta:
        ordering = ['sensor_id', 'date', 'time']

from django.contrib import admin
from MQTT.models import Sensor, EnvironmentData, CarbonDioxideData,ParticleMatterData, ParticleNumberData


# Register your models here.
class SensorList(admin.ModelAdmin):
    list_display = ('sensor_id', 'name', 'type', 'location')


class EnvironmentList(admin.ModelAdmin):
    list_display = ('sensor_id', 'date', 'time', 'temperature', 'humidity', 'HeatIndex')


class CarbonDioxideList(admin.ModelAdmin):
    list_display = ('sensor_id', 'date', 'time', 'concentration')


class ParticleMatterList(admin.ModelAdmin):
    list_display = ('sensor_id', 'date', 'time', 'pm100_ATM', 'pm025_ATM',
                    'pm010_ATM', 'pm100_TSI', 'pm025_TSI', 'pm010_TSI')


class ParticleNumberList(admin.ModelAdmin):
    list_display = ('sensor_id', 'date', 'time', 'Diameter_100', 'Diameter_050',
                    'Diameter_025', 'Diameter_010', 'Diameter_005', 'Diameter_003')


admin.site.register(Sensor, SensorList)
admin.site.register(EnvironmentData, EnvironmentList)
admin.site.register(CarbonDioxideData, CarbonDioxideList)
admin.site.register(ParticleMatterData, ParticleMatterList)
admin.site.register(ParticleNumberData, ParticleNumberList)


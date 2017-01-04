from django.shortcuts import render
from django.shortcuts import HttpResponse
from MQTT.models import Sensor, EnvironmentData, ParticleMatterData

'''
學習筆記：
 * views.py用來撈資料
 * 撈好的資料放在dict中：{'網頁裡的tag名稱': 變數名稱, }
'''


# Create your views here.
def index(request):
    test = Sensor.objects.all()
    sensor = Sensor.objects.get(sensor_id='Sensor_7688Duo')
    pm = ParticleMatterData.objects.all().reverse()[:10]
    return render(request, 'MQTT/index.html', {'sensor': sensor, 'test': test, 'PM': pm})
#   return HttpResponse("Hi my system! 施工中")

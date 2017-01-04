from django.shortcuts import render
from django.shortcuts import HttpResponse
from MQTT.models import Sensor
import time


# Create your views here.
def index(request):
    return render(request, 'MQTT/index.html')
#   return HttpResponse("Hi my system! 施工中")

localtime = time.asctime(time.localtime(time.time()))
print('this is  view.py at {0}'.format(localtime))

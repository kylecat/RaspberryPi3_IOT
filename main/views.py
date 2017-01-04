from django.shortcuts import render
from django.shortcuts import HttpResponse
import time


# Create your views here.
def index(request):
    return render(request, 'main/index.html')
#   return HttpResponse("Hi my system! 施工中")

localtime = time.asctime(time.localtime(time.time()))
print('this is  view.py at {0}'.format(localtime))

from django.shortcuts import render
from django.http import HttpResponse
from . import views
from time import sleep
from decimal import Decimal
import RPi.GPIO as GPIO
import dht11

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def ajax_test(request):
    if is_ajax(request=request):
        message = "This is ajax"
    else:
        message = "Not ajax"
    return HttpResponse(message)
    

def index(request):
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)  #setup gpio number mode to BCM
	pin = 18
	data1 = dht11.DHT11(18)		
	getResult = data1.read()  #get GPIO data
	temperature = 0
	humidity = 0
	if getResult.is_valid:
		if 0 == getResult.temperature and 0 == getResult.humidity :
			pass
		else:
			temperature = getResult.temperature
			humidity = getResult.humidity
			#print("temperature= ", temperature )
			#print("humidity= ", humidity)
	else :
		print("error= ", getResult.error_code)	
	#print("request=", request.method)
	if is_ajax(request):  # 判断是否是ajax请求
		if request.method == 'POST':
			print("temperature=", temperature)
			print("humidity=", humidity)
			sdata = []
			sdata.append(temperature)
			sdata.append("/")  # add this so that can split string easily
			sdata.append(humidity)  # you will get a string(sdata) like "27.1/50.0"
			return HttpResponse(sdata)
		else:
			return render(request, 'index.html')

	return render(request, "index.html")


from django.shortcuts import render
from django.http import JsonResponse
from time import sleep
import routeros_api
import json
import environ
import time
# Create your views here.


def hotspot_active(request):
    env = environ.Env()
    environ.Env.read_env()
    host = '192.168.1.1'
    user = env('USER_MIKROTIK')
    passwordmikrotik = env('PASS_MIKROTIK')

    connetion = routeros_api.RouterOsApiPool(
        host, username=user, password=passwordmikrotik, port=64991, plaintext_login=True)
    api = connetion.get_api()

    list_ipadd = api.get_resource('ip/hotspot/active')
    show_ipadd = list_ipadd.get()

    data = {
        "isUser": False,
        "response": show_ipadd,
    }
    return JsonResponse(data)

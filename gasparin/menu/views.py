# menu
import os
import json
from django.http import HttpResponse
from django.shortcuts import render
from gasparin.settings import BASE_DIR

def menu_view(request):
    return render(request, 'menu.html')

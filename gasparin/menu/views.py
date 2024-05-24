# menu
import os
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from gasparin.settings import BASE_DIR

JSON_FILE_PATH = os.path.join(BASE_DIR, 'video_processing', 'yolomodels', 'config.json')

def get_menu_options():
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r') as file:
            return json.load(file)
    return {"task": "", "model": "", "visual": ""}

def save_menu_options(data):
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file)

def menu_view(request):
    if request.method == 'POST':
        task = request.POST.get('task', '')
        model = request.POST.get('model', '')
        visual = request.POST.get('visual', '')

        # Load current menu options from JSON file
        menu_options = get_menu_options()

        # Update menu options
        if task:
            menu_options['task'] = task
        if model:
            menu_options['model'] = model
        if visual:
            menu_options['visual'] = visual
        
        save_menu_options(menu_options)

        return redirect('stream')

    elif request.method == 'GET':
        # Renderizar el formulario de registro con GET
        return render(request, 'menu.html')
# register_logic.py

from django.shortcuts import render, redirect
import os
import json
from django.http import HttpResponse
from gasparin.settings import BASE_DIR

def register_view(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Obtener la ruta completa al archivo users.json dentro del directorio static
        file_path = os.path.join(BASE_DIR, 'register', 'static', 'users.json')

        try:
            # Abrir el archivo JSON
            with open(file_path, 'r') as f:
                users = json.load(f)['users']
            
            # Verificar si el usuario ya existe
            for user in users:
                if user['username'] == username:
                    return HttpResponse("El nombre de usuario ya está en uso.")
            
            # Si el usuario no existe, agregarlo al archivo JSON
            users.append({'username': username, 'password': password})
            with open(file_path, 'w') as f:
                json.dump({'users': users}, f, indent=4)
            
            # Redirigir a la página de inicio de sesión
            return redirect('login')
        except FileNotFoundError:
            # Manejar el caso en el que el archivo no se pueda encontrar
            print("Error: El archivo users.json no se encontró en la ruta:", file_path)
            return HttpResponse("Error: El archivo users.json no se encontró.")
    elif request.method == 'GET':
        # Renderizar el formulario de registro con GET
        return render(request, 'register.html')

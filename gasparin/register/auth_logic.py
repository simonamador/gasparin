# auth_logic.py

import os
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from gasparin.settings import BASE_DIR

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Obtener la ruta completa al archivo users.json dentro del directorio static
        file_path = os.path.join(BASE_DIR, 'register', 'static', 'users.json')

        try:
            # Abrir el archivo JSON
            with open(file_path, 'r') as f:
                users = json.load(f)['users']
            
            # Verificar las credenciales del usuario
            for user in users:
                if user['username'] == username and user['password'] == password:
                    # Redirigir al menú después del inicio de sesión exitoso
                    return redirect('menu')

            # Si no se encuentra el usuario o la contraseña es incorrecta, mostrar un mensaje de error
            return HttpResponse("Nombre de usuario o contraseña incorrectos.")
        except FileNotFoundError:
            # Manejar el caso en el que el archivo no se pueda encontrar
            print("Error: El archivo users.json no se encontró en la ruta:", file_path)
            return HttpResponse("Error: El archivo users.json no se encontró.")
    elif request.method == 'GET':
        # Renderizar el formulario de inicio de sesión
        return render(request, 'login.html')

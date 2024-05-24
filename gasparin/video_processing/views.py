from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse
from video_processing.camera import VideoCamera, Live_from_Video
from gasparin.settings import BASE_DIR

import os
import json

JSON_FILE_PATH = os.path.join(BASE_DIR, 'video_processing', 'yolomodels', 'config.json')

def get_menu_options():
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r') as file:
            return json.load(file)
    return {"task": "", "model": "", "visual": ""}

# Create your views here.
def index(request):
	menu_options = get_menu_options()
	return render(request, 'video_processing/index.html',  {'menu_options': menu_options})

def gen(camera):
	while True:
		frame, legend = camera.get_frame()
		yield (b'--frame\r\n'
					b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')	

def legend_gen(camera):
	while True:
		frame, legend = camera.get_frame()
		yield (b'--frame\r\n'
		 			b'Content-Type: image/jpeg\r\n\r\n' + legend + b'\r\n\r\n')
		
def live_video_feed(request):
	return StreamingHttpResponse(gen(Live_from_Video()),
					content_type='multipart/x-mixed-replace; boundary=frame')

def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')

def legend_feed(request):
	return StreamingHttpResponse(legend_gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')

def legend_live(request):
	return StreamingHttpResponse(legend_gen(Live_from_Video()),
					content_type='multipart/x-mixed-replace; boundary=frame')
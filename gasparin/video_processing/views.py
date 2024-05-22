from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse
from video_processing.camera import VideoCamera, Live_from_Video

# Create your views here.
def index(request):
	return render(request, 'video_processing/index.html')

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
import cv2
import pyopencl as cl
import numpy as np
import os
from video_processing.yolomodels import ICSI_detect
from threading import Thread
from time import sleep
from  gasparin.settings import BASE_DIR
import json


# Initialize OpenCL context and queue
platforms = cl.get_platforms()
# Select the first platform and the first GPU device
platform = platforms[0]
device = platform.get_devices()[0]
context = cl.Context([device])
queue = cl.CommandQueue(context)


class Live_from_Video(object):
	def __init__(self):
		self.video = cv2.VideoCapture(1)
		self.model = ICSI_detect.ICSI_detect()
		self.device = device

		JSON_FILE_PATH = os.path.join(BASE_DIR, 'video_processing', 'yolomodels', 'config.json')
		if os.path.exists(JSON_FILE_PATH):
			with open(JSON_FILE_PATH, 'r') as file:
				settings = json.load(file)
				self.TASK_ID = settings['task']
		else:
			self.TASK_ID = 'ICSI'
		sleep(1)


	def __del__(self):
		self.video.release()

	def get_frame(self):
		if not self.video.isOpened():
			raise IOError("Cannot open webcam")
		success, image = self.video.read()
		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
		# so we must encode it into JPEG in order to correctly display the
		# video stream.
		if self.TASK_ID == 'Inmovilizar esperma':
			n_img, legend = self.model.sperm_selector(image)
		else:
			n_img, legend = self.model.ICSI_annotation(image)
		frame_flip = cv2.flip(n_img,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		ret, leg_jpeg = cv2.imencode('.jpg', legend)
		return jpeg.tobytes(), leg_jpeg.tobytes()

class VideoCamera(object):
	def __init__(self):
		self.model = ICSI_detect.ICSI_detect()
		self.device = device
		JSON_FILE_PATH = os.path.join(BASE_DIR, 'video_processing', 'yolomodels', 'config.json')
		if os.path.exists(JSON_FILE_PATH):
			with open(JSON_FILE_PATH, 'r') as file:
				settings = json.load(file)
				self.TASK_ID = settings['task']
		else:
			self.TASK_ID = 'ICSI'

		if self.TASK_ID == 'Inmovilizar esperma':
			self.url = cv2.VideoCapture('video_processing/videos/ICSI4.mp4')
		else:
			self.url = cv2.VideoCapture('video_processing/videos/ICSI3.mp4')
				
		self.url.set(cv2.CAP_PROP_FPS, 10)
		self.frame = 0

		self.FPS = 15
		# Start frame retrieval thread
		self.thread = Thread(target=self.update, args=())
		self.thread.daemon = True
		self.thread.start()
		sleep(1)

	def __del__(self):
		cv2.destroyAllWindows()

	def update(self):
		self.img, self.legend = 0,0
		counter = 0
		while True:
			if self.url.isOpened():
				success, frame = self.url.read()
				if not success:
					break
				counter +=1
				if counter % self.FPS == 0:
					if self.TASK_ID == 'Inmovilizar esperma':
						self.img, self.legend = self.model.sperm_selector(frame)
					else:
						self.img, self.legend = self.model.ICSI_annotation(frame)
			else:
				self.img, self.legend = 0, 0

	def get_frame(self):
		import numpy as np
		resize = cv2.resize(self.img, (640, 480), interpolation = cv2.INTER_LINEAR) 
		ret, jpeg = cv2.imencode('.jpg', resize)
		ret, leg_jpeg = cv2.imencode('.jpg', self.legend)
		return jpeg.tobytes(), leg_jpeg.tobytes()
		# else:
		# 	ret, jpeg = cv2.imencode('.jpg', np.zeros((480, 640)))
		# 	return jpeg.tobytes(), None

# Helper function to create an OpenCL buffer from a numpy array
def create_cl_buffer(context, array, flags=cl.mem_flags.READ_WRITE):
    return cl.Buffer(context, flags | cl.mem_flags.COPY_HOST_PTR, hostbuf=array)
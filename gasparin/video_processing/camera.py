import cv2
import os
from video_processing.yolomodels import ICSI_detect
from threading import Thread
import time

class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success, image = self.video.read()
		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
		# so we must encode it into JPEG in order to correctly display the
		# video stream.
		n_img, legend = self.model.ICSI_annotation(image)
		frame_flip = cv2.flip(n_img,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes(), legend

class LiveWebCam(object):
	def __init__(self):
		self.model = ICSI_detect.ICSI_detect()

		self.url = cv2.VideoCapture('video_processing/videos/ICSI4.mp4')
		
		print(self.url.get(cv2.CAP_PROP_FPS))
		
		self.url.set(cv2.CAP_PROP_FPS, 10)
		self.frame = 0

		self.FPS = 15
		# Start frame retrieval thread
		self.thread = Thread(target=self.update, args=())
		self.thread.daemon = True
		self.thread.start()

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
					self.img, self.legend = self.model.sperm_selector(frame)
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
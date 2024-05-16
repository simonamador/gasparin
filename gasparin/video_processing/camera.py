import cv2
import torch
import os
from video_processing.yolomodels import ICSI_detect

class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)
		self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

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
		self.url = cv2.VideoCapture('video_processing/videos/ICSI3.mp4')
		self.model = ICSI_detect.ICSI_detect()
		self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

	def __del__(self):
		cv2.destroyAllWindows()

	def get_frame(self):
		import numpy as np
		success,imgNp = self.url.read()
		if success:
			n_img, legend = self.model.ICSI_annotation(imgNp)
			resize = cv2.cuda.resize(n_img, (640, 480), interpolation = cv2.INTER_LINEAR) 
			ret, jpeg = cv2.imencode('.jpg', resize)
			return jpeg.tobytes(), legend
		else:
			ret, jpeg = cv2.imencode('.jpg', np.zeros((480, 640)))
			return jpeg.tobytes(), None
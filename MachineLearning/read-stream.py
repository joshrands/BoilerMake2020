import cv2
import urllib.request
import numpy as np

stream = urllib.request.urlopen('http://192.168.1.114:8000/stream.mjpg')
raw_bytes = ''.encode()
while True:
	raw_bytes += stream.read(1024)
	a = raw_bytes.find('\xff\xd8'.encode())
	b = raw_bytes.find('\xff\xd9'.encode())
	if a != -1 and b != -1:
		jpg = raw_bytes[a:b+2]
		raw_bytes = raw_bytes[b+2:]
		i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
		print(i)
		cv2.imshow('i', i)
		if (cv2.waitKey(1) == 27):
			exit(0)



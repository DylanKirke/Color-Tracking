import numpy as np
import wiringpi as wp
import cv2 as cv
import RPi.GPIO as GPIO
import sys
import time
import imutils

# gpio setup

mode = GPIO.getmode()

flag = 1;
f1 = 37
b1 = 38
f2 = 35
b2 = 36

GPIO.setmode(GPIO.BOARD)
GPIO.setup(f1, GPIO.OUT)
GPIO.setup(b1, GPIO.OUT)
GPIO.setup(f2, GPIO.OUT)
GPIO.setup(b2, GPIO.OUT)

#GPIO functions
def forward():
	print("forward")
	GPIO.output(f1, GPIO.HIGH)
	GPIO.output(f2, GPIO.HIGH)


def left():
	print("left")
	GPIO.output(f1, GPIO.HIGH)
	GPIO.output(f2, GPIO.LOW)

def right():
	print("RIGHT")
	GPIO.output(f1, GPIO.LOW)
	GPIO.output(f2, GPIO.HIGH)

def stop():
	print("stopping")
	GPIO.output(f1, GPIO.LOW)
	GPIO.output(f2, GPIO.LOW)


video_capture = cv.VideoCapture(0)
video_capture.set(3, 160)
video_capture.set(4, 120)

while(True):
	# Capture the frames

	(ret, frame) = video_capture.read()

	#resize image
	frame = imutils.resize(frame, width=600)

	#convert to hsv
	hsv = cv.cvtColor(frame,  cv.COLOR_BGR2HSV)

	#binary thresholding to locate green
	mask = cv.inRange(hsv, (44,54,63), (63, 255, 255))

	#smooth out edges to reduce nosie
	mask = cv.erode(mask, None, iterations=5)
	mask = cv.dilate(mask, None, iterations=5)

	#display live feed to screen - comment out when run on pi.
	cv.imshow("ds", mask)
	if cv.waitKey(1) & 0xFF == ord('q'):
		break
	contour = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	if len(contour) > 0:

		c = max(contour, key=cv.contourArea)
		((x,y), radius) =cv.minEnclosingCircle(c)
		M = cv.moments(c)
		center = (int(M['m10']/M["m00"]), int(M["m01"]/M["m00"]))
		print center

		time.sleep(0.01)
		if center[0] > 400:
			right()
			print "right"
		elif center[0] < 200:
			left()
			print "left"
		elif radius > 100:
			stop()
			print "stop"
		if radius < 70:
			forward()
			print("forward")
		else:
			stop()
			time.sleep(0.01)
	else:
		stop()
		time.sleep(0.01)

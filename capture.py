#Functions used to capture photos

import time
import cv2

#Create pipeline to grab feed from CSI camera
print("Initialising Camera")
def gstreamer_pipeline(
	capture_width=512,
	capture_height=384,
	display_width=512,
	display_height=384,
	framerate=21,
	flip_method=0,
	sensorID=0,
	):
	return (
		"nvarguscamerasrc sensor_id=%d ! "
		"video/x-raw(memory:NVMM), "
		"width=(int)%d, height=(int)%d, "
		"format=(string)NV12, framerate=(fraction)%d/1 ! "
		"nvvidconv flip-method=%d ! "
		"video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
		"videoconvert ! "
		"video/x-raw, format=(string)BGR ! appsink"
		% (
			sensorID,
			capture_width,
			capture_height,
			framerate,
			flip_method,
			display_width,
			display_height,
		)
	)
# Call this function in other files to take photos
def capture_input0():
    #Capture input from camera
    ret, frame = cap0.read()
    return frame
def capture_input1():
    #Capture input from camera
    ret, frame = cap1.read()
    return frame

# Release the camera
def release():
    cap0.release()
    cap1.release()
print("Instantiating camera object")
cap0 = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
cap1 = cv2.VideoCapture(gstreamer_pipeline(sensorID=1), cv2.CAP_GSTREAMER)

# for test
'''
try:
    img0 = capture_input0()
    img1 = capture_input1()
    cv2.imshow("img0",img0)
    cv2.imshow("img1",img1)
    cv2.waitKey()
finally:
    release()
'''



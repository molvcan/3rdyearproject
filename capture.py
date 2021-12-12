#Functions used to capture photos

import time
import cv2

#Create pipeline to grab feed from CSI camera
print("Initialising Camera")
def gstreamer_pipeline(
	capture_width=3280,
	capture_height=2464,
	display_width=1640,
	display_height=1232,
	framerate=21,
	flip_method=0,
	):
	return (
		"nvarguscamerasrc ! "
		"video/x-raw(memory:NVMM), "
		"width=(int)%d, height=(int)%d, "
		"format=(string)NV12, framerate=(fraction)%d/1 ! "
		"nvvidconv flip-method=%d ! "
		"video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
		"videoconvert ! "
		"video/x-raw, format=(string)BGR ! appsink"
		% (
			capture_width,
			capture_height,
			framerate,
			flip_method,
			display_width,
			display_height,
		)
	)
# Call this function in other files to take photos
def capture_input():
    #Capture input from camera
    ret, frame = cap.read()
    return frame

# Release the camera
def release():
    cap.release()

print("Instantiating camera object")
cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)




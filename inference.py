'''Main code to run entire model'''
import tensorflow as tf
import numpy as np
from tensorflow.python.saved_model import signature_constants, tag_constants
from tensorflow.python.framework import convert_to_constants
import time
import cv2
from adafruit_servokit import ServoKit
import board
import busio

model_name = 'B0_Accelerated'

#Load model
print("Loading Model")
saved_model_loaded = tf.saved_model.load(
    model_name, tags=[tag_constants.SERVING])

#Intantiate graphs from runtime engine
print("Instantiating graph")
graph_func = saved_model_loaded.signatures[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY]

#Convert graph variables to constants
print("Freezing graph")
graph_func = convert_to_constants.convert_variables_to_constants_v2(
    graph_func)


def inference(input):
	'''Run inference on input'''
	x = tf.constant(np.expand_dims(input, axis=0).astype(np.float32))
	pred = graph_func(x) 

	return pred[0].numpy()[0]

labels = ["cardboard", "glass", "metal", "paper", "plastic"]
iflg = 0
previousOut = None
queue = [0]
N = 10 #Queue length

def prediction(input):
	prediction = inference(input)
	output = np.argmax(prediction)
	return labels[output]

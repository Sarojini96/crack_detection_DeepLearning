#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 12:25:21 2020

@author: sarojini
"""

from __future__ import division, print_function
# coding=utf-8
import cv2
import os
from keras.preprocessing import image
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
INPUT_IMAGE_WIDTH = 64
INPUT_IMAGE_HEIGHT =64
print(INPUT_IMAGE_WIDTH, INPUT_IMAGE_HEIGHT)
def draw_found_bounding_boxes(img, boxes,color=(255,0,0)):
    for box in boxes:
        cv2.rectangle(img, box[0:2], box[2:4], color, 4)
def scan_image(img,cell_width,cell_height,stride_x,stride_y):
    boxes = []
    
    for x0 in range(0,int(img.shape[1])-cell_width,stride_x):
        for y0 in range(0,int(img.shape[0])-cell_height,stride_y):            
            x1 = x0 + cell_width
            y1 = y0 + cell_height
            subimg = img[y0:y1,x0:x1]                
            subimg_converted = subimg.reshape(1,cell_width,cell_height,3) 
            pred = predict_crack_or_no_crack(subimg)
            if numpy.isclose(pred["crack_prob"], 1, rtol=1e-05, atol=1e-08, equal_nan=False):
                boxes.append((x0,y0,x1,y1))
    return boxes 
# Model saved with Keras model.save()
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'crack_detection.h5')

# Load trained model
model = tf.keras.models.load_model(MODEL_PATH)

    #load and preprocess the image and predict
img = image.load_img('test.jpg')
img = img.resize((128, 128))
x = tf.keras.preprocessing.image.img_to_array(img)
x = np.expand_dims(x, axis=0)
images = np.vstack([x])
preds = model.predict(images)
print(preds)
class_name = "crack" if preds[0] < 0.5 else "no_crack"  
boxes = scan_image(img,cell_width=INPUT_IMAGE_WIDTH,cell_height=INPUT_IMAGE_HEIGHT,stride_x=16,stride_y=16)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # fix color order (depends on OpenCV version)
draw_found_bounding_boxes(img,boxes)
plt.rcParams['figure.figsize'] = [20, 10]
plt.imshow(img, interpolation='nearest', aspect='auto')
plt.title(class_name)
plt.imshow(img)
plt.show()

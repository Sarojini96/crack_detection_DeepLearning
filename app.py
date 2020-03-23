from __future__ import division, print_function
# coding=utf-8

import os
import io

import numpy as np
from PIL import Image
import tensorflow as tf
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template, jsonify
import cv2
import matplotlib.pyplot as plt


app = Flask('crack_detection')

# Model saved with Keras model.save()
MODEL_PATH1 = os.path.join(os.path.dirname(__file__), 'models', 'crack_detection.h5')
MODEL_PATH2 = os.path.join(os.path.dirname(__file__), 'models', 'test_model1.h5')

# Load trained model
model = tf.keras.models.load_model(MODEL_PATH1)
model._make_predict_function()
# Load trained model
model1 = tf.keras.models.load_model(MODEL_PATH1)
model1._make_predict_function()
print('Model loaded. Start serving...')


print('Model loaded. Check http://127.0.0.1:8080/')


def predictcrack(img, model):
    img = img.resize((128, 128))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    preds = model.predict(images)
    print(preds)
    return preds
def predictsides(img, model1):
    img = img.resize((128, 128))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    preds = model1.predict(images)
    print(preds)
    return preds

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict_image_class():
    img = request.files['file'].read()
    img = Image.open(io.BytesIO(img))
    prediction = predictcrack(img, model)
    class_name = "crack" if prediction[0] < 0.5 else "no_crack" 
    response = {"prediction": class_name}
    print(class_name)
    if class_name == 'no_crack':
       print("Sending for Second Test")
       prediction1 = predictsides(img, model1)
       class_name1 = "RHS" if prediction1 >=0.34 else "LHS"
       print(prediction1)
       print(class_name1)
       response = {"prediction1": class_name1 ,"prediction" : class_name}

    return jsonify(response)




if __name__ == '__main__':
    http_server = WSGIServer(('', 8080), app)
    http_server.serve_forever()

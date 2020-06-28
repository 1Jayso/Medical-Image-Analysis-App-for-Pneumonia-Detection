
from flask import render_template, jsonify, Flask, redirect, url_for, request
from app import app 
import random
import os
from PIL import Image

# from keras.applications.resnet50 import ResNet50
import tensorflow as tf
from tensorflow import keras
from keras.models import model_from_json
from keras.models import load_model
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.applications.imagenet_utils import preprocess_input
import cv2
import numpy as np
from keras.backend import clear_session


@app.route('/')



@app.route('/upload')
def upload_file2():
   return render_template('index.html')



def init(): 
	json_file = open('models/model.json','r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	#load weights into new model
	loaded_model.load_weights("models/model.h5")
	print("Loaded Model from disk")
    
	#compile and evaluate loaded model
	loaded_model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
	graph = tf.get_default_graph()
	return loaded_model,graph


clear_session()

global graph, model
model, graph = init()



	
@app.route('/uploaded', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
    #   graph = tf.get_default_graph()
      img = cv2.imread(path)
      img = cv2.resize(img, (64,64))
      img = np.array(img, dtype='float32')
      img = img/255.0
      img = img.reshape((1,64,64,3))
      img.shape

    #   clear_session()

   with graph.as_default():
      pred = model.predict(img)
      pred1 = model.predict_classes(img)
      if pred1==1:
        print("Patient1 has Pneumonia and the prediction accuracy is approximatly",int(pred1*100),"%")
        print("The actual predicted value is", int(pred*100),"%")
      else:
        print("patient2 is healthy")
        print("The actual predicted value is", int(pred*100),"%")   
      
      predict =  int(pred*100)
      print(pred)
      f.save(path)
      return render_template('uploaded.html', title='Success', predict=predict, user_image=f.filename)



@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/map')
def map():
    return render_template('map.html', title='Map')


@app.route('/map/refresh', methods=['POST'])
def map_refresh():
    points = [(random.uniform(48.8434100, 48.8634100),
               random.uniform(2.3388000, 2.3588000))
              for _ in range(random.randint(2, 9))]
    return jsonify({'points': points})


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')
from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from flask import jsonify
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import pickle
import cv2
from keras.preprocessing.image import img_to_array
import sqlite3

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/model.h5'

# Load your trained model
model = load_model(MODEL_PATH)
print('Model loaded. Check http://127.0.0.1:5000/')

# Pill ID | Pill Name                     | Generic Name            | Drug Class
#----------------------------------------------------------------------------------------------
# 1       | LILLY 3228 25mg               | atomoxetine             | CNS stimulants
# 2       | LILLY 3229 40mg               | atomoxetine             | CNS stimulants
# 3       | LILLY 3238 18mg               | atomoxetine             | CNS stimulants
# 4       | LILLY 3239 60 mg              | atomoxetine             | CNS stimulants
# 5       | LILLY 3250 80 mg              | atomoxetine             | CNS stimulants
# 6       | LILLY 3251 100 mg             | atomoxetine             | CNS stimulants
# 7       | Cialis 10 mg                  | tadalafil               | Impotence agents
# 8       | Cialis 20 mg                  | tadalafil               | Impotence agents
# 9       | Kombiglyze XR 2.5/1000 4222   | metformin/saxagliptin   | Antidiabetic combinations
# 10      | Roche 75 mg                   | oseltamivir             | Neuraminidase inhibitors
# 50      | SYNTHROID 75                  | levothyroxine           | Thyroid drugs
# 100     | Risperidone 93 225 0.5mg      | risperidone             | Atypical antipsychotics

# Database
import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None 
 
def get_pill_name(conn, pill_id):
    """
    Query pills by their pill id
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT name FROM pills WHERE id=?", (pill_id,))
    rows = cur.fetchall()
    for row in rows:
        pill_name = str(row[0])
        print(pill_name)

    return pill_name

def get_pill_generic_name(conn, pill_id):
    """
    Query pills by their pill id
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT generic_name FROM pills WHERE id=?", (pill_id,))
    rows = cur.fetchall()
    for row in rows:
        generic_name = str(row[0])
        print(generic_name)

    return generic_name

def get_pill_drug_class(conn, pill_id):
    """
    Query pills by their pill id
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT drug_class FROM pills WHERE id=?", (pill_id,))
    rows = cur.fetchall()
    for row in rows:
        drug_class = str(row[0])
        print(drug_class)

    return drug_class

def get_pill_error(conn, error_key):
    """
    Query pills by their pill id
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT error_text FROM pill_errors WHERE error_key=?", (error_key,))
    rows = cur.fetchall()
    for row in rows:
        error = str(row[0])
        print(error)

    return error

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html');

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    
    # Connecting to the database.
    database = "pills.db"
    conn = create_connection(database)

    # Initializing the output dictionary (JSON format).
    data = {"success": False}

    if request.method == 'POST':

        f = request.files['file']
        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        lb = pickle.loads(open("lb.pickle", "rb").read())
        
        # Load the image.
        image = cv2.imread(file_path)
        print("Image successfully uploaded.")

        # Image preprocessing.
        image = cv2.resize(image, (96, 96))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        
        # Predicting the label of the input image.
        print("[INFO] classifying image...")
        proba = model.predict(image)[0]
        print("Proba:", proba)
        idx = np.argmax(proba)
        print("idx:", idx)                # index 0 in array relates to class 1

        label = lb.classes_[idx]
        print("Label:", label)

        new_label = "{}: {:.2f}%".format(label, proba[idx] * 100)
        print(new_label)

        # Prediction probability.
        prob = proba[idx] * 100
        data["probability"] = prob

        if prob < 50:
            data["error_message"] = get_pill_error(conn, "LOW_PROB")
        else:    
            # Return prediction
            if new_label:
                data["success"] = True

            # Retrieving remaining info from database (Pill_name, Generic_name and Drug Class). 
            database = "pills.db"
     
            # Connecting to the database.
            conn = create_connection(database)

            data["pill_id"] = label  
            data["pill_name"] = get_pill_name(conn, label)
            data["generic name"] = get_pill_generic_name(conn, label)
            data["drug_class"] = get_pill_drug_class(conn, label)

            conn.close()

    return jsonify(data)

if __name__ == '__main__':
    #app.run(port=5002, debug=True)

    # Serve the app with gevent
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()

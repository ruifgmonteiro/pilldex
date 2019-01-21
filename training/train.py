#!/usr/bin/env python
'''
    File name: train.py
    Author: Rui Monteiro
    Date created: 20/10/2018
    Date last modified: 21/11/2018
    Python Version: 3.6

# USAGE
# python train.py --dataset dataset --model pilldex.model --labelbin lb.pickle

# tensorboard --logdir=logs/ --port=8101
'''
import matplotlib
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam, SGD
from keras.preprocessing.image import img_to_array
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from pyimagesearch.smallervggnet import SmallerVGGNet
import matplotlib.pyplot as plt
from imutils import paths
import numpy as np
import argparse
import random
import pickle
import cv2
import os
from phdnet.phdnet import PHDNet
from pyimagesearch.smallervggnet import SmallerVGGNet
import Augmentor
from Augmentor.Pipeline import Pipeline
from sklearn.metrics import classification_report,confusion_matrix
import itertools
from keras.callbacks import TensorBoard
from time import time

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
    help="path to input dataset (i.e., directory of images)")
ap.add_argument("-m", "--model", required=True,
    help="path to output model")
ap.add_argument("-l", "--labelbin", required=True,
    help="path to output label binarizer")
ap.add_argument("-p", "--plot", type=str, default="plot.png",
    help="path to output accuracy/loss plot")
args = vars(ap.parse_args())

# initialize the number of epochs to train for, initial learning rate,
# batch size, and image dimensions
online_data_augment=False   
EPOCHS = 150
INIT_LR = 2e-5
BS = 32
IMAGE_DIMS = (96, 96, 3)

# initialize the data and labels
data = []
labels = []

# grab the image paths and randomly shuffle them
print("[INFO] loading images...")
imagePaths = sorted(list(paths.list_images(args["dataset"])))
random.seed(42)
random.shuffle(imagePaths)

# loop over the input images
for imagePath in imagePaths:
    # load the image, pre-process it, and store it in the data list
    image = cv2.imread(imagePath)
    image = cv2.resize(image, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
    image = img_to_array(image)
    data.append(image)
 
    # extract the class label from the image path and update the
    # labels list
    label = imagePath.split(os.path.sep)[-2]
    labels.append(label)    

# scale the raw pixel intensities to the range [0, 1]
data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)
print("[INFO] data matrix: {:.2f}MB".format(
    data.nbytes / (1024 * 1000.0)))

# binarize the labels
lb = LabelBinarizer()
labels = lb.fit_transform(labels)

# partition the data into training and testing splits using 80% of
# the data for training and the remaining 20% for testing
(trainX, testX, trainY, testY) = train_test_split(data,
    labels, test_size=0.2, random_state=42)

# initialize the model
print("[INFO] compiling model...")
model = SmallerVGGNet.build(width=IMAGE_DIMS[1], height=IMAGE_DIMS[0], depth=IMAGE_DIMS[2], classes=len(lb.classes_))
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

# Tensorboard Log
#tensorboard = TensorBoard(log_dir='Log/', histogram_freq=0, write_graph=True, write_images=True)
tensorboard = TensorBoard(log_dir="logs/{}".format(time()))

# Training the network
print("[INFO] training network...")
H = model.fit(trainX, trainY, batch_size=BS, epochs=EPOCHS, validation_data=(testX, testY), callbacks=[tensorboard])

# save the model to disk
print("[INFO] serializing network...")
model.save(args["model"])

# save the label binarizer to disk
print("[INFO] serializing label binarizer...")
f = open(args["labelbin"], "wb")
f.write(pickle.dumps(lb))
f.close()

model_json = model.to_json()

with open("model.json", "w") as json_file:
  json_file.write(model_json)

model.save("model.h5")

# Plot the training and validation accuracy
plt.plot(H.history['acc'])
plt.plot(H.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# Plot the training and validation loss
plt.plot(H.history['loss'])
plt.plot(H.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

#   Avaliação   final   com os  casos   de  teste  - Evaluate
scores  =   model.evaluate(testX,  testY, verbose=1)  
print('Scores:  ',  scores) 
print("Accuracy:    %.2f%%" %   (scores[1]*100))    
print("Erro modelo:    %.2f%%" %   (100-scores[1]*100))

# Plotting the confusion matrix
def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j], horizontalalignment="center", color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

# Printing the confusion matrix
Y_pred = model.predict(testX)
print(Y_pred)
y_pred = np.argmax(Y_pred, axis=1)
print(y_pred)

target_names = []
for i in range(1,101):
    target_names.append("class_" + str(i))
    i+=1
print(target_names)
print(testY) 
print(classification_report(np.argmax(testY ,axis=1), y_pred,target_names=target_names))

print(confusion_matrix(np.argmax(testY,axis=1), y_pred))

# Compute confusion matrix
cnf_matrix = (confusion_matrix(np.argmax(testY,axis=1), y_pred))

np.set_printoptions(precision=2)

plt.figure()

# Plot non-normalized confusion matrix
plot_confusion_matrix(cnf_matrix, classes=target_names,
                      title='Confusion matrix')
plt.figure()
plt.show()       
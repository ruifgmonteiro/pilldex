'''
    File name: pillnet.py
    Author: Rui Monteiro
    Date created: 20/10/2018
    Date last modified: 21/11/2018
    Python Version: 3.6
'''    

# import the necessary packages
from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dropout
from keras.layers.core import Dense
from keras import backend as K
from keras.constraints import maxnorm

class PillNet:
    
    @staticmethod
    def build(width, height, depth, classes):
        # initialize the model along with the input shape to be
        # "channels last" and the channels dimension itself
        model = Sequential()
        inputShape = (height, width, depth)
        chanDim = -1

        # if we are using "channels first", update the input shape
        # and channels dimension
        if K.image_data_format() == "channels_first":
            inputShape = (depth, height, width)
            chanDim = 1

        model = Sequential()    
        model.add(Conv2D(32, (3, 3), input_shape=inputShape, activation='relu', padding='same'))
        model.add(BatchNormalization()) # Using BatchNormalization after activations
        model.add(Dropout(0.2))
        model.add(Conv2D(2*32, (3, 3), activation='relu', padding='same'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))  
        model.add(Flatten())
        model.add(Dropout(0.2))
        model.add(Dense(2000, activation='relu', kernel_constraint=maxnorm(3)))
        model.add(BatchNormalization()) 
        model.add(Dropout(0.5))    
        model.add(Dense(1000, activation='relu', kernel_constraint=maxnorm(3)))
        model.add(BatchNormalization())   
        model.add(Dropout(0.2))    
        model.add(Dense(classes, activation='softmax'))    

        model.summary()

        return model

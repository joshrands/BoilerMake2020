from platform import python_version
print(python_version())
<<<<<<< HEAD
from defines import *
=======
>>>>>>> e67f2d0fca2b87a9fabc62448271c2a50e5d453a

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import RMSprop

import cv2
import time
import numpy as np
import random

def getFlattenArray(img):
    # flatten image 
    in_arr = np.array(img)
    out_arr = in_arr.flatten()
    out_arr = out_arr.tolist()

    return out_arr

<<<<<<< HEAD
model = keras.models.load_model("model-garbage-0.h5")
cap = cv2.VideoCapture(1)
=======
model = keras.models.load_model("model-v1.h5")
cap = cv2.VideoCapture(3)
>>>>>>> e67f2d0fca2b87a9fabc62448271c2a50e5d453a

# grab picture from webcam every second and run through model
while cap.isOpened():
    ret, frame = cap.read()
    if ret == True:
        # Display the resulting frame
        cv2.imshow('Frame',frame)

    #    print(len(frame[0]),len(frame[1]))

#        scale_percent = 3
#        width = int(frame.shape[1] * scale_percent / 100)
#        height = int(frame.shape[0] * scale_percent / 100)
<<<<<<< HEAD
        dim = (img_height, img_width)
=======
        dim = (57, 32)
>>>>>>> e67f2d0fca2b87a9fabc62448271c2a50e5d453a

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        resized = cv2.resize(gray, dim, interpolation = cv2.INTER_AREA)

    #        cv2.imshow("Frame", resized)
    #        display_sample(gray, width, height)
        # Press Q on keyboard to  exit

        flat_img = getFlattenArray(resized)
        for x in flat_img:
            print(x)
    #    print(len(flat_img))

        predicted = model.predict([flat_img]).argmax()
        print(predicted)
        if (predicted == 1):
<<<<<<< HEAD
            print("Hawt garbage")
        else:
            print("Clean")

        time.sleep(1)
=======
            print("Heart attack!")
        else:
            print("You good")

        time.sleep(2)
>>>>>>> e67f2d0fca2b87a9fabc62448271c2a50e5d453a

#    cv2.destroyAllWindows()

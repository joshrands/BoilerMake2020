import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import RMSprop

from defines import *

import cv2
import time
import numpy as np
import random

model = keras.models.load_model("model-garbage-1.h5")
#video_input = int(input("Enter video input: "))
ip_addr = input("Enter BARBARA ip: ")

cap = cv2.VideoCapture('http://' + ip_addr + ':8000/stream.mjpg')

if (cap.isOpened() == False):
    print("Error opening camera")

# grab picture from webcam every second and run through model
count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if ret == True:
        # Display the resulting frame
#        cv2.imshow('Frame',frame)

    #    print(len(frame[0]),len(frame[1]))

#        scale_percent = 3
#        width = int(frame.shape[1] * scale_percent / 100)
#        height = int(frame.shape[0] * scale_percent / 100)
        dim = (img_height, img_width)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        resized = cv2.resize(gray, dim, interpolation = cv2.INTER_AREA)

        cv2.imshow("Frame", resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        resized = resized.tolist()

        final_in = []
        for row in resized:
            new_row = []
            for val in row:
                new_row.append([float(val) / 255.0])
            final_in.append(new_row)  
    #        cv2.imshow("Frame", resized)
    #        display_sample(gray, width, height)
        # Press Q on keyboard to  exit

   #    print(len(flat_img))

        predicted = model.predict([final_in]).argmax()
#        print(predicted)
        count += 1
        if (predicted == 1):
            print("Hawt gawbage")
        else:
            print("Clean")

        time.sleep(0.1)

#    cv2.destroyAllWindows()

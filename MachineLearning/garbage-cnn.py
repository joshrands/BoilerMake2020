# CNN to detect garbage 
from defines import *

import tensorflow
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.optimizers import RMSprop
import cv2
import time
import numpy as np
import random

train_data = []
version = input("Enter version to save as: ")

import matplotlib.pyplot as plt

def getFlattenArray(img):
    # flatten image 
    in_arr = np.array(img)
    out_arr = in_arr.flatten()
    out_arr = out_arr.tolist()

    return out_arr

# scaling images 
#scale_percent = 3

def getFramesFromVideo(file_name, garbage):
    print("Getting frames from " + file_name)
    cap = cv2.VideoCapture(file_name)

    if (cap.isOpened()== False): 
        print("Error opening video stream or file")

    success,image = cap.read()
    count = 0
    while success:
#        cv2.imshow(image)
#        print(getFlattenArray(image))
        width = img_width 
        height = img_height 

        dim = (height, width)
 
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        resized = cv2.resize(gray, dim, interpolation = cv2.INTER_AREA)

#        cv2.imshow("Frame", resized)
#        display_sample(gray, width, height)
        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

#        flat_img = getFlattenArray(resized)
#        print(len(flat_img))
#        for data in img_data:
#            print(data)
        resized = resized.tolist()

        final_in = []
        for row in resized:
            new_row = []
            for val in row:
                new_row.append([float(val) / 255.0])
            final_in.append(new_row)            

        if (garbage == 1):
            train_data.append([final_in, [0, 1]])
        else:
            train_data.append([final_in, [1, 0]])

        #cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file      
        success,image = cap.read()
#        print('Read a new frame: ', success)
        count += 1

    print("Read " + str(count) + " frames")

getFramesFromVideo("./garbage/dirty1.mp4", 1)
getFramesFromVideo("./garbage/dirty2.mp4", 1)
getFramesFromVideo("./garbage/dirty3.mp4", 1)
getFramesFromVideo("./garbage/dirty4.mp4", 1)
getFramesFromVideo("./garbage/dirty5.mp4", 1)
getFramesFromVideo("./garbage/dirty6.mp4", 1)
getFramesFromVideo("./garbage/dirty7.mp4", 1)
getFramesFromVideo("./garbage/dirty8.mp4", 1)
getFramesFromVideo("./garbage/dirty9.mp4", 1)
getFramesFromVideo("./garbage/dirty10.mp4", 1)
getFramesFromVideo("./garbage/dirty11.mp4", 1)
getFramesFromVideo("./garbage/dirty12.mp4", 1)
getFramesFromVideo("./garbage/dirty13.mp4", 1)
getFramesFromVideo("./garbage/dirty14.mp4", 1)
getFramesFromVideo("./garbage/dirty15.mp4", 1)

getFramesFromVideo("./clean/clean1.mp4", 0)
#getFramesFromVideo("./clean/clean2.mp4", 0)
getFramesFromVideo("./clean/clean3.mp4", 0)
getFramesFromVideo("./clean/clean4.mp4", 0)
getFramesFromVideo("./clean/clean5.mp4", 0)
getFramesFromVideo("./clean/clean6.mp4", 0)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(img_width,img_height,1)))
# 64 3x3 kernels
model.add(Conv2D(64, (3, 3), activation='relu'))
# Reduce by taking the max of each 2x2 block
model.add(MaxPooling2D(pool_size=(2, 2)))
# Dropout to avoid overfitting
model.add(Dropout(0.25))
# Flatten the results to one dimension for passing into our final layer
model.add(Flatten())
# A hidden layer to learn with
model.add(Dense(128, activation='relu'))
# Another dropout
model.add(Dropout(0.4))
# A hidden layer to learn with
model.add(Dense(128, activation='relu'))
# Another dropout
model.add(Dropout(0.3))
# Final categorization from 0-9 with softmax
model.add(Dense(2, activation='softmax'))

model.summary()

# optimizer and loss function? TODO: Figure out what this is 
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# shuffle train data
for i in range(len(train_data)-1, 0, -1): 
      
    # Pick a random index from 0 to i  
    j = random.randint(0, i + 1)  
    
    # Swap arr[i] with the element at random index  
    train_data[i], train_data[j] = train_data[j], train_data[i]  


# split data into train and test data
print("Length = " + str(len(train_data)))
split = int(len(train_data) * 0.8)
print("Split at " + str(split))
test_data = train_data[split:]
train_data = train_data[:split]

print("Data successfully split")

# split train_data into train_x and train_y
x_train = []
y_train = []
for pair in train_data:
    x_train.append(pair[0])
    y_train.append(pair[1])

print("Training data set complete.")

x_test = []
y_test = []
for pair in test_data:
    x_test.append(pair[0])
    y_test.append(pair[1])

print("Testing data set complete.")
#print(x_train[0])

history = model.fit(x_train, y_train,
                    batch_size=32,
                    epochs=5,
                    verbose=2,
                    validation_data=(x_test, y_test))

# fit the model to the training data 
#history = model.fit(x_train, y_train,
                    #batch_size=100,
                    #epochs=5,
                    #verbose=2,
                    #shuffle=True,
                    #callbacks=[cp_callback],
                    #validation_data=(x_test, y_test))

# evaluate the model on new images 
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

model.save("model-garbage-" + str(version) + ".h5")

print("Model saved.")

#saver = tf.compat.v1.train.Saver()
#sess = tf.Session()
#sess.run(tf.global_variables_initializer())
#saver.save(sess, 'heart_attack_v1')

for x in range(len(test_data)):
    test_image = [test_data[x][0]]
#    print(test_image)
#    print(len(test_image))
    predicted = model.predict(test_image).argmax()
    label = 0
    if (test_data[x][1][1] == 1):
        label = 1


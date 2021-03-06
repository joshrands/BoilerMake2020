import numpy as np
#import cv, cv2
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file")
parser.add_argument("-d")

args = parser.parse_args()
arg_vals = vars(args)

#cap = cv2.VideoCapture(0)
#video_input = arg_vals['d']
#if (arg_vals['d'] == None):
video_input = int(input("Enter video input: "))

cap = cv2.VideoCapture(video_input)

#file_name = arg_vals['file']
#if (file_name == None):
file_name = input("Enter output file name: ")

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#fourcc = cv2.CV_FOURCC(*'XVID')
fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
out = cv2.VideoWriter("./Raw/" + file_name + ".avi",fourcc, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
#        frame = cv2.flip(frame,0)
#        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()

#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np 
import requests

cap0 = cv2.VideoCapture(0) #Initiating camera. '0' refers to inbuilt/default camera.
                          #change number to switch camera
cap1 = cv2.VideoCapture(0) #camera instance for calibration

#camera calibration over segmented image. 

ret0,frame0 = cap0.read()
imgref = cv2.flip(frame0,0)
imgref = cv2.rectangle(imgref,(255,115),(260,155),(255,100,0),1) #jump point new
crop_imgref = imgref[115:155,255:260]
crop_seg_mval = np.mean(crop_imgref)
print("Mean Pixel weight of the ROI =",crop_seg_mval)
cap0.release()


# In[ ]:


#function to trigger servo motor 
def jump():
    response = requests.get('http://192.168.5.1/?State=J')
    response = requests.get('http://192.168.5.1/?State=I')
    response.close()

while(True): #indefinite loop to handle frames one by one. 
    ret,frame = cap1.read() #Read the camera frame
    #cv2.imshow('video',frame) #Display/show the frame
    img2=cv2.flip(frame,0)
    img2 = cv2.rectangle(img2, (150,100) ,(188,155), (0,255,0), 2) #start point #Adjust the values for bigger screens.
    '''
    Position the trex inside this reference bbox.Refer attached screenshot.
    '''
    #img2 = cv2.rectangle(img2,(255,115),(260,155),(255,100,0),1) #jump point new
    crop_img = img2[115:155, 255:260]#segmented portion of the frame. 
    crop_seg_val = np.mean(crop_img)
    #print(crop_seg_val)
    tf = 2 #Tuning factor. Play with this for better result
    #if crop_seg_val < (crop_seg_val - tf): #uncomment this after positioning the camera.!!!!!!!!!!!
        #jump()                             #uncomment this after positioning the camera.!!!!!!!!!!!
    cv2.imshow('Flipped video',img2)        #commentout for better performance
    if cv2.waitKey(1) & 0xFF == ord('q'): # press 'q' to terminate the program.
        break

cap1.release() #Terminate/release the camera
cv2.destroyAllWindows() 




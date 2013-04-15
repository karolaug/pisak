#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import time

device = 0
cap = cv2.VideoCapture(device)

cap.set(3,1280)
cap.set(4,720)


while True:
	ret,im = cap.read()
	
	print("TIME: "+str(time.time()))
	
	cv2.imshow('video test',im)
	
	#time.sleep(0.33)
	
	key = cv2.waitKey(10)
	
	if key == 27:
		cv2.destroyAllWindows()
		break
	if key == ord(' '):
		cv2.imwrite('vid_result.jpg',im)


import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def nothing(x):
    pass

cv2.namedWindow('b&w1')
cv2.namedWindow('b&w2')

cv2.createTrackbar('maxValue', 'b&w1', 0, 255, nothing)
cv2.createTrackbar('blockSize', 'b&w1', 2, 107, nothing)
cv2.createTrackbar('C', 'b&w1', 0, 255, nothing)

cv2.createTrackbar('maxValue', 'b&w2', 0, 255, nothing)
cv2.createTrackbar('blockSize', 'b&w2', 2, 107, nothing)
cv2.createTrackbar('C', 'b&w2', 0, 255, nothing)

while(1):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    max1 = cv2.getTrackbarPos('maxValue', 'b&w1')
    block1 = 2*cv2.getTrackbarPos('blockSize', 'b&w1')+1
    c1 = cv2.getTrackbarPos('C', 'b&w1')

    max2 = cv2.getTrackbarPos('maxValue', 'b&w2')
    block2 = 2*cv2.getTrackbarPos('blockSize', 'b&w2')+1
    c2 = cv2.getTrackbarPos('C', 'b&w2')

    black1 = cv2.adaptiveThreshold(gray, max1, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block1, c1)

    black2 = cv2.adaptiveThreshold(gray, max2, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block2, c2)

    edges = cv2.Canny

    cv2.imshow('true', frame)
    cv2.imshow('gray', gray)
    cv2.imshow('b&w1', black1)
    cv2.imshow('b&w2', black2)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

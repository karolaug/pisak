#Camera_Get_Set.py
#By Forrest L. Erickson of VRX Company Inc. 8-31-12.
#Opens the camera and reads and reports the settings.
#Then tries to set for higher resolution.
#Workes with Logitech C525 for resolutions 960 by 720 and 1600 by 896


import cv2.cv as cv
import numpy

CV_CAP_PROP_POS_MSEC = 0
CV_CAP_PROP_POS_FRAMES = 1
CV_CAP_PROP_POS_AVI_RATIO = 2
CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4
CV_CAP_PROP_FPS = 5
CV_CAP_PROP_POS_FOURCC = 6
CV_CAP_PROP_POS_FRAME_COUNT = 7
CV_CAP_PROP_BRIGHTNESS = 8
CV_CAP_PROP_CONTRAST = 9
CV_CAP_PROP_SATURATION = 10
CV_CAP_PROP_HUE = 11

CV_CAPTURE_PROPERTIES = tuple({
CV_CAP_PROP_POS_MSEC,
CV_CAP_PROP_POS_FRAMES,
CV_CAP_PROP_POS_AVI_RATIO,
CV_CAP_PROP_FRAME_WIDTH,
CV_CAP_PROP_FRAME_HEIGHT,
CV_CAP_PROP_FPS,
CV_CAP_PROP_POS_FOURCC,
CV_CAP_PROP_POS_FRAME_COUNT,
CV_CAP_PROP_BRIGHTNESS,
CV_CAP_PROP_CONTRAST,
CV_CAP_PROP_SATURATION,
CV_CAP_PROP_HUE})

CV_CAPTURE_PROPERTIES_NAMES = [
"CV_CAP_PROP_POS_MSEC",
"CV_CAP_PROP_POS_FRAMES",
"CV_CAP_PROP_POS_AVI_RATIO",
"CV_CAP_PROP_FRAME_WIDTH",
"CV_CAP_PROP_FRAME_HEIGHT",
"CV_CAP_PROP_FPS",
"CV_CAP_PROP_POS_FOURCC",
"CV_CAP_PROP_POS_FRAME_COUNT",
"CV_CAP_PROP_BRIGHTNESS",
"CV_CAP_PROP_CONTRAST",
"CV_CAP_PROP_SATURATION",
"CV_CAP_PROP_HUE"]


capture = cv.CaptureFromCAM(0)

print ("\nCamera properties before query of frame.")
for i in range(len(CV_CAPTURE_PROPERTIES_NAMES)):
#    camera_valeus =[CV_CAPTURE_PROPERTIES_NAMES, foo]
    foo = cv.GetCaptureProperty(capture, CV_CAPTURE_PROPERTIES[i])
    camera_values =[CV_CAPTURE_PROPERTIES_NAMES[i], foo]
#    print str(camera_values)
    print str(CV_CAPTURE_PROPERTIES_NAMES[i]) + ": " + str(foo)


print ("\nOpen a window for display of image")
cv.NamedWindow("Camera", 1)
while True:
    img = cv.QueryFrame(capture)
    cv.ShowImage("Camera", img)
    if cv.WaitKey(10) == 27:
        break
cv.DestroyWindow("Camera")


#cv.SetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH, 1024)
#cv.SetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT, 768)
cv.SetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH, 1600)
cv.SetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT, 896)


print ("\nCamera properties after query and display of frame.")
for i in range(len(CV_CAPTURE_PROPERTIES_NAMES)):
#    camera_valeus =[CV_CAPTURE_PROPERTIES_NAMES, foo]
    foo = cv.GetCaptureProperty(capture, CV_CAPTURE_PROPERTIES[i])
    camera_values =[CV_CAPTURE_PROPERTIES_NAMES[i], foo]
#    print str(camera_values)
    print str(CV_CAPTURE_PROPERTIES_NAMES[i]) + ": " + str(foo)


print ("/nOpen a window for display of image")
cv.NamedWindow("Camera", 1)
while True:
    img = cv.QueryFrame(capture)
    cv.ShowImage("Camera", img)
    if cv.WaitKey(10) == 27:
        break
cv.DestroyWindow("Camera")

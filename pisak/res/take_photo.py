import camera, cv2, time, os.path
from pisak import res

cams = camera.lookForCameras()
cam = camera.Camera(cams['Camera_1'])
time.sleep(0.05)
frame = cam.frame()
cam.close()
cv2.imwrite(os.path.join(res.PATH, 'zdjecie.jpg'), frame)

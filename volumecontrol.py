# here use your index finger and thunb to control sound of the system


import cv2 as cv
import time
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import handtrackingmodule as htm
wCam, hCam = 640, 480
cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.HandSensor(detconf=0.7)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volrange = volume.GetVolumeRange()
minvol = volrange[0]
maxvol = volrange[1]
volume.SetMasterVolumeLevel(-20.0, None)
while True:
    success, img = cap.read()
    img1 = detector.findHands(img)
    lmlist = detector.findPos(img, draw=False)
    if len(lmlist) != 0:
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cv.circle(img, (x1, y1), 10, (255, 0, 255), cv.FILLED)
        cv.circle(img, (x2, y2), 10, (255, 0, 255), cv.FILLED)
        cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        length = np.hypot(x2 - x1, y2 - y1)
        vol = np.interp(length, [50, 300], [minvol, maxvol])
        volume.SetMasterVolumeLevel(vol, None)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv.putText(img, f'FPS:{int(fps)}', (40, 50), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cv.imshow("IMG", img)
    if cv.waitKey(1) and 0xff == 'q':
        break

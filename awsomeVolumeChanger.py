import time
import cv2
from HandTrackingModule import HandTrackDetector
import subprocess
import warnings
import numpy as np
import platform

warnings.filterwarnings("ignore")



def set_master_volume(vol):

    volume = vol
    try:
        volume = int(volume)

        if (volume <= 100) and (volume >= 0):
            subprocess.call(["amixer", "-D", "pulse", "sset", "Master", str(volume)+"%"])
            valid = True
    except ValueError:
        pass

ptime = 0
ctime = 0
prev_distance = 0
cap = cv2.VideoCapture(0)
detector = HandTrackDetector()
while True:
    ret,frame = cap.read()
    frame = detector.findHands(frame,draw=True)
    lmpos = detector.findPosition(frame,draw=False)
    if len(lmpos) != 0:
        d = detector.calcDistance(frame,lmpos[4],lmpos[8])
        d = int(d)
        if 'Windows' in platform.platform():
            winval = np.interp(d,[0,200],[-65,0])
            print(winval)
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            if (winval<=0) and (winval>=-65):
                try:
                    volume.SetMasterVolumeLevel(int(winval) , None)
                except Exception:
                    pass
        else:
            set_master_volume(d)
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(frame,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),3)
    cv2.imshow("frame",frame)

    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows() 

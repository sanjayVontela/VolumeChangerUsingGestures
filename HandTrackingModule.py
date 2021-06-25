import cv2
import mediapipe as mp
import time
import numpy as np
import math

from scipy.spatial import distance
class HandTrackDetector:
    def __init__(self,mode = False, maxHands = 2, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,frame,draw=True):
        imageRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame,handLms, self.mpHands.HAND_CONNECTIONS)
                else:
                    self.mpDraw.draw_landmarks(frame,handLms)
        return frame


    def findPosition(self,frame,handNo = 0,draw=True):
        lmpos = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                    h,w,c = frame.shape
                    cx,cy  = int(lm.x*w), int(lm.y*h)
                    lmpos.append([id,cx,cy])
                    if draw:
                        cv2.circle(frame,(cx,cy),10,(255,255,0),cv2.FILLED)
        return lmpos


    def calcDistance(self,frame,p1,p2,draw=True,handNo=0):
        cx1,cy1 = p1[1],p1[2]
        cx2,cy2 = p2[1],p2[2]
        d =  math.hypot(cx2 - cx1, cy2 - cy1)
        # print(cx1,cx2,cy1,cy2)
        if draw:
            cv2.line(frame,(cx1,cy1),(cx2,cy2),(255,255,123),9)
        return d
def main():
    ptime = 0
    ctime = 0
    cap = cv2.VideoCapture(0)
    detector = HandTrackDetector()
    while True:
        ret,frame = cap.read()
        frame = detector.findHands(frame,draw=True)
        lmpos = detector.findPosition(frame)
        if len(lmpos) != 0:
            print(lmpos[4])
        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        cv2.putText(frame,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),3)
        cv2.imshow("frame",frame)

        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows() 

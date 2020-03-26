import cv2
import numpy as np
from collections import deque
path_video="./videos/video01.avi"
point=deque(maxlen=20)
cap=cv2.VideoCapture(path_video)
def segmentation(frame):
    lowerb=np.array([90,40,0])
    upperb=np.array([210,140,80])
    gray=cv2.inRange(frame,lowerb,upperb)
    element=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    gray=cv2.morphologyEx(gray,cv2.MORPH_OPEN,element,iterations=3)
    return gray
def contorno(gray,frame):
    cnt, _ = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cx=0
    cy=0
    if cnt:
        cnt = sorted(cnt, key=cv2.contourArea, reverse=True)[:1]
        (cx, cy), radius = cv2.minEnclosingCircle(cnt[0])
        cv2.circle(frame, (int(cx), int(cy)), int(radius), (0, 255, 0), 3)
        cv2.circle(frame, (int(cx), int(cy)), 6, (0, 0, 255), cv2.FILLED)
    return int(cx),int(cy)

while(cap.isOpened()):
    ok,frame=cap.read()
    if not ok:
        break
    gray=segmentation(frame)
    cx,cy=contorno(gray,frame)
    if cx==0:
        continue
    point.append((cx,cy))
    for i in range(len(point)-1):
        cv2.line(frame,point[i],point[i+1],(0,0,255),2)

    cv2.imshow('gray',gray)
    cv2.imshow("frame",frame)
    if cv2.waitKey(30) & 0xFF ==ord("q"):
        break
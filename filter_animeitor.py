from kalman2D import Kalman
from time import sleep
import cv2
import numpy as np
cv2.namedWindow("image")
img= np.zeros((400,700,3))
img[0:-1,200:202]=255
rastro=[]
rastroKF=[]
vx=[]
vy=[]
KF =Kalman()

def click_mauser(event, x, y, flags, param):
    fil=KF.correction(np.array([[x],[y]]),1)
    fx=fil[0][0]
    fy=fil[1][0]
    vx0=fil[2][0]
    vx.append(vx0)
    vy=fil[3][0]
    modulo_velocidade=np.sqrt(vx0**2+vy**2)
    print(modulo_velocidade)
    cv2.putText(img,'{:0.2f} m/s'.format(modulo_velocidade), (25, 60), cv2.FONT_ITALIC, 0.7, (255, 255, 255), 1)

    KF.prediction()
    rastroKF.append(((int(fx),int(fy))))
    rastro.append((x,y))

cv2.setMouseCallback("image", click_mauser)

while(True):

    while(len(rastro)>800):
        del rastro[0]
        del rastroKF[0]

    if len(rastro)>2:
        del rastro[0]
        del rastroKF[0]

    cv2.circle(img,(20,18),2,(0,0,255),2,1)
    cv2.putText(img,'kalman',(25,20),cv2.FONT_ITALIC,0.7,(255,255,255),1)
    cv2.circle(img, (20, 35), 2, (255, 255, 0), 2, 1)
    cv2.putText(img, 'Sensor', (25, 40), cv2.FONT_ITALIC, 0.7, (255, 255, 255), 1)
    for center in rastro:
        cv2.circle(img,center,1,(255,255,0),2,1)
    for centerkf in rastroKF:
        cv2.circle(img,centerkf, 1, (0, 0, 255), 2, 1)

    if len(vx)>0:
        cv2.line(img,(rastroKF[-1]),(rastroKF[-1][0]+int(vx[-1]),rastroKF[-1][1]),(255,0,255),2)
    cv2.imshow("image",img)
    img[:,:]=0
    sleep(1/10)
    if cv2.waitKey(1)=="q":
        break
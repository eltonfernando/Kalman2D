import cv2
cap=cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
out = cv2.VideoWriter('video.avi', fourcc, 25, (width,height))
while(True):
    ret,frame=cap.read()
    cv2.imshow("frame",frame)
    out.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
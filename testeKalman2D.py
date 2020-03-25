import matplotlib.pyplot as plt
import time
from kalman2D import Kalman
import numpy as np

Fk=Kalman()
tm=[]
medidax=[]
mediday=[]
pred_x=[]
pred_y=[]
medida=[[0,0],[1,1],[2,1],[3,1],[4,2],[4,3],[6,4],[7,5],[8,5],[9,5],[9,5],[9,4],[9,3],[9,2],[9,1],[8,1],[7,1],[6,1]]
for x in medida:
    time.sleep(1/30)
    mdx=x[0]
    mdy=x[1]
    if x[0]==4:
        Fk.correction(np.array([[mdx],[mdy]]),0)
    else:
        re=Fk.correction(np.array([[mdx], [mdy]]), 1)
        print('re= '+str(re.T[0]))
    medidax.append(mdx)
    mediday.append(mdy)
    pred_x.append(Fk.x[0])
    pred_y.append(Fk.x[1])
    Fk.prediction()

plt.scatter(medidax,mediday)
plt.scatter(pred_x,pred_y,color='r')
plt.plot(pred_x,pred_y)
plt.show()
print(Fk.x)
print('x0='+str(Fk.x[0:2]))


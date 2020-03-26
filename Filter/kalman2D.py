'''
import numpy as np
import time
import matplotlib.pyplot as plt
#!/usr/bin/python
# coding: utf-8
'''

import numpy as np

class Kalman:
    def __init__(self,FPS=30):
        """
        x: matriz 4x1 estado (x,y) velocidade em x e velocidade em y
        P: matriz 4x4 incerteza inicial
        u: matriz de aceleração
        F: matriz 4x4 funcão de estado
        H: matriz 2x4 função de medição
        R: matriz 2x2 incerteza de medição (R2 com oclusao)
        Q: matriz 4x4 incerteza do modelo (Q2 com oclusao)
        I: matriz 4x4 identidade
        lastResult: matriz 2x1 guarda resuldado enterior
        :param FPS: Taxa de amostragem
        """
        delta=1/FPS
        self.x = np.array([[0.], [0.],[0],[0]])  # initial state (location and velocity)
        self.P = np.eye(4)  # initial uncertainty
        #self.u = np.array([[0.], [0.],[0.],[0.]])  # external motion
        self.F = np.array([[1.,0, delta,0], [0, 1.,0,delta],[0,0,1,0],[0,0,0,1]])  # next state function
        self.H = np.array([[1., 0.],[0,1],[0,0],[0,0]]).T  # measurement function
        peso=0.999
        inser=1-peso
        self.R = np.eye(2)*0.01#peso  # incerteza do sensor sem oclusão
        self.R2=np.eye(2)*0.1 #incerteza do sensor com oclusão
        self.Q = np.eye(4)*0.0002#*inser  #incerteza do modelo sem oclusão
        self.Q2=np.eye(4)*0.00001 #incerteza do modelo com oclusão
        self.I = np.eye(4)  # identity matrix
        self.lastResult = np.array([[0], [0]])
        self.flag=1
    def correction(self,Z,flag=1):
        """
        y=Z-HK
        S=H*P*trans(H) +R
        K=P*trans(H)*inv(S)
        x=x+(k*y)
        P=(I-k*H)P
        :param Z: np.array[[x],[y]]
        :param flag: 0 quando não tem medição
        :return:Matrix 2x1 com coordenada (x,y)
        isso pode ser alterado para retorna velocidade
        estimada pelo filtro
        """
        self.flag=flag
        # sem oclusão (usa dado de medida)
        if self.flag:
            y = Z - (np.dot(self.H, self.x))
            S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R
            k = np.dot(self.P, np.dot(self.H.T, np.linalg.inv(S)))
            self.x = self.x + np.dot(k, y)
            self.P = np.dot((self.I - np.dot(k, self.H)), self.P)
        # situação com oclusão
        # (não consguir medir usa estimativa anterior)
        else:
            Z = self.lastResult  # usa a medição estimada para prever
            y = Z - (np.dot(self.H, self.x))
            S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R2
            k = np.dot(self.P, np.dot(self.H.T, np.linalg.inv(S)))
            self.x = self.x + np.dot(k, y)
            self.P = np.dot((self.I - np.dot(k, self.H)), self.P)
        return self.x#[0:2] # (x,y)matrix 2x1
    def prediction(self):
        """
        Estima medida futura
        x'=FX + U
        P'=FPtrans(F) + Q
        :return:
        """
        # sem oclusão
        if self.flag:
            self.x=np.dot(self.F,self.x)#+self.u
            self.P = np.dot(self.F,np.dot(self.P,self.F.T))+self.Q
            self.lastResult=self.x[0:2]
        # com coclusao
        else:
            self.x = np.dot(self.F, self.x) # +self.u
            self.P = np.dot(self.F, np.dot(self.P, self.F.T)) + self.Q2
            self.lastResult = self.x[0:2]



# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 11:24:38 2020

@author: nasredine
"""
import matplotlib.pyplot as plt
from Stripe_parser import *
from Voltage_parser import *
import numpy as np




def MagneticField(x,y,xA,xB,yA,yB,current):
    const = 1.0 * 10**(-7) # const = mu/4pi

    r1 = np.sqrt((x-xA)**2+(y-yA)**2)
    r2 = np.sqrt((x-xB)**2+(y-yB)**2)
    L = np.sqrt((xB-xA)**2+(yB-yA)**2)
    CosTheta1 = (r2**2 - r1**2 - L**2)/(2*L*r1)
    CosTheta2 = (r2**2 - r1**2 + L**2)/(2*L*r2)
    distance = np.sqrt(2*r1**2*r2**2+2*r1**2*L**2+2*r2**2*L**2-r1**4-r2**4-L**4)/(2*L)
    Bfield = const * current * (CosTheta2 - CosTheta1)/distance
    return Bfield




def TotalField(current_idx):
    x=[]
    y=[]
    start_gridx = 0#-10*10**(-6)
    end_gridx = 400*10**(-6)
    start_gridy = 0#-10*10**(-6)
    end_gridy = 400*10**(-6)
    segments = 300
    
    x_delta = (end_gridx-start_gridx)/segments
    y_delta = (end_gridy-start_gridy)/segments
    for i in range(1,segments):
        x.append(start_gridx + x_delta*i)
    for ii in range(1,segments):
        y.append(start_gridy + y_delta*ii)

#    x = np.linspace(0,1600,200)
#    y = np.linspace(0,1600,200)
    X,Y = np.meshgrid(x,y)
    #wire=gridPlot('vdd','AES.def')
    wire=probe_generator_segmented(10,'AES.def','vdd')
    xA,yA,xB,yB = [] ,[] , [], []
    xAn = wire [0][0]
    xBn = wire [0][1]
    yAn = wire [1][0]
    yBn = wire [1][1]
    for i,ii,iii,iiii in zip(xAn,yAn,xBn,yBn):
        xA.append(i*10**(-9))
        yA.append(ii*10**(-9))
        xB.append(iii*10**(-9))
        yB.append(iiii*10**(-9))
    #print ([xA,xB])
    #current = Current('FULL_AES_Voltage_probe.txt','FULL_AES_VOLTAGE_PROBE.dump_pwl','FULL_AES_Resistance_probe.txt','FULL_AES_RESISTANCE_PROBE.effr')
    #current = Current('Voltage_probe.txt','tran_vdd.ptiavg123.dump_pwl','Resistance_probe.txt','effr123.rpt')
    current = Current('NEW_AES/FULL_AES_Voltage_probe.txt','NEW_AES/tran_vdd.ptiavg (8).dump_pwl','NEW_AES/FULL_AES_Resistance_probe.txt','NEW_AES/vdd (8).effr')

    Field = []
    Total_Field = []
    #print (xA[0],xB[0],yA[0],yB[0],current[0][0])
    #Mag = MagneticField(x,y,wire[1],current[0][0])
    #print (len(current[0]))
    print ('Calculating magnetic field . . .' )
    
    
    
    Total_Field = []
    for i in range(0,len(current)-1):
        Mag = []
        Mag = MagneticField (X , Y , xA[i],xB[i],yA[i],yB[i] , current[i][current_idx] )
        Field.append(Mag)
    for i in range (0, len(Field[0])):
        tmp = 0
        for j in range (0, len(Field)):
            tmp = tmp + Field[j][i]
        Total_Field.append(tmp)
    #plt.pcolor(Mag, vmin=-1*(10**(-15)), vmax=-1*(10**(-11)))
    
    
    
    negative_field = np.zeros((len(Total_Field),len(Total_Field[0])))
    for c,i in enumerate(Total_Field):
        for cc,ii in enumerate(i):
            if (ii < 0):
                negative_field[c][cc] = ii
            else:
                negative_field[c][cc] = 0
                
    positive_field = np.zeros((len(Total_Field),len(Total_Field[0])))
    for c,i in enumerate(Total_Field):
        for cc,ii in enumerate(i):
            if (ii > 0):
                positive_field[c][cc] = ii
            else:
                positive_field[c][cc] = 0    
    
    
    minn = []
    maxx = []
    for i in Total_Field:
        minn.append(min(i))
        maxx.append(max(i))
    print ('minimum B field is = ',min(minn) , ' max is = ', max(maxx))
    plt.figure("total magnetic field",figsize=(12,14))
    
    return plt.pcolormesh(X,Y,positive_field,vmin=0,vmax=0.001396394568209751)#-0.0005665265102547159

    

    
    
    
   
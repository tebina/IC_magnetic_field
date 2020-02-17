# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 09:30:25 2020

@author: nasredine
"""

import matplotlib.pyplot as plt
import numpy as np

from utils import *

    

def Voltage_parser(source_file,probe_file):
    print ('parsing voltage values . . .')
    file = open (source_file)
    list = file.readlines()
    probe_data=[]
    probe_vect = []
    for line in list:
            probe_data=[]
            temp = split_space(line)
            word = temp[0]
            ff = open (probe_file)
            list2 = ff.readlines()
            for line2 in list2:    
                parts = split_semic(line2)
                if (len(parts)>0):
                    if (parts[0]==word):
                        data = split_space(parts[2])
                        for i in data[2:]:
                            probe_data.append(float(i))
            if (len(probe_data) !=0) :
                probe_vect.append(probe_data)
    print ('parsing done')
    return probe_vect                        
            


    
def vectors_def(source_file,probe_file):
    print ('creating time and voltage vectors . . .')
    vect_temp = Voltage_parser(source_file,probe_file)
    time_vect_out = []
    data_vect_out = []
    time_vect = []
    data_vect = []
    for t in vect_temp:
        time_vect=[]
        data_vect=[]
        for c,i in enumerate(t):
            if  (c % 2 == 0):
                time_vect.append(i)
            
            else:
                data_vect.append(i)
        time_vect_out.append(time_vect)
        data_vect_out.append(data_vect)
    return time_vect_out,data_vect_out

def d_plot(source_file,probe_file):
    vect = vectors_def(source_file,probe_file)
    time = vect[0]
    data = vect[1]
    plt.figure(figsize=(12,6))
    plt.plot(time[0] , data[50] , lw=1 , color = 'red' , label= 'Magnetic Field')
    

def Diff_Voltage (source_file,probe_file):
    print ('calculating voltage in each segment ...')
    vect = vectors_def(source_file,probe_file)
    time = vect[0]
    time = time [0]
    data = vect[1]
    odd_data = []
    even_data = []
    Voltage_all = []
    for c,i in enumerate(data):
        if  (c % 2 == 0):
            even_data.append(i)
            
        else:
            odd_data.append(i)
    for i,j in zip((even_data),(odd_data)):
        Voltage = []
        for x,y in zip(i,j):
            Voltage.append(y-x)
        Voltage_all.append(Voltage)
    
    return Voltage_all


def res_parse(source_file,data_file):
    print ('parsing resistance . . .' )
    res=[]
    f = open (source_file)
    list = f.readlines()
    for line in list:
        temp = split_space(line)
        word = temp[6]
        ff = open (data_file)
        list2 = ff.readlines()
        for line2 in list2:
            temp2 = split_space(line2)
            if (len(temp2)>3):
                if temp2[2] == word:
                    res.append(temp2[1])
    return res



def Current (voltage_source_file,voltage_probe_file,res_source_file,res_probe_file):
     print ('calculating current values . . .' )
     res = res_parse(res_source_file,res_probe_file)
     voltage = Diff_Voltage(voltage_source_file,voltage_probe_file)
     current = []
     for c,i in enumerate(voltage):
         current_temp = []
         for ii in i:
             current_temp.append(ii/float(res[c]))
         current.append(current_temp)
     t=max(current[0]) 
     for c,i in enumerate(current[0]):
         if (i==t):
             max_idx = c 
     print ('max_idx = ',max_idx)
     print ('max_value = ',t)

     tt=min(current[0])
     for c,i in enumerate(current[0]):
         if (i==tt):
             min_idx = c 
     print ('min_idx = ',min_idx)
     #plt.plot (current[61])
     print ('min_value = ',tt)
     return current
  
    
    
    

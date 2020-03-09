# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 11:52:24 2020

@author: nasredine
"""

import matplotlib.pyplot as plt 
from utils import *


def parser(text_file):
    """ parse defined grid component type from DEF file
    """
    file = open (text_file)
    list = file.readlines()
    start_points = []
    end_points = []
    for line in list :
        if line != '\n': #skip empty lines
            #parts = split_plus(line)
            #each_part2 = split_space(parts[0])
            each_part2 = split_space(line) 
            if each_part2[0] == '-': 
                if each_part2[1] == 'vdd':
                    net = 'vdd'
                elif each_part2[1] == 'gnd':
                    net = 'gnd'
            if  each_part2[0] == 'NEW':  
                if each_part2[2] != '0':
                    if each_part2[5] in ('BLOCKRING','RING','STRIPE','FOLLOWPIN'):#,'FOLLOWPIN')
                        pt1 = (each_part2[1] , net , int (each_part2[7]), int(each_part2[8])) # nano
                        start_points.append(pt1)
                        if (each_part2[11])== '*' :
                            pt2 = (each_part2[1] , net , int (each_part2[7]), int(each_part2[12]))
                        elif each_part2 [12] == '*':
                            pt2 = (each_part2[1] , net , int (each_part2[11]), int(each_part2[8]))                      
                        end_points.append(pt2)
            elif  (each_part2[0]=='+' and each_part2[1]=='ROUTED') :  
                if each_part2[3] != '0':
                    if each_part2[6] in ('BLOCKRING','RING','STRIPE','FOLLOWPIN'):#,'FOLLOWPIN')
                        pt1 = (each_part2[2] , net , int (each_part2[8]), int(each_part2[9])) # nano
                        start_points.append(pt1)
                        if (each_part2[12])== '*' :
                            pt2 = (each_part2[2] , net , int (each_part2[8]), int(each_part2[13]))
                        elif each_part2 [13] == '*':
                            pt2 = (each_part2[2] , net , int (each_part2[12]), int(each_part2[9]))                      
                        end_points.append(pt2)
    
    
    return (start_points,end_points)

def gridPlot (net , text_file):
    """ plot grid from coordinates parsed from parser
    """
    var = parser(text_file)
    start_points_temp = var [0]
    end_points_temp = var [1]
    start_points =[]
    end_points = []
    if net == 'gnd':
        for i in start_points_temp:
            for ii in i :
                
                if ii == 'gnd' :
                    start_points.append(i)
        for p in end_points_temp:
            for pp in p :
                if pp == 'gnd' :
                    end_points.append(p)
    
    if net == 'vdd':
        for i in start_points_temp:
            for ii in i :
                if ii == 'vdd' :
                    start_points.append(i)
        for p in end_points_temp:
            for pp in p :
                if pp == 'vdd' :
                    end_points.append(p) 
    
    start_x_cord = []
    start_y_cord = []
    end_x_cord = []
    end_y_cord = []
    for q in start_points:
        start_x_cord.append(q[2])
        start_y_cord.append(q[3])
    for qq in end_points:
        end_x_cord.append (qq[2])
        end_y_cord.append (qq[3])

    x_values = [start_x_cord , end_x_cord]
    y_values = [start_y_cord , end_y_cord]    
    
    #plt.figure(figsize=(12,12))
    #plt.plot (x_values, y_values)
    #plt.show()
    return [x_values , y_values]   #in nano             

def probing_points(segments,text_file,net):
    """ generate probing model by splitting every line into segments 
        the number of segments per line can be defined 7
        inorder to be more close or distant from the extremeties of the lines 
        """
    temp = parser(text_file)
    start_points_temp = temp [0]
    end_points_temp = temp [1]
    start_points =[]
    end_points = []
    if net == 'gnd':
        for i in start_points_temp:
            for ii in i :
                
                if ii == 'gnd' :
                    start_points.append(i)
        for p in end_points_temp:
            for pp in p :
                if pp == 'gnd' :
                    end_points.append(p)
    
    if net == 'vdd':
        for i in start_points_temp:
            for ii in i :
                if ii == 'vdd' :
                    start_points.append(i)
        for p in end_points_temp:
            for pp in p :
                if pp == 'vdd' :
                    end_points.append(p) 
    start_x_cord = []
    start_y_cord = []
    end_x_cord = []
    end_y_cord = []
    metal =[]
    for t in start_points:
        for ii in range(1, segments):
            metal.append(t[0])

    for q in start_points:
        start_x_cord.append(float(q[2]))
        start_y_cord.append(float(q[3]))
    for qq in end_points:
        end_x_cord.append (float(qq[2]))
        end_y_cord.append (float(qq[3]))

    x_delta = []
    y_delta = []

    for i,ii in zip(start_x_cord,end_x_cord):
        x_delta.append((ii - i)/ segments)
            
    for i,ii in zip(start_y_cord,end_y_cord):
        y_delta.append((ii - i)/ segments)
    
    x_points = []
    y_points = []

    for c , i in enumerate (start_x_cord):
        #x_points= []
        for ii in range(1, segments):
            x_points.append(i + ii * x_delta[c])
        #x_points_cord.append(x_points)
    for c , i in enumerate (start_y_cord):
        #y_points= []
        for ii in range(1, segments) :
            y_points.append(i + ii * y_delta[c])
            
        #y_points_cord.append(y_points)
    
    #plt.figure(figsize=(12,12))
    #plt.plot (x_points, y_points,'ro')
    #plt.show()

    return x_points , y_points ,metal
    
    
           
def probe_generator_segmented (segments_pre_line , text_file , net):
    """
    """
    points_per_line = (segments_pre_line*10)+1
    temp = probing_points (points_per_line , text_file , net)
    x_coords = temp [0]
    y_coords = temp [1]
    metal = temp [2]
    start_x_coord = []
    end_x_coord = []
    start_y_coord = []
    end_y_coord = []
    f = open ("FULL_AES_Voltage_probe.txt","w+")
    for i in range(0,len(x_coords)-1):
        if (i % ((points_per_line-1)/segments_pre_line) == 0):
            f.write("Probe"+str(i)+" %f %f %s %s\n" % (x_coords[i]/1000,y_coords[i]/1000,metal[i],net))
        if ((i+1) % ((points_per_line-1)/segments_pre_line) == 0):
            f.write("Probe"+str(i)+" %f %f %s %s\n" % (x_coords[i]/1000,y_coords[i]/1000,metal[i],net))
        #for ii in range (1,segments_per_line):
           # print (x_coords[ii],y_coords[ii],metal[i])
    f.close
    ff = open ("FULL_AES_Resistance_probe.txt","w+")        
    print (len(x_coords))
    for i in range(0,len(x_coords)):
        if (i % ((points_per_line-1)/segments_pre_line) == 0) : 
            ff.write("%f %f %s " % (x_coords[i]/1000,y_coords[i]/1000,str(metal[i])))
            #print ('START POINT',i, 'is ', x_coords[i]/1000)
            start_x_coord.append(x_coords[i])
            
            start_y_coord.append(y_coords[i])
        if ((i+1) % ((points_per_line-1)/segments_pre_line) == 0):
            ff.write("%f %f %s SEGMENT%s\n" % (x_coords[i]/1000,y_coords[i]/1000,str(metal[i]),str(i)))
            #print ('END POINT',i, 'is ', x_coords[i]/1000)
            end_x_coord.append(x_coords[i])
            end_y_coord.append(y_coords[i])
    ff.close    
    x_values = [start_x_coord , end_x_coord]
    y_values = [start_y_coord , end_y_coord]    
    
    plt.figure(figsize=(12,12))
    plt.plot (x_values, y_values)
    plt.show()
    return [x_values , y_values] 
       
    
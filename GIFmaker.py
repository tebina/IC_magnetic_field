# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 15:11:24 2020

@author: Nasreddine
"""

from utils import *
import numpy as np
import matplotlib.pyplot as plt
from MagneticFieldGen import *
import glob
import imageio

def animate(start_idx,end_idx):
    array = np.linspace(start_idx,end_idx,(end_idx-start_idx)+1,dtype = int)
    for i in array:
        magnetic_plot = TotalField(i)
        plt.colorbar()
        plt.savefig('NEW_GIF/figure_'+str(i)+'.png')
        plt.clf()
    plt.close
    file_list = glob.glob('NEW_GIF/*.png') # Get all the pngs in the current directory
    list.sort(file_list, key=lambda x: int(x.split('_')[2].split('.png')[0])) # Sort the images by #
    
    
    images = list()
    for y in range(start_idx,end_idx+1):
        images.append(imageio.imread('NEW_GIF/figure_' + str(y) + '.png'))
    imageio.mimsave("NEW_GIF/Magnetic_emission.gif", images)
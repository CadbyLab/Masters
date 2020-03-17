#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 16:07:36 2020

@author: mattarnold
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import im_func_lib as funci
import sys

input_data = '/Users/mattarnold/iCloud Drive (Archive)/Documents/Documents – Matt’s MacBook Pro/Uni/Imaging Msc/semester 2/Python Module/PTC'#sys.argv[1]
files = funci.get_file_list(input_data) 


def ptc_crop(file_list,crop_size):
    dark_frame = np.load('dark_frame.npy')
    
    num_files = len(file_list)
    data_table = np.zeros((num_files,2))
    
    crop_bbox = np.load('crop_box.npy')
    
    y_low, y_high, x_low, x_high = crop_bbox[0,0],crop_bbox[0,1],crop_bbox[1,0],crop_bbox[1,1]
    for I in range(num_files):
        work_img = funci.load_img(files[I])
        for J in range(np.size(work_img,2)):
            work_img[:,:,J] = np.subtract(work_img[:,:,J],dark_frame)
        crop_image = work_img [y_low : y_high, x_low : x_high,:]
        
        
        data_table[I,0] = np.mean(crop_image)
        data_table[I,1] = np.std(crop_image)
    return print(data_table) #np.save('mean_std_data',data_table)
    
test = ptc_crop(files,50)
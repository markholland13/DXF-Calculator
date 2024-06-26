#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 21:56:27 2018

@author: Laurent Rudloff
"""

import numpy as np
import pandas as pd
import os
import sys
import time

# Used to create the needed folders
from folderinit import FolderInit
from dxfreader import DxfParser, plot_dxf


createpics = True


start = time.time()

# Initiate the folders
folderinit= FolderInit([('..', 'A1 - Estimate', ),
                        ('..', 'B1 - Reports', ),
                        ('..', 'C1 - Train', 'Dxf',),
                        ('..', 'C1 - Train', 'Targets',),
                        ('..', 'X2 - Backup',),
                        ('..', 'Y2 - Sample DXF',),
                        ])

# Early stop if all the folders not pre-existing
folderinit.projectverification()
if not folderinit.valid:
    print()
    sys.exit('All the folders have been initiated, please restart program')


# DXF parser setting and dataset definition
dxfparser = DxfParser(min_edge_length=1,
                        roundigexp=3,
                        max_distance_correction=1.5)

dxffolder = '../Y2 - Sample DXF' #os.path.join('..', 'Y2 - Sample DXF')
dxflist = [os.path.join(dxffolder, file) for file in os.listdir(dxffolder) if file.endswith('.dxf')]
columns = ['cut_length', 'num_closed_patterns', 'num_open_patterns', 'total_area', 'minimum_rectangle_area',
           'minimum_rectangle_dim1', 'minimum_rectangle_dim2', 'convex_hull_area', 'no_hole_area',
           'thickness', 'unit', 'material', 'bend_radius', 'bend_angle', 'bend_direction',
           'deformation_length', 'possible_imperfection', 'bend_bend_distance', 'bend_bend_angle',
           'merged_bend', 'punch_length', 'radius_approx', 'bend_edge_distance', 'bend_edge_angle',
           'bend_edge_length']

# Dataset construction
dataset = pd.DataFrame(columns=columns)
totalfiles = len(dxflist)
counter = 0
valid = 0

print('Pandas version -->', pd.__version__)

for dxffile in dxflist[:]:
    counter += 1
    details = {}
    name = os.path.split(dxffile)[-1].split('.')[0]
    try:
        details = dxfparser.parse(dxffile)
        dataset.loc[name] = [details.get(x, np.nan) for x in dataset.columns]
        print('{:05d} / {}'.format(counter, totalfiles), name, '- OK')
        if createpics:
            plot_dxf(details, name, '../B1 - Reports')
        valid += 1
    except:
        dataset.loc[name] = [details.get(x, 'ERROR') for x in dataset.columns]
        print('{:05d} / {}'.format(counter, totalfiles), name, '- ERROR')



dataset.to_csv('../B1 - Reports/dataset.csv')

end = time.time()
timespent = (end-start)/60

print('DONE ! --> {} files parsed in {:.2f} minutes'.format(valid, timespent))


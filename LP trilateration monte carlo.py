# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 18:47:19 3306

@author: CMDR CodexNecro81s
"""

from tqdm import tqdm
import EDSM_lib
import numpy as np
import math
import miniball


# # Dixon Dock example in HR 2551
# systems = {'Col 285 Sector FG-X d1-49':{'min':36,'max':39},
#             'Hyades Sector EB-X d1-59':{'min':40,'max':43},
#             'Hyades Sector IR-U b3-5':{'min':34,'max':38}}

# # Herpin Research Base in Wregoe HV-Z b15-0
# systems = {'Wregoe CU-B B15-0':{'min':26,'max':28},
#             'Wregoe YY-B B15-0':{'min':39,'max':41},
#             'Wregoe NW-X B16-0':{'min':38,'max':41}}

# 34 Virginis Abandoned SRV
systems = {'Mel 111 Sector BL-O B6-0':{'min':37,'max':40},
            'HIP 63386':{'min':47,'max':50},
            'Col 285 Sector CI-V b18-0':{'min':62,'max':64}}

#number of random points inside bounding box of source systems
sample_size = 100000

print('Getting source system coordinates')
results = {}
for system in tqdm(systems):
    result = EDSM_lib.GetSystemsData(system,1,1,1)
    results[system] = {'coords':{'x':0,'y':0,'z':0}}
    results[system]['coords']['x'] = result[0]['coords']['x']
    results[system]['coords']['y'] = result[0]['coords']['y']
    results[system]['coords']['z'] = result[0]['coords']['z']

#Calculating bounding box  
bounds = {}
bounds['xmin'] = min([results[key]['coords']['x'] for key in results.keys()])
bounds['xmax'] = max([results[key]['coords']['x'] for key in results.keys()])
bounds['ymin'] = min([results[key]['coords']['y'] for key in results.keys()])
bounds['ymax'] = max([results[key]['coords']['y'] for key in results.keys()])
bounds['zmin'] = min([results[key]['coords']['z'] for key in results.keys()])
bounds['zmax'] = max([results[key]['coords']['z'] for key in results.keys()])

#Generating random points in bounding box
print('Generating points')
points = [np.random.uniform(low=bounds['xmin'], high=bounds['xmax'], size=(sample_size,)),
          np.random.uniform(low=bounds['ymin'], high=bounds['ymax'], size=(sample_size,)),
          np.random.uniform(low=bounds['zmin'], high=bounds['zmax'], size=(sample_size,))]
points = np.transpose(np.array(points))

#Checking points that match source system criteria
print('Testing points')
pts_in_range = []
for [x,y,z] in tqdm(points):
    inRange = True
    for system in results:
        dist = math.sqrt((results[system]['coords']['x'] - x)**2 +
                         (results[system]['coords']['y'] - y)**2 +
                         (results[system]['coords']['z'] - z)**2)
        if((dist > systems[system]['max']) or
           (dist < systems[system]['min'])):
            inRange = False
    if inRange:
        pts_in_range.append([x,y,z])

#Calculating valid points bounding sphere
pts_in_range = np.array(pts_in_range)
C, r2 = miniball.get_bounding_ball(pts_in_range)

#Get known systems in sphere
print('Fetching targets')
targets = EDSM_lib.GetSphereSystemsXYZ(C[0],
                                      C[1],
                                      C[2],
                                      math.sqrt(r2),
                                      0,
                                      1,
                                      1,
                                      1,
                                      1,
                                      1)

targets = sorted(targets, key= lambda i: i['distance'], reverse=False)

print('Target center', C);
print('Target radius', math.sqrt(r2));
print('Known targets nearby:')
print('{:30} {:3}'.format('Name', 'Distance'))
for target in targets:
    print('{:30} {:3}'.format(target['name'], target['distance']))

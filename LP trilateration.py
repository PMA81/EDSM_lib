# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 01:19:01 3306

@author: CMDR CodexNecro81
"""

from operator import itemgetter
from tqdm import tqdm
import EDSM_lib

# # Dixon Dock example, will rank HR 2551 highest
# systems = {'Col 285 Sector FG-X d1-49':{'min':36,'max':39},
#            'Hyades Sector EB-X d1-59':{'min':40,'max':43},
#            'Hyades Sector IR-U b3-5':{'min':34,'max':38}}

# # Herpin Research Base
# systems = {'Wregoe CU-B B15-0':{'min':26,'max':28},
#            'Wregoe YY-B B15-0':{'min':39,'max':41},
#            'Wregoe NW-X B16-0':{'min':38,'max':41}}

# 34 Virginis Abandoned SRV ' need to increase range by 1ly to work...
systems = {'Mel 111 Sector BL-O B6-0':{'min':36,'max':41},
           'HIP 63386':{'min':46,'max':51},
           'Col 285 Sector CI-V b18-0':{'min':61,'max':65}}

results = {}
for system in tqdm(systems):
    result = EDSM_lib.GetSystemsData(system,1,1,1)
    results[system] = {'coords':{'x':0,'y':0,'z':0},'targets':[]}
    results[system]['coords']['x'] = result[0]['coords']['x']
    results[system]['coords']['y'] = result[0]['coords']['y']
    results[system]['coords']['z'] = result[0]['coords']['z']
    results[system]['targets'] = EDSM_lib.GetSphereSystemsXYZ(result[0]['coords']['x'],
                                                              result[0]['coords']['y'],
                                                              result[0]['coords']['z'],
                                                              systems[system]['max'],
                                                              systems[system]['min'],
                                                              1,
                                                              1,
                                                              1,
                                                              1,
                                                              1)

ranks = {}
for system in results:
    for target in results[system]['targets']:
        if(target['name'] in ranks):
            ranks[target['name']]['hits'] += 1;
        else:
            ranks[target['name']] = {'name':target['name'],
                                     'coords':{'x':target['coords']['x'],
                                               'y':target['coords']['y'],
                                               'z':target['coords']['z']},
                                     'hits':0}

ranks = sorted(ranks.values(), key=itemgetter('hits'), reverse=True)

print()
print('{:30} {:3}'.format('System', 'Hits'))
for system in ranks:
    if(system['hits']>0):
        print('{:30} {:3}'.format(system['name'], system['hits']))

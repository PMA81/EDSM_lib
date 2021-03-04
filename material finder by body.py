# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 15:45:49 2021

@author: CMDR CodexNecro81
"""
from tqdm import tqdm

import requests
import EDSM_lib
import numpy as np

import six
import sys
sys.modules['sklearn.externals.six'] = six
import mlrose

from collections import deque

current_location = "Shinrarta Dezhra"
max_distance = 500
material = "Technetium"

prefix = 'https://api.canonn.tech:2053/bodies?material_contains=' + material

# bodies with materials in sites
ap_url = prefix + '&apsites_null=false' #amphora plants
bm_url = prefix + '&bmsites_null=false' #bark mounds
bt_url = prefix + '&btsites_null=false' #brain trees
cs_url = prefix + '&cssites_null=false' #crystalline shards
fg_url = prefix + '&fgsites_null=false' #fungal gourds
fm_url = prefix + '&fmsites_null=false' #fumaroles
gv_url = prefix + '&gvsites_null=false' #gas vents
gy_url = prefix + '&gysites_null=false' #geysers
ls_url = prefix + '&lssites_null=false' #lava spouts
tw_url = prefix + '&twsites_null=false' #tube worms

url_list = []
url_list.append(ap_url)
url_list.append(bm_url)
url_list.append(bt_url)
url_list.append(cs_url)
url_list.append(fg_url)
url_list.append(fm_url)
url_list.append(gv_url)
url_list.append(gy_url)
url_list.append(ls_url)
url_list.append(tw_url)

def contains_material(value):
    return value.lower() == material.lower()

print()
print('Fetching sites...')
results_by_page = 100

request=[]
for url in tqdm(url_list):
    start = 0
    http_request = requests.get(url + '&_limit=' + str(results_by_page))
    temp = http_request.json()
    
    while len(temp)>0:
       for body in temp:
            body['url']=url
            body['site_type']=''
            if(len(body['apsites'])>0):
                body['site_type']+='Ap'
            if(len(body['bmsites'])>0):
                body['site_type']+='Bm'
            if(len(body['btsites'])>0):
                body['site_type']+='Bt'
            if(len(body['cssites'])>0):
                body['site_type']+='Cs'
            if(len(body['fgsites'])>0):
                body['site_type']+='Fg'
            if(len(body['fmsites'])>0):
                body['site_type']+='Fm'
            if(len(body['gvsites'])>0):
                body['site_type']+='Gv'
            if(len(body['gysites'])>0):
                body['site_type']+='Gy'
            if(len(body['lssites'])>0):
                body['site_type']+='Ls'
            if(len(body['twsites'])>0):
                body['site_type']+='Tw'
                
       start+=results_by_page
       http_request = requests.get(url +
                                   '&_limit=' + str(results_by_page) +
                                   '&_start=' + str(start))
       temp = http_request.json()
       request.extend(temp)

current_location_info = EDSM_lib.GetSysData(current_location,1,1)

close_sites=[]

systemlen = 6
bodylen = 4
typelen = 4
distlen = 4
coords_list = []

print()
print('Filtering...')

for body in tqdm(request):
    distance = (body['system']['edsmCoordX'] - current_location_info['coords']['x'])**2
    distance += (body['system']['edsmCoordY'] - current_location_info['coords']['y'])**2
    distance += (body['system']['edsmCoordZ'] - current_location_info['coords']['z'])**2
    distance = np.sqrt(distance)
    mp = map(contains_material, body['material'].keys())
    if((distance < max_distance) and
       (any(mp) == True)):
        body['distance'] = distance
        close_sites.append(body)
        coords_list.append((body['system']['edsmCoordX'],
                            body['system']['edsmCoordY'],
                            body['system']['edsmCoordZ']))
        systemlen = max(systemlen, len(body['system']['systemName']))
        bodylen = max(bodylen, len(body['bodyName']) - len(body['system']['systemName']))
        typelen = max(typelen, len(body['site_type']))
        if(distance>0):
            distlen = max(distlen, max(int(np.ceil(np.log10(distance))),2))

close_sites = sorted(close_sites, key = lambda i: i['distance'], reverse=False)

print()
print('Total systems filtered:', '{}'.format(len(close_sites)), ', plotting...')


# # Initialize fitness function object using coords_list
# fitness_coords = mlrose.TravellingSales(coords = coords_list)

# problem_fit = mlrose.TSPOpt(length = len(coords_list), fitness_fn = fitness_coords,
#                             maximize=False)

# # # Solve problem using simulated annealing
# # best_state, best_fitness = mlrose.simulated_annealing(problem_fit,
# #                                                       random_state = 2,
# #                                                       schedule=mlrose.GeomDecay(),
# #                                                       max_attempts=200)

# # Solve problem using random hill climb
# best_state, best_fitness = mlrose.hill_climb(problem_fit,
#                                               random_state = 2)

# seq = [x['distance'] for x in close_sites]
# closest_hop = next((index for (index, d) in enumerate(close_sites) if d['distance'] == min(seq)), None)

# d=deque(best_state)
# d.rotate(-list(d).index(closest_hop))

# print()
# print('Total distance:', "{:.3f}".format(best_fitness), 'ly')

# idx=0
# strformat = '{:' + str(max(int(np.ceil(np.log10(len(close_sites)))),2)+1) + '}'
# strformat += ' {:' + str(systemlen) + '}'
# strformat += ' {:' + str(bodylen) + '}'
# strformat += ' {:' + str(typelen) + '}'
# strformat += ' {:' + str(distlen) + '}'
# strformat += ' {:9}'

# print(strformat.format('Hop', 'System', 'Body', 'Type', 'Dist', 'DB'))
# for hop in d:
#     print(strformat.format(idx+1,
#                             close_sites[hop]['system']['systemName'],
#                             close_sites[hop]['bodyName'].replace(close_sites[hop]['system']['systemName']+" ", ""),
#                             close_sites[hop]['site_type'],
#                             int(close_sites[hop]['distance']),
#                             close_sites[hop]['url'].replace(prefix + '&','').replace('_null=false','')
#                             )
#           )
#     idx+=1

# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 17:03:28 2021

@author: CMDR CodexNecro81
"""
import itertools
import numpy as np
from tqdm import tqdm
from operator import itemgetter
import EDSM_lib

rare_list = {
    "Andrade Legacy":{"system":"Aerial","allocation":7,"pad":"L"},
    "Bloch Station":{"system":"Ethgreze","allocation":7,"pad":"L"},
    "Yurchikhin Port":{"system":"Geras","allocation":27,"pad":"L"},
    "Blaauw City":{"system":"Irukama","allocation":16,"pad":"L"},
    "Gustav Sporer Port":{"system":"Goman","allocation":16,"pad":"L"},
    "West Market":{"system":"Karsuki Ti","allocation":18,"pad":"L"},
    "Lave Station":{"system":"Lave","allocation":12,"pad":"L"}
             }

destination = "Luyten's Star"


destination_info = EDSM_lib.GetSysData(destination, showCoordinates='1')

hops=[]

for station in tqdm(rare_list):
    rare_list[station]['info'] = EDSM_lib.GetSysData(rare_list[station]['system'], showCoordinates='1')
    hops.append(station)

# generate permutation list
p = {}
for i in tqdm(range(len(hops))):
    path_station = itertools.permutations(hops,i+1)
    j=1
    p[i+1] = {}
    for stations in path_station:
        last = [
            destination_info['coords']['x'],
            destination_info['coords']['y'],
            destination_info['coords']['z']]
        d_hop = 0
        for station in stations:
            current = [
                rare_list[station]['info']['coords']['x'],
                rare_list[station]['info']['coords']['y'],
                rare_list[station]['info']['coords']['z']]
            d_hop += np.sqrt(
                (current[0] - last[0])**2+
                (current[1] - last[1])**2+
                (current[2] - last[2])**2)
            last = current
        last = [
            destination_info['coords']['x'],
            destination_info['coords']['y'],
            destination_info['coords']['z']]
        d_hop += np.sqrt(
            (current[0] - last[0])**2+
            (current[1] - last[1])**2+
            (current[2] - last[2])**2)

        p[i+1][j] = {"path":stations,"distance":d_hop}
        j+=1

#now select smallest subset form all
minimum = {}
for hops in p:
    min_hop = p[hops][1]
    for path in p[hops]:
        if(p[hops][path]['distance'] < min_hop['distance']):
            min_hop = p[hops][path]
    minimum[hops] = min_hop

#now calculate the cargo space needed
for hops in minimum:
    minimum[hops]['cargo'] = 0
    for station in minimum[hops]['path']:
        minimum[hops]['cargo'] += rare_list[station]['allocation']
    minimum[hops]['rank'] = minimum[hops]['cargo'] / minimum[hops]['distance']
    
s = sorted(minimum.values(), key=itemgetter('rank'), reverse=True)

print()
strformat = '{:.3f} {:.4f} {:5} {}'
strsformat = '{:5} {:6} {:5} {}'
print(strsformat.format('rank', 'distance', 'cargo', 'route'))
for item in s:
    print(strformat.format(
        item['rank'],
        item['distance'],
        item['cargo'],
        np.array(item['path'])))

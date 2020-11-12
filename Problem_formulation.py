# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 09:11:23 2020

@author: Reinier
"""
import numpy as np

Flights = np.array([1,2,3,4])
Flights_arrival = np.array([10,10.5,11,11.5])
Flights_t_stay = np.array([1,1,1,1])
Flights_PAX = np.array([100,200,100,200])

Gates = np.array([1,2,3,4])
Gates_distance = np.array([100,200,300,400])


#Generate Xij's
Xijs = np.zeros(Flights[-1])
for flightnumber in Flights:
    Xi = 'x'+str(flightnumber)
    Xis = np.array([])
    for gatenumber in Gates:
        Xij = Xi+str(gatenumber)
        Xis = np.append(Xis,Xij)
    Xijs = np.vstack([Xijs,Xis])

Xijs = np.delete(Xijs,0,axis=0)

for Xi in Xijs:
    constraint = 'Flight assigned to gate: '
    flag = 0
    while flag < len(Xi):
        if flag == 0:
            constraint = constraint + str(Xi[flag])
        else:
            constraint = constraint + ' + ' + str(Xi[flag])
        flag = flag + 1
    print(constraint+' = 1')
        
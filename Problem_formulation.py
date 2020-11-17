# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 09:11:23 2020

@author: Reinier
"""
import numpy as np
import math
import sys

#i = flight number
#j = gate number

#define flights
Flights = np.array([1,2,3,4])
Flights_arrival = np.array([10,10,10,10])
Flights_class = np.array([4,4,4,4])
Flights_t_stay = np.array([1,1,1,1])
Flights_PAX = np.array([100,200,300,400,])

#define gates
Gates = np.array([1,2,3,4])
Gates_class = np.array([4,4,4,4])
Gates_distance = np.array([1000,2000,3000,4000])

#Check input data for errors
Stop = False
if len(Flights) != len(Flights_arrival):
    print('missing arrival times')
    Stop = True
if len(Flights) != len(Flights_class):
    print('missing flight-gate class compatibility')
    Stop = True
if len(Flights) != len(Flights_t_stay):
    print('missing flight staying times')
    Stop = True
if len(Flights) != len(Flights_PAX):
    print('missing number of passengers for flights')
    Stop = True
if len(Gates) != len(Gates_class):
    print('missing gate class compatibility')
    Stop = True
if len(Gates) != len(Gates_distance):
    print('missing gate distances')
    Stop = True
if Stop:
    sys.exit()
    

#Generate time interval (in hours) array
t_start = 9
t = t_start
t_int = min(Flights_t_stay,)/2
tmax = 13
times = np.array([])
while t <= tmax:
    times = np.append(times,t)
    t += t_int
    
#Generate ait
index = 0
ait = times
while index < len(Flights):
    Arrival = Flights_arrival[index]
    Departure = Arrival + math.ceil(Flights_t_stay[index]/t_int)*t_int
    a = np.array([])
    for time in times:
        if time > (Arrival-t_int) and time+t_int <= (Departure):
            a = np.append(a,1)
        else:
            a = np.append(a,0)
    ait = np.vstack([ait,a])
    index += 1
ait = np.delete(ait,0,axis=0)

#Generate Xij's
Xijs = []
for flightnumber in Flights:
    Xi = 'x'+str(flightnumber)
    Xis = np.array([])
    for gatenumber in Gates:
        Xij = Xi+str(gatenumber)
        Xis = np.append(Xis,Xij)
    Xijs.append(Xis)
    
#DEFINE VARIABLES -------------------------------------------------------------
type_variable = "int+ "

for flight in range(len(Flights)):
    for gate in range(len(Gates)):
        definition = "dvar " + type_variable + Xijs[(flight)][(gate)] + ";"
        print(definition) 
#Print white line
print(" ")
#-----------------------------------------------------------------------------

#Write constraint that each gate has at most one flight at the time. Including compatibility.
time_count = 0
for time in times:
    gate_count = 0
    for gatenumber in Gates: 
        entry = False
        flight_count = 0
        constraint = ""
        constraint_name = "One_Flight_per_gate_for_gate_" + str(gatenumber) + '_at_' + str(round(time,2)) + ": "
        for flightnumber in Flights: 
            Xij = Xijs[(flightnumber -1)][(gatenumber-1)]
            GateClassReq = Flights_class[flight_count] #Check Gate class needed
            GateClassActual = Gates_class[gate_count]  #Check current gate class
            if flightnumber == Flights[-1] and ait[flight_count][time_count]>0:
                if GateClassReq == GateClassActual:
                    constraint += str(Xij)
                    entry = True
                    last = 0
            elif ait[flight_count][time_count]>0:
                if GateClassReq == GateClassActual:
                    constraint += str(Xij) + " + "
                    entry = True
                    last = 1
            flight_count += 1
        if entry:
            #Arithmatic in order to get the code right.
            if last == 1:
                constraint = constraint_name + constraint[:-3] + " <= 1;"
            if last == 0:
                constraint = constraint_name + constraint + " <= 1;"
            print(constraint)
        gate_count += 1
    time_count += 1
print()

#Write constraint that each flight is assigned to one gate at time t
time_count = 0
for time in times:
    flight_count = 0
    for Xi in Xijs:
        entry = False
        constraint = 'Flight_assigned_to_gate_at_' + str(round(time,2)) + ': '
        flag = 0
        while flag < len(Xi):
            if flag == 0 and ait[flight_count][time_count]>0:
                constraint += str(Xi[flag]) 
                entry = True
            elif ait[flight_count][time_count]>0:
                constraint += ' + ' + str(Xi[flag])
                entry = True
            flag += 1
        flight_count += 1
        if entry:

            print(constraint+' == 1;')
    time_count += 1
print()

#Write objective function:
objective = 'Objective: '
Xicount = 0
while Xicount < len(Xijs):
    PAXobjective = Flights_PAX[Xicount]
    Xi = Xijs[Xicount]
    Xijcount = 0
    while Xijcount < len(Xi):
        DistanceObjective = Gates_distance[Xijcount]
        Xij = Xi[Xijcount]
        objective += str(PAXobjective) + '*' + str(DistanceObjective) + '*' + str(Xij) + ' + '
        Xijcount += 1
    Xicount += 1
objective = objective[:-3]
print()
print(objective + ';') 
    


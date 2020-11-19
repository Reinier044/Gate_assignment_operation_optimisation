# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 09:11:23 2020

@author: Reinier
"""
import numpy as np
import math
import sys
import copy

from dataset_generator import Flights,Flights_arrival,Flights_class,Flights_t_stay,Flights_max_tow,Flights_PAX, Gates, Gates_class, Gates_distance

#define storage lists
variables = []
all_core_constraints = []
all_constraints = []


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
if max(Flights_max_tow)>2:
    print('More Toos is currently not supported')
    Stop = True
if Stop:
    sys.exit()
    

#Generate time interval (in hours) array
t_start = 9
t = t_start
t_int = 0.25
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
            if a.size == 0 or a[-1] == 0:
                a = np.append(a,1)
            else:
                a = np.append(a,a[-1]+1)
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

#Generate base Yik's
Yik = []
flightnumber = 0
while flightnumber < len(Flights):
    maxtows = Flights_max_tow[flightnumber]
    tows = 0
    Yi = np.array([])
    while tows-1 < maxtows:
        Yi = np.append(Yi,('y'+str(Flights[flightnumber])+str(tows)))
        tows += 1
    Yik.append(Yi)
    flightnumber += 1

#Generate Yik's for each time iteration
Yik_t = []
for time_count in range(len(times)):
    Yik_temp = []
    for Yi in Yik:
        Yi_temp = np.array([])
        for Y in Yi:
            Yi_temp = np.append(Yi_temp,(Y+'_'+str(time_count)))
        Yik_temp.append(Yi_temp)
    Yik_t.append(Yik_temp)
    
    
#Write constraint that each gate has at most one flight at the time. Including compatibility.
time_count = 0
for time in times:
    gate_count = 0
    for gatenumber in Gates: 
        entry = False
        flight_count = 0
        constraint = ""
        time = round(time,2)
        constraint_name = "Occupied_gate" + str(gatenumber) + '_at_' + str(time).replace(".", "h") + ": "
        for flightnumber in Flights: 
            Xij = Xijs[(flightnumber -1)][(gatenumber-1)]
            GateClassReq = Flights_class[flight_count] #Check Gate class needed
            GateClassActual = Gates_class[gate_count]  #Check current gate class
            maxtows = Flights_max_tow[flight_count] #Check how many tows the flight needs
            if flightnumber == Flights[-1] and ait[flight_count][time_count]>0:
                if GateClassReq == GateClassActual: #Check if flight is compatible with gate
                    #Generate Xijkl's for the gate constraints
                    for tows in range(maxtows+1):
                        for tow in range(tows+1):
                            variable = str(Xij)+str(tows)+str(tow)
                            constraint += variable + " + "
                            variables.append(variable)
                    entry = True
                    last = 0
                constraint = constraint[:-3]
                
            elif ait[flight_count][time_count]>0:
                if GateClassReq == GateClassActual: #Check if flight is compatible with gate
                    for tows in range(maxtows+1):
                        for tow in range(tows+1):
                            variable = str(Xij)+str(tows)+str(tow)
                            constraint += variable + " + "
                            variables.append(variable)
                    entry = True
                    last = 1
            flight_count += 1
        
        if entry:
            #Arithmatic in order to get the code right.
            if last == 1:
                all_core_constraints.append((constraint[:-3] + " <= 1;"))
                constraint = constraint_name + constraint + " <= 1;"
                all_constraints.append(constraint)
            if last == 0:
                all_core_constraints.append((constraint + " <= 1;"))
                constraint = constraint_name + constraint + " <= 1;"
                all_constraints.append(constraint)
        gate_count += 1
    time_count += 1


#Master Flight constraint builder:
#for each time segment
time_count = 0
for time in times:
    
    #For each flight
    flight_count = 0
    for Xi in Xijs:
        entry = False
        time = round(time,2)
        
        #check if aircraft is currently present
        if ait[flight_count][time_count]>0:
            secondpresence = False
            thirdpresence = False
            
            #Aircraft in second stay time segment
            if max(ait[flight_count])>=2:
                secondpresence = True
            if max(ait[flight_count])>=3:
                thirdpresence = True
            
            #For each tow segment
            maxtows = Flights_max_tow[flight_count]
            tows = 0
            constraint = []
            while tows < maxtows:
                if tows == 0:
                    constraint_name = 'Flight' + str(Flights[flight_count])+ '_tow00_at_' + str(time).replace(".", "h") + ': '
                    core_constraint = ''
                    for Xij in Xi:
                        variable = Xij + '00'
                        core_constraint += variable + ' + '
                        variables.append(variable)
                    core_constraint = core_constraint[:-3] + ' - ' + str(Yik[flight_count][0])+'_'+str(time_count) + ' == 0;'
                    all_core_constraints.append(core_constraint)
                    constraint.append(constraint_name + core_constraint)
                    tows +=1
                if tows == 1 and secondpresence:
                    constraint_name = 'Flight' + str(Flights[flight_count])+ '_tow10_at_' + str(time).replace(".", "h") + ': '
                    core_constraint = ''
                    for Xij in Xi:
                        variable = Xij + '10'
                        core_constraint += variable + ' + '
                        variables.append(variable)
                    core_constraint = core_constraint[:-3] + ' - ' + str(Yik[flight_count][1])+'_'+str(time_count) + ' == 0;'
                    all_core_constraints.append(core_constraint)
                    constraint.append(constraint_name + core_constraint)
                    if ait[flight_count][time_count]>=2:
                        constraint_name = 'Flight' + str(Flights[flight_count])+ '_tow11_at_' + str(time).replace(".", "h") + ': '
                        core_constraint = ''
                        for Xij in Xi:
                            variable = Xij + '11'
                            core_constraint += variable + ' + '
                            variables.append(variable)
                        core_constraint = core_constraint[:-3] + ' - ' + str(Yik[flight_count][1])+'_'+str(time_count) + ' == 0;' 
                        all_core_constraints.append(core_constraint)
                        constraint.append(constraint_name + core_constraint)
                    tows +=1
                if tows == 2 and thirdpresence:
                    constraint_name = 'Flight' + str(Flights[flight_count])+ '_tow20_at_' + str(time).replace(".", "h") + ': '
                    core_constraint = ''
                    for Xij in Xi:
                        variable = Xij + '20'
                        core_constraint += variable + ' + '
                        variables.append(variable)
                    core_constraint = core_constraint[:-3] + ' - ' + str(Yik[flight_count][2])+'_'+str(time_count) + ' == 0;'
                    all_core_constraints.append(core_constraint)
                    constraint.append(constraint_name+core_constraint)
                    if ait[flight_count][time_count]>=2:
                        constraint_name = 'Flight' + str(Flights[flight_count])+ '_tow21_at_' + str(time).replace(".", "h") + ': '
                        core_constraint = ''
                        for Xij in Xi:
                            variable = Xij + '21'
                            core_constraint += variable + ' + '
                            variables.append(variable)
                        core_constraint = core_constraint[:-3] + ' - ' + str(Yik[flight_count][2])+'_'+str(time_count) + ' == 0;'
                        all_core_constraints.append(core_constraint)
                        constraint.append(constraint_name+core_constraint)
                    if ait[flight_count][time_count]>=3:
                        constraint_name = 'Flight' + str(Flights[flight_count])+ '_tow22_at_' + str(time).replace(".", "h") + ': '
                        core_constraint = ''
                        for Xij in Xi:
                            variable = Xij + '22'
                            core_constraint += variable + ' + '
                            variables.append(variable)
                        core_constraint = core_constraint[:-3] + ' - ' + str(Yik[flight_count][2])+'_'+str(time_count) + ' == 0;'
                        all_core_constraints.append(core_constraint)
                        constraint.append(constraint_name + core_constraint)
                    tows += 1 
                  
             
        #Only keep constraints that are true with respect to aircraft presence.
            for constrain in constraint:
                all_constraints.append(constrain)
                              
        flight_count += 1
    time_count += 1



#Sum of Yik = 1
Yicount = 0
for Yi in Yik:
    constraint_name = 'Number_tows_Flight'+str(Flights[Yicount]) + ': '
    constraint = ''
    for y in Yi:
        for time_count in range(len(times)):
            y_variable = str(y)+'_'+str(time_count)
            constraint += y_variable +' + '
            variables.append(y_variable)
    Yicount += 1
    constraint = constraint[:-3] + ' == 1;'
    all_core_constraints.append(constraint)
    all_constraints.append(constraint_name + constraint) 
    

#DEFINE VARIABLES -------------------------------------------------------------

variables = list(dict.fromkeys(variables)) #removes duplicates

type_variable = "int+ "

for variable in variables:
        definition = "dvar " + type_variable + variable + ";"
        print(definition) 
print()


#-----------------------------------------------------------------------------


#---------------------------Filter duplicates----------------------------------
original_constraints = copy.copy(all_constraints)
original_cores = copy.copy(all_core_constraints)

#check for duplicate constraints
original_removes = []
deletions = 0
c = 0
while c < len(all_core_constraints):
    c2 = c
    while c2 <= len(all_core_constraints)-deletions:
        if all_core_constraints[c2]== all_core_constraints[c] and c2 != c:
#            print('removed: ' + str(c2))
#            print('original = ' + str(c))
#            print(c2)
#            print(all_core_constraints[c2])
#            print(all_core_constraints[c2])
            original_removes.append(c2)
            deletions +=1
        c2 += 1
    c += 1

#Remove the duplicate constraints
original_removes.sort()
original_removes = list(dict.fromkeys(original_removes))
deletions = 0
for removes in original_removes:
    del all_core_constraints[(removes-deletions)]
    del all_constraints[(removes-deletions)]
    deletions += 1
    
#-----------------------------------------------------------------------------
    
for constraint in all_constraints:
    print(constraint)

           



#Write objective function: REVISE!!!!!!!!
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
    


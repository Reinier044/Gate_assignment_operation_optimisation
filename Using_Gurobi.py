from gurobipy import *
import numpy as np
import math
import sys
import copy

#from test_set_Stijn import Flights,Flights_arrival,Flights_class,Flights_t_stay,Flights_max_tow,Flights_PAX, Gates, Gates_class, Gates_distance, open_time,operating_hours,t_int
#from mini_dataset import Flights,Flights_arrival,Flights_class,Flights_t_stay,Flights_max_tow,Flights_PAX, Gates, Gates_class, Gates_distance, open_time,operating_hours,t_int
#from dataset_generator import Flights,Flights_arrival,Flights_class,Flights_t_stay,Flights_max_tow,Flights_PAX, Gates, Gates_class, Gates_distance,open_time,operating_hours,t_int
from dataset import Flights,Flights_arrival,Flights_class,Flights_t_stay,Flights_max_tow,Flights_PAX, Gates, Gates_class, Gates_distance, open_time,operating_hours,t_int


#define storage lists
variables = []
all_anti_constraints = []
all_anti_core_constraints = []
all_core_constraints = []
all_constraints = []

text_file = open("gurobi_test.txt", "w")
model = Model("Gate Assignment")

#towing cost
t_cost = 1000
t_anti_cost = 0


#Check input data for errors
Stop = False
if len(Flights) != len(Flights_arrival):
    print('missing arrival times \n \n \n')
    Stop = True
if len(Flights) != len(Flights_class):
    print('missing flight-gate class compatibility \n \n \n')
    Stop = True
if len(Flights) != len(Flights_t_stay):
    print('missing flight staying times \n \n \n')
    Stop = True
if len(Flights) != len(Flights_PAX):
    print('missing number of passengers for flights \n \n \n')
    Stop = True
if len(Gates) != len(Gates_class):
    print('missing gate class compatibility \n \n \n')
    Stop = True
if len(Gates) != len(Gates_distance):
    print('missing gate distances \n \n \n')
    Stop = True
if max(Flights_max_tow)>2:
    print('More Toos is currently not supported \n \n \n')
    Stop = True
if Stop:
    sys.exit()
    

#Generate time interval (in hours) array
t_start = open_time
t_dep = []
for i in range(len(Flights_arrival)):
    t_dep.append((Flights_arrival[i] + Flights_t_stay[i]))
t = t_start
tmax = max(t_dep)
times = np.array([])
while t <= tmax+t_int:
    times = np.append(times,t)
    t += t_int
print('time intervals created')

   
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
print('ait created')

#Generate Xij's
#Xijs_var = []
Xijs = []
for flightnumber in Flights:
    Xi = 'x'+str(flightnumber)
    Xis = np.array([])
    #Xis_var = np.array([])
    for gatenumber in Gates:
        Xij = Xi+str(gatenumber)
        #Xij_var = model.addVar(vtype=GRB.INTEGER, name=Xij)
        Xis = np.append(Xis,Xij)
        #Xis_var = np.append(Xis_var, Xij_var)
    Xijs.append(Xis)
    #Xijs_var.append(Xis_var)
print('Xijs created')

#Generate base Yik's
Yik = []
Yik_var = []
flightnumber = 0
while flightnumber < len(Flights):
    maxtows = Flights_max_tow[flightnumber]
    tows = 0
    Yi = np.array([])
    Yi_var = np.array([])
    while tows-1 < maxtows:
        Yi = np.append(Yi,('y'+str(Flights[flightnumber])+str(tows)))
        Y_var = model.addVar(vtype=GRB.INTEGER, name=('y'+str(Flights[flightnumber])+str(tows)))
        Yi_var = np.append(Yi_var, Y_var)
        tows += 1
    Yik.append(Yi)
    Yik_var.append(Yi_var)
    flightnumber += 1
print('Yiks created')

model.update()

#Write constraint that each gate has at most one flight at the time. Including compatibility.
all_x_variables = []
all_x_variables_names = []
time_count = 0
tows_done = np.ones(len(Flights))
tows_done_next = np.ones(len(Flights))
tows_done_old = []
flight_presence = np.zeros(len(Flights))
for time in times:
    gate_count = 0   
    for gatenumber in Gates:
        if gatenumber == Gates[0]:
            tows_done = tows_done_next
            tows_done_old.append(copy.deepcopy(tows_done_next))
        else:
            tows_done = tows_done_old[-1]
            
        entry = False
        flight_count = 0
        constraint = ""
        constraint_var = []
        anti_constraint = ''
        anti_constraint_var = []
        time = round(time,2)
        constraint_name = "Occupied_gate" + str(gatenumber) + '_at_' + str(time).replace(".", "h") + ": "
        anti_constraint_name = "Dont_occupy_gate"+ str(gatenumber) + '_at_' + str(time).replace(".", "h") + ": "

        for flightnumber in Flights:
            #print((maxtows-(tows_done[(flightnumber-1)])))
            Xij = Xijs[(flightnumber -1)][(gatenumber-1)]
            GateClassReq = Flights_class[flight_count] #Check Gate class needed
            GateClassActual = Gates_class[gate_count]  #Check current gate class
            maxtows = Flights_max_tow[flight_count] #Check how many tows the flight needs
            if flightnumber == Flights[-1] and ait[flight_count][time_count]>0:
                if GateClassReq <= GateClassActual: #Check if flight is compatible with gate
                    #Generate Xijkl's for the gate constraints
                    tows = 0
                    while tows < maxtows+1:
                        tow = 0
                        while tow < int(tows_done[flightnumber-1]):
                            #Filter tows that are impossible
                            if (maxtows-(tows_done[(flightnumber-1)]))==1:
                                if tow >0:
                                    break
                                
                            if (maxtows-(tows_done[(flightnumber-1)]))==0:
                                if tows == 0 and tow != 0:
                                    break
                                if tows == 1 and tow != 1 :
                                    tow += 1 
                                if tows == 2 and tow == 0:
                                    tow +=1
                                if tow > 1:
                                    break
                                
                            if int(maxtows-(tows_done[(flightnumber-1)]))<=-1:
                                if tows == 0 and tow != 0:
                                    break
                                if tows == 1 and tow != 1:
                                    tow += 1
                                if tows == 2 and tow != 2:
                                    while tow < 2:
                                        tow += 1 
                                
                                if tow > 2:
                                    break 
                            if tow > tows:
                                break
                            variable = str(Xij)+str(tows)+str(tow)
                            if variable not in all_x_variables_names:
                                all_x_variables_names.append(variable) #add variable name to list
                                variable_var = model.addVar(vtype=GRB.INTEGER, name=variable) #create gurobi variable and add to list
                                all_x_variables.append(variable_var)
                            else:
                                variable_var = all_x_variables[all_x_variables_names.index(variable)]
                            constraint += variable + " + "
                            constraint_var.append(variable_var) #adding all variables for a specific constraint to a list
                            variables.append(variable)
                            tow += 1
                        tows += 1
                    entry = True
                    last = 0
                    tows_store = (tows_done[(flightnumber-1)])+ 1
                    indexes = [flightnumber-1]
                    for index in indexes:
                        tows_done_next[index] = tows_store
                
                #Write constraint that blocks incompatible gate-aircraft combinations                
                else:
                    #Generate Xijkl's for the gate constraints
                    tows = 0
                    while tows < maxtows+1:
                        tow = 0
                        while tow < int(tows_done[flightnumber-1]):
                            #Filter tows that are impossible
                            if (maxtows-(tows_done[(flightnumber-1)]))==1:
                                if tow >0:
                                    break
                                
                            if (maxtows-(tows_done[(flightnumber-1)]))==0:
                                if tows == 0 and tow != 0:
                                    break
                                if tows == 1 and tow != 1 :
                                    tow += 1 
                                if tows == 2 and tow == 0:
                                    tow +=1
                                if tow > 1:
                                    break
                                
                            if int(maxtows-(tows_done[(flightnumber-1)]))<=-1:
                                if tows == 0 and tow != 0:
                                    break
                                if tows == 1 and tow != 1:
                                    tow += 1
                                if tows == 2 and tow != 2:
                                    while tow < 2:
                                        tow += 1 
                                if tow > 2:
                                    break 
                            if tow > tows:
                                break
                            variable = str(Xij)+str(tows)+str(tow)
                            if variable not in all_x_variables_names:
                                all_x_variables_names.append(variable) #add variable name to list
                                variable_var = model.addVar(vtype=GRB.INTEGER, name=variable) #create gurobi variable and add to list
                                all_x_variables.append(variable_var)
                            else:
                                variable_var = all_x_variables[all_x_variables_names.index(variable)]
                            anti_constraint += variable + " + "
                            anti_constraint_var.append(variable_var) #adding all variables for a specific constraint to a list
                            variables.append(variable)
                            tow += 1
                        tows += 1
                    entry = True
                    last = 0
                    tows_store = (tows_done[(flightnumber-1)])
                    indexes = [flightnumber-1]
                    for index in indexes:
                        tows_done_next[index] = tows_store + 1
                constraint = constraint[:-3]
                anti_constraint = anti_constraint[:-3]
                flight_presence[flightnumber-1] = flight_presence[flightnumber-1] + 1
                
            #For the last Xijkl in the 
            elif ait[flight_count][time_count]>0:
                if GateClassReq <= GateClassActual: #Check if flight is compatible with gate
                    tows = 0
                    while tows < maxtows+1:
                        tow = 0
                        while tow < int(tows_done[flightnumber-1]):
                            #Filter tows that have already been done
                            if (maxtows-(tows_done[(flightnumber-1)]))==1:
                                if tow >0:
                                    break
                                
                            if (maxtows-(tows_done[(flightnumber-1)]))==0:
                                if tows == 0 and tow != 0:
                                    break
                                if tows == 1 and tow != 1 :
                                    tow += 1 
                                if tows == 2 and tow == 0:
                                    tow +=1
                                if tow > 1:
                                    break
                                
                            if int(maxtows-(tows_done[(flightnumber-1)]))<=-1:
                                if tows == 0 and tow != 0:
                                    break
                                if tows == 1 and tow != 1:
                                    tow += 1
                                if tows == 2 and tow != 2:
                                    while tow < 2:
                                        tow += 1  
                                if tow > 2:
                                    break 
                            if tow > tows:
                                break
                            variable = str(Xij)+str(tows)+str(tow)
                            if variable not in all_x_variables_names:
                                all_x_variables_names.append(variable) #add variable name to list
                                variable_var = model.addVar(vtype=GRB.INTEGER, name=variable) #create gurobi variable and add to list
                                all_x_variables.append(variable_var)
                            else:
                                variable_var = all_x_variables[all_x_variables_names.index(variable)]
                            constraint += variable + " + "
                            constraint_var.append(variable_var) #adding all variables for a specific constraint to a list
                            variables.append(variable)
                            tow += 1
                        tows += 1
                    entry = True
                    last = 1
                    tows_store = (tows_done[(flightnumber-1)])
                    indexes = [flightnumber-1]
                    for index in indexes:
                        tows_done_next[index] = tows_store + 1
                    
                #Write constraint that blocks incompatible gate-aircraft combinations  
                else: 
                    tows = 0
                    while tows < maxtows+1:
                        tow = 0
                        while tow < int(tows_done[flightnumber-1]):
                            #Filter tows that are impossible
                            if (maxtows-(tows_done[(flightnumber-1)]))==1:
                                if tow >0:
                                    break
                                
                            if (maxtows-(tows_done[(flightnumber-1)]))==0:
                                if tows == 0 and tow != 0:
                                    break
                                if tows == 1 and tow != 1 :
                                    tow += 1 
                                if tows == 2 and tow == 0:
                                    tow +=1
                                if tow > 1:
                                    break
                                
                            if int(maxtows-(tows_done[(flightnumber-1)]))<=-1:
                                if tows == 0 and tow != 0:
                                    break
                                if tows == 1 and tow != 1:
                                    tow += 1
                                if tows == 2 and tow != 2:
                                    while tow < 2:
                                        tow += 1 
                                if tow > 2:
                                    break 
                            if tow > tows:
                                break
                            variable = str(Xij)+str(tows)+str(tow)
                            if variable not in all_x_variables_names:
                                all_x_variables_names.append(variable) #add variable name to list
                                variable_var = model.addVar(vtype=GRB.INTEGER, name=variable) #create gurobi variable and add to list
                                all_x_variables.append(variable_var)
                            else:
                                variable_var = all_x_variables[all_x_variables_names.index(variable)]
                            anti_constraint += variable + " + "
                            anti_constraint_var.append(variable_var)
                            variables.append(variable)
                            tow += 1
                        tows += 1
                    entry = True
                    last = 1
                    tows_store = (tows_done[(flightnumber-1)])
                    indexes = [flightnumber-1]
                    for index in indexes:
                        tows_done_next[index] = tows_store + 1

                          
            flight_count += 1
          

        if entry:
            #Arithmatic in order to get the code right.
            if last == 1:
                if len(constraint)>0:
                    all_core_constraints.append((constraint[:-3] + " <= 1;"))
                    constraint = constraint_name + constraint[:-3] + " <= 1;"
                    all_constraints.append(constraint)
                    #creating the constraint in gurobi
                    gurobi_constraint = 0
                    for var in constraint_var:
                        gurobi_constraint += var
                    model.addConstr(gurobi_constraint, "<= " , 1, name=constraint_name)
                    
                if len(anti_constraint)>0:
                    all_anti_core_constraints.append((anti_constraint[:-3] + " == 0;"))                    
                    anti_constraint = anti_constraint_name + anti_constraint[:-3] + ' == 0;'
                    all_anti_constraints.append(anti_constraint)
                    gurobi_constraint = 0
                    for var in anti_constraint_var:
                        gurobi_constraint += var
                    model.addConstr(gurobi_constraint, "== " , 0, name=anti_constraint_name)
            if last == 0:
                if len(constraint)>0:
                    all_core_constraints.append((constraint + " <= 1;"))
                    constraint = constraint_name + constraint + " <= 1;"
                    all_constraints.append(constraint)
                    #creating the constraint in gurobi
                    gurobi_constraint = 0
                    for var in constraint_var:
                        gurobi_constraint += var
                    model.addConstr(gurobi_constraint, "<= " , 1, name=constraint_name)
                if len(anti_constraint)>0:
                    all_anti_core_constraints.append((anti_constraint + "== 0"))
                    anti_constraint = anti_constraint_name+ anti_constraint + " == 0;"
                    all_anti_constraints.append(anti_constraint)    
                    gurobi_constraint = 0
                    for var in anti_constraint_var:
                        gurobi_constraint += var
                    model.addConstr(gurobi_constraint, "== " , 0, name=anti_constraint_name)

        gate_count += 1
    time_count += 1
print('Constraints for gates created')


for i in range(len(all_anti_constraints)):
    if len(all_anti_constraints[i])>34:
        all_constraints.append(all_anti_constraints[i])
        all_core_constraints.append(all_anti_core_constraints[i])
        
model.update()
#--------------------Master Flight constraint builder--------------------------
Flight_tow_possibilities = np.zeros(len(Flights))
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
                Flight_tow_possibilities[flight_count] = 1
            if max(ait[flight_count])>=3:
                thirdpresence = True
                Flight_tow_possibilities[flight_count] = 2
            #For each tow segment
            maxtows = Flights_max_tow[flight_count]
            tows = 0
            constraint = []
            while tows < maxtows:
                if tows == 0:
                    constraint_name = 'Flight' + str(Flights[flight_count])+ '_tow00_at_' + str(time).replace(".", "h") + ': '
                    core_constraint = ''
                    constraint_var = []
                    for Xij in Xi:
                        variable = Xij + '00'
                        if variable not in all_x_variables_names:
                            all_x_variables_names.append(variable) #add variable name to list
                            variable_var = model.addVar(vtype=GRB.INTEGER, name=variable) #create gurobi variable and add to list
                            all_x_variables.append(variable_var)
                        else:
                            variable_var = all_x_variables[all_x_variables_names.index(variable)]
                        constraint_var.append(variable_var)
                        core_constraint += variable + ' + '
                        variables.append(variable)
                    
                    gurobi_constraint = 0
                    for var in constraint_var:
                        gurobi_constraint += var
                    gurobi_constraint -= Yik_var[flight_count][0]
                    model.addConstr(gurobi_constraint, "== " , 0, name=constraint_name)
                    core_constraint = core_constraint[:-3] + ' - ' + str(Yik[flight_count][0])+ ' == 0;'
                    all_core_constraints.append(core_constraint)
                    constraint.append(constraint_name + core_constraint)
                    tows +=1
                if tows == 1 and secondpresence:
                    constraint_name = 'Flight' + str(Flights[flight_count])+ '_tow10_at_' + str(time).replace(".", "h") + ': '
                    core_constraint = ''
                    constraint_var = []
                    for Xij in Xi:
                        variable = Xij + '10'
                        if variable not in all_x_variables_names:
                            all_x_variables_names.append(variable) #add variable name to list
                            variable_var = model.addVar(vtype=GRB.INTEGER, name=variable) #create gurobi variable and add to list
                            all_x_variables.append(variable_var)
                        else:
                            variable_var = all_x_variables[all_x_variables_names.index(variable)]
                        constraint_var.append(variable_var)
                        core_constraint += variable + ' + '
                        variables.append(variable)
                    gurobi_constraint = 0
                    for var in constraint_var:
                        gurobi_constraint += var
                    gurobi_constraint -= Yik_var[flight_count][1]
                    model.addConstr(gurobi_constraint, "== " , 0, name=constraint_name)
                    core_constraint = core_constraint[:-3] + ' - ' + str(Yik[flight_count][1])+ ' == 0;'
                    all_core_constraints.append(core_constraint)
                    constraint.append(constraint_name + core_constraint)
                    if ait[flight_count][time_count]>=2:
                        constraint_name = 'Flight' + str(Flights[flight_count])+ '_tow11_at_' + str(time).replace(".", "h") + ': '
                        core_constraint = ''
                        constraint_var = []
                        for Xij in Xi:
                            variable = Xij + '11'
                            if variable not in all_x_variables_names:
                                all_x_variables_names.append(variable) #add variable name to list
                                variable_var = model.addVar(vtype=GRB.INTEGER, name=variable) #create gurobi variable and add to list
                                all_x_variables.append(variable_var)
                            else:
                                variable_var = all_x_variables[all_x_variables_names.index(variable)]
                            constraint_var.append(variable_var)
                            core_constraint += variable + ' + '
                            variables.append(variable)
                        gurobi_constraint = 0
                        for var in constraint_var:
                            gurobi_constraint += var
                        gurobi_constraint -= Yik_var[flight_count][1]
                        model.addConstr(gurobi_constraint, "== " , 0, name=constraint_name)
                        core_constraint = core_constraint[:-3] + ' - ' + str(Yik[flight_count][1]) + ' == 0;' 
                        all_core_constraints.append(core_constraint)
                        constraint.append(constraint_name + core_constraint)
                    tows +=1
                if tows == 2 and thirdpresence:
                    constraint_name = 'Flight' + str(Flights[flight_count])+ '_tow20_at_' + str(time).replace(".", "h") + ': '
                    core_constraint = ''
                    constraint_var = []
                    for Xij in Xi:
                        variable = Xij + '20'
                        if variable not in all_x_variables_names:
                            all_x_variables_names.append(variable) #add variable name to list
                            variable_var = model.addVar(vtype=GRB.INTEGER, name=variable) #create gurobi variable and add to list
                            all_x_variables.append(variable_var)
                        else:
                            variable_var = all_x_variables[all_x_variables_names.index(variable)]
                        constraint_var.append(variable_var)
                        core_constraint += variable + ' + '
                        variables.append(variable)
                    gurobi_constraint = 0
                    for var in constraint_var:
                        gurobi_constraint += var
                    gurobi_constraint -= Yik_var[flight_count][2]
                    model.addConstr(gurobi_constraint, "== " , 0, name=constraint_name)
                    core_constraint = core_constraint[:-3] + ' - ' + str(Yik[flight_count][2])+ ' == 0;'
                    all_core_constraints.append(core_constraint)
                    constraint.append(constraint_name+core_constraint)
                    if ait[flight_count][time_count]>=2:
                        constraint_name = 'Flight' + str(Flights[flight_count])+ '_tow21_at_' + str(time).replace(".", "h") + ': '
                        core_constraint = ''
                        constraint_var = []
                        for Xij in Xi:
                            variable = Xij + '21'
                            if variable not in all_x_variables_names:
                                all_x_variables_names.append(variable) #add variable name to list
                                variable_var = model.addVar(vtype=GRB.INTEGER, name=variable) #create gurobi variable and add to list
                                all_x_variables.append(variable_var)
                            else:
                                variable_var = all_x_variables[all_x_variables_names.index(variable)]
                            constraint_var.append(variable_var)
                            core_constraint += variable + ' + '
                            variables.append(variable)
                        gurobi_constraint = 0
                        for var in constraint_var:
                            gurobi_constraint += var
                        gurobi_constraint -= Yik_var[flight_count][2]
                        model.addConstr(gurobi_constraint, "== " , 0, name=constraint_name)
                        core_constraint = core_constraint[:-3] + ' - ' + str(Yik[flight_count][2]) + ' == 0;'
                        all_core_constraints.append(core_constraint)
                        constraint.append(constraint_name+core_constraint)
                    if ait[flight_count][time_count]>=3:
                        constraint_name = 'Flight' + str(Flights[flight_count])+ '_tow22_at_' + str(time).replace(".", "h") + ': '
                        core_constraint = ''
                        constraint_var = []
                        for Xij in Xi:
                            variable = Xij + '22'
                            if variable not in all_x_variables_names:
                                all_x_variables_names.append(variable) #add variable name to list
                                variable_var = model.addVar(vtype=GRB.INTEGER, name=variable) #create gurobi variable and add to list
                                all_x_variables.append(variable_var)
                            else:
                                variable_var = all_x_variables[all_x_variables_names.index(variable)]
                            
                            constraint_var.append(variable_var)
                            core_constraint += variable + ' + '
                            variables.append(variable)
                        gurobi_constraint = 0
                        for var in constraint_var:
                            gurobi_constraint += var
                        gurobi_constraint -= Yik_var[flight_count][2]
                        model.addConstr(gurobi_constraint, "== " , 0, name=constraint_name)
                        core_constraint = core_constraint[:-3] + ' - ' + str(Yik[flight_count][2]) + ' == 0;'
                        all_core_constraints.append(core_constraint)
                        constraint.append(constraint_name + core_constraint)
                    tows += 1 
                    
             
        #Only keep constraints that are true with respect to aircraft presence.
            for constrain in constraint:
                all_constraints.append(constrain)
                              
        flight_count += 1
    time_count += 1
print('Constraints for flights created')
model.update()

#Sum of Yik = 1
Yicount = 0
for Yi in Yik:
    constraint_name = 'Number_tows_Flight'+str(Flights[Yicount]) + ': '
    constraint = ''
    maxy = Flight_tow_possibilities[Yicount]
    count_y = 0
    for y in Yi:
        if count_y < maxy+1:
            y_variable = str(y)
            constraint += y_variable +' + '
            variables.append(y_variable)
            count_y +=1
    Yicount += 1
    constraint = constraint[:-3] + ' == 1;'
    all_core_constraints.append(constraint)
    all_constraints.append(constraint_name + constraint) 
    
Yicount = 0
for Yi_var in Yik_var:
    constraint_name = 'Number_tows_Flight'+str(Flights[Yicount]) + ': '
    constraint_var = 0
    maxy = Flight_tow_possibilities[Yicount]
    count_y = 0
    for y in Yi_var:
        if count_y < maxy+1:
            y_variable = y
            constraint_var += y_variable
            count_y +=1
    Yicount += 1
    model.addConstr(constraint_var, "== " , 1, name=constraint_name)
print('Constraints for tows created')   
model.update()

#-----------------Write to file------------------------------------------------

#Write variables
variables = list(dict.fromkeys(variables)) #removes duplicates
type_variable = "int+ "
for variable in variables:
        definition = "dvar " + type_variable + variable + ";"
        n = text_file.write(definition + "\n")
n= text_file.write("\n")
print('Variables written')

#Write objective function:
objective = ''
objective_gurobi = 0
Xicount = 0
while Xicount < len(Xijs):
    PAXobjective = Flights_PAX[Xicount]
    Xi = Xijs[Xicount]
    Xijcount = 0
    while Xijcount < len(Xi):
        DistanceObjective = Gates_distance[Xijcount]
        Xij = Xi[Xijcount]
        Xij_cost = PAXobjective*DistanceObjective
        maxtows = Flights_max_tow[Xicount]
        tows = 0
        while tows < maxtows+1:
            for tow in range(maxtows+1):
                if tows == 0:
                    if tow == 0:
                        objective += str(int(Xij_cost)) + '*' + str(Xij) +str(tow)+str(tows)+ ' + ' 
                        variable = str(Xij) +str(tow)+str(tows)
                        if variable not in all_x_variables_names:
                            all_x_variables_names.append(variable) #add variable name to list
                            variable_var = model.addVar(vtype=GRB.INTEGER, name=variable) #create gurobi variable and add to list
                            all_x_variables.append(variable_var)
                        else:
                            variable_var = all_x_variables[all_x_variables_names.index(variable)]
                        objective_gurobi += Xij_cost * variable_var
                    if  tow >=1:
                        objective += str(int(Xij_cost/3))+ '*' + str(Xij) + str(tow)+str(tows) + ' + '
                        variable = str(Xij) +str(tow)+str(tows)
                        if variable not in all_x_variables_names:
                            all_x_variables_names.append(variable) #add variable name to list
                            variable_var = model.addVar(vtype=GRB.INTEGER, name=variable) #create gurobi variable and add to list
                            all_x_variables.append(variable_var)
                        else:
                            variable_var = all_x_variables[all_x_variables_names.index(variable)]
                        objective_gurobi += (Xij_cost/3) * variable_var
                if tows == 1 and tow>0:
                    if tow == 1:
                        objective += str(int(2*(Xij_cost)/3))+ '*' + str(Xij) + str(tow)+str(tows) + ' + '
                        variable = str(Xij) +str(tow)+str(tows)
                        if variable not in all_x_variables_names:
                            all_x_variables_names.append(variable) #add variable name to list
                            variable_var = model.addVar(vtype=GRB.INTEGER, name=variable) #create gurobi variable and add to list
                            all_x_variables.append(variable_var)
                        else:
                            variable_var = all_x_variables[all_x_variables_names.index(variable)]
                        objective_gurobi += (2*Xij_cost/3) * variable_var
                if tows == 2 and tow>1:
                    if tow == 2:
                        objective += str(int(2*(Xij_cost)/3))+ '*' + str(Xij) + str(tow)+str(tows) + ' + ' 
                        variable = str(Xij) +str(tow)+str(tows)
                        if variable not in all_x_variables_names:
                            all_x_variables_names.append(variable) #add variable name to list
                            variable_var = model.addVar(vtype=GRB.INTEGER, name=variable) #create gurobi variable and add to list
                            all_x_variables.append(variable_var)
                        else:
                            variable_var = all_x_variables[all_x_variables_names.index(variable)]
                        objective_gurobi += (2*Xij_cost/3) * variable_var
            tows +=1
        Xijcount += 1
    Xicount += 1
    
for Yi_var in Yik_var:
    objective += str(t_anti_cost) + '*'+str(Yi[0]) + " + " + str(t_cost) + '*'+str(Yi[1]) + " + " + str(2*t_cost)+'*' + str(Yi[2]) + " + "
    objective_gurobi += t_anti_cost * Yi_var[0] + t_cost * Yi_var[1] +(2* t_cost) * Yi_var[2]

model.setObjective(objective_gurobi, GRB.MINIMIZE)
objective = objective[:-3]
n = text_file.write("minimize" + "\n" + objective + ';' +"\n" + "\n")

print('Objective written')

#Write constraints
n= text_file.write("subject to { \n")
for constraint in all_constraints:
    n = text_file.write(constraint + "\n")
n= text_file.write("}" + "\n")
print('Constrains written \n')

text_file.close()
    




model.update()
model.optimize()

text_file = open("Solution.txt", "w")
for var in model.getVars():
    if var.x == 1:
        n = text_file.write(str(var.varName) + " = " + str(var.x) + "\n")
text_file.close()

status = model.status
if status != GRB.Status.OPTIMAL:
    if status == GRB.Status.UNBOUNDED:
        print('The model cannot be solved because it is unbounded')
    elif status == GRB.Status.INFEASIBLE:
        print('The model is infeasible; computing IIS')
        model.computeIIS()
        print('\nThe following constraint(s) cannot be satisfied:')
        for c in model.getConstrs():
            if c.IISConstr:
                print('%s' % c.constrName)
    elif status != GRB.Status.INF_OR_UNBD:
        print('Optimization was stopped with status %d' % status)
    


# print (model.display())

print("------------------------------------------------")
for var in model.getVars():
    if var.x ==1:
        print(var.varName, " = ", var.x)
print ("Objective Function =", model.objVal/1.0)
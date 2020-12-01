import pandas as pd
import matplotlib.pyplot as plt
#from mini_dataset import Flights,Flights_arrival,Flights_class,Flights_t_stay,Flights_max_tow,Flights_PAX, Gates, Gates_class, Gates_distance, open_time,operating_hours,t_int
from dataset import Flights,Flights_arrival,Flights_class,Flights_t_stay,Flights_max_tow,Flights_PAX, Gates, Gates_class, Gates_distance, open_time,operating_hours,t_int
#from test_set_Stijn import Flights,Flights_arrival,Flights_class,Flights_t_stay,Flights_max_tow,Flights_PAX, Gates, Gates_class, Gates_distance, open_time,operating_hours,t_int
import numpy as np
import plotly.express as px
import matplotlib.patches as mpatches

# =============================================================================
# READ SOLUTION FILE
# =============================================================================

solution_file = open("Solution.txt", "r")
solution = solution_file.readlines()
solution_file.close()

# =============================================================================
# FILTER SOLUTION
# =============================================================================
true_solution = []

# If the variable has value 1 then append to the true solution
for i in range(len(solution)):
    solution[i] = solution[i].replace(";\n", "")
    if "= 1" in solution[i]:
        true_solution.append(solution[i])

# Sort true solution
true_solution.sort()

# =============================================================================
# GENERATE SOLUTION MATRIX
# =============================================================================

# Make empty solution matrix
solution_matrix = np.zeros((len(Flights),len(Gates)))

# Make empty dataframe
solution_df = pd.DataFrame(columns=['flight_number','gate_number','start','end','order'])
# Loop over all flights and gates to contstruct matrix
for flight in range(len(Flights)):
    for gate in range(len(Gates)):
        for i in range(len(true_solution)):
            
            # Check how the x value is described
            # Flight number is smaller than 10 (9 in code)
            if flight < 9:
                
                # Gate number is smaller than 10 (9 in code)
                if len(true_solution[i]) == 9:
                    if true_solution[i][0] == "x" and true_solution[i][1] == str(flight+1) and true_solution[i][2] == str(gate+1):
                        solution_matrix[flight][gate] = 1
                        
                        # Append to dataframe
                        temp_df = pd.DataFrame({'flight_number':flight+1, 'gate_number':gate+1, 'start':Flights_arrival[flight], 'end':(Flights_arrival[flight]+Flights_t_stay[flight]), 'order':int(true_solution[i][4])}, index=[0])
                        solution_df = solution_df.append(temp_df,ignore_index=True)
                        
                # Gate number is larger than 10        
                else:
                    if true_solution[i][0] == "x" and true_solution[i][1] == str(flight+1) and true_solution[i][2:4] == str(gate+1):
                        solution_matrix[flight][gate] = 1

                        # Append to dataframe
                        print(true_solution[i], len(true_solution[i]))
                        temp_df = pd.DataFrame({'flight_number':flight, 'gate_number':gate, 'start':Flights_arrival[flight], 'end':(Flights_arrival[flight]+Flights_t_stay[flight]), 'order':int(true_solution[i][5])}, index=[0])
                        solution_df = solution_df.append(temp_df,ignore_index=True)
                        
            # Flight number is larger than 10
            else:
                
                # Gate number is smaller than 10
                if len(true_solution[i]) == 10:
                    if true_solution[i][0] == "x" and true_solution[i][1:3] == str(flight+1) and true_solution[i][3] == str(gate+1):
                        solution_matrix[flight][gate] = 1
                        
                        # Append to dataframe
                        temp_df = pd.DataFrame({'flight_number':flight, 'gate_number':gate, 'start':Flights_arrival[flight], 'end':(Flights_arrival[flight]+Flights_t_stay[flight]), 'order':int(true_solution[i][5])}, index=[0])
                        solution_df = solution_df.append(temp_df,ignore_index=True)
                        
                # Gate number is larger than 10
                else:
                    if true_solution[i][0] == "x" and true_solution[i][1:3] == str(flight+1) and true_solution[i][3:5] == str(gate+1):
                        solution_matrix[flight][gate] = 1 
                        
                        # Append to dataframe
                        temp_df = pd.DataFrame({'flight_number':flight, 'gate_number':gate, 'start':Flights_arrival[flight], 'end':(Flights_arrival[flight]+Flights_t_stay[flight]), 'order':int(true_solution[i][6])}, index=[0])
                        solution_df = solution_df.append(temp_df,ignore_index=True)



## Test data set
#solution_df = pd.DataFrame([{'flight_number':1,'gate_number':1,'start':10,'end':11,'order':0},
#                           {'flight_number':2,'gate_number':4,'start':10.2,'end':11.2,'order':2},
#                           {'flight_number':2,'gate_number':3,'start':10.2,'end':11.2,'order':0},
#                           {'flight_number':2,'gate_number':2,'start':10.2,'end':11.2,'order':1},
#                           {'flight_number':3,'gate_number':3,'start':10.5,'end':11.5,'order':0},
#                           {'flight_number':3,'gate_number':5,'start':10.5,'end':11.5,'order':1},
#                           {'flight_number':4,'gate_number':2,'start':10.9,'end':11.9,'order':0},
#                           {'flight_number':5,'gate_number':3,'start':11.2,'end':12.2,'order':0}])


# Update start and end time for stays at gates
for i in range(len(solution_df)):
    
    if solution_df['order'][i] == 0:
        
        for j in range(len(solution_df)):
            if solution_df['gate_number'][i] == solution_df['gate_number'][j] and solution_df['end'][i] > solution_df['start'][j] and solution_df['flight_number'][i] != solution_df['flight_number'][j] and solution_df['start'][i] < solution_df['start'][j]:
                solution_df.loc[i,'end'] = solution_df['start'][j]
            
        for k in range(len(solution_df)):
            if solution_df['order'][k] == 1 and solution_df['flight_number'][i] == solution_df['flight_number'][k] :
               solution_df.loc[k,'start'] = solution_df['end'][i]
    
    elif solution_df['order'][i] == 1:
        
        for j in range(len(solution_df)):
            if solution_df['gate_number'][i] == solution_df['gate_number'][j] and solution_df['end'][i] > solution_df['start'][j] and solution_df['flight_number'][i] != solution_df['flight_number'][j] and solution_df['start'][i] < solution_df['start'][j]:
                solution_df.loc[i,'end'] = solution_df['start'][j]
            
        for k in range(len(solution_df)):
            if solution_df['order'][k] == 2 and solution_df['flight_number'][i] == solution_df['flight_number'][k] :
               solution_df.loc[k,'start'] = solution_df['end'][i]
            
# =============================================================================
# PLOT DATA
# =============================================================================

# SETUP CHART
# Declaring a figure "gnt" 
fig, gnt = plt.subplots() 
  
# Setting Y-axis limits 
gnt.set_ylim(0, (len(Gates)) + 1) 
  
# Setting X-axis limits 
gnt.set_xlim(open_time, (open_time + operating_hours + 1)) 
  
# Setting Chart title
gnt.set_title('Gate schedule')

# Setting labels for x-axis and y-axis 
gnt.set_xlabel('Time') 
gnt.set_ylabel('Gate') 
  
# Set legend
small_label = mpatches.Patch(color='Red', label='Small aircraft')
medium_label = mpatches.Patch(color='Blue', label='Medium aircraft')
large_label = mpatches.Patch(color='Orange', label='Large aircraft')

gnt.legend(handles=[small_label,medium_label,large_label])

# Setting ticks on y-axis and x-axis
gnt.set_yticks(Gates) 
gnt.set_xticks(np.arange(open_time,(open_time + operating_hours + 1), 1))

# Labelling tickes of y-axis 
gnt.set_yticklabels(np.asarray(Gates, dtype="<U16", order='C')) 
  
# Setting graph attribute 
gnt.grid(True) 

# PLOT SCHEDULE
for i in range(len(solution_df)):

    # Set color based on capacity of aircraft
    if Flights_class[solution_df['flight_number'][i] - 1] == 1:
        color = 'Red'
        label = 'Small aircraft'
    
    elif Flights_class[solution_df['flight_number'][i] - 1] == 2:
        color = 'Blue'
        label = 'Medium aircraft'
        
    elif Flights_class[solution_df['flight_number'][i] - 1] == 3:
        color = 'Orange'
        label = 'Large aircraft'
    
    plt.broken_barh([(solution_df['start'][i] + 0.03, solution_df['end'][i] - solution_df['start'][i] - 0.03,)], (solution_df['gate_number'][i] - 0.45, 0.9), color=color, label=label)

#gnt.legend()


# =============================================================================
# NOT USED CODE
# =============================================================================

# plot schedule

# plt.figure(figsize=(16.5, 3.5))

# for i in range(len(Flights)):
#     gate = 0
#     for j in range(len(Gates)):
#         if results[i, j] == 1:
#             gate = j
#             break

#     if flight_movements[i] == 0:
#         color = "BLUE"
#     elif flight_movements[i] == 1:
#         color = "ORANGE"
#     elif flight_movements[i] == 2:
#         color = "RED"

#     plt.broken_barh([(SCHDLSPLIT[i][0][0], SCHDLSPLIT[i][0][1] - SCHDLSPLIT[i][0][0])], (bay - 0.45 + 1, 0.9), color=color)



# plt.yticks(np.array([(x + 1) for x in range(n_bays)]))
# xticks = np.linspace(0, 24 * 60, 24 * 60 / 60 + 1)
# plt.xticks(xticks, [("{:02d}:{:02d}".format(int(x[0]), int(x[1]))) for x in [(x // 60, x % 60) for x in xticks]])

# plt.ylabel("Bay #")
# plt.xlabel("Time [HH:MM]")
# plt.tight_layout()
# plt.grid()

#Xijs = []
#for flightnumber in Flights:
#    Xi = 'x'+str(flightnumber)
#    Xis = np.array([])
#    for gatenumber in Gates:
#        Xij = Xi+str(gatenumber)
#        Xis = np.append(Xis,Xij)
#    Xijs.append(Xis)

#for i in range(len(Flights)):
#    gate = 0
#    for j in range(len(Gates)):
#        if solution_matrix[i, j] == 1:
#            gate = j
#            
#            if (Flights[i] % 2) == 0:  
#               color = "BLUE"
#            elif (Flights[i] % 3) == 0:  
#               color = "RED"
#            else:  
#               color = "ORANGE"  
#            
#            break 
#            
#
#    plt.broken_barh([(Flights_arrival[i], Flights_t_stay[i])], (gate - 0.45 + 1, 0.9), color=color)
#
#
#plt.yticks(np.array([(x + 1) for x in range(len(Gates))]))
#xticks = np.linspace(0, 24 * 60, 24 * 60 / 60 + 1)
#plt.xticks(xticks, [("{:02d}:{:02d}".format(int(x[0]), int(x[1]))) for x in [(x // 60, x % 60) for x in xticks]])
#plt.ylabel("Bay #")
#plt.xlabel("Time [HH:MM]")
#plt.tight_layout()
#plt.grid()

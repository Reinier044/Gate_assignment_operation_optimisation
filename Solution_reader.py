import pandas as pd
import matplotlib.pyplot as plt
from mini_dataset import Flights,Flights_arrival,Flights_class,Flights_t_stay,Flights_max_tow,Flights_PAX, Gates, Gates_class, Gates_distance, open_time,operating_hours,t_int
#from dataset import Flights,Flights_arrival,Flights_class,Flights_t_stay,Flights_max_tow,Flights_PAX, Gates, Gates_class, Gates_distance, open_time,operating_hours,t_int
#from test_set_Stijn import Flights,Flights_arrival,Flights_class,Flights_t_stay,Flights_max_tow,Flights_PAX, Gates, Gates_class, Gates_distance, open_time,operating_hours,t_int
import numpy as np
import matplotlib.patches as mpatches
from Using_Gurobi import tow1_times, tow2_times

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
    solution[i] = solution[i].replace("\n", "")
    if "= 1" in solution[i]:
        true_solution.append(solution[i])

# Sort true solution
true_solution.sort()

# =============================================================================
# GENERATE SOLUTION MATRIX AND SOLUTION DATAFRAME
# =============================================================================

# Make empty solution matrix
solution_matrix = np.zeros((len(Flights),len(Gates)))

# Make empty dataframe
solution_df = pd.DataFrame(columns=['flight_number','gate_number','start','end','tows'])

# Loop over all flights and gates to contstruct matrix
for ts in true_solution:
    x = False
    to_gate = False
    to_tows = False
    n_flight = ''
    n_gate = ''
    n_tows = ''
    
    # Split solution in: flight, gate and n tows
    for i in ts:
        if i == ' ':
            break
        
        if i == 'x':
            x = True
            continue
        
        if x and not to_gate and i != '_':
            n_flight += i
            
        if x and i == '_' and not to_gate:
            to_gate = True
            continue
            
        if x and to_gate and not to_tows and i != '_':
            n_gate += i
            
        if x and i == '_' and to_gate:
            to_tows = True
            
        if x and to_gate and to_tows and i != '_':
            n_tows += i
        
    if x:
        # Append to dataframe
        temp_df = pd.DataFrame({'flight_number':int(n_flight), 'gate_number':int(n_gate), 'start':Flights_arrival[int(n_flight) - 1], 'end':(Flights_arrival[int(n_flight) - 1] + Flights_t_stay[int(n_flight) - 1]), 'tows':int(n_tows[-1])}, index=[0])
        solution_df = solution_df.append(temp_df,ignore_index=True)

# Update start and end time of stay at gate using the tow 1 and tow 2 times
for flight in Flights:
    # Check tow 1 times
    if tow1_times[flight - 1] != 0:
        
        for k in range(len(solution_df)):
            if solution_df['flight_number'][k] == flight and solution_df['tows'][k] == 1:
        
                for i in range(len(solution_df)):
                    if solution_df['flight_number'][i] == flight and solution_df['tows'][i] == 0:
                        solution_df.loc[i,'end'] = tow1_times[flight - 1]
                    
                        for j in range(len(solution_df)):
                            if solution_df['flight_number'][j] == flight and solution_df['tows'][j] == 1:
                                solution_df.loc[j,'start'] = solution_df['end'][i]
                                break
                        break
                break
                        
    # Check tow 2 times                            
    if tow2_times[flight - 1] != 0:
      
        for k in range(len(solution_df)):
            if solution_df['flight_number'][k] == flight and solution_df['tows'][k] == 2:
        
                for i in range(len(solution_df)):
                    if solution_df['flight_number'][i] == flight and solution_df['tows'][i] == 1:
                        solution_df.loc[i,'end'] = tow2_times[flight - 1]
            
                        for j in range(len(solution_df)):
                            if solution_df['flight_number'][j] == flight and solution_df['tows'][j] == 2:
                                solution_df.loc[j,'start'] = solution_df['end'][i]
                                break
                        break
                break
            
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
gnt.set_xlabel('Time [Hours]') 
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

plt.savefig('figures/schedule_scen1')
""" Data set """
# =============================================================================
# RELEVANT ARRAYS
# =============================================================================
# flights_pax
# arrival_times
# flights_t_stay
# gates_distance

# Imports
import numpy as np
import random
import math
import sys
import matplotlib.pyplot as plt

# =============================================================================
# PARAMETERS
# ============================================================================
# Flights
n_flights = 350
large_aircraft_percentage = 0.1
medium_aircraft_percentage = 0.6

# Airport
open_time = 5
operating_hours = 24
close_time = open_time+operating_hours
t_int = 0.25
inv_t_int = 1/t_int

printed = 0
n_ac_per_interval = n_flights/(operating_hours/t_int)

#Feedback realism of generated dataset
if n_flights/operating_hours > 50:
    print("airport size unrealistic based on flights/hour. \n")
    printed = 1
elif n_flights/operating_hours > 30 and printed == 0:
    print("airport has size of Schiphol based on flights/hour. \n")
    printed = 1
elif n_flights/operating_hours > 12 and printed == 0:
    print("airport has size of secondary airport based on flights/hour (eg Milan Linate). \n")
    printed = 1
elif n_flights/operating_hours > 6 and printed == 0:
    print("airport has size of Rotterdam based on flights/hour. \n")
    printed = 1
elif printed == 0:
    print("airport is pretty small based on flights/hour. \n")
    

# Aircraft
n_large_aircraft  = int(large_aircraft_percentage*n_flights)
n_medium_aircraft = int(medium_aircraft_percentage*n_flights)
n_small_aircraft = n_flights - n_large_aircraft - n_medium_aircraft

n_pax_large = 400
n_pax_medium = 250
n_pax_small = 100

t_stay_large = [t_int*60,t_int*60*12] # [min]
t_stay_medium = [t_int*60,t_int*60*8] # [min]
t_stay_small = [t_int*60,t_int*60*4] # [min]

# Gates
n_gates = 50 
n_terminals = 1
dist_gates_to_hall = 20
gate_seperation = 7
large_gate_percentage = 0.3
medium_gate_percentage = 0.6

n_large_gates = int(large_gate_percentage * n_gates)
n_medium_gates = int(medium_gate_percentage * n_gates)
n_small_gates = n_gates - n_large_gates - n_medium_gates

#Check input data for errors
Stop = False
if n_flights != (n_large_aircraft+n_medium_aircraft+n_small_aircraft):
    print('missing aircraft in the type classification \n \n\n')
    Stop = True
if n_gates != (n_large_gates + n_medium_gates + n_small_gates):
    print('missing gates in the type classification \n \n \n')
    Stop = True
if Stop:
    sys.exit()

# =============================================================================
# FLIGHT DATA GENERATOR
# =============================================================================
# Generate list with aircraft
flights_pax = []
flights_generated = 0
aircraft_list = [100,250,400]

while flights_generated < n_flights:
    n_pax = random.choice(aircraft_list)
    
    if n_pax == n_pax_large and flights_pax.count(400) < n_large_aircraft:
        flights_pax.append(n_pax)
        flights_generated += 1
    
    if n_pax == n_pax_medium and flights_pax.count(250) < n_medium_aircraft:
        flights_pax.append(n_pax)
        flights_generated += 1
        
    if n_pax == n_pax_small and flights_pax.count(100) < n_small_aircraft:
        flights_pax.append(n_pax)
        flights_generated += 1
    
    if flights_pax.count(400) == n_large_aircraft:
        aircraft_list = [100,250]
        
    if flights_pax.count(250) == n_medium_aircraft:
        aircraft_list = [100,400]
        
    if flights_pax.count(100) == n_small_aircraft:
        aircraft_list = [250,400]
 
# Generate list with flight class
flights_class = []
for flight_pax in flights_pax:
    if flight_pax == 400:
        flights_class.append(3) #3
        
    if flight_pax == 250:
        flights_class.append(2) #2
        
    if flight_pax == 100:
       flights_class.append(1)
        
# Generate list with arrival times
arrival_times = []
hour = open_time
aircraft_landed = 0
iterations = 0

while aircraft_landed < n_flights: 
    n_arrivals = random.randint(0,int(n_ac_per_interval*2.5)) #was 12
    arrival_interval = 0
    
    for arrival in range(n_arrivals):
        arrival_interval += random.randint(0,int((60*t_int)/n_arrivals))
        time = math.ceil((hour + (arrival_interval / 60))*inv_t_int)/(inv_t_int)
        time = int(time) + random.choice([0,0.25,0.5,0.75])
        arrival_times.append(time)
        aircraft_landed += 1
        
        # Check if all aircraft already landed
        if aircraft_landed == n_flights:
            iterations += 1
            #Check if landing times are within operating times.
            if time > close_time:
                arrival_times = []
                hour = open_time
                aircraft_landed = 0
                
            #Check if landing times are not too early.
            elif time < (close_time - 2*t_int):
                arrival_times = []
                hour = open_time
                aircraft_landed = 0
            
            else:
                print("Generation took ",iterations," iterations. \n")
                break
    
    # Update hour to plan next hour
    hour += t_int
    
# Generate list with staying times based on n pax
flights_t_stay = []
    
for n_pax in flights_pax:
    if n_pax == 400:    
        stay_time = int(round((random.randint(t_stay_large[0], t_stay_large[1]) / 60),2)) + random.choice([0,0.25,0.5,0.75])
        if stay_time < 0.75:
            stay_time = 0.75
        flights_t_stay.append(stay_time)
    
    if n_pax == 250: 
        stay_time = int(round((random.randint(t_stay_medium[0], t_stay_medium[1]) / 60),2)) + random.choice([0,0.25,0.5,0.75])
        if stay_time < 0.75:
            stay_time = 0.75
        flights_t_stay.append(stay_time)

    if n_pax == 100:
        stay_time = int(round((random.randint(t_stay_small[0], t_stay_small[1]) / 60),2)) + random.choice([0,0.25,0.5,0.75])
        if stay_time < 0.75:
            stay_time = 0.75
        flights_t_stay.append(stay_time)

# Generate list with maximal amount of tows per aircraft
flights_max_tow = []

for flight in range(n_flights):
    # For now only 2 tows
    flights_max_tow.append(2)    
            
# =============================================================================
# GATE DATA GENERATOR
# =============================================================================
gates_distance = []
gates_per_terminal_lst  = []

# Calculate the amount of gates per terminal
for terminal in range(n_terminals):
    gates_per_terminal = n_gates // n_terminals
    
    # Terminal 1 is largest terminal
    if terminal == 0:    
        gates_per_terminal += n_gates % n_terminals

    gates_per_terminal_lst.append(gates_per_terminal)
    
# Determine distances from gate to main hall
for terminal_gates in gates_per_terminal_lst:
    
    dist_gates = []
    
    # If there is an even number gates per terminal
    if terminal_gates % 2 == 0:
        
        for gate in range(int(terminal_gates / 2)):
            if gate == 0:
                dist_to_exit = dist_gates_to_hall + gate_seperation / 2
                dist_gates.append(dist_to_exit)
            
            else:
                dist_to_exit += gate_seperation
                dist_gates.append(dist_to_exit)
        
        # Append distances to list        
        for dist_gate in dist_gates[::-1]:
            gates_distance.append(dist_gate)
        
        for dist_gate in dist_gates:
            gates_distance.append(dist_gate)
            
    # If there is an uneven number gates per terminal
    if terminal_gates % 2 != 0:
        
        for gate in range(terminal_gates // 2):
            if gate == 0:
                dist_to_exit = dist_gates_to_hall + gate_seperation
                dist_gates.append(dist_to_exit)
            
            else:
                dist_to_exit += gate_seperation
                dist_gates.append(dist_to_exit)
        
        # Append distances to list
        for dist_gate in dist_gates[::-1]:
            gates_distance.append(dist_gate)
        
        gates_distance.append(3 + dist_gates_to_hall)
        
        for dist_gate in dist_gates:
            gates_distance.append(dist_gate)

# Generate list with gate classes
gates_class = []
gates_generated = 0
gates_list = [1,2,3]     
            
while gates_generated < n_gates:
    gate_class = random.choice(gates_list)
    
    if gate_class == 3 and gates_class.count(3) < n_large_gates:
        gates_class.append(gate_class)
        gates_generated += 1
    
    if gate_class == 2 and gates_class.count(2) < n_medium_gates:
        gates_class.append(gate_class)
        gates_generated += 1
        
    if gate_class == 1 and gates_class.count(1) < n_small_gates:
        gates_class.append(gate_class)
        gates_generated += 1
    
    if gates_class.count(3) == n_large_gates:
        gates_list = [1,2]
        
    if gates_class.count(2) == n_medium_gates:
        gates_list = [1,3]
        
    if gates_class.count(1) == n_small_gates:
        gates_list = [2,3]




#to remove classes temporarily REMOVE LATER!!!!!!!
#gates_class_copy = []
#for gate in range(len(gates_class)):
#    gates_class_copy.append(1)
#gates_class = gates_class_copy
# =============================================================================
# LIST TO ARRAY CONVERSION
# =============================================================================
text_file = open("dataset.txt", "w")


Flights = np.arange(n_flights)+1
Flights_arrival = np.array(arrival_times)
Flights_t_stay = np.array(flights_t_stay)
Flights_PAX = np.array(flights_pax)
Flights_class = np.array(flights_class)
Flights_max_tow = np.array(flights_max_tow)

Gates = np.arange(n_gates)+1
gates_distance.sort()
Gates_distance = np.array(gates_distance)
gates_class.sort(reverse=True)
Gates_class = np.array(gates_class)


# =============================================================================
# Write to file
# =============================================================================
n = text_file.write("Flights = "+ str(list(Flights)) + "\n" + "Flights_arrival = " + str(list(Flights_arrival)) + "\n" + "Flights_t_stay = " + str(list(Flights_t_stay)) + "\n")
n = text_file.write("Flights_PAX = "+ str(list(Flights_PAX)) + "\n" + "Flights_class = " + str(list(Flights_class)) + "\n" + "Flights_max_tow = " + str(list(Flights_max_tow)) + "\n")
n = text_file.write("Gates = "+ str(list(Gates)) + "\n" + "Gates_distance = " + str(list(Gates_distance)) + "\n" + "Gates_class = " + str(list(Gates_class)) + "\n") 
n = text_file.write("open_time = " + str(open_time) + "\n" + "operating_hours = " + str(operating_hours) + "\n" + "t_int = " + str(t_int)) 
text_file.close()
    
    
#check aircraft present lower than gates
time = open_time
time_lst = np.arange(open_time,close_time, t_int)
aircraft_present_slot = []
while time < close_time: 
    aircraft_present = 0
    aircraft_present_small = 0
    aircraft_present_medium = 0
    aircraft_present_large = 0
    for flight_index in range(len(Flights)):
        if Flights_arrival[flight_index] <= time and (Flights_arrival[flight_index] + Flights_t_stay[flight_index]) > time:
            aircraft_present += 1
            if Flights_class[flight_index] == 0: 
                aircraft_present_small += 1
            elif Flights_class[flight_index] == 1: 
                aircraft_present_medium += 1
            elif Flights_class[flight_index] == 0: 
                aircraft_present_large += 1
    
    aircraft_present_slot.append(aircraft_present)
    
    if aircraft_present > n_gates:
        print("To many aircraft at: ", time, ". ", aircraft_present, " aircraft on ", n_gates, " gates.")
    if aircraft_present_small > n_small_gates:
        print("To many small aircraft at: ", time, ". ", aircraft_present_small, " aircraft on ", n_small_gates, " gates.")
    if aircraft_present_medium > n_medium_gates:
        print("To many medium aircraft at: ", time, ". ", aircraft_present_medium, " aircraft on ", n_medium_gates, " gates.")
    if aircraft_present_large > n_large_gates:
        print("To many large aircraft at: ", time, ". ", aircraft_present_large, " aircraft on ", n_large_gates, " gates.")
    
        
    time += t_int

#This plot shows a histogram of the aircraft in the timeslots
# plt.bar(time_lst, aircraft_present_slot, t_int)
# plt.yticks(np.arange(0,(max(aircraft_present_slot)+1), 1))
# plt.show

print("====================================================================================== ")
print("------------------------------Dataset generated--------------------------------------- ")
print("====================================================================================== \n ")   
    
    
    
    
    



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

# =============================================================================
# PARAMETERS
# =============================================================================
# Flights
n_flights = 50

# Airport
open_time = 10
operating_hours = 5

# Aircraft
n_large_aircraft  = 15
n_medium_aircraft = 15
n_small_aircraft = 20

n_pax_large = 400
n_pax_medium = 250
n_pax_small = 100

t_stay_large = [120,240] # [min]
t_stay_medium = [60,180] # [min]
t_stay_small = [30,120] # [min]

# Gates
n_gates = 21
n_terminals = 2
dist_gates_to_hall = 20
gate_seperation = 7

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
        
# Generate list with arrival times
arrival_times = []
hour = open_time
aircraft_landed = 0

while aircraft_landed < n_flights: 
    n_arrivals = random.randint(int(n_flights / operating_hours), 12)
    arrival_interval = 0
    
    for arrival in range(n_arrivals):
        arrival_interval += random.randint(5,int(60/n_arrivals))
        arrival_times.append((hour + (arrival_interval / 60)))
        aircraft_landed += 1
        
        # Check if all aircraft already landed
        if aircraft_landed == n_flights:
            break
    
    # Update hour to plan next hour
    hour += 1
    
# Generate list with staying times based on n pax
flights_t_stay = []
    
for n_pax in flights_pax:
    if n_pax == 400:    
       flights_t_stay.append(random.randint(t_stay_large[0], t_stay_large[1]) / 60)
    
    if n_pax == 250: 
        flights_t_stay.append(random.randint(t_stay_medium[0], t_stay_medium[1]) / 60)

    if n_pax == 100:
        flights_t_stay.append(random.randint(t_stay_small[0], t_stay_small[1]) / 60)
            
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
    
# =============================================================================
# LIST TO ARRAY CONVERSION
# =============================================================================
Flights = np.arange(n_flights)
Flights_arrival = np.array(arrival_times)
Flights_t_stay = np.array(flights_t_stay)
Flights_PAX = np.array(flights_pax)
Gates = np.arange(n_gates)
Gates_distance = np.array(gates_distance)
    
#Flights_max_tow = np.array([2,2,2,2])
#Flights_class = np.array([3,3,2,3])
#Gates_class = np.array([2,2,3,3])
    
    
    
    
    
    
    
    
    
    
    
    
    



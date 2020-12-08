import numpy as np
import matplotlib.pyplot as plt

Flights =           [1,     2,      3,      4,      5,      6,      7,      8,      9,      10,     11,     12,     13,     14,     15,     16,     17,     18,     19,     20,     21,     22,     23,     24,     25,     26,     27,     28,     29,     30,     31,     32,     33,     34,     35,     36,     37,     38,     39,     40,     41,     42,     43,     44,     45,      46,     47,     48,     49,     50,     51,     52,     53,     54,     55,     56,     57,     58,    59,     60]
Flights_arrival =   [7.5,   7.25,   7.0,    7.0,    7.0,    7.25,   7.0,    8.5,    8.5,    8.25,   8.25,   8.5,    8.25,   8.0,    8.0,    8.5,    9.5,    9.0,    9.75,   9.5,    9.0,    9.5,    9.25,   9.0,    9.25,   9.25,   9.5,    9.0,    9.5,    10.0,   10.25,  10.25,  10.5,   10.75,  10.0,   10.25,  11.75,  11.0,   11.75,  11.25,  11.25,  11.0,   11.25,  11.5,   11.0,   11.25,  11.75,  11.25,  11.0,   11.5,   11.25,  11.75,  11.0,   12.75,  12.25,  12.0,   12.25,  12.25,  12.75,  12.5]
Flights_t_stay =    [1.75,  0.75,   0.75,   2.75,   0.75,   1.0,    1.5,    2.5,    0.75,   0.75,   1.75,   0.75,   0.75,   0.75,   0.75,   0.75,   0.75,   0.75,   0.75,   0.75,   1.5,    0.75,   0.75,   1.75,   1.0,    0.75,   1.75,   0.75,   0.75,   0.75,   0.75,   0.75,   1.0,    0.75,   0.75,   1.25,   0.75,   0.75,   1.0,    1.0,    0.75,   1.5,    0.75,   1.75,   0.75,   0.75,   0.75,   0.75,   1.25,   0.75,   0.75,   1.25,   0.75,   0.75,   1.5,    0.75,   1.5,    1.25,   0.75,   0.75]
Flights_PAX =       [400,   100,    100,    400,    250,    400,    250,    400,    100,    100,    250,    100,    100,    250,    100,    250,    400,    100,    100,    100,    250,    100,    100,    250,    250,    400,    250,    100,    100,    250,    100,    100,    250,    100,    100,    250,    250,    250,    250,    250,    250,    250,    250,    250,    250,    250,    250,    250,    250,    250,    250,    250,    250,    250,    250,    250,    250,    250,    250,    250]
Flights_class = [   3,      1,      1,      3,      2,      3,      2,      3,      1,      1,      2,      1,      1,      2,      1,      2,      3,      1,      1,      1,      2,      1,      1,      2,      2,      3,      2,      1,      1,      2,      1,      1,      2,      1,      1,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2]
Flights_max_tow = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
Gates =             [1,   2,   3,   4,  5,  6,  7,  8,  9,  10, 11, 12,  13,  14,  15]
Gates_distance =    [145, 125, 105, 85, 65, 45, 25, 25, 45, 65, 85, 105, 125, 145, 165]
Gates_class =       [3,   3,   2,   2,  2,  3,  2,  2,  3,  2,  2,  2,   2,   3,   3]
open_time = 7
operating_hours = 6
t_int = 0.25

average_time_stay = sum(Flights_t_stay)/len(Flights_t_stay)

close_time = open_time+operating_hours
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
    
    time += t_int

print("Average staying time: ", average_time_stay)
print("Number of large aircraft: ", Flights_PAX.count(400))
print("Number of medium aircraft: ", Flights_PAX.count(250))
print("Number of small aircraft: ", Flights_PAX.count(100))
# #This plot shows a histogram of the aircraft in the timeslots
# plt.bar(time_lst, aircraft_present_slot, t_int)
# plt.yticks(np.arange(0,(max(aircraft_present_slot)+1), 1))
# plt.show
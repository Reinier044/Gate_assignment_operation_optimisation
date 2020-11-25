import pandas as pd
import matplotlib.pyplot as plt
from mini_dataset import Flights,Flights_arrival,Flights_class,Flights_t_stay,Flights_max_tow,Flights_PAX, Gates, Gates_class, Gates_distance, open_time,operating_hours,t_int
#from dataset import Flights,Flights_arrival,Flights_class,Flights_t_stay,Flights_max_tow,Flights_PAX, Gates, Gates_class, Gates_distance, open_time,operating_hours,t_int
#from test_set_Stijn import Flights,Flights_arrival,Flights_class,Flights_t_stay,Flights_max_tow,Flights_PAX, Gates, Gates_class, Gates_distance, open_time,operating_hours,t_int
import numpy as np

#Reading solution file

solution_file = open("Solution.txt", "r")
solution = solution_file.readlines()
solution_file.close()

Xijs = []
for flightnumber in Flights:
    Xi = 'x'+str(flightnumber)
    Xis = np.array([])
    for gatenumber in Gates:
        Xij = Xi+str(gatenumber)
        Xis = np.append(Xis,Xij)
    Xijs.append(Xis)

true_solution = []
for i in range(len(solution)):
    solution[i] = solution[i].replace(";\n", "")
    if "= 1" in solution[i]:
        true_solution.append(solution[i])

solution_matrix = np.zeros((len(Flights),len(Gates)))
for i in range(len(Flights)):
    for j in range(len(Gates)):
        for k in range(len(true_solution)):
            if true_solution[k][0:1] == "x" and true_solution[k][1:2] == str(i+1) and true_solution[k][2:3] == str(j+1):
                solution_matrix[i][j] = 1
print(solution_matrix)
print(len(Flights))
true_solution.sort()
#Plots



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

for i in range(len(Flights)):
    gate = 0
    for j in range(len(Gates)):
        if solution_matrix[i, j] == 1:
            gate = j
            
            if (Flights[i] % 2) == 0:  
               color = "BLUE"
            elif (Flights[i] % 3) == 0:  
               color = "RED"
            else:  
               color = "ORANGE"  
            
            break 
            

    plt.broken_barh([(Flights_arrival[i], Flights_t_stay[i])], (gate - 0.45 + 1, 0.9), color=color)


plt.yticks(np.array([(x + 1) for x in range(len(Gates))]))
xticks = np.linspace(0, 24 * 60, 24 * 60 / 60 + 1)
plt.xticks(xticks, [("{:02d}:{:02d}".format(int(x[0]), int(x[1]))) for x in [(x // 60, x % 60) for x in xticks]])
plt.ylabel("Bay #")
plt.xlabel("Time [HH:MM]")
plt.tight_layout()
plt.grid()

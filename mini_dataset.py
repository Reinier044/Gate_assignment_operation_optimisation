# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 09:05:28 2020

@author: Reini
"""
import numpy as np
#define flights
Flights = np.array([1,2,3,4])
Flights_arrival = np.array([10,10,10,11])
Flights_class = np.array([3,2,1,1])
Flights_t_stay = np.array([1,1,1,1])
Flights_max_tow = np.array([2,2,2,2])
Flights_PAX = np.array([100,200,300,400,])

#define gates
Gates = np.array([1,2,3])
Gates_class = np.array([3,2,1])
Gates_distance = np.array([1000,2000,3000])

#define other parameters
open_time = 10
operating_hours = 3
t_int = 0.25
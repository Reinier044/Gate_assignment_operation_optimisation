# operations_optimisation_gate_assignment

This is the model accompanying the assignment for the Course AE4441-16 Operations Optimisation. 
The model was written by Stijn Brunia (4549643), Matthijs Torsij (4533399) & Reinier Vos (4588304). 
To run the model, simply run "Execute_Optimization.py". It will produce a plot containing the
assignments made by the solver. The complete solution is stored under variable "solution_df". Or
in "Solution.txt".

"Execute_Optimization.py" is running the model as defined by "model.py". Here, the input data can be 
specified. Either, "dataset.py","mini_dataset.py" or "dataset_generator.py" can be used. The latter 
generates a new airport and flight schedule according to the initialization parameters give. 
"mini_dataset.py" contains a very small dataset used for quick verification.  "dataset.py" contains 
the final and definitive model used for the sensitivity analysis. As a sidenote, CPLEX_code contains 
the code required to run the model in another solver for validation. However, the datasets we used
were too big for CPLEX, hence only mini_dataset was used to partly validate the code. If there are 
any remaining questions, do not hesitate to contact us.

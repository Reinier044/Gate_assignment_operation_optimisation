#Reading solution file

solution_file = open("Solution.txt", "r")
solution = solution_file.readlines()
solution_file.close()

true_solution = []
for i in range(len(solution)):
    solution[i] = solution[i].replace(";\n", "")
    if "= 1" in solution[i]:
        true_solution.append(solution[i])
        print(solution[i])

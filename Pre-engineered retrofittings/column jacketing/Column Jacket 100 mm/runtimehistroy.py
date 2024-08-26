import openseespy.opensees as ops
import TimeX
import time
import numpy as np
import os
os.chdir(r'E:\4th year project\opensees\Pushover all typology\Pre Engineered Buildings\column jacketing\Column Jacket 100 mm')

j_set = {"iv","chichi","bigbear","kern","palm","park_field","landers","loma","nr","whittier","san_fernando"}
No_of_Scaling = 5

# Run OpenSees simulations
for j in j_set:
    for i in range(5, No_of_Scaling+1):  # Adjust the range as needed ####
        TimeX.times(i, j)
        time.sleep(2)

max_values = []  # List to store maximum absolute values

##Process results with NumPy
for j in j_set:
    for i in range(5, No_of_Scaling+1):  # Adjust the range as needed
        # Load the data from the file using numpy
        

        data = np.loadtxt(f'Out/di{i}_{j}.out')

        c1 = data[:, 0]
        c2 = data[:, 1]
        c3 = data[:, 2]
        c4 = data[:, 3]
        d1 = np.max(np.abs(c1-c2))
        d2 = np.max(np.abs(c2-c3))
        d3 = np.max(np.abs(c3-c4))
        
        abs_max_difference = np.max([d1,d2,d3])

        max_values.append(abs_max_difference) #interstorey Drift

        with open('maxx_values.txt', 'a') as file:
            # Write the max absolute value to the file
            file.write(f'drift_{i/10}g_{j}.out: \t {abs_max_difference/3*100:.6f}\n')
            


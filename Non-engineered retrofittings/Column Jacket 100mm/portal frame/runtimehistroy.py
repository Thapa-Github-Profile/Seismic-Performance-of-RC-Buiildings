import time

import numpy as np
import openseespy.opensees as ops

import TimeX

j_set = ["bigbear","iv","chichi","kern","landers","loma","nr","palm","park_field","san_fernando","whittier"]
No_of_Scaling = 5

### Run OpenSees simulations
for j in j_set:
    for i in range(5, No_of_Scaling + 1):  # Adjust the range as needed
        TimeX.times(i, j)
        time.sleep(2)


max_values = []  # List to store maximum absolute values

##Process results with NumPy
for j in j_set:
    for i in range(5, No_of_Scaling + 1):  # Adjust the range as needed
        # Load the data from the file using numpy
        data = np.loadtxt(f"Out/di{i}_{j}.out")
        c1 = data[:, 0]
        c2 = data[:, 1]
        c3 = data[:, 2]
        c4 = data[:, 3]
        d1 = np.max(np.abs(c1 - c2))
        d2 = np.max(np.abs(c2 - c3))
        d3 = np.max(np.abs(c3 - c4))

        abs_max_difference = np.max([d1, d2, d3])

        max_values.append(abs_max_difference)  # interstorey Drift

        file = open("maxx_values.txt", "a")
        # Write the max absolute value to the file
        file.write(f"drift_{i/10}g_{j}.out: \t {abs_max_difference/3*100:.6f}\n")
        file.close()

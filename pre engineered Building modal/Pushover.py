
import openseespy.postprocessing.Get_Rendering as opsplt
import os
import openseespy.opensees as ops
from Modal import *
#from mode_analysis import *
import time
#PLEASE CHANGE THIS, Output file will be saved in this directory
os.chdir(r"E:\4th year project\opensees\Pushover all typology\Pre Engineered Buildings\pre engineered Building modal")
# START ANALYSIS
import Gravity
print("ooo Analysis: Pushover ooo")
start_time = time.time()
# SET RECORDERS
# Global behaviour
ops.recorder('Node', '-file', 'DisplacementX.out', '-time', '-node',4, '-dof', 1, 'disp')
ops.recorder('Node', '-file', 'ReactionsX.out', '-time', '-node',1,5,9,13,17,21,25,29,33,37,41, '-dof', 1, 'reaction')
with open("modeshape1.out", "r") as file:
    data = [float(value) for line in file for value in line.strip().split()]

# ANALYSIS
#pattern(’Plain’, patternTag, tsTag, ’-fact’, fact)
ops.timeSeries('Linear', 2)
ops.pattern('Plain', 2, 2)
# Apply lateral load based on first mode shape in x direction (EC8-1)
ops.load(3000, data[1]/data[3], 0.0, 0.0, 0.0, 0.0, 0.0) # 3000 and 4000 are tags of master node
ops.load(4000, data[2]/data[3], 0.0, 0.0, 0.0, 0.0, 0.0)
ops.load(5000, 1, 0.0, 0.0, 0.0, 0.0, 0.0)
# Define step parameters
step = 0.0001
numbersteps = 4000

# Constraint Handler
#ops.constraints('Transformation')

# DOF Numberer
ops.numberer('RCM')

# System of Equations
ops.system('BandGeneral')

# Convergence Test
ops.test('NormDispIncr', 0.0000001, 50)

# Algorithm
ops.algorithm('NewtonLineSearch', '-type', 'Bisection', '-tol', 8.0e-1, '-maxIter', 1000, '-minEta', 1.0e-1, '-maxEta', 1.0e1, 'pFlag', 1)

# Integrator
ops.integrator('DisplacementControl', 5000, 1, step,10)

# Analysis Type
ops.analysis('Static')

# Record initial state of the model
ops.record()

# Analyze model
ops.analyze(numbersteps)

# Reset for the next analysis sequence
ops.wipe()

# ###########################################################
# #Graph Visulalization
# ###########################################################

import numpy as np
import matplotlib.pyplot as plt

# Define the file paths for the recorded data
reaction_file = 'ReactionsX.out'
disp_file = 'DisplacementX.out'

# Load reaction and displacement data from files
reactions_data = np.loadtxt(reaction_file, delimiter=None)  # Adjust delimiter and skiprows if needed
displacements_data = np.loadtxt(disp_file, delimiter=None)  # Adjust delimiter and skiprows if needed

# Extract data columns#4,8,12,16,32,28,24,20,
time_displacements = displacements_data[:, 0]
d500 = displacements_data[:, 1]


#1,5,9,13,17,21,25,29,33,37,41
time_reactions = reactions_data[:, 0]
r1 = reactions_data[:, 1]
r5 = reactions_data[:, 2]
r9 = reactions_data[:, 3]
r13 = reactions_data[:, 4]
r17 = reactions_data[:, 5]
r21 = reactions_data[:, 6]
r25 = reactions_data[:, 7]
r29 = reactions_data[:, 8]
r33 = reactions_data[:, 9]
r37 = reactions_data[:, 10]
r41 = reactions_data[:, 11]

# Calculate the sum of reactions for each time step
sum_reactions = -(r1+r5+r9+r13+r17+r21+r25+r29+r33+r37+r41)
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")
# Plot the sum of reactions and average of displacements
plt.figure(figsize=(10, 6))
plt.plot(d500, sum_reactions, label='Sum of Reactions vs. Displacements of Masternode')
plt.xlabel('Average Displacement (m)')
plt.ylabel('Sum of Horizontal Reactions (kN)')
plt.title('Pushover Curve')
plt.grid(True)
plt.legend()
plt.show()
 
#plot base shear ratio vs Drift ratio
plt.figure(figsize=(10, 6))
plt.plot(d500, sum_reactions/2250, label='Base shear/Total weight vs. Average Displacement (m) ')
plt.xlabel('Average Displacement (m)')
plt.ylabel('Base shear/total weight')
plt.title('Pushover Curve')
plt.grid(True)
plt.legend()
plt.show()

######Saving in Excel ##############
import pandas as pd
# Your code to load data and calculate sum_reactions
# Create a DataFrame
data = {
    'Time': time_displacements,
    'Displacement': d500,
    'Base Shear': sum_reactions,
    'Base/weight': sum_reactions/2250
}
df = pd.DataFrame(data)
# Define the output Excel file path
output_excel_file = 'out.xlsx'
# Export the DataFrame to Excel
df.to_excel(output_excel_file, index=False)
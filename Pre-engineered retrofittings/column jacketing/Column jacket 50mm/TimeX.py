import Modal
direction = 'X'
lamda = 1, 
acc_dir = 'acc_1.txt'
alpha = 0.29
omega = 14
d_o_f = 1    
from openseespy.opensees import *
    

## Records the response of a number of nodes at every converged step
# Global behaviour
# records horizontal reactions of node 1 to 4
recorder('Node','-file','rxn.out','-time','-node',1,'-dof',d_o_f,'reaction')
# records horizontal displacements of node 5 to 8
recorder('Node','-file','disp.out','-time','-node',3,'-dof',d_o_f,'disp')
# records horizontal accelerations of node 5 to 8
recorder('Node','-file','accel.out','-time','-node',3,'-dof',d_o_f,'accel')


import numpy as np
# Reading omega for obraining Rayleigh damping model
xi = 0.05
a_R, b_R = (0, 2*xi/omega)


## Analysis Parameters
accelerogram = np.loadtxt(acc_dir)      # Loads accelerogram file
dt = 0.02                               # Time-Step
n_steps = len(accelerogram)             # Number of steps
tol = 0.00001                            # prescribed tolerance
max_iter = 5000                       # Maximum number of iterations per step




# Uses the norm of the left hand side solution vector of the matrix equation to
# determine if convergence has been reached
test('NormDispIncr', tol, max_iter,0,0)

# RCM numberer uses the reverse Cuthill-McKee scheme to order the matrix equations
numberer('RCM')

# Construct a BandGeneralSOE linear system of equation object
system('BandGen')

# The relationship between load factor and time is input by the user as a 
# series of discrete points
timeSeries('Path', 3, '-dt', dt, '-values', *accelerogram, '-factor', 1)

# allows the user to apply a uniform excitation to a model acting in a certain direction
pattern('UniformExcitation', 2, 1,'-accel', 3)

# Constructs a transformation constraint handler, 
# which enforces the constraints using the transformation method.
constraints('Transformation')

# Create a Newmark integrator.
integrator('Newmark', 0.5, 0.25)

# assign damping to all previously-defined elements and nodes
rayleigh(a_R, b_R, 0.0, 0.0)

# Introduces line search to the Newton algorithm to solve the nonlinear residual equation
algorithm('NewtonLineSearch',True,False,False,False,0.8,100,0.1,10.0)

# Constructs the Transient Analysis object
analysis('Transient')

import time as time
# Measure analysis duration
t = 0
ok = 0
print('Running Time-History analysis with lambda=',lamda)
start_time = time.time()
final_time = getTime() + n_steps*dt
dt_analysis = 0.1*dt

while (ok == 0 and t <= final_time):

    ok = analyze(1, dt_analysis)
    t = getTime()    
    
finish_time = time.time()

if ok == 0:
    print('Time-History Analysis in {} Done in {:1.2f} seconds'.format(direction, finish_time-start_time))
else:
    print('Time-History Analysis in {} Failed in {:1.2f} seconds'.format(direction, finish_time-start_time))

wipe()


#graph visulaixation
import matplotlib.pyplot as plt
story_accel_X = np.loadtxt('accel.out')
plt.figure(figsize=(12,5))
plt.plot(story_accel_X[:,0], story_accel_X[:,1], color = '#DE3163', linewidth=1.2)
#time = np.arange(0, len(np.loadtxt('acc_1.txt')) * 0.02, 0.02)
#plt.plot(time, np.loadtxt('acc_1.txt'))
plt.ylabel('Horizontal Acceleration (m/s2)', {'fontname':'Cambria', 'fontstyle':'italic','size':14})
plt.xlabel('Time (sec)', {'fontname':'Cambria', 'fontstyle':'italic','size':14})
plt.grid(which='both')
plt.title('Time history of horizontal acceleration',{'fontname':'Cambria', 'fontstyle':'normal','size':16})
plt.yticks(fontname = 'Cambria', fontsize = 14);
plt.xticks(fontname = 'Cambria', fontsize = 14);
plt.legend(['X-Direction', 'Y-Direction'], prop={'family':'Cambria','size':14});
plt.show()
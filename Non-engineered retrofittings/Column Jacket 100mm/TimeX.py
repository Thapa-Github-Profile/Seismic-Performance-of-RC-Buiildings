import numpy as np
import random
import openseespy.opensees as ops
import Modal
import os
os.chdir(r'E:\4th year project\opensees\Pushover all typology\Non engineered buildings\column jacketing\Column Jacket 100mm')  
import matplotlib.pyplot as plt
def times(i,j):
    # import Gravity
    
    ops.recorder('Node', '-file', f'Out/di{i}_{j}.out', '-node', 1,2,3,4, '-dof', 1, 'disp')
    # Rayleigh damping model
    t1=0.421 # first mode time period  hhhh
    t2=0.405 # second mode time period hhhh
    xi1 = 0.05
    xi2 = 0.05
    omega1 =  2*3.1415/t1
    omega2 =  2*3.1415/t2
    aR =   2*(omega1*omega2*(omega2*xi1-omega1*xi2))/(omega2**2-omega1**2)
    bR =   2*(omega2*xi2-omega1*xi1)/(omega2**2-omega1**2)
   
    ## Analysis Parameters
    acc_datafile = f'GM/{j}.txt'
    accelerogram = np.loadtxt(acc_datafile,delimiter=None)[:,1]  # Loads accelerogram file
    pga= np.max(np.abs(accelerogram))
    TS= np.loadtxt(acc_datafile,delimiter=None)[:,0] 
    dt = TS[2]-TS[1] # Time-Step
    n_steps = len(accelerogram)  # Number of steps
    tol = 0.0001  # prescribed tolerance
    max_iter = 5000  # Maximum number of iterations per step
    ops.test('NormDispIncr', tol, max_iter, 0, 0)
    ops.numberer('RCM')
    ops.system('BandGen')
    a=random.randint(0, 10000000)
    ops.timeSeries('Path', a, '-dt', dt, '-values', *accelerogram, '-factor', i * 0.981/pga)
    ops.pattern('UniformExcitation', a, 1, '-accel', a)
    ops.constraints('Transformation')
    ops.integrator('Newmark', 0.5, 0.25)
    
    ops.rayleigh(aR, bR, 0., 0.)

    ops.algorithm('NewtonLineSearch', True, False, False, False, 0.8, 100, 0.1, 10.0)
    ops.analysis('Transient')
    print(f'TH Started - Scaling Factor: {i/10}g-Earthquake:{j}')
    aa=ops.analyze(n_steps, dt)
    if(aa<0):
        return
    print(f'TH Finished')
    # ops.wipe()
    ops.setTime(0.0)
    ## Set the loads constant in the domain
    ops.loadConst()
    ## Remove all recorder objects.
    ops.remove('recorders')
    ## destroy all components of the Analysis object
    ops.wipeAnalysis()
    
    


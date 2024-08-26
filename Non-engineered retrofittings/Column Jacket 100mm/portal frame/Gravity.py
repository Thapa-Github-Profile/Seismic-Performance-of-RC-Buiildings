################################################################################
# START ANALYSIS
################################################################################
from Modal import *
import openseespy.opensees as ops
ops.recorder('Node', '-file', 'Gravity_Reactions.out','-time','-node', 1,5,9 ,  '-dof', 2, 'reaction')
ops.timeSeries('Linear', 1)
ops.pattern('Plain', 1, 1)
# First Floor
ops.load(2,0,-55.037,0)
ops.load(6,0,-85.235,0)
ops.load(10,0,-61.98,0)

# Second Floor
ops.load(3,0,-55.037,0)
ops.load(7,0,-85.235,0)
ops.load(11,0,-61.98,0)

# Third Flor
ops.load(4,0,-28.311,0)
ops.load(8,0,-47.265,0)
ops.load(12,0,-32.295,0)

              
# Constraint Handler 
ops.constraints('Transformation')
# DOF Numberer                                
ops.numberer('RCM')   
# System of Equations  
ops.system('BandGeneral') 
# Convergence Test 
ops.test('NormDispIncr',0.000001,100,0,2)   
# Solution Algorithm 
ops.algorithm('Newton') 
# Integrator
#integrator LoadControl $lambda <$numIter $minLambda $maxLambda>  
ops.integrator('LoadControl',0.1)   
# Analysis Type 
ops.analysis('Static')
# Record initial state of model 
ops.record
# Analyze model 
ops.analyze(10)  
ops.loadConst('-time', 0.0)
print("ooo  Gravity  Completed ")

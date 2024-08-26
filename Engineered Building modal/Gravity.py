################################################################################
# START ANALYSIS
################################################################################
from Modal import *
import openseespy.opensees as ops
ops.recorder('Node', '-file', 'Gravity_Reactions.out','-time','-node', 1,5,9,13,17,21,25,29,33,37,41 ,  '-dof', 3, 'reaction')
ops.timeSeries('Linear', 1)
ops.pattern('Plain', 1, 1)
# First Floor
ops.load(2,0,0,-69.21,0,0,0)
ops.load(6,0,0,-97.85,0,0,0)
ops.load(10,0,0,-99.55,0,0,0)
ops.load(14,0,0,-70.75,0,0,0)
ops.load(18,0,0,-99.34,0,0,0)
ops.load(22,0,0,-127.29,0,0,0)
ops.load(26,0,0,-129.18,0,0,0)
ops.load(30,0,0,-70.76,0,0,0)
ops.load(34,0,0,-68.32,0,0,0)
ops.load(38,0,0,-97.69,0,0,0)
ops.load(42,0,0,-66.98,0,0,0)

# Second Floor
ops.load(3,0,0,-69.21,0,0,0)
ops.load(7,0,0,-97.85,0,0,0)
ops.load(11,0,0,-99.55,0,0,0)
ops.load(15,0,0,-70.75,0,0,0)
ops.load(19,0,0,-99.34,0,0,0)
ops.load(23,0,0,-127.29,0,0,0)
ops.load(27,0,0,-129.18,0,0,0)
ops.load(31,0,0,-70.76,0,0,0)
ops.load(35,0,0,-68.32,0,0,0)
ops.load(39,0,0,-97.69,0,0,0)
ops.load(43,0,0,-66.98,0,0,0)

# Third Floor
ops.load(4,0,0,-33.95,0,0,0)
ops.load(8,0,0,-53.4,0,0,0)
ops.load(12,0,0,-54.43,0,0,0)
ops.load(16,0,0,-34.91,0,0,0)
ops.load(20,0,0,-54.32,0,0,0)
ops.load(24,0,0,-84.55,0,0,0)
ops.load(28,0,0,-74.29,0,0,0)
ops.load(32,0,0,-34.9,0,0,0)
ops.load(36,0,0,-33.44,0,0,0)
ops.load(40,0,0,-53.16,0,0,0)
ops.load(44,0,0,-32.63,0,0,0)

              
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

################################################################################
# START ANALYSIS
################################################################################
from Modal import *
import openseespy.opensees as ops
ops.recorder('Node', '-file', 'Gravity_Reactions.out','-time','-node', 1,5,9,13,17,21,25,29,33,37,41 ,  '-dof', 3, 'reaction')
ops.timeSeries('Linear', 1)
ops.pattern('Plain', 1, 1)
# First Floor
ops.load(2,0,0,-66.6,0,0,0)
ops.load(6,0,0,-95.24,0,0,0)
ops.load(10,0,0,-96.95,0,0,0)
ops.load(14,0,0,-68.14,0,0,0)
ops.load(18,0,0,-96.74,0,0,0)
ops.load(22,0,0,-124.69,0,0,0)
ops.load(26,0,0,-126.57,0,0,0)
ops.load(30,0,0,-68.15,0,0,0)
ops.load(34,0,0,-65.72,0,0,0)
ops.load(38,0,0,-95.08,0,0,0)
ops.load(42,0,0,-64.38,0,0,0)

# Second Floor
ops.load(3,0,0,-65.451048,0,0,0)
ops.load(7,0,0,-94.091248,0,0,0)
ops.load(11,0,0,-95.795748,0,0,0)
ops.load(15,0,0,-66.993748,0,0,0)
ops.load(19,0,0,-95.588348,0,0,0)
ops.load(23,0,0,-123.536448,0,0,0)
ops.load(27,0,0,-125.423848,0,0,0)
ops.load(31,0,0,-67.002948,0,0,0)
ops.load(35,0,0,-64.568548,0,0,0)
ops.load(39,0,0,-93.932248,0,0,0)
ops.load(43,0,0,-63.225748,0,0,0)

# Third Floor
ops.load(4,0,0,-32.07,0,0,0)
ops.load(8,0,0,-51.52,0,0,0)
ops.load(12,0,0,-52.56,0,0,0)
ops.load(16,0,0,-33.03,0,0,0)
ops.load(20,0,0,-52.44,0,0,0)
ops.load(24,0,0,-82.67,0,0,0)
ops.load(28,0,0,-72.42,0,0,0)
ops.load(32,0,0,-33.03,0,0,0)
ops.load(36,0,0,-31.56,0,0,0)
ops.load(40,0,0,-51.28,0,0,0)
ops.load(44,0,0,-30.76,0,0,0)
           
# Constraint Handler 
ops.constraints('Transformation')
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

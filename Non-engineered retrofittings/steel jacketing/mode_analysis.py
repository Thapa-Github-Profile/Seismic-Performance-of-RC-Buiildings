import Modal
import openseespy.opensees as ops
import numpy as np


# Records Eigenvector entries for Node 1,3 & 5 @ dof 1 
ops.recorder('Node', '-file', 'modeshape1.out', '-node', *list(range(1,5)), '-dof', 1, 'eigen 1')
ops.recorder('Node', '-file', 'modeshape2.out', '-node', *list(range(1,5)), '-dof', 1, 'eigen 2')
ops.recorder('Node', '-file', 'modeshape3.out','-node', *list(range(1,5)), '-dof', 1, 'eigen 3')                 

# Constructs a transformation constraint handler, 
# which enforces the constraints using the transformation method.
ops.constraints('Transformation')

# Constructs a Plain degree-of-freedom numbering object
# to provide the mapping between the degrees-of-freedom at
# the nodes and the equation numbers.
ops.numberer('Plain')

# Construct a BandGeneralSOE linear system of equation object
ops.system('BandGen')

# Uses the norm of the left hand side solution vector of the matrix equation to
# determine if convergence has been reached
ops.test('NormDispIncr', 1.0e-12, 25, 0, 2)

# Uses the Newton-Raphson algorithm to solve the nonlinear residual equation
ops.algorithm('Newton')

# Create a Newmark integrator.
ops.integrator('Newmark', 0.5, 0.25)

# Constructs the Transient Analysis object
ops.analysis('Transient')

# Eigenvalue analysis
n_evs=3
lamda = np.array(ops.eigen(n_evs))


# Writing Eigenvalue information to file
with open('ModalAnalysis_Node_EigenVectors_EigenVal.out', "w") as eig_file:
    # Writing data to a file
    eig_file.write("lambda omega period frequency\n")
    for l in lamda:
        line_to_write = [l, l**0.5, 2*np.pi/(l**0.5), (l**0.5)/(2*np.pi)]
        eig_file.write('{:2.6e} {:2.6e} {:2.6e} {:2.6e}'.format(*line_to_write))
        eig_file.write('\n')


# Record eigenvectors 
ops.record()    

print("Modal analysis Done!")
# Import OpenSeesPy library
import openseespy.opensees as ops
import matplotlib.pyplot as plt
import openseespy.postprocessing.Get_Rendering as opsplt
import os
# Unit KN, m, s
#os.chdir(r"C:\Users\lenovo\Downloads\Retrofit_noneng\NonEngineered")
ops.wipe()
ops.model('BasicBuilder', '-ndm', 3, '-ndf', 6)  # 3 dimensions, 6 DOF per node
# GLOBAL GEOMETRY
x = [0.0, 3.2, 7.1]
y = [0.0, 3.07, 6.58, 10.04]
z = [0.0, 3, 6, 9]

nodeID = 1  # Start with the first node ID
for i in range(len(x)):
    for j in range(len(y)):
        for k in range(len(z)):
            x_coord = x[i]
            y_coord = y[j]
            z_coord = z[k]
            # Check if x_coord is 7.1 , y coord is 10.04 and z_coord is 9
            if not (x_coord == 7.1 and z_coord == 9 and y_coord==10.05):
                # Create the node and assign coordinates
                ops.node(nodeID, x_coord, y_coord, z_coord)
                
                if z_coord == 0: #fixing base
                    ops.fix(nodeID, 1, 1, 1, 1, 1, 1)
                # Increment the node ID
                nodeID += 1

totalid=nodeID-1
# RESTRAINTS
# rigid diaphragm nodes (Modal Shape herda yo section lai comment garna parxa)
#Defining the center of each floor
ops.node(300,3.55,5.02,3) #300,400,500 are unique random tag no for rigid diaphgram
ops.node(400,3.55,5.02,6)
ops.node(500,3.55,5.02,9)



# Mass 1st floor
ops.mass(2,5.62,5.62,5.62,0,0,0)
ops.mass(6,8.28,8.28,8.28,0,0,0)
ops.mass(10,8.68,8.68,8.68,0,0,0)
ops.mass(14,6.01,6.01,6.01,0,0,0)
ops.mass(18,8.69,8.69,8.69,0,0,0)
ops.mass(22,11.21,11.21,11.21,0,0,0)
ops.mass(26,11.73,11.73,11.73,0,0,0)
ops.mass(30,9.22,9.22,9.22,0,0,0)
ops.mass(34,6.32,6.32,6.32,0,0,0)
ops.mass(38,9.18,9.18,9.18,0,0,0)
ops.mass(42,9.62,9.62,9.62,0,0,0)
ops.mass(46,6.76,6.76,6.76,0,0,0)








#Mass 2nd floor
ops.mass(3,5.62,5.62,5.62,0,0,0)
ops.mass(7,8.28,8.28,8.28,0,0,0)
ops.mass(11,8.68,8.68,8.68,0,0,0)
ops.mass(15,6.01,6.01,6.01,0,0,0)
ops.mass(19,8.69,8.69,8.69,0,0,0)
ops.mass(23,11.21,11.21,11.21,0,0,0)
ops.mass(27,11.73,11.73,11.73,0,0,0)
ops.mass(31,9.22,9.22,9.22,0,0,0)
ops.mass(35,6.32,6.32,6.32,0,0,0)
ops.mass(39,9.18,9.18,9.18,0,0,0)
ops.mass(43,9.62,9.62,9.62,0,0,0)
ops.mass(47,6.76,6.76,6.76,0,0,0)











#Mass for top Floor
ops.mass(4,2.89,2.89,2.89,0,0,0)
ops.mass(8,4.61,4.61,4.61,0,0,0)
ops.mass(12,4.83,4.83,4.83,0,0,0)
ops.mass(16,3.12,3.12,3.12,0,0,0)
ops.mass(20,4.82,4.82,4.82,0,0,0)
ops.mass(24,7.44,7.44,7.44,0,0,0)
ops.mass(28,7.84,7.84,7.84,0,0,0)
ops.mass(32,5.22,5.22,5.22,0,0,0)
ops.mass(36,3.3,3.3,3.3,0,0,0)
ops.mass(40,5.27,5.27,5.27,0,0,0)
ops.mass(44,5.54,5.54,5.54,0,0,0)
ops.mass(48,3.56,3.56,3.56,0,0,0)






# Fixing central node
ops.fix(300,0,0,1,1,1,0)
ops.fix(400,0,0,1,1,1,0)
ops.fix(500,0,0,1,1,1,0)

# Assigning load to central node (Master Node)
#rigidDiaphragm(perpDirn, Master node tag, Slave node Tag), perpDirn=3(Z axis in this case). 
ops.rigidDiaphragm(3, 300, 2,6,10,14,18,22,26,30,34,38,42,46)
ops.rigidDiaphragm(3, 400, 3,7,11,15,19,23,27,31,35,39,43,47)
ops.rigidDiaphragm(3, 500, 4,8,12,16,20,24,28,32,36,40,44,48)
# Define the model in OpenSeesPy
# Definition of materials IDs
C_unconf = 1
C_conf = 2
R_steel = 3

# Basic parameters for materials
fc_1 = -15000  # f'c in compression for unconfined concrete
fc_2 = -15000  # f'c in compression for confined concrete
epsc = -0.002  # strain at maximum stress in compression
fu_1 = fc_1 * 0.2  # ultimate stress for unconfined concrete
fu_2 = fc_2 * 0.2  # ultimate stress for confined concrete
epsu = -0.02  # strain at ultimate stress in compression
lambda_ = 0.1  # ratio between reloading stiffness and initial stiffness in compression
ft_1 = fc_1 * -0.1  # maximum stress in tension for unconfined concrete
ft_2 = fc_2 * -0.1  # maximum stress in tension for confined concrete
Et_1 = ft_1 / 0.002  # Elastic modulus in tension for unconfined concrete
Et_2 = ft_2 / 0.002  # Elastic modulus in tension for confined concrete
fy = 415000  # fy for reinforcing steel
Es = 210000000  # E for reinforcing steel
b = 0.005  # strain hardening ratio
R0 = 20  # smoothness of the elastic-to-plastic transition
cR1 = 0.925  # smoothness of the elastic-to-plastic transition
cR2 = 0.15  # smoothness of the elastic-to-plastic transition

# Definition of Concrete02 material
# uniaxialMaterial Concrete02 $matTag $fpc $epsc0 $fpcu $epsU $lambda $ft $Ets
ops.uniaxialMaterial('Concrete02', C_unconf, fc_1, epsc, fu_1, epsu, lambda_, ft_1, Et_1)
ops.uniaxialMaterial('Concrete02', C_conf, fc_2, epsc, fu_2, epsu, lambda_, ft_2, Et_2)

# Definition of Steel02 steel
# uniaxialMaterial Steel02 $matTag $Fy $E $b $R0 $cR1 $cR2
ops.uniaxialMaterial('Steel02', R_steel, fy, Es, b, R0, cR1, cR2)


# Continue with the rest of your analysis and modeling in OpenSeesPy.
# SECTIONS
# Define section IDs
col230x230_4_16 = 1
#Col230x230_4_16 = 2
Col230x230_4_12 = 3
Beam230x350= 4

# Define dimensions
pi = 3.14
Rebar_16 = pi * 0.016 * 0.016 / 4  # area rebar 
Rebar_20 = pi * 0.02 * 0.02 / 4 
Rebar_12 = pi * 0.012 * 0.012 / 4 
b_col = 0.23  # column base
h_col = 0.23  # column height
cover_Col = 0.02  # column cover
b_beam = 0.23  # beam base
h_beam = 0.35  # beam height
cover_Beam = 0.02  # beam cover

# # Load procedure
import FiberBuilder
# Build sections
# ColumnBuilder(id, HSec, BSec, cover, coreID, coverID, steelID, barAreaCorner, barAreaInt) # 4 Bars in Corners  and 4 bars in intermidiate
# BeamBuilder(id, HSec, BSec, cover, coreID, coverID, steelID, numBarsTop, barAreaTop, numBarsBot, barAreaBot) #assume no intermidiate bar
#FiberBuilder.ColumnBuilder(col230x230_4_16, h_col, b_col, cover_Col, C_conf, C_unconf, R_steel, Rebar_20, 0.000001)
FiberBuilder.ColumnBuilder(col230x230_4_16, h_col, b_col, cover_Col, C_conf, C_unconf, R_steel, Rebar_16, 0.000001)
FiberBuilder.ColumnBuilder(Col230x230_4_12, h_col, b_col, cover_Col, C_conf, C_unconf, R_steel, Rebar_12, 0.000001)
FiberBuilder.BeamBuilder(Beam230x350, h_beam, b_beam, cover_Beam, C_conf, C_unconf, R_steel, 3, Rebar_12, 3, Rebar_12)

# ELEMENTS
# Definition of transformation IDs
PDTransCol = 1
LTransBeaX = 2
LTransBeaY = 3

# Definition of transformations
# geomTransf PDelta $transfTag $vecxzX $vecxzY $vecxzZ <-jntOffset $dXi $dYi $dZi $dXj $dYj $dZj>
ops.geomTransf('PDelta', PDTransCol, -1, 0, 0)  # P-Delta effects included
ops.geomTransf('PDelta', LTransBeaX, 0, 1, 0)
ops.geomTransf('PDelta', LTransBeaY, 1, 0, 0)
# Definition of the number of integration points
NI = 5
# Define element properties (e.g., section and transformation tags)
# Initialize the element tag


######################  COLUMN  ##############################################
# First Floor Column
#ops.element('nonlinearBeamColumn', eleTag, i, j, NI, Col300x300, PDTransCol)
ops.element('nonlinearBeamColumn', 1, 1, 2, NI, col230x230_4_16, PDTransCol)
ops.element('nonlinearBeamColumn', 2, 5, 6, NI, col230x230_4_16, PDTransCol)
ops.element('nonlinearBeamColumn', 3, 9,10, NI, col230x230_4_16, PDTransCol)
ops.element('nonlinearBeamColumn', 4, 13, 14, NI, col230x230_4_16, PDTransCol)
ops.element('nonlinearBeamColumn', 5, 17, 18, NI, col230x230_4_16, PDTransCol)
ops.element('nonlinearBeamColumn', 6, 21, 22, NI, col230x230_4_16, PDTransCol)
ops.element('nonlinearBeamColumn', 7, 25, 26, NI, col230x230_4_16, PDTransCol)
ops.element('nonlinearBeamColumn', 8, 29, 30, NI, col230x230_4_16, PDTransCol)
ops.element('nonlinearBeamColumn', 9, 33, 34, NI, col230x230_4_16, PDTransCol)
ops.element('nonlinearBeamColumn', 10, 37, 38, NI, col230x230_4_16, PDTransCol)
ops.element('nonlinearBeamColumn', 11, 41, 42, NI, col230x230_4_16, PDTransCol)
ops.element('nonlinearBeamColumn', 12, 45, 46, NI, col230x230_4_16, PDTransCol)
# # Second Floor Column
ops.element('nonlinearBeamColumn', 13, 2, 3, NI,   Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 14, 6, 7, NI,   Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 15, 10, 11, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 16, 14, 15, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 17, 18, 19, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 18, 22, 23, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 19, 26, 27, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 20, 30, 31, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 21, 34, 35, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 22, 38, 39, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 23, 42, 43, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 24, 46, 47, NI, Col230x230_4_12, PDTransCol)


# # Top Floor Column
ops.element('nonlinearBeamColumn', 25, 3, 4, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 26, 7, 8, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 27, 11, 12, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 28, 15, 16, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 29, 19, 20, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 30, 23, 24, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 31, 27, 28, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 32, 31, 32, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 33, 35, 36, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 34, 39, 40, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 35, 43, 44, NI, Col230x230_4_12, PDTransCol)
ops.element('nonlinearBeamColumn', 36, 47, 48, NI, Col230x230_4_12, PDTransCol)




# ###############################  BEAM PARALLEL TO X-AXIS  ################################
# #First Floor
ops.element('nonlinearBeamColumn', 37, 2, 18, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 38, 6, 22, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 39, 10, 26, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 40, 14, 30, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 41, 18, 34, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 42, 22, 38, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 43, 26, 42, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 44, 30, 46, NI, Beam230x350, LTransBeaX)

# #Second Floor
ops.element('nonlinearBeamColumn', 45, 3, 19, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 46, 7, 23, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 47, 11, 27, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 48, 15, 31, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 49, 19, 35, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 50, 23, 39, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 51, 27, 43, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 52, 31, 47, NI, Beam230x350, LTransBeaX)

# #Top Floor
ops.element('nonlinearBeamColumn', 53, 4, 20, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 54, 8, 24, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 55, 12, 28, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 56, 16, 32, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 57, 20, 36, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 58, 24, 40, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 59, 28, 44, NI, Beam230x350, LTransBeaX)
ops.element('nonlinearBeamColumn', 60, 32, 48, NI, Beam230x350, LTransBeaX)



# ###############################  BEAM PARALLEL TO Y-AXIS  ################################

# # First Floor
ops.element('nonlinearBeamColumn', 61, 2, 6, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 62, 6, 10, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 63, 10, 14, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 64, 18, 22, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 65, 22, 26, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 66, 26, 30, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 67, 34, 38, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 68, 38, 42, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 69, 42, 46, NI, Beam230x350, LTransBeaY)

# # Second Floor
ops.element('nonlinearBeamColumn', 70, 3, 7, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 71, 7, 11, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 72, 11, 15, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 73, 19, 23, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 74, 23, 27, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 75, 27, 31, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 76, 35, 39, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 77, 39, 43, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 78, 43, 47, NI, Beam230x350, LTransBeaY)

# # Top Floor
ops.element('nonlinearBeamColumn', 79, 4, 8, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 80, 8, 12, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 81, 12, 16, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 82, 20, 24, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 83, 24, 28, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 84, 28, 32, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 85, 36, 40, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 86, 40, 44, NI, Beam230x350, LTransBeaY)
ops.element('nonlinearBeamColumn', 87, 44, 48, NI, Beam230x350, LTransBeaY)


#opsplt.plot_model()
opsplt.plot_model("nodes","elements")
opsplt.plot_modeshape(1)
#opsplt.plot_modeshape(2)
#opsplt.plot_modeshape(3)

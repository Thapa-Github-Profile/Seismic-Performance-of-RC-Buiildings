# Import OpenSeesPy library
import openseespy.opensees as ops
import matplotlib.pyplot as plt
import os
os.chdir(r"E:\4th year project\opensees\Pushover all typology\Pre Engineered Buildings\column jacketing\Column jacket 75mm")
import openseespy.postprocessing.Get_Rendering as opsplt
ops.wipe()
ops.model('BasicBuilder', '-ndm', 3, '-ndf', 6)  # 3 dimensions, 6 DOF per node
# GLOBAL GEOMETRY
x=[0.0, 3.734, 7.391] 
y=[0.0, 3.734, 7.34,11.15]
z=[0.0, 2.845, 5.69,8.534]

nodeID = 1   ################################## Start with the first node ID
for i in range(len(x)):
    for j in range(len(y)):
        for k in range(len(z)):
            x_coord = x[i]
            y_coord = y[j]
            z_coord = z[k]
            # Check if x_coord is 7.391 and z_coord is 8.534
            if not (x_coord==7.391 and y_coord==11.15 and z_coord==z[k]):
                # Create the node and assign coordinates
                ops.node(nodeID, x_coord, y_coord, z_coord)
                            
                if z_coord == 0: #fixing base
                    ops.fix(nodeID, 1, 1, 1, 1, 1, 1)
                # Increment the node ID
                nodeID += 1

totalid=nodeID-1
#Assigning mass in each nodeID
##### First floor#####
ops.mass(2,6.52,6.52,6.52,0,0,0)
ops.mass(6,9.21,9.21,9.21,0,0,0)
ops.mass(10,9.38,9.38,9.38,0,0,0)
ops.mass(14,6.68,6.68,6.68,0,0,0)
ops.mass(18,9.37,9.37,9.37,0,0,0)
ops.mass(22,11.79,11.79,11.79,0,0,0)
ops.mass(26,12.18,12.18,12.18,0,0,0)
ops.mass(30,6.68,6.68,6.68,0,0,0)
ops.mass(34,6.43,6.43,6.43,0,0,0)
ops.mass(38,9.21,9.21,9.21,0,0,0)
ops.mass(42,6.31,6.31,6.31,0,0,0)


#############second floor#################
ops.mass(3,6.4,6.4,6.4,0,0,0)
ops.mass(7,9.09,9.09,9.09,0,0,0)
ops.mass(11,9.27,9.27,9.27,0,0,0)
ops.mass(15,6.56,6.56,6.56,0,0,0)
ops.mass(19,9.25,9.25,9.25,0,0,0)
ops.mass(23,11.67,11.67,11.67,0,0,0)
ops.mass(27,12.06,12.06,12.06,0,0,0)
ops.mass(31,6.56,6.56,6.56,0,0,0)
ops.mass(35,6.32,6.32,6.32,0,0,0)
ops.mass(39,9.09,9.09,9.09,0,0,0)
ops.mass(43,6.19,6.19,6.19,0,0,0)


##########3rd floor##############
ops.mass(4,3.96,3.96,3.96,0,0,0)
ops.mass(8,5.91,5.91,5.91,0,0,0)
ops.mass(12,6.04,6.04,6.04,0,0,0)
ops.mass(16,4.07,4.07,4.07,0,0,0)
ops.mass(20,6.03,6.03,6.03,0,0,0)
ops.mass(24,8.4,8.4,8.4,0,0,0)
ops.mass(28,8.06,8.06,8.06,0,0,0)
ops.mass(32,4.07,4.07,4.07,0,0,0)
ops.mass(36,3.9,3.9,3.9,0,0,0)
ops.mass(40,5.9,5.9,5.9,0,0,0)
ops.mass(44,3.8,3.8,3.8,0,0,0)


# RESTRAINTS
# rigid diaphragm nodes (Modal Shape herda yo section lai comment garna parxa)
#Defining the center of each floor
x_rigid= 3.315
y_rigid= 4.828
ops.node(3000,x_rigid,y_rigid,2.845) #300,400,500 are unique random tag no for rigid diaphgram
ops.node(4000,x_rigid,y_rigid,5.69)
ops.node(5000,x_rigid,y_rigid,8.534)

# Fixing central node
ops.fix(3000,0,0,1,1,1,0)
ops.fix(4000,0,0,1,1,1,0)
ops.fix(5000,0,0,1,1,1,0)

#Assigning mass at master node of floor with rigid diaphgram
#ops.mass(3000,107.5,107.5,107.5,0,0,0)
##ops.mass(4000,107.5,107.5,107.5,0,0,0)
#ops.mass(5000,75,75,75,0,0,0)



# Assigning load to central node (Master Node) / Assigning diaphragm
# rigidDiaphragm(perpDirn, Master node tag, Slave node Tag), perpDirn=3(Z axis in this case). 
ops.rigidDiaphragm(3, 3000, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42)
ops.rigidDiaphragm(3, 4000, 3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43)
ops.rigidDiaphragm(3, 5000, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44)

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
Col230x300_8x12 = 1 ### Frst floor column #######
Beam230x325_1 = 3   #### Beam Frst and 2nd ####
Col230x230_4x12 = 2  #### second and 3rd #######
Beam230x325_2 =4   ##### 3rd beam ##########

# Define dimensions
pi = 3.14
Rebar_16 = pi * 0.016 * 0.016 / 4 # area rebar 16mm
Rebar_20 = pi * 0.020 * 0.020 / 4 # area rebar 20mm
Rebar_12 = pi * 0.012 * 0.012 / 4 # area rebar 12mm
Rebar_10 = pi * 0.010 * 0.010 / 4 # area rebar 12mm

h_col1 = 0.3    # 1st column depth
b_col = 0.23   # column base
h_col = 0.23   # column height
cover_col = 0.02   # column cover
b_beam = 0.23  # beam base
h_beam = 0.325  # beam height
r_beam = 0.02  # beam cover
# # Load procedure
import FiberBuilder


# Build sections
jack_unconfinedID = 100
Jacket_confinedID = 101
JbarAreaInt= Rebar_12
JbarAreaCorner= Rebar_12
thickness = 0.075
jacket_Cover=0.02
ops.uniaxialMaterial('Concrete02', jack_unconfinedID, fc_1, epsc, fu_1, epsu, lambda_, ft_1, Et_1)
ops.uniaxialMaterial('Concrete02', Jacket_confinedID, fc_1, epsc, fu_1, epsu, lambda_, ft_1, Et_1)

#JacketBuilder(id, HSec, BSec, cover, coreID, coverID, steelID, barAreaCorner, barAreaInt,jack_unconfinedID,Jacket_confinedID,JbarAreaInt,JbarAreaCorner,thickness,jacket_Cover) 
#BeamBuilder(id, HSec, BSec, cover, coreID, coverID, steelID, numBarsTop, barAreaTop, numBarsBot, barAreaBot) #assume no intermidiate bar
FiberBuilder.JacketBuilder(Col230x300_8x12, h_col1, b_col, cover_col, C_conf, C_unconf, R_steel, Rebar_12, Rebar_12, jack_unconfinedID,Jacket_confinedID,JbarAreaInt,JbarAreaCorner,thickness,jacket_Cover)
FiberBuilder.JacketBuilder(Col230x230_4x12, h_col, b_col, cover_col, C_conf, C_unconf, R_steel, Rebar_12, 0.000000001, jack_unconfinedID,Jacket_confinedID,JbarAreaInt,JbarAreaCorner,thickness,jacket_Cover)

FiberBuilder.BeamBuilder(Beam230x325_1, h_beam, b_beam, r_beam, C_conf, C_unconf, R_steel, 3, Rebar_16, 3, Rebar_12) ### 1st and 2nd
FiberBuilder.BeamBuilder(Beam230x325_2, h_beam, b_beam, r_beam, C_conf, C_unconf, R_steel, 2, Rebar_16, 2, Rebar_12) ### 3rd floor


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
NI = 4
# Define element properties (e.g., section and transformation tags)
# Initialize the element tag


######################  COLUMN  ##############################################
# Ground Floor Column
#ops.element('nonlinearBeamColumn', eleTag, i, j, NI, Col300x300, PDTransCol)
ops.element('nonlinearBeamColumn',1 ,1 , 2, NI,Col230x300_8x12 , PDTransCol)
ops.element('nonlinearBeamColumn',2 ,5 , 6, NI, Col230x300_8x12, PDTransCol)
ops.element('nonlinearBeamColumn',3 ,9 , 10,NI, Col230x300_8x12, PDTransCol)
ops.element('nonlinearBeamColumn',4 ,13, 14,NI, Col230x300_8x12, PDTransCol)
ops.element('nonlinearBeamColumn',5 ,17, 18,NI, Col230x300_8x12, PDTransCol)
ops.element('nonlinearBeamColumn',6 ,21, 22,NI, Col230x300_8x12, PDTransCol)
ops.element('nonlinearBeamColumn',7 ,25, 26,NI, Col230x300_8x12, PDTransCol)
ops.element('nonlinearBeamColumn',8 ,29, 30,NI, Col230x300_8x12, PDTransCol)
ops.element('nonlinearBeamColumn',9 ,33, 34,NI, Col230x300_8x12, PDTransCol)
ops.element('nonlinearBeamColumn',10 ,37, 38,NI, Col230x300_8x12, PDTransCol)
ops.element('nonlinearBeamColumn',11 ,41, 42,NI, Col230x300_8x12, PDTransCol)

################column elements##################
####### First Floor ####################
#ops.element('nonlinearBeamColumn', eleTag, i, j, NI, Col300x300, PDTransCol)
ops.element('nonlinearBeamColumn',12 ,2 , 3, NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',13 ,6 , 7, NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',14 ,10 ,11,NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',15 ,14, 15,NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',16 ,18, 19,NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',17 ,22, 23,NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',18 ,26, 27,NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',19 ,30, 31,NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',20 ,34, 35,NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',21 ,38, 39,NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',22 ,42, 43,NI, Col230x230_4x12, PDTransCol)

################column elements##################
####### second  Floor ####################
#ops.element('nonlinearBeamColumn', eleTag, i, j, NI, Col300x300, PDTransCol)
ops.element('nonlinearBeamColumn',23 ,3 , 4, NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',24 ,7 , 8, NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',25 ,11, 12,NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',26 ,15, 16,NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',27 ,19, 20,NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',28 ,23, 24,NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',29 ,27, 28,NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',30 ,31, 32,NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',31 ,35, 36,NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',32 ,39, 40,NI, Col230x230_4x12, PDTransCol)
ops.element('nonlinearBeamColumn',33 ,43, 44,NI, Col230x230_4x12, PDTransCol)

##### Beams Parllel to X- axis########
########### Ground Floor ##############
ops.element('nonlinearBeamColumn', 34, 2, 18, NI,Beam230x325_1 , LTransBeaX)
ops.element('nonlinearBeamColumn', 35, 6, 22, NI, Beam230x325_1, LTransBeaX)
ops.element('nonlinearBeamColumn', 36, 10, 26, NI, Beam230x325_1, LTransBeaX)
ops.element('nonlinearBeamColumn', 37, 14, 30, NI, Beam230x325_1, LTransBeaX)
ops.element('nonlinearBeamColumn', 38, 18, 34, NI, Beam230x325_1, LTransBeaX)
ops.element('nonlinearBeamColumn', 39, 22, 38, NI, Beam230x325_1, LTransBeaX)
ops.element('nonlinearBeamColumn', 40, 26, 42, NI, Beam230x325_1, LTransBeaX)


########### First Floor ##############
ops.element('nonlinearBeamColumn', 41, 3, 19, NI, Beam230x325_1, LTransBeaX)
ops.element('nonlinearBeamColumn', 42, 7, 23, NI, Beam230x325_1, LTransBeaX)
ops.element('nonlinearBeamColumn', 43, 11, 27, NI, Beam230x325_1, LTransBeaX)
ops.element('nonlinearBeamColumn', 44, 15, 31, NI, Beam230x325_1, LTransBeaX)
ops.element('nonlinearBeamColumn', 45, 19, 35, NI, Beam230x325_1, LTransBeaX)
ops.element('nonlinearBeamColumn', 46, 23, 39, NI, Beam230x325_1, LTransBeaX)
ops.element('nonlinearBeamColumn', 47, 27, 43, NI, Beam230x325_1, LTransBeaX)

########### Second Floor ##############
ops.element('nonlinearBeamColumn', 48, 4, 20, NI, Beam230x325_2, LTransBeaX)
ops.element('nonlinearBeamColumn', 49, 8, 24, NI, Beam230x325_2, LTransBeaX)
ops.element('nonlinearBeamColumn', 50, 12,28, NI, Beam230x325_2, LTransBeaX)
ops.element('nonlinearBeamColumn', 51, 16, 32, NI, Beam230x325_2, LTransBeaX)
ops.element('nonlinearBeamColumn', 52, 20, 36, NI, Beam230x325_2, LTransBeaX)
ops.element('nonlinearBeamColumn', 53, 24, 40, NI, Beam230x325_2, LTransBeaX)
ops.element('nonlinearBeamColumn', 54, 28, 44, NI, Beam230x325_2, LTransBeaX)

##### Beams Parllel to Y- axis########
########### Ground Floor ##############
ops.element('nonlinearBeamColumn', 55, 2, 6 , NI, Beam230x325_1, LTransBeaY)
ops.element('nonlinearBeamColumn', 56, 6, 10, NI, Beam230x325_1, LTransBeaY)
ops.element('nonlinearBeamColumn', 57, 10, 14, NI, Beam230x325_1, LTransBeaY)
ops.element('nonlinearBeamColumn', 58, 18, 22, NI, Beam230x325_1, LTransBeaY)
ops.element('nonlinearBeamColumn', 59, 22, 26, NI, Beam230x325_1, LTransBeaY)
ops.element('nonlinearBeamColumn', 60, 26, 30, NI, Beam230x325_1, LTransBeaY)
ops.element('nonlinearBeamColumn', 61, 34, 38, NI, Beam230x325_1, LTransBeaY)
ops.element('nonlinearBeamColumn', 62, 38, 42, NI, Beam230x325_1, LTransBeaY)

##### Beams Parllel to Y- axis########
########### First Floor ##############
ops.element('nonlinearBeamColumn', 63, 3, 7 , NI, Beam230x325_1, LTransBeaY)
ops.element('nonlinearBeamColumn', 64, 7, 11, NI, Beam230x325_1, LTransBeaY)
ops.element('nonlinearBeamColumn', 65, 11, 15, NI, Beam230x325_1, LTransBeaY)
ops.element('nonlinearBeamColumn', 66, 19, 23, NI, Beam230x325_1, LTransBeaY)
ops.element('nonlinearBeamColumn', 67, 23, 27, NI, Beam230x325_1, LTransBeaY)
ops.element('nonlinearBeamColumn', 68, 27, 31, NI, Beam230x325_1, LTransBeaY)
ops.element('nonlinearBeamColumn', 69, 35, 39, NI, Beam230x325_1, LTransBeaY)
ops.element('nonlinearBeamColumn', 70, 39, 43, NI, Beam230x325_1, LTransBeaY)

##### Beams Parllel to Y- axis########
########### Second Floor ##############
ops.element('nonlinearBeamColumn', 71, 4, 8, NI, Beam230x325_2, LTransBeaY)
ops.element('nonlinearBeamColumn', 72, 8, 12, NI, Beam230x325_2, LTransBeaY)
ops.element('nonlinearBeamColumn', 73, 12, 16, NI, Beam230x325_2, LTransBeaY)
ops.element('nonlinearBeamColumn', 74, 20, 24, NI, Beam230x325_2, LTransBeaY)
ops.element('nonlinearBeamColumn', 75, 24, 28, NI, Beam230x325_2, LTransBeaY)
ops.element('nonlinearBeamColumn', 76, 28, 32, NI, Beam230x325_2, LTransBeaY)
ops.element('nonlinearBeamColumn', 77, 36, 40, NI, Beam230x325_2, LTransBeaY)
ops.element('nonlinearBeamColumn', 78, 40, 44, NI, Beam230x325_2, LTransBeaY)

# opsplt.plot_model()
# opsplt.plot_model("nodes","elements")
opsplt.plot_modeshape(1)
# opsplt.plot_modeshape(2)
# opsplt.plot_modeshape(3)

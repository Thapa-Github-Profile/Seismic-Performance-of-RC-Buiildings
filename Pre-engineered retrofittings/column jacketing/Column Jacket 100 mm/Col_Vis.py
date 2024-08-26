import opsvis as opsv
import matplotlib.pyplot as plt
import openseespy.opensees as ops
#Section Tag
C_unconf = 1
C_conf = 2
R_steel = 3


# Basic parameters for materials
# Units: kN, m, sec
# Concrete Parameter
fc_1 = -20000  # f'c in compression for unconfined concrete
fc_2 = -20000  # f'c in compression for confined concrete
fc_3 = -20000  # f'c in compression for Jacket concrete
epsc = -0.002  # strain at maximum stress in compression
fu_1 = fc_1 * 0.2  # ultimate stress for unconfined concrete
fu_2 = fc_2 * 0.2  # ultimate stress for confined concrete
epsu = -0.02  # strain at ultimate stress in compression
lambda_ = 0.1  # ratio between reloading stiffness and initial stiffness in compression
ft_1 = fc_1 * -0.1  # maximum stress in tension for unconfined concrete
ft_2 = fc_2 * -0.1  # maximum stress in tension for confined concrete
Et_1 = ft_1 / 0.002  # Elastic modulus in tension for unconfined concrete
Et_2 = ft_2 / 0.002  # Elastic modulus in tension for confined concrete
# Steel Parameter
fy = 415000  # fy for reinforcing steel
Es = 210000000  # E for reinforcing steel
b = 0.005  # strain hardening ratio
R0 = 20  # smoothness of the elastic-to-plastic transition
cR1 = 0.925  # smoothness of the elastic-to-plastic transition
cR2 = 0.15  # smoothness of the elastic-to-plastic transition
#Material Defination--Concrete
ops.uniaxialMaterial('Concrete02', C_conf, fc_2, epsc, fu_2, epsu, lambda_, ft_2, Et_2)
ops.uniaxialMaterial('Concrete02', C_unconf, fc_1, epsc, fu_1, epsu, lambda_, ft_1, Et_1)

# Definition of Steel02 steel
# uniaxialMaterial Steel02 $matTag $Fy $E $b $R0 $cR1 $cR2
ops.uniaxialMaterial('Steel02', R_steel, fy, Es, b, R0, cR1, cR2)

#Section Defination
id=1
HSec=0.3
BSec=0.3
cover=0.04
coreID=C_conf
coverID=C_unconf
steelID=R_steel
barAreaCorner=0.000314
barAreaInt=0.000114
coverY = HSec / 2.0
coverZ = BSec / 2.0
coreY = coverY - cover
coreZ = coverZ - cover


#layer(’straight’, matTag, numFiber, areaFiber, *start, *end)
ColumnBuilder = [['section', 'Fiber', 3, '-GJ', 10000000],
            ['patch', 'quadr', coreID, 8, 8, -coreY, coreZ, -coreY, -coreZ, coreY, -coreZ, coreY, coreZ],
            ['patch', 'quadr', coverID, 2, 8, -coverY, coverZ, -coreY, coreZ, coreY, coreZ, coverY, coverZ],
            ['patch', 'quadr', coverID, 2, 8, -coreY, -coreZ, -coverY, -coverZ, coverY, -coverZ, coreY, -coreZ],
            ['patch', 'quadr', coverID, 8, 2, -coverY, coverZ, -coverY, -coverZ, -coreY, -coreZ, -coreY, coreZ],
            ['patch', 'quadr', coverID, 8, 2, coreY, coreZ, coreY, -coreZ, coverY, -coverZ, coverY, coverZ],
            ['layer','straight', steelID, 1, barAreaInt, 0, coreZ, coreY, coreZ],  # intermediate skin reinforcement +z
            ['layer','straight', steelID, 1, barAreaInt, 0, -coreZ, coreY, -coreZ],  # intermediate skin reinforcement -z
            ['layer','straight', steelID, 1, barAreaInt, coreY, 0, coreY, coreZ],  # intermediate skin reinforcement +y
            ['layer','straight', steelID, 1, barAreaInt, -coreY, 0, coreY, -coreZ],  # intermediate skin reinforcement -y
            ['layer','straight', steelID, 2, barAreaCorner, coreY, coreZ, coreY, -coreZ],  # top layer reinforcement
            ['layer','straight', steelID, 2, barAreaCorner, -coreY, coreZ, -coreY, -coreZ]]  # bottom layer reinforcement
                
matcolor = ['w', 'grey', 'r','c','k','w']
opsv.plot_fiber_section(ColumnBuilder, matcolor= matcolor)
plt.axis('equal')
plt.show()

#Jacket Parameters
jackcoverID = 4
ops.uniaxialMaterial('Concrete02', jackcoverID, fc_3, epsc, fu_2, epsu, lambda_, ft_2, Et_2)
jacket_thickness = 0.08
jacket_Cover = 0.04
coverYplusjacket = coreY + jacket_thickness
coverZplusjacket = coreZ + jacket_thickness
barAreajac = 0.0001


#layer(’straight’, matTag, numFiber, areaFiber, *start, *end)
ColumnJacketBuilder = [['section', 'Fiber', 3, '-GJ', 10000000],
            ['patch', 'quadr', coreID, 8, 8, -coreY, coreZ, -coreY, -coreZ, coreY, -coreZ, coreY, coreZ],
            ['patch', 'quadr', jackcoverID, 4, 8, -coverYplusjacket, coverZplusjacket, -coreY, coreZ, coreY, coreZ, coverYplusjacket, coverZplusjacket],
            ['patch', 'quadr', jackcoverID, 4, 8, -coreY, -coreZ, -coverYplusjacket, -coverZplusjacket, coverYplusjacket, -coverZplusjacket, coreY, -coreZ],
            ['patch', 'quadr', jackcoverID, 8, 4, -coverYplusjacket, coverZplusjacket, -coverYplusjacket, -coverZplusjacket, -coreY, -coreZ, -coreY, coreZ],
            ['patch', 'quadr', jackcoverID, 8, 4, coreY, coreZ, coreY, -coreZ, coverYplusjacket, -coverZplusjacket, coverYplusjacket, coverZplusjacket],
            ['layer','straight', steelID, 1, barAreaInt, 0, coreZ, coreY, coreZ],  # intermediate skin reinforcement +z
            ['layer','straight', steelID, 1, barAreaInt, 0, -coreZ, coreY, -coreZ],  # intermediate skin reinforcement -z
            ['layer','straight', steelID, 1, barAreaInt, coreY, 0, coreY, coreZ],  # intermediate skin reinforcement +y
            ['layer','straight', steelID, 1, barAreaInt, -coreY, 0, coreY, -coreZ],  # intermediate skin reinforcement -y
            ['layer','straight', steelID, 2, barAreaCorner, coreY, coreZ, coreY, -coreZ],  # top layer reinforcement
            ['layer','straight', steelID, 2, barAreaCorner, -coreY, coreZ, -coreY, -coreZ],  # bottom layer reinforcement
            ['layer','straight', steelID, 1, barAreaInt, 0, -coverZplusjacket+jacket_Cover, coverYplusjacket, -coverZplusjacket],  #Jacket intermediate skin reinforcement -z
            ['layer','straight', steelID, 1, barAreaInt, 0, coverZplusjacket-jacket_Cover, coverYplusjacket, -coverZplusjacket],  #Jacket intermediate skin reinforcement +z
            ['layer','straight', steelID, 1, barAreaInt, coverYplusjacket-jacket_Cover, 0, coverYplusjacket-jacket_Cover, coverZplusjacket-jacket_Cover],  #Jacket intermediate skin reinforcement +y
            ['layer','straight', steelID, 1, barAreaInt, -coverYplusjacket+jacket_Cover, 0, coverYplusjacket-jacket_Cover, -coverZplusjacket-jacket_Cover], #Jacket intermediate skin reinforcement -y
            ['layer','straight', steelID, 2, barAreaCorner, coverYplusjacket-jacket_Cover, coverZplusjacket-jacket_Cover, coverYplusjacket-jacket_Cover, -coverZplusjacket+jacket_Cover],  # Jacket top layer reinforcement
            ['layer','straight', steelID, 2, barAreaCorner, -coverYplusjacket+jacket_Cover, coverZplusjacket-jacket_Cover, -coverYplusjacket+jacket_Cover, -coverZplusjacket+jacket_Cover]]  # Jacket bottom layer reinforcement  
matcolor = ['w', 'grey', 'r','c','k','w']
opsv.plot_fiber_section(ColumnJacketBuilder, matcolor= matcolor)
plt.axis('equal')
plt.show()
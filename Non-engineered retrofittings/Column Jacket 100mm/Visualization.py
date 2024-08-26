import opsvis as opsv
import matplotlib.pyplot as plt
import openseespy.opensees as ops

C_unconf = 1
C_conf = 2
R_steel = 3
Jacket = 4

# Basic parameters for materials
# Units: kN, m, sec
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

fy = 415000  # fy for reinforcing steel
Es = 210000000  # E for reinforcing steel
b = 0.005  # strain hardening ratio
R0 = 20  # smoothness of the elastic-to-plastic transition
cR1 = 0.925  # smoothness of the elastic-to-plastic transition
cR2 = 0.15  # smoothness of the elastic-to-plastic transition

ops.uniaxialMaterial('Concrete02', C_conf, fc_2, epsc, fu_2, epsu, lambda_, ft_2, Et_2)
ops.uniaxialMaterial('Concrete02', C_unconf, fc_1, epsc, fu_1, epsu, lambda_, ft_1, Et_1)
ops.uniaxialMaterial('Concrete02', Jacket, fc_3, epsc, fu_2, epsu, lambda_, ft_2, Et_2)
# Definition of Steel02 steel
# uniaxialMaterial Steel02 $matTag $Fy $E $b $R0 $cR1 $cR2
ops.uniaxialMaterial('Steel02', R_steel, fy, Es, b, R0, cR1, cR2)

id=1
HSec=0.3
BSec=0.3
coverH=0.04
coverB=0.04
coreID=C_conf
coverID=C_unconf
steelID=R_steel
numBarsTop=2
barAreaCorner=0.0001
numBarsBot=3
barAreaBot=0.0001
numBarsIntTot=1
barAreaInt=0.0001
coverY = HSec / 2.0
coverZ = BSec / 2.0
coreY = coverY - coverH
coreZ = coverZ - coverB
numBarsInt = numBarsIntTot 
totaljacketrebar = 16
jacketrebar = 4
jacket_thickness = 0.04
coverYplusjacket = (HSec + 2* jacket_thickness)/2
coverZplusjacket = (BSec + 2* jacket_thickness)/2
barAreajac = 0.0001
JacketcoverID = Jacket

ColumnBuilder = [['section', 'Fiber', 3, '-GJ', 10000000],
            ['patch', 'quadr', coreID, 8, 8, -coreY, coreZ, -coreY, -coreZ, coreY, -coreZ, coreY, coreZ],
            ['patch', 'quadr', coverID, 2, 8, -coverY, coverZ, -coreY, coreZ, coreY, coreZ, coverY, coverZ],
            ['patch', 'quadr', coverID, 2, 8, -coreY, -coreZ, -coverY, -coverZ, coverY, -coverZ, coreY, -coreZ],
            ['patch', 'quadr', coverID, 8, 2, -coverY, coverZ, -coverY, -coverZ, -coreY, -coreZ, -coreY, coreZ],
            ['patch', 'quadr', coverID, 8, 2, coreY, coreZ, coreY, -coreZ, coverY, -coverZ, coverY, coverZ],
            ['straight', steelID, 1, barAreaInt, 0, coreZ, coreY, coreZ],  # intermediate skin reinforcement +z
            ['straight', steelID, 1, barAreaInt, 0, -coreZ, coreY, -coreZ],  # intermediate skin reinforcement -z
            ['straight', steelID, 1, barAreaInt, coreY, 0, coreY, coreZ],  # intermediate skin reinforcement +y
            ['straight', steelID, 1, barAreaInt, -coreY, 0, coreY, -coreZ],  # intermediate skin reinforcement -y
            ['straight', steelID, 2, barAreaCorner, coreY, coreZ, coreY, -coreZ],  # top layer reinforcement
            ['straight', steelID, 2, barAreaCorner, -coreY, coreZ, -coreY, -coreZ],  # bottom layer reinforcement
            ['patch', 'quadr', coreID, 2, 8, -coverYplusjacket, coverZplusjacket, -coverY, coverZ, coverY, coverZ, coverYplusjacket, coverZplusjacket],
            ['patch', 'quadr', coreID, 2, 8, -coverY, -coverZ, -coverYplusjacket, -coverZplusjacket, coverYplusjacket, -coverZplusjacket, coverY, -coverZ],
            ['patch', 'quadr', coreID, 8, 2, -coverYplusjacket, coverZplusjacket, -coverYplusjacket, -coverZplusjacket, -coverY, -coverZ, -coverY, coverZ],
            ['patch', 'quadr', coreID, 8, 2, coverY, coverZ, coverY, -coverZ, coverYplusjacket, -coverZplusjacket, coverYplusjacket, coverZplusjacket]]
             

matcolor = ['w', 'grey', 'r','c','k','w']
opsv.plot_fiber_section(ColumnBuilder, matcolor= matcolor)
plt.axis('equal')
plt.show()
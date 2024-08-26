#
	#                        y
	#                        ^
	#                        |
	#             -------------------     --   --
	#             |   o     o     o  |     |    -- coverH
	#             |                  |     |
	#             |   o            o |     |
	#      z <--- |          +       |     HSec
	#             |   o            o |     |
	#             |                  |     |
	#             |   o o o o o o    |    -- coverH
	#             -------------------     --   --
	#             |-------Bsec------|
	#             |---| coverB  |---|
	#
	#                       y
	#                       ^
	#                       |
	#             ---------------------
	#             |\      cover       /|
	#             | \------Top-------/ |
	#             |c|                |c|
	#             |o|                |o|
	#     z <-----|v|       core     |v|  HSec
	#             |e|                |e|
	#             |r|                |r|
	#             | /-------Bot------\ |
	#             |/      cover       \|
	#             ---------------------
	#                       Bsec
	#
	#
	# Notes
	#    The core concrete ends at the NA of the reinforcement
	#    The center of the section is at (0,0) in the local axis system

import openseespy.opensees as ops
def BuildRCrectSection_Jacket(id, HSec, BSec, coverH, coverB, coreID, coverID, steelID, numBarsTop, barAreaTop, numBarsBot, barAreaBot, numBarsIntTot, barAreaInt, nfCoreY, nfCoreZ, nfCoverY, nfCoverZ, totaljacketrebar, barAreajac,jacket_thickness, JacketcoverID):
    coverY = HSec / 2.0
    coverZ = BSec / 2.0
    coreY = coverY - coverH
    coreZ = coverZ - coverB
    numBarsInt = numBarsIntTot / 2
    jacketrebar = totaljacketrebar / 4
    coverYplusjacket = (HSec + 2* jacket_thickness)/2
    coverZplusjacket = (BSec + 2* jacket_thickness)/2
#defining pre-jacketed section
    # Define the fiber section
    ops.section('Fiber', id, '-GJ', 1000000000)

    # Define the core patch
    ops.patch('quadr', coreID, nfCoreZ, nfCoreY, -coreY, coreZ, -coreY, -coreZ, coreY, -coreZ, coreY, coreZ)

    # Define the four cover patches
    ops.patch('quadr', coverID, 2, nfCoverY, -coverY, coverZ, -coreY, coreZ, coreY, coreZ, coverY, coverZ)
    ops.patch('quadr', coverID, 2, nfCoverY, -coreY, -coreZ, -coverY, -coverZ, coverY, -coverZ, coreY, -coreZ)
    ops.patch('quadr', coverID, nfCoverZ, 2, -coverY, coverZ, -coverY, -coverZ, -coreY, -coreZ, -coreY, coreZ)
    ops.patch('quadr', coverID, nfCoverZ, 2, coreY, coreZ, coreY, -coreZ, coverY, -coverZ, coverY, coverZ)

    # Define reinforcing layers
    ops.layer('straight', steelID, numBarsInt, barAreaInt, -coreY, coreZ, coreY, coreZ)  # intermediate skin reinforcement +z
    ops.layer('straight', steelID, numBarsInt, barAreaInt, -coreY, -coreZ, coreY, -coreZ)  # intermediate skin reinforcement -z
    ops.layer('straight', steelID, numBarsTop, barAreaTop, coreY, coreZ, coreY, -coreZ)  # top layer reinforcement
    ops.layer('straight', steelID, numBarsBot, barAreaBot, -coreY, coreZ, -coreY, -coreZ)  # bottom layer reinforcement
#defining jacketed section
    # Defining Jacketed reinforcing layer
    ops.layer('straight', steelID, jacketrebar, barAreajac, -coverY, coverZ, coverY, coverZ)  # intermediate skin reinforcement +z
    ops.layer('straight', steelID, jacketrebar, barAreajac, -coverY, -coverZ, coverY, -coverZ)  # intermediate skin reinforcement -z
    ops.layer('straight', steelID, jacketrebar, barAreajac, coverY, coverZ, coverY, -coverZ)  # top layer reinforcement
    ops.layer('straight', steelID, jacketrebar, barAreajac, -coverY, coverZ, -coverY, -coverZ)  # bottom layer reinforcement
    # Defining Jacketed concrete in trapezoidal shape element
    ops.patch('quadr', JacketcoverID, 2, nfCoverY, -coverYplusjacket, coverZplusjacket, -coverY, coverZ, coverY, coverZ, coverYplusjacket, coverZplusjacket)
    ops.patch('quadr', JacketcoverID, 2, nfCoverY, -coverY, -coverZ, -coverYplusjacket, -coverZplusjacket, coverYplusjacket, -coverZplusjacket, coverY, -coverZ)
    ops.patch('quadr', JacketcoverID, nfCoverZ, 2, -coverYplusjacket, coverZplusjacket, -coverYplusjacket, -coverZplusjacket, -coverY, -coverZ, -coverY, coverZ)
    ops.patch('quadr', JacketcoverID, nfCoverZ, 2, coverY, coverZ, coverY, -coverZ, coverYplusjacket, -coverZplusjacket, coverYplusjacket, coverZplusjacket)
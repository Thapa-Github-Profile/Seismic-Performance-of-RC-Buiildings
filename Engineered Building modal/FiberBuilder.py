import openseespy.opensees as ops
def ColumnBuilder(id, HSec, BSec, cover, coreID, coverID, steelID, barAreaCorner, barAreaInt):
    coverY = HSec / 2.0
    coverZ = BSec / 2.0
    coreY = coverY - cover
    coreZ = coverZ - cover
    # Define the fiber section
    ops.section('Fiber', id, '-GJ', 1000000000)
    # Define the core patch
    ops.patch('quadr', coreID, 8, 8, -coreY, coreZ, -coreY, -coreZ, coreY, -coreZ, coreY, coreZ)
    # Define the four cover patches
    ops.patch('quadr', coverID, 2, 8, -coverY, coverZ, -coreY, coreZ, coreY, coreZ, coverY, coverZ)
    ops.patch('quadr', coverID, 2, 8, -coreY, -coreZ, -coverY, -coverZ, coverY, -coverZ, coreY, -coreZ)
    ops.patch('quadr', coverID, 8, 2, -coverY, coverZ, -coverY, -coverZ, -coreY, -coreZ, -coreY, coreZ)
    ops.patch('quadr', coverID, 8, 2, coreY, coreZ, coreY, -coreZ, coverY, -coverZ, coverY, coverZ)
    # Define reinforcing layers
    #layer(’straight’, matTag, numFiber, areaFiber, *start, *end)
    ops.layer('straight', steelID, 1, barAreaInt, 0, coreZ, coreY, coreZ)  # intermediate skin reinforcement +z
    ops.layer('straight', steelID, 1, barAreaInt, 0, -coreZ, coreY, -coreZ)  # intermediate skin reinforcement -z
    ops.layer('straight', steelID, 1, barAreaInt, coreY, 0, coreY, coreZ)  # intermediate skin reinforcement +y
    ops.layer('straight', steelID, 1, barAreaInt, -coreY, 0, coreY, -coreZ)  # intermediate skin reinforcement -y
    ops.layer('straight', steelID, 2, barAreaCorner, coreY, coreZ, coreY, -coreZ)  # top layer reinforcement
    ops.layer('straight', steelID, 2, barAreaCorner, -coreY, coreZ, -coreY, -coreZ)  # bottom layer reinforcement

def BeamBuilder(id, HSec, BSec, cover, coreID, coverID, steelID, numBarsTop, barAreaTop, numBarsBot, barAreaBot):
    coverY = HSec / 2.0
    coverZ = BSec / 2.0
    coreY = coverY - cover
    coreZ = coverZ - cover
    # Define the fiber section
    ops.section('Fiber', id, '-GJ', 1000000000)
    # Define the core patch
    ops.patch('quadr', coreID, 8, 8, -coreY, coreZ, -coreY, -coreZ, coreY, -coreZ, coreY, coreZ)
    # Define the four cover patches
    ops.patch('quadr', coverID, 2, 8, -coverY, coverZ, -coreY, coreZ, coreY, coreZ, coverY, coverZ)
    ops.patch('quadr', coverID, 2, 8, -coreY, -coreZ, -coverY, -coverZ, coverY, -coverZ, coreY, -coreZ)
    ops.patch('quadr', coverID, 8, 2, -coverY, coverZ, -coverY, -coverZ, -coreY, -coreZ, -coreY, coreZ)
    ops.patch('quadr', coverID, 8, 2, coreY, coreZ, coreY, -coreZ, coverY, -coverZ, coverY, coverZ)
    # Define reinforcing layers
    ops.layer('straight', steelID, numBarsTop, barAreaTop, coreY, coreZ, coreY, -coreZ)  # top layer reinforcement
    ops.layer('straight', steelID, numBarsBot, barAreaBot, -coreY, coreZ, -coreY, -coreZ)  # bottom layer reinforcement
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
    
    
def JacketBuilder(id, HSec, BSec, cover, coreID, steelID1,steelID2, barAreaCorner, barAreaInt,jack_unconfinedID,Jacket_confinedID,JbarAreaInt,JbarAreaCorner,thickness,jacket_Cover):
    coverY = HSec / 2.0
    coverZ = BSec / 2.0
    coreY = coverY - cover
    coreZ = coverZ - cover
    coverYplusjacket = coverY+thickness
    coverZplusjacket = coverZ+thickness
    # Define the fiber section
    ops.section('Fiber', id, '-GJ', 10000000)
    ops.patch('quadr', coreID, 8, 8, -coreY, coreZ, -coreY, -coreZ, coreY, -coreZ, coreY, coreZ)
    ops.patch( 'quadr', jack_unconfinedID, 4, 8, -coverYplusjacket, coverZplusjacket, -(coverYplusjacket-jacket_Cover), (coverZplusjacket-jacket_Cover), (coverYplusjacket-jacket_Cover), (coverZplusjacket-jacket_Cover), coverYplusjacket, coverZplusjacket)
    ops.patch( 'quadr', jack_unconfinedID, 4, 8, -(coverYplusjacket-jacket_Cover), -(coverZplusjacket-jacket_Cover), -coverYplusjacket, -coverZplusjacket, coverYplusjacket, -coverZplusjacket, (coverYplusjacket-jacket_Cover), -(coverZplusjacket-jacket_Cover))
    ops.patch( 'quadr', jack_unconfinedID, 8, 4, -coverYplusjacket, coverZplusjacket, -coverYplusjacket, -coverZplusjacket, -(coverYplusjacket-jacket_Cover), -(coverZplusjacket-jacket_Cover), -(coverYplusjacket-jacket_Cover), (coverZplusjacket-jacket_Cover))
    ops.patch( 'quadr', jack_unconfinedID, 8, 4, (coverYplusjacket-jacket_Cover), (coverZplusjacket-jacket_Cover), (coverYplusjacket-jacket_Cover), -(coverZplusjacket-jacket_Cover), coverYplusjacket, -coverZplusjacket, coverYplusjacket, coverZplusjacket)
    
    ops.patch( 'quadr', Jacket_confinedID, 4, 8, -(coverYplusjacket-jacket_Cover), (coverZplusjacket-jacket_Cover), -coreY, coreZ, coreY, coreZ, (coverYplusjacket-jacket_Cover), (coverZplusjacket-jacket_Cover))
    ops.patch( 'quadr', Jacket_confinedID, 4, 8, -coreY, -coreZ, -(coverYplusjacket-jacket_Cover), -(coverZplusjacket-jacket_Cover), (coverYplusjacket-jacket_Cover), -(coverZplusjacket-jacket_Cover), coreY, -coreZ)
    ops.patch( 'quadr', Jacket_confinedID, 8, 4, -(coverYplusjacket-jacket_Cover), (coverZplusjacket-jacket_Cover), -(coverYplusjacket-jacket_Cover), -(coverZplusjacket-jacket_Cover), -coreY, -coreZ, -coreY, coreZ)
    ops.patch( 'quadr', Jacket_confinedID, 8, 4, coreY, coreZ, coreY, -coreZ, (coverYplusjacket-jacket_Cover), -(coverZplusjacket-jacket_Cover), (coverYplusjacket-jacket_Cover), (coverZplusjacket-jacket_Cover))
    
    ops.layer('straight', steelID1, 1, barAreaInt, 0, coreZ, coreY, coreZ)  # intermediate skin reinforcement +z
    ops.layer('straight', steelID1, 1, barAreaInt, 0, -coreZ, coreY, -coreZ)  # intermediate skin reinforcement -z
    ops.layer('straight', steelID1, 1, barAreaInt, coreY, 0, coreY, coreZ) # intermediate skin reinforcement +y
    ops.layer('straight', steelID1, 1, barAreaInt, -coreY, 0, coreY, -coreZ)  # intermediate skin reinforcement -y
    ops.layer('straight', steelID1, 2, barAreaCorner, coreY, coreZ, coreY, -coreZ)  # top layer reinforcement
    ops.layer('straight', steelID1, 2, barAreaCorner, -coreY, coreZ, -coreY, -coreZ)  # bottom layer reinforcement
    
    ops.layer('straight', steelID2, 1, JbarAreaInt, 0, -coverZplusjacket+jacket_Cover, coverYplusjacket, -coverZplusjacket)  #Jacket intermediate skin reinforcement -z
    ops.layer('straight', steelID2, 1, JbarAreaInt, 0, coverZplusjacket-jacket_Cover, coverYplusjacket, -coverZplusjacket)  #Jacket intermediate skin reinforcement +z
    ops.layer('straight', steelID2, 1, JbarAreaInt, coverYplusjacket-jacket_Cover, 0, coverYplusjacket-jacket_Cover, coverZplusjacket-jacket_Cover)  #Jacket intermediate skin reinforcement +y
    ops.layer('straight', steelID2, 1, JbarAreaInt, -coverYplusjacket+jacket_Cover, 0, coverYplusjacket-jacket_Cover, -coverZplusjacket-jacket_Cover) #Jacket intermediate skin reinforcement -y
    ops.layer('straight', steelID2, 2, JbarAreaCorner, coverYplusjacket-jacket_Cover, coverZplusjacket-jacket_Cover, coverYplusjacket-jacket_Cover, -coverZplusjacket+jacket_Cover)  # Jacket top layer reinforcement
    ops.layer('straight', steelID2, 2, JbarAreaCorner, -coverYplusjacket+jacket_Cover, coverZplusjacket-jacket_Cover, -coverYplusjacket+jacket_Cover, -coverZplusjacket+jacket_Cover)  # Jacket bottom layer reinforcement  

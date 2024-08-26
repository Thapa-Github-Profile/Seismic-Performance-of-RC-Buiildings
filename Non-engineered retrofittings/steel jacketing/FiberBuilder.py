import openseespy.opensees as ops
def ColumnBuilder(id, HSec, BSec, cover, coreID, coverID, steelID, barAreaCorner, barAreaInt):
    coverY = HSec / 2.0
    coverZ = BSec / 2.0
    coreY = coverY - cover
    coreZ = coverZ - cover
    # Define the fiber section
    ops.section('Fiber', id, '-GJ', 10000000)
    # Define the core patch
    ops.patch('quadr', coreID, 6, 6, -coreY, coreZ, -coreY, -coreZ, coreY, -coreZ, coreY, coreZ)
    # Define the four cover patches
    ops.patch('quadr', coverID, 2, 6, -coverY, coverZ, -coreY, coreZ, coreY, coreZ, coverY, coverZ)
    ops.patch('quadr', coverID, 2, 6, -coreY, -coreZ, -coverY, -coverZ, coverY, -coverZ, coreY, -coreZ)
    ops.patch('quadr', coverID, 6, 2, -coverY, coverZ, -coverY, -coverZ, -coreY, -coreZ, -coreY, coreZ)
    ops.patch('quadr', coverID, 6, 2, coreY, coreZ, coreY, -coreZ, coverY, -coverZ, coverY, coverZ)
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
    ops.patch('quadr', coreID, 6, 6, -coreY, coreZ, -coreY, -coreZ, coreY, -coreZ, coreY, coreZ)
    # Define the four cover patches
    ops.patch('quadr', coverID, 2, 6, -coverY, coverZ, -coreY, coreZ, coreY, coreZ, coverY, coverZ)
    ops.patch('quadr', coverID, 2, 6, -coreY, -coreZ, -coverY, -coverZ, coverY, -coverZ, coreY, -coreZ)
    ops.patch('quadr', coverID, 6, 2, -coverY, coverZ, -coverY, -coverZ, -coreY, -coreZ, -coreY, coreZ)
    ops.patch('quadr', coverID, 6, 2, coreY, coreZ, coreY, -coreZ, coverY, -coverZ, coverY, coverZ)
    # Define reinforcing layers
    ops.layer('straight', steelID, numBarsTop, barAreaTop, coreY, coreZ, coreY, -coreZ)  # top layer reinforcement
    ops.layer('straight', steelID, numBarsBot, barAreaBot, -coreY, coreZ, -coreY, -coreZ)  # bottom layer reinforcement

def CFRPBuilder(id, HSec, BSec, cover, coreID, coverID, steelID, barAreaCorner, barAreaInt,fiberid,ft ):
    coverY = HSec / 2.0
    coverZ = BSec / 2.0
    coreY = coverY - cover
    coreZ = coverZ - cover
    # Define the fiber section
    ops.section('Fiber', id, '-GJ', 10000000)
    # Define the core patch
    ops.patch('quadr', coreID, 6, 6, -coreY, coreZ, -coreY, -coreZ, coreY, -coreZ, coreY, coreZ)
    # Define the four cover patches
    ops.patch('quadr', coverID, 2, 6, -coverY, coverZ, -coreY, coreZ, coreY, coreZ, coverY, coverZ)
    ops.patch('quadr', coverID, 2, 6, -coreY, -coreZ, -coverY, -coverZ, coverY, -coverZ, coreY, -coreZ)
    ops.patch('quadr', coverID, 6, 2, -coverY, coverZ, -coverY, -coverZ, -coreY, -coreZ, -coreY, coreZ)
    ops.patch('quadr', coverID, 6, 2, coreY, coreZ, coreY, -coreZ, coverY, -coverZ, coverY, coverZ)
    
    ops.patch('quadr', fiberid, 2, 6, -(coverY+ft), (coverZ+ft), -coverY, coverZ, coverY, coverZ, (coverY+ft), (coverZ+ft))
    ops.patch('quadr', fiberid, 2, 6, -coverY, -coverZ, -(coverY+ft), -(coverZ+ft), (coverY+ft), -(coverZ+ft), coverY, -coverZ)
    ops.patch('quadr', fiberid, 6, 2, -(coverY+ft), (coverZ+ft), -(coverY+ft), -(coverZ+ft), -coverY, -coverZ, -coverY, coverZ)
    ops.patch('quadr', fiberid, 6, 2, coverY, coverZ, coverY, -coverZ, (coverY+ft), -(coverZ+ft), (coverY+ft), (coverZ+ft))
    # Define reinforcing layers
    #layer(’straight’, matTag, numFiber, areaFiber, *start, *end)
    ops.layer('straight', steelID, 1, barAreaInt, 0, coreZ, coreY, coreZ)  # intermediate skin reinforcement +z
    ops.layer('straight', steelID, 1, barAreaInt, 0, -coreZ, coreY, -coreZ)  # intermediate skin reinforcement -z
    ops.layer('straight', steelID, 1, barAreaInt, coreY, 0, coreY, coreZ)  # intermediate skin reinforcement +y
    ops.layer('straight', steelID, 1, barAreaInt, -coreY, 0, coreY, -coreZ)  # intermediate skin reinforcement -y
    ops.layer('straight', steelID, 2, barAreaCorner, coreY, coreZ, coreY, -coreZ)  # top layer reinforcement
    ops.layer('straight', steelID, 2, barAreaCorner, -coreY, coreZ, -coreY, -coreZ)  # bottom layer reinforcement

def AngleBuilder(id, HSec, BSec, cover, coreID, coverID, steelID, barAreaCorner, barAreaInt,angleid,b,ft ):
    coverY = HSec / 2.0
    coverZ = BSec / 2.0
    coreY = coverY - cover
    coreZ = coverZ - cover
    # Define the fiber section
    ops.section('Fiber', id, '-GJ', 10000000)
    # Define the core patch
    ops.patch('quadr', coreID, 6, 6, -coreY, coreZ, -coreY, -coreZ, coreY, -coreZ, coreY, coreZ)
    # Define the four cover patches
    ops.patch('quadr', coverID, 2, 6, -coverY, coverZ, -coreY, coreZ, coreY, coreZ, coverY, coverZ)
    ops.patch('quadr', coverID, 2, 6, -coreY, -coreZ, -coverY, -coverZ, coverY, -coverZ, coreY, -coreZ)
    ops.patch('quadr', coverID, 6, 2, -coverY, coverZ, -coverY, -coverZ, -coreY, -coreZ, -coreY, coreZ)
    ops.patch('quadr', coverID, 6, 2, coreY, coreZ, coreY, -coreZ, coverY, -coverZ, coverY, coverZ)
    
    ops.patch('quadr', angleid, 1, 6, -(coverY+ft), (coverZ+ft), -coverY, coverZ, -(coverY-b), coverZ, -(coverY-b), (coverZ+ft))
    ops.patch('quadr', angleid, 6, 1, -(coverY+ft), (coverZ+ft), -(coverY+ft), coverZ-b, -coverY, coverZ-b, -coverY, coverZ)
    ops.patch('quadr', angleid, 1, 6, -(coverY+ft), -(coverZ+ft), -coverY, -coverZ, -(coverY-b), -coverZ, -(coverY-b), -(coverZ+ft))
    ops.patch('quadr', angleid, 6, 1, -(coverY+ft), -(coverZ+ft), -(coverY+ft), -(coverZ-b), -coverY, -(coverZ-b), -coverY, -coverZ)
    ops.patch('quadr', angleid, 1, 6,  (coverY+ft), (coverZ+ft),  coverY, coverZ,  (coverY-b), coverZ,  (coverY-b), (coverZ+ft))
    ops.patch('quadr', angleid, 6, 1,  (coverY+ft), (coverZ+ft),  (coverY+ft), coverZ-b,  coverY, coverZ-b, coverY, coverZ)
    ops.patch('quadr', angleid, 1, 6,  (coverY+ft), -(coverZ+ft),  coverY, -coverZ, (coverY-b), -coverZ, (coverY-b), -(coverZ+ft))
    ops.patch('quadr', angleid, 6, 1,  (coverY+ft), -(coverZ+ft),  (coverY+ft), -(coverZ-b), coverY, -(coverZ-b), coverY, -coverZ)
           
    ops.patch('quadr', angleid, 1, 6, -(coverY+ft), (coverZ+ft), -coverY, coverZ, -(coverY-b), coverZ, -(coverY-b), (coverZ+ft))
    ops.patch('quadr', angleid, 1, 6, -(coverY+ft), (coverZ+ft), -(coverY+ft), coverZ-ft, -coverY, coverZ-ft, -coverY, coverZ)
    ops.patch('quadr', angleid, 6, 1, -(coverY+ft), (coverZ+ft), -(coverY+ft), -(coverZ+ft), -coverY, -coverZ, -coverY, coverZ)
    ops.patch('quadr', angleid, 6, 1, coverY, coverZ, coverY, -coverZ, (coverY+ft), -(coverZ+ft), (coverY+ft), (coverZ+ft))
    ops.patch('quadr', angleid, 1, 6, -(coverY+ft), (coverZ+ft), -coverY, coverZ, coverY, coverZ, (coverY+ft), (coverZ+ft))
    ops.patch('quadr', angleid, 1, 6, -coverY, -coverZ, -(coverY+ft), -(coverZ+ft), (coverY+ft), -(coverZ+ft), coverY, -coverZ)
    ops.patch('quadr', angleid, 6, 1, -(coverY+ft), (coverZ+ft), -(coverY+ft), -(coverZ+ft), -coverY, -coverZ, -coverY, coverZ)
    ops.patch('quadr', angleid, 6, 1, coverY, coverZ, coverY, -coverZ, (coverY+ft), -(coverZ+ft), (coverY+ft), (coverZ+ft))
    # Define reinforcing layers
    #layer(’straight’, matTag, numFiber, areaFiber, *start, *end)
    ops.layer('straight', steelID, 1, barAreaInt, 0, coreZ, coreY, coreZ)  # intermediate skin reinforcement +z
    ops.layer('straight', steelID, 1, barAreaInt, 0, -coreZ, coreY, -coreZ)  # intermediate skin reinforcement -z
    ops.layer('straight', steelID, 1, barAreaInt, coreY, 0, coreY, coreZ)  # intermediate skin reinforcement +y
    ops.layer('straight', steelID, 1, barAreaInt, -coreY, 0, coreY, -coreZ)  # intermediate skin reinforcement -y
    ops.layer('straight', steelID, 2, barAreaCorner, coreY, coreZ, coreY, -coreZ)  # top layer reinforcement
    ops.layer('straight', steelID, 2, barAreaCorner, -coreY, coreZ, -coreY, -coreZ)  # bottom layer reinforcement

def JacketBuilder(id, HSec, BSec, cover, coreID, coverID, steelID, barAreaCorner, barAreaInt,jackcoverID,JbarAreaInt,JbarAreaCorner,thickness,jacket_Cover):
    coverY = HSec / 2.0
    coverZ = BSec / 2.0
    coreY = coverY - cover
    coreZ = coverZ - cover
    coverYplusjacket = coverY+thickness
    coverZplusjacket = coverZ+thickness
    # Define the fiber section
    ops.section('Fiber', id, '-GJ', 10000000)
    ops.patch('quadr', coreID, 8, 8, -coreY, coreZ, -coreY, -coreZ, coreY, -coreZ, coreY, coreZ)
    ops.patch( 'quadr', jackcoverID, 4, 8, -coverYplusjacket, coverZplusjacket, -coreY, coreZ, coreY, coreZ, coverYplusjacket, coverZplusjacket)
    ops.patch( 'quadr', jackcoverID, 4, 8, -coreY, -coreZ, -coverYplusjacket, -coverZplusjacket, coverYplusjacket, -coverZplusjacket, coreY, -coreZ)
    ops.patch( 'quadr', jackcoverID, 8, 4, -coverYplusjacket, coverZplusjacket, -coverYplusjacket, -coverZplusjacket, -coreY, -coreZ, -coreY, coreZ)
    ops.patch( 'quadr', jackcoverID, 8, 4, coreY, coreZ, coreY, -coreZ, coverYplusjacket, -coverZplusjacket, coverYplusjacket, coverZplusjacket)
    ops.layer('straight', steelID, 1, barAreaInt, 0, coreZ, coreY, coreZ)  # intermediate skin reinforcement +z
    ops.layer('straight', steelID, 1, barAreaInt, 0, -coreZ, coreY, -coreZ)  # intermediate skin reinforcement -z
    ops.layer('straight', steelID, 1, barAreaInt, coreY, 0, coreY, coreZ) # intermediate skin reinforcement +y
    ops.layer('straight', steelID, 1, barAreaInt, -coreY, 0, coreY, -coreZ)  # intermediate skin reinforcement -y
    ops.layer('straight', steelID, 2, barAreaCorner, coreY, coreZ, coreY, -coreZ)  # top layer reinforcement
    ops.layer('straight', steelID, 2, barAreaCorner, -coreY, coreZ, -coreY, -coreZ)  # bottom layer reinforcement
    
    ops.layer('straight', steelID, 1, JbarAreaInt, 0, -coverZplusjacket+jacket_Cover, coverYplusjacket, -coverZplusjacket)  #Jacket intermediate skin reinforcement -z
    ops.layer('straight', steelID, 1, JbarAreaInt, 0, coverZplusjacket-jacket_Cover, coverYplusjacket, -coverZplusjacket)  #Jacket intermediate skin reinforcement +z
    ops.layer('straight', steelID, 1, JbarAreaInt, coverYplusjacket-jacket_Cover, 0, coverYplusjacket-jacket_Cover, coverZplusjacket-jacket_Cover)  #Jacket intermediate skin reinforcement +y
    ops.layer('straight', steelID, 1, JbarAreaInt, -coverYplusjacket+jacket_Cover, 0, coverYplusjacket-jacket_Cover, -coverZplusjacket-jacket_Cover) #Jacket intermediate skin reinforcement -y
    ops.layer('straight', steelID, 2, JbarAreaCorner, coverYplusjacket-jacket_Cover, coverZplusjacket-jacket_Cover, coverYplusjacket-jacket_Cover, -coverZplusjacket+jacket_Cover)  # Jacket top layer reinforcement
    ops.layer('straight', steelID, 2, JbarAreaCorner, -coverYplusjacket+jacket_Cover, coverZplusjacket-jacket_Cover, -coverYplusjacket+jacket_Cover, -coverZplusjacket+jacket_Cover)  # Jacket bottom layer reinforcement  

#===============================================================================
# @author: zedtran
# 
# Course:         COMP5710
# Assignment:     4
# Date:           09/22/18
# AUBGID:         DZT0021
# Name:           Tran, Don
# 
# Description:    dispatch receives parameter URL parameter dictionary and handles 
#                 the creation and validation of a custom/default 6-sided Rubik's cube.
#===============================================================================
import numpy as np
import random

'''
    Method Name: dispatch(parm={})
    
    Description: Called by the microservice. Receives a Py type(dictionary) representation of a string from a valid HTTP 'GET' 
                 Request. (xRef Customer Requirements for HTTP Response Message dictionary).
'''
def dispatch(parm={}):
    httpResponse = {}
    status = getStatusType(parm)
    if status == 0:
        httpResponse['status'] = 'created'
        httpResponse['cube'] = createCube(parm)
    elif status == 1:
        httpResponse['status'] = 'error: at least two faces have the same color'   
    elif status == 2:
        httpResponse['status'] = 'error: face color is missing'
    elif status == 3:
        httpResponse['status'] = 'error: cube must be specified'
    elif status == 4:
        httpResponse['status'] = 'error: op code is missing'
    elif status == 5:
        httpResponse['status'] = 'error: cube is not sized properly'
    elif status == 6:
        httpResponse['status'] = 'full'
    elif status == 7:
        httpResponse['status'] = 'crosses'
    elif status == 8:
        httpResponse['status'] = 'spots'
    elif status == 9:
        httpResponse['status'] = 'unknown'
    elif status == 10:
        httpResponse['status'] = 'error: unsolvable cube configuration'
    elif status == 11:
        httpResponse['status'] = 'error: face is unknown'
    elif status == 12:
        httpResponse['status'] = 'error: face is missing'
    elif status == 13:
        httpResponse['status'] = 'rotated'
        httpResponse['cube'] = rotateCube(parm['face'].replace(' ', ''), parm['cube'].split(','))
    elif status == 14:
        httpResponse['status'] = 'error: method is unknown'
    elif status == 15:
        httpResponse['status'] = 'error: n is invalid'
    elif status == 16:
        randomness, nRandomRotates = getScrambleRandomness(parm)
        httpResponse['status'] = 'scrambled %s' %(randomness)
        httpResponse['rotations'] = nRandomRotates 
    return httpResponse

#-------------- Inward facing methods ----------------

def createCube(parm):
    # Create cube and set default value for faces
    cube = []
    faceF = 'green'
    faceR = 'yellow'
    faceB = 'blue'
    faceL = 'white'
    faceT = 'red'
    faceU = 'orange' 
    #===========================================================================
    # For every key in the dictionary, if the key is one of the valid faces,
    # and if the key's value is custom, then use the custom value for 
    # the appropriate key. Uses a whitelist approach for specific keys
    #===========================================================================
    for key in parm.keys():
        if key == 'f':
            faceF = parm[key]
        if key == 'r':
            faceR = parm[key]
        if key == 'b':
            faceB = parm[key]
        if key == 'l':
            faceL = parm[key]
        if key == 't':
            faceT = parm[key]
        if key == 'u':
            faceU = parm[key]           
    # Populate the cube
    for i in range(0, 54):
        if i < 9:
            cube.append(faceF)
        if i >= 9 and i < 18:
            cube.append(faceR)
        if i >= 18 and i < 27:
            cube.append(faceB)
        if i >= 27 and i < 36:
            cube.append(faceL)
        if i >= 36 and i < 45:
            cube.append(faceT)
        if i >= 45 and i < 54:
            cube.append(faceU)        
    return cube                               

#===============================================================================
# Performs status checking and returns an integer value representing
# a specific status. 
#
# INWARD FACING STATUS CODES:
#     0 = No error on op=create
#     1 = Duplicate Values Detected on op=create
#     2 = Face value declared but missing from parm on op=create
#     3 = Cube not specified for op = check OR op = rotate
#     4 = 'op' declared in parm but not specified or is length invalid for op=check
#     5 = Cube doesn't have 54 elements for op = check (cube not sized properly)
#     6 = Check cube status is Full for op = check
#     7 = Check cube status is Crosses for op = check
#     8 = Check cube status is spots for op = check
#     9 = Check cube status is unknown for op = check
#    10 = Check cube status is unsolvable for op = check
#    11 = Rotate cube status is error on unknown face
#    12 = Rotate cube status is error on missing face 
#    13 = No error on op=rotate
#    14 = Scramble cube status is error on missing/invalid method
#    15 = Scramble cube status is error on mising/invalid n
#    16 = No error on op=scramble
#===============================================================================

def getStatusType(parm={}):
    status = -1
    cubeFromArgs = createCube(parm)
    validOps = ['create', 'check', 'rotate', 'scramble']
    faceValues = getParmFaces(parm)  
    # If op is not declared in parm or if op was declared in parm 
    # but not specified as an existing, valid op
    if not('op' in parm):
        status = 4
    elif ('op' in parm) and not(parm['op'] in validOps):
        status = 4    
    # == Status codes for op = create == #
    elif parm['op'] == 'create':
        status = getCreateStatus(cubeFromArgs, parm) 
    # == Status codes for op = check == #        
    elif parm['op'] == 'check':
        status = getCheckStatus(parm, faceValues, cubeFromArgs)
    # == Status codes for op = rotate == #
    elif parm['op'] == 'rotate':
        status = getRotateStatus(parm, faceValues, cubeFromArgs)
    # == Status codes for op = scramble == #
    elif parm['op'] == 'scramble':
        status = getScrambleStatus(parm)    
    return status

def getCreateStatus(cubeFromArgs=[], parm={}):
    cubeSet = set(cubeFromArgs) # Generates a unique items list from cubeFromArgs
    status = 0 #Default correct status code
    # This means there are less than 6 unique face values (i.e. Duplicates)
    if len(cubeSet) != 6:
        status = 1
    # This means a face value was declared in parms but was not specified (missing face or faces)    
    for key in parm.keys():
        if key in ('f', 'r', 'b', 'l', 't', 'u'):
            if len(parm[key].replace(' ', '')) == 0:
                status = 2
    return status

def getCheckStatus(parm={}, faceValues=[], cubeFromArgs=[]):
    # If a cube wasn't provided
    if not('cube' in parm):
        status = 3
    # Cube doesn't have enough elements assigned
    elif ('cube' in parm) and (len(parm['cube'].split(',')) != 54):
        status = 5
    elif not(isLegal(faceValues, cubeFromArgs, parm['cube'].split(','))):
        status = 10 
    elif isFull(cubeFromArgs, parm['cube'].split(',')):
        status = 6
    elif isCrosses(parm['cube'].split(',')):
        status = 7
    elif isSpots(parm['cube'].split(',')):
        status = 8
    else:
        status = 9
    return status
    
def getRotateStatus(parm={}, faceValues=[], cubeFromArgs=[]):
    rotFaceCommands = ['f', 'F', 'r', 'R', 'b', 'B', 'l', 'L', 't', 'T', 'u', 'U']
    if not(all (k in parm for k in ('f', 'r', 'b', 'l', 't', 'u', 'cube'))):
        status = 3 # cube not specified
    elif ('face' in parm) and not(parm['face'] in rotFaceCommands):
        status = 11 # face is unknown
    elif not('face' in parm):
        status = 12 # face is missing
    elif (len(parm['cube'].split(',')) != 54): 
        status = 5
    elif not(isLegal(faceValues, cubeFromArgs, parm['cube'].split(','))):
        status = 10 
    else:
        status = 13
    return status

def getScrambleStatus(parm={}):
    methods = ('random', 'transition')
    validNs = [a for a in range(100)]
    if ('method' in parm) and not(parm['method'] in methods):
        status = 14 # method is unknown, invalid, or missing
    elif ('n' in parm):
        try:
            if (int(parm['n']) not in validNs):
                status = 15 # n is out of allowable range
            else: 
                status = 16
        except ValueError:
            status = 15 # n is missing or an invalid literal for conversion to int
    else:
        status = 16
    return status

def getScrambleRandomness(parm={}):   
    rotateCommands = ['f', 'F', 'r', 'R', 'b', 'B', 'l', 'L', 't', 'T', 'u', 'U']     
    method = parm['method'] if ('method' in parm) else 'random'
    n = int(parm['n']) if ('n' in parm) else 0
    cube = createCube(parm)
    if method == 'random':
        # Sampling with replacement
        nRandomRotates = np.random.choice(rotateCommands, size=n, replace=True)
        for rotationCommand in nRandomRotates:
            cube = rotateCube(rotationCommand, cube)
        randomness = computeRandomness(cube)
    else:        
        nRandomRotates = [] 
        y = 0
        while y < n:
            tmpDict = {}
            for rotation in rotateCommands:
                tmpCube = rotateCube(rotation, cube[:])
                tmpRandomness = computeRandomness(tmpCube)
                tmpDict[rotation] = tmpRandomness
            # Get the first key with the smallest value in the dictionary
            key_min = min(tmpDict.keys(), key=(lambda k: tmpDict[k])) 
            # Get all the keys with the same value as key_min  
            min_keys = [k for k,v in tmpDict.items() if v == tmpDict[key_min]]
            # Randomly select the minimum target key
            randomChoice = random.choice(min_keys)
            # Rotate the cube
            cube = rotateCube(randomChoice, cube)
            nRandomRotates.append(randomChoice)
            y += 1
        randomness = computeRandomness(cube)
    return randomness, list(nRandomRotates)

def computeRandomness(cube=[]):
    summation = 0
    # Taking slices after rotation
    cubeSlices = [cube[i:j] for i,j in [(0, 9), (9, 18), (18, 27), (27, 36), (36, 45), (45, 54)]]
    for cubeSlice in cubeSlices:
        sliceSet = set(cubeSlice)
        for item in sliceSet:
            k = cubeSlice.count(item)
            summation += (k*(k-1))/2
    return int(round((summation/216.0)*100))    

def getParmFaces(parm={}):
    keyFaces = {'f':'green', 'r':'yellow', 'b':'blue', 'l':'white', 't':'red', 'u':'orange'}
    faces = []
    # Populate face values from key args from the specified query string 
    for key in keyFaces:
        if key in parm:
            faces.append(parm[key])
        elif not(key in parm):
            #NOTE: The order the key/items are "yielded" by vanilla python is b-f-l-r-u-t
            faces.append(keyFaces[key])
    return faces
    
def isFull(cubeFromArgs=[], cubeFromKey=[]):
    full = False
        
    faceF = len(set(cubeFromArgs[0:9]).union(set(cubeFromKey[0:9]))) == 1
    faceR = len(set(cubeFromArgs[9:18]).union(set(cubeFromKey[9:18]))) == 1
    faceB = len(set(cubeFromArgs[18:27]).union(set(cubeFromKey[18:27]))) == 1
    faceL = len(set(cubeFromArgs[27:36]).union(set(cubeFromKey[27:36]))) == 1
    faceT = len(set(cubeFromArgs[36:45]).union(set(cubeFromKey[36:45]))) == 1
    faceU = len(set(cubeFromArgs[45:54]).union(set(cubeFromKey[45:54]))) == 1

    if all((faceF, faceR, faceB, faceL, faceT, faceU)): 
        full = True    
    return full
    
def isCrosses(cubeFromKey=[]):
    crosses = False
    
    crossF = list(set([cubeFromKey[i] for i in (1,3,4,5,7)])) 
    crossR = list(set([cubeFromKey[i] for i in (10,12,13,14,16)]))
    crossB = list(set([cubeFromKey[i] for i in (19,21,22,23,25)]))
    crossL = list(set([cubeFromKey[i] for i in (28,30,31,32,34)]))
    crossT = list(set([cubeFromKey[i] for i in (37,39,40,41,43)]))
    crossU = list(set([cubeFromKey[i] for i in (46,48,49,50,52)])) 
    
    borderF = list(set([cubeFromKey[i] for i in (9,11,15,17)])) 
    borderR = list(set([cubeFromKey[i] for i in (36,38,42,44)]))
    borderB = list(set([cubeFromKey[i] for i in (27,29,33,35)]))
    borderL = list(set([cubeFromKey[i] for i in (45,47,51,53)]))
    borderT = list(set([cubeFromKey[i] for i in (0,2,6,8)]))
    borderU = list(set([cubeFromKey[i] for i in (18,20,24,26)]))
    
    length = 1
    if all(len(lst) == length for lst in [crossF, crossR, crossB, crossL, crossT, crossU]):
        if all(len(lst) == length for lst in [borderF, borderR, borderB, borderL, borderT, borderU]):
            unionCross = sorted(list(set().union(crossF, crossR, crossB, crossL, crossT, crossU)))
            unionBorder = sorted(list(set().union(borderF, borderR, borderB, borderL, borderT, borderU)))
            if len(unionCross) == len(unionBorder):
                falseCount = 0
                for i in range(len(unionCross)):
                    if unionCross[i] != unionBorder[i]:
                        falseCount += 1
                if falseCount == 0:
                    crosses = True
                      
    return crosses

def isSpots(cubeFromKey=[]):
    spots = False

    sameF = len(set([cubeFromKey[i] for i in (27,28,29,30,32,33,34,35)])) == 1
    sameR = len(set([cubeFromKey[i] for i in (36,37,38,39,41,42,43,44)])) == 1
    sameB = len(set([cubeFromKey[i] for i in (9,10,11,12,14,15,16,17)])) == 1
    sameL = len(set([cubeFromKey[i] for i in (45,46,47,48,50,51,52,53)])) == 1
    sameT = len(set([cubeFromKey[i] for i in (18,19,20,21,23,24,25,26)])) == 1
    sameU = len(set([cubeFromKey[i] for i in (0,1,2,3,5,6,7,8)])) == 1
        
    if all((sameF, sameR, sameB, sameL, sameT, sameU)):
        spots = True
    
    return spots

def isLegal(faceOptions=[], cubeFromArgs=[], cubeFromKey=[]): 
    cornerIndeces = [0,29,42,2,9,44,18,11,38,20,27,36,8,15,47,6,35,45,24,17,53,26,33,51]
    edgeIndeces = [1,43,7,46,52,25,19,37,28,39,41,10,16,50,34,48,3,32,5,12,14,21,23,30]
            
    sameF = cubeFromKey[4]==faceOptions[1] # f
    sameR = cubeFromKey[13]==faceOptions[3] # r
    sameB = cubeFromKey[22]==faceOptions[0] # b
    sameL = cubeFromKey[31]==faceOptions[2] # l
    sameT = cubeFromKey[40]==faceOptions[5] # t
    sameU = cubeFromKey[49]==faceOptions[4] # u
        
    uniqueCorners = [tuple(x) for x in set(map(frozenset, group(cubeFromKey, cornerIndeces, 3)))]
    uniqueEdges = [tuple(x) for x in set(map(frozenset, group(cubeFromKey, edgeIndeces, 2)))]
    
    # Check if there are more then 9 of each color # 
    cubeSlices = [cubeFromKey[i] for i in (4, 13, 22, 31, 40, 49)]
    for i in range(len(cubeSlices)):
        if cubeFromKey.count(cubeSlices[i]) != 9:
            return False
    
    # Check if colors used in parm arguments are the only ones used in the cube 
    if set(cubeFromArgs) != set(cubeFromKey):
        return False
    # Check if middle facelets specified by parms are the same ones used in parm['cube']
    if not(all((sameF, sameR, sameB, sameL, sameT, sameU))):
        return False
    # Validate there are 8 distinct corners    
    if len(set(uniqueCorners)) != 8: 
        return False
    # Validate there are 12 distinct edges
    if len(set(uniqueEdges)) != 12: 
        return False
    # Make sure that edge pair combinations don't have front with back, left with right, or top with under
    for tup in uniqueEdges:
        if (faceOptions[0] in tup) and (faceOptions[1] in tup):
            return False
        elif (faceOptions[4] in tup) and (faceOptions[5] in tup):
            return False
        elif (faceOptions[2] in tup) and (faceOptions[3] in tup):
            return False  
    # Make sure that no two elements in each corner contain an illegal pair (i.e. top & under, front & back, left & right)
    for tup in uniqueCorners:
        if (faceOptions[0] in tup) and (faceOptions[1] in tup):
            return False
        elif (faceOptions[4] in tup) and (faceOptions[5] in tup):
            return False
        elif (faceOptions[2] in tup) and (faceOptions[3] in tup):
            return False
    return True

#=== GROUP A LIST INTO SEQUENTIAL N-TUPLES USING RELEVANT INDECES ===#

def group(cube, indexList, n):
    tupList = []
    for i in range(0, len(indexList), n):
        val = indexList[i:i+n]
        tup = ()
        for j in range(len(val)):
            tup = tup + (cube[val[j]], )
        tupList.append(tup)
    return tupList
            
def rotateCube(face, cube=[]):
    newCube = cube[:]
    rotVals = getRotateIndices(face)       
    if face.isupper():
        for i in range(12):
            newCube[rotVals[0][i]] = cube[rotVals[0][i+3]]
        for j in range(8):
            newCube[rotVals[1][j]] = cube[rotVals[1][j+2]]
    else:
        for i in range(12):
            newCube[rotVals[0][i+3]] = cube[rotVals[0][i]]
        for j in range(8):
            newCube[rotVals[1][j+2]] = cube[rotVals[1][j]]
    return newCube
    
def getRotateIndices(key):
    adjToFaceF = [42, 43, 44, 9, 12, 15, 47, 46, 45, 35, 32, 29, 42, 43, 44]
    faceF = [0, 1, 2, 5, 8, 7, 6, 3, 0, 1]
    
    adjToFaceR = [44, 41, 38, 18, 21, 24, 53, 50, 47, 8, 5, 2, 44, 41, 38]
    faceR = [9, 10, 11, 14, 17, 16, 15, 12, 9, 10]
    
    adjToFaceB = [38, 37, 36, 27, 30, 33, 51, 52, 53, 17, 14, 11, 38, 37, 36]
    faceB = [18, 19, 20, 23, 26, 25, 24, 21, 18, 19]
    
    adjToFaceL = [36, 39, 42, 0, 3, 6, 45, 48, 51, 26, 23, 20, 36, 39, 42]
    faceL = [27, 28, 29, 32, 35, 34, 33, 30, 27, 28]
    
    adjToFaceT = [0, 1, 2, 27, 28, 29, 18, 19, 20, 9, 10, 11, 0, 1, 2]
    faceT = [36, 37, 38, 41, 44, 43, 42, 39, 36, 37]
    
    adjToFaceU = [6, 7, 8, 15, 16, 17, 24, 25, 26, 33, 34, 35, 6, 7, 8]
    faceU = [47, 50, 53, 52, 51, 48, 45, 46, 47, 50]
    
    options = {
        ('f', 'F'): [adjToFaceF, faceF],
        ('r', 'R'): [adjToFaceR, faceR],
        ('b', 'B'): [adjToFaceB, faceB],
        ('l', 'L'): [adjToFaceL, faceL],
        ('t', 'T'): [adjToFaceT, faceT],
        ('u', 'U'): [adjToFaceU, faceU]
    }
    for keyTuple in options.keys():
        if key in keyTuple:
            return options.get(keyTuple)
#===============================================================================
# Created on Sep 24, 2018
# 
# @author: zedtran
# 
# Course:         COMP5710
# Assignment:     4
# Date:           09/22/18
# AUBGID:         DZT0021
# Name:           Tran, Don
# 
# Description:    Development testing code for createCube method in RCube.dispatch
#===============================================================================

import unittest
import RCube.dispatch as RCube

class CreateCubeTest(unittest.TestCase):
# Happy paths: 
#      input: parm: {'op':'create'} ... no options
#
#      output: Default model cube, which is a JSON string:
#                {
#                 'status': 'created', 
#                 'cube': ['green',  'green', 'green', 
#                         'green', 'green', 'green', 
#                         'green', 'green', 'green', 
#                         'yellow', 'yellow', 'yellow', 
#                         'yellow', 'yellow', 'yellow', 
#                         'yellow', 'yellow', 'yellow',  
#                         'blue', 'blue', 'blue', 
#                         'blue', 'blue', 'blue', 
#                         'blue', 'blue', 'blue', 
#                         'white', 'white', 'white', 
#                         'white', 'white', 'white', 
#                         'white', 'white', 'white', 
#                         'red', 'red', 'red', 
#                         'red', 'red', 'red', 
#                         'red', 'red', 'red', 
#                         'orange', 'orange', 'orange', 
#                         'orange', 'orange', 'orange', 
#                         'orange', 'orange', 'orange']
#                }
#
#       input: parm: {'op':'create', 'r':'r', 'l':'l', 't':'t', 'u':'u', 'f':'f', 'b':'b'}
#       output: Custom model cube 
#
#       input: parm: {'op':'create', 'r':'r', 'b':'b', 'l':'l', 't':'t', 'u':'u'}
#       output: 
#
#       input: parm: {'op':'create', 'r':'', 'b':'', 'l':'', 't':'', 'u':''}
#       output: 
#
#       input: parm: {'op':'create', 'f':'f', 'r':'       ', 'b':'b', 'l':'l', 't':'t', 'u':'u'}
#       output: 
#
#       input: parm: {'op':'create', 'f':'f', 'r':'r', 'b':'b', 'l':'l', 't':'1'}
#       output: 
#
#       input: parm: {'op':'create', 'f':'f', 'r':'r', 'b':'b', 'l':'l', 't':'1', 'under':'42'}
#       output:  
#
#
# Sad Paths:
#
#       input: parm: {'op':'create', 'f':'red', 'r':'red'}
#       output:  
#
#       input: parm: {'op':'create', 'f':'red'}
#       output:  
#
#       input: parm: {'op':'create', 'f':'green', 'u':'GREEN'}
#       output: 
#
#       input: parm: {'op':'create', \
#                'f':'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', \
#                'r':'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr', \
#                'b':'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', \
#                'l':'llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll', \
#                't':'tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt', \
#                'u':'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'}
#
#       output: 
#
#       input: parm: {'op':'create', 'f':''} 
#       output: {'status': 'error: face color is missing'}
#
#   HAPPY PATHS
    def test100_010_ShouldCreateMultipleFaceCube(self):
        parm = {'op':'create'}
        expectedFaces = ['green', 'yellow', 'blue', 'white', 'red', 'orange']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for face in expectedFaces:
            for _ in range(0, 9):
                self.assertEqual(face, actualResult[elementIndex])
                elementIndex += 1
            
    def test100_020_ShouldCreateMultipleFaceCubeWithOptions(self):
        parm = {'op':'create', 'r':'r', 'l':'l', 't':'t', 'u':'u', 'f':'f', 'b':'b'}
        expectedFaces = ['f', 'r', 'b', 'l', 't', 'u']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for face in expectedFaces:
            for _ in range(0, 9):
                self.assertEqual(face, actualResult[elementIndex])
                elementIndex += 1
                
    # Accepting risk that if this test works for one face, it works individually for the others
    def test100_030_ShouldCreateMultipleFaceCubeWithDefaultValue(self):
        parm = {'op':'create', 'r':'r', 'b':'b', 'l':'l', 't':'t', 'u':'u'}
        expectedFaces = ['green', 'r', 'b', 'l', 't', 'u']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for face in expectedFaces:
            for _ in range(0, 9):
                self.assertEqual(face, actualResult[elementIndex])
                elementIndex += 1
                
    # Accepting risk that if this test works for one face, it works individually for the others
    def test100_031_ShouldCreateMultipleFaceCubeWithDefaultValueandMissingFace(self):
        parm = {'op':'create', 'r':'', 'b':'', 'l':'', 't':'', 'u':''}
        expectedFaces = ['green', '', '', '', '', '']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for face in expectedFaces:
            for _ in range(0, 9):
                self.assertEqual(face, actualResult[elementIndex])
                elementIndex += 1
                
    # Accepting risk that if this test works for one face, it works individually for the others
    def test100_032_ShouldCreateMultipleFaceCubeWithAnEmptyUntrimmedValue(self):
        parm = {'op':'create', 'f':'f', 'r':'       ', 'b':'b', 'l':'l', 't':'t', 'u':'u'}
        expectedFaces = ['f', '       ', 'b', 'l', 't', 'u']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for face in expectedFaces:
            for _ in range(0, 9):
                self.assertEqual(face, actualResult[elementIndex])
                elementIndex += 1
                
    def test100_040_ShouldCreateMultipleFaceCubeWithCustomValueAndDefaultOrange(self):
        parm = {'op':'create', 'f':'f', 'r':'r', 'b':'b', 'l':'l', 't':'1'}
        expectedFaces = ['f', 'r', 'b', 'l', '1', 'orange']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for face in expectedFaces:
            for _ in range(0, 9):
                self.assertEqual(face, actualResult[elementIndex])
                elementIndex += 1
    
    def test100_050_ShouldCreateMultipleFaceCubeWithCustomValueAndDefaultOrange(self):
        parm = {'op':'create', 'f':'f', 'r':'r', 'b':'b', 'l':'l', 't':'1', 'under':'42'}
        expectedFaces = ['f', 'r', 'b', 'l', '1', 'orange']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for face in expectedFaces:
            for _ in range(0, 9):
                self.assertEqual(face, actualResult[elementIndex])
                elementIndex += 1
    
    
#   SAD PATHS
    
    # It is easier to make this test a green light test since handling of this condition will be
    # the job of dispatch
    def test100_060_ShouldCreateCubeWithExplicitDuplicateValues(self):
        parm = {'op':'create', 'f':'red', 'r':'red'}
        expectedFaces = ['red', 'red', 'blue', 'white', 'red', 'orange']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for face in expectedFaces:
            for _ in range(0, 9):
                self.assertEqual(face, actualResult[elementIndex])
                elementIndex += 1
    
    # It is easier to make this test a green light test since handling of this condition will be
    # the job of dispatch      
    def test100_070_ShouldCreateCubeWithImplicitDuplicateValues(self):
        parm = {'op':'create', 'f':'red'}
        expectedFaces = ['red', 'yellow', 'blue', 'white', 'red', 'orange']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for face in expectedFaces:
            for _ in range(0, 9):
                self.assertEqual(face, actualResult[elementIndex])
                elementIndex += 1
                
    #======= REMOVED TEST -- Case Sensitive Check Not Required ==================
    # def test100_080_ShouldCreateCubeWithCaseSensitiveDuplicateValues(self):
    #     parm = {'op':'create', 'f':'green', 'u':'GREEN'}
    #     expectedFaces = ['green', 'yellow', 'blue', 'white', 'red', 'GREEN']
    #     actualResult = RCube.createCube(parm)
    #     elementIndex = 0
    #     for face in expectedFaces:
    #         for _ in range(0, 9):
    #             self.assertEqual(face, actualResult[elementIndex])
    #             elementIndex += 1
    #===========================================================================
                
                
    def test100_090_ShouldCreateCubeWithLongQueryValues(self):
        parm = {'op':'create', \
                'f':'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', \
                'r':'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr', \
                'b':'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', \
                'l':'llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll', \
                't':'tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt', \
                'u':'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'}
        
        expectedFaces = ['ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', \
             'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr', \
             'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', \
             'llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll', \
             'tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt', \
             'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for face in expectedFaces:
            for _ in range(0, 9):
                self.assertEqual(face, actualResult[elementIndex])
                elementIndex += 1
                
    
    def test100_091_ShouldCreateCubeWithMissingFace(self):
        parm = {'op':'create', 'f':''}
        expectedFaces = ['','yellow','blue','white','red','orange']
        actualResult = RCube.createCube(parm)
        elementIndex = 0
        for face in expectedFaces:
            for _ in range(0, 9):
                self.assertEqual(face, actualResult[elementIndex])
                elementIndex += 1   
                
    def test100_ShouldReturnError(self):
        #queryString = "op=check&f=f&r=r&b=b&l=l&t=t&u=u&cube=f,f,f,t,f,f,f,f,f,r,r,r,r,r,r,r,r,r,b,u,b,b,b,b,b,b,b,l,l,l,l,l,l,l,l,l,t,t,t,f,t,t,t,t,t,u,u,u,b,u,u,u,u,u"
        parm = {'op':'check','f':'f', 'r':'r', 'b':'b','l':'l', 't':'t', 'u':'u', 'cube':'f,f,f,f,f,f,t,f,f,r,r,r,r,r,r,r,r,r,f,b,b,b,b,b,b,b,b,l,l,l,l,l,l,l,l,l,t,t,t,t,t,t,t,t,b,u,u,u,u,u,u,u,u,u'}   
        RCube.dispatch(parm) 
        
    def test900_ShouldReturnError(self):
        #queryString = "op=check&f=f&r=r&b=b&l=l&t=t&u=u&cube=f,f,f,t,f,f,f,f,f,r,r,r,r,r,r,r,r,r,b,u,b,b,b,b,b,b,b,l,l,l,l,l,l,l,l,l,t,t,t,f,t,t,t,t,t,u,u,u,b,u,u,u,u,u"
        parm = {'op':'scramble', 'n':'6', 'method':'transition'}   
        RCube.dispatch(parm)     
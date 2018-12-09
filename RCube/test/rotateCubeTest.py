#===============================================================================
# Created on Oct 24, 2018
# 
# @author: zedtran
# 
# Course:         COMP5710
# Assignment:     6
# Date:           10/24/18
# AUBGID:         DZT0021
# Name:           Tran, Don
# 
# Description:    Development testing code for createCube method in RCube.dispatch
#===============================================================================

import unittest
import RCube.dispatch as RCube

class rotateCubeTest(unittest.TestCase):
            
    def test100_010_ShouldReturnRotatedFacef(self):
        parm = {'op':'rotate', 
                'f':'g',
                'r':'r', 
                'b':'b', 
                'l':'o', 
                't':'w', 
                'u':'y',
                'face':'f', 
                'cube':['g','g','g','g','g','g','g','g','g','r','r','r','r','r','r','r','r','r','b','b','b','b','b','b','b','b','b','o','o','o','o','o','o','o','o','o','w','w','w','w','w','w','w','w','w','y','y','y','y','y','y','y','y','y']}
        expectedFaces = ['g','g','g','g','g','g','g','g','g','w','r','r','w','r','r','w','r','r','b','b','b','b','b','b','b','b','b','o','o','y','o','o','y','o','o','y','w','w','w','w','w','w','o','o','o','r','r','r','y','y','y','y','y','y']
        actualResult = RCube.rotateCube(parm['face'], parm['cube'])
        for i in range(54):
            self.assertEqual(expectedFaces[i], actualResult[i])
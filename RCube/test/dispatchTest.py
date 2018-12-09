#===============================================================================
# 
# @author: zedtran
# 
# Course:         COMP5710
# Assignment:     4
# Date:           09/22/18
# AUBGID:         DZT0021
# Name:           Tran, Don
# 
# Description:    Acceptance Test cases for RCube.dispatch
#===============================================================================


import unittest
import httplib
import json

class DispatchTest(unittest.TestCase):
        
    def setUp(self):
        self.key = "status"
        self.errorValue = "error:"
        self.operation ="op"
        self.scramble ="create"

    @classmethod
    def setUpClass(cls):
        cls.ERROR = "error:"
        cls.DEFAULT_SIZE = 3
        cls.MICROSERVICE_PATH = "/rcube?"
        cls.MICROSERVICE_URL="127.0.0.1"
        cls.MICROSERVICE_PORT = 5000
#        cls.MICFROSERVICE_URL="umphrda-rcube.mybluemix.net"
#        cls.MICROSERVICE_PORT = 80
        
    def httpGetAndResponse(self, queryString):
        '''Make HTTP request to URL:PORT for /rcube?querystring; result is a JSON string'''
        try:
            theConnection = httplib.HTTPConnection(self.MICROSERVICE_URL, self.MICROSERVICE_PORT)
            theConnection.request("GET", self.MICROSERVICE_PATH + queryString.replace(' ', ''))
            theStringResponse = theConnection.getresponse().read()
            return theStringResponse 
        except Exception as e:
            theStringResponse = "{'diagnostic': 'error: " + str(e) + "'}"
            return theStringResponse
        
    def string2dict(self, httpResponse):
        '''Convert JSON string to dictionary'''
        result = {}
        try:
            jsonString = httpResponse.replace("'", "\"")
            unicodeDictionary = json.loads(jsonString)
            for element in unicodeDictionary:
                if(isinstance(unicodeDictionary[element],unicode)):
                    result[str(element)] = str(unicodeDictionary[element])
                else:
                    result[str(element)] = unicodeDictionary[element]
        except Exception as e:
            result['diagnostic'] = str(e)
        return result
        
# Acceptance Tests =====================================================================
#
# 100 dispatch - basic functionality
# Desired level of confidence: boundary value analysis
# Analysis 
# inputs:     http:// ...myURL... /httpGetAndResponse?parm
#            parm is a string consisting of key-value pairs
#            At a minimum, parm must contain one key of "op"
#
# outputs:    A JSON string containing, at a minimum, a key of "status"
#
# Happy path 
#      input:   parm having at least one element with a key of "op"        
#      output:  JSON string containing a key of "status" 
#
# Sad path 
#      input:   no string       
#      output:  dictionary consisting of an element with a key of "status" and value of "error: op code is missing"
#
#      input:   valid parm string with at least one key-value pair, no key of "op"
#      output:  dictionary consisting of an element with a key of "status" and value of "error: op code is missing"
#
#
#
# Note:  These tests require an active web service
#
#
# Happy path
    def test100_010_ShouldReturnSuccessKey(self):
        queryString="op=create"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
    
    # Sad path
    
    def test100_900_ShouldReturnErrorOnEmptyParm(self):
        queryString=""
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])
    
    def test100_910_ShouldReturnErrorOnMissingOp(self):
        queryString="f=red"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error:',resultDict['status'][0:6])


# Acceptance Tests =========================================================================================
#
# 200 dispatch -- op-create
# Desired level of confidence is BVA
# Analysis 
#    inputs:     http:// ...myURL... /rcube?op=create<options>
#        where <options> can be zero or one of: 
#            f=<string>  String of length .GT. 0. Optional. Defaults to "green" Unvalidated.
#            r=<string>  String of length .GT. 0. Optional. Defaults to "yellow" Unvalidated.
#            b=<string>  String of length .GT. 0. Optional. Defaults to "blue" Unvalidated.
#            l=<string>  String of length .GT. 0. Optional. Defaults to "white" Unvalidated.
#            t=<string>  String of length .GT. 0. Optional. Defaults to "red" Unvalidated.
#            u=<string>  String of length .GT. 0. Optional. Defaults to "orange" Unvalidated.
# 
#    outputs:    A JSON string containing, at a minimum, a key of "status"
#
#
# Note:  These tests require an active web service

    # HAPPY PATHS
    def test200_010_ShouldCreateDefaultCubeStatus(self):
        queryString="op=create"
        resultString = self.httpGetAndResponse(queryString) # The JSON String 
        resultDict = self.string2dict(resultString) # JSON String converted to Dictionary for easier handling
        self.assertIn('status', resultDict)
        self.assertEquals('created', resultDict['status'][0:7])

    # Here, we are making sure cube is in our dictionary # IDEALLY we want this to be a red test, but key/pair 'cube' was provided
    def test200_020_ShouldCreateDefaultCubeKey(self):
        queryString="op=create"
        resultString = self.httpGetAndResponse(queryString) # The JSON String 
        resultDict = self.string2dict(resultString) # JSON String converted to Dictionary for easier handling
        self.assertIn('cube', resultDict) 
        
    def test200_130_ShouldCreateDefaultCubeValue(self):
        queryString="op=create"
        resultString = self.httpGetAndResponse(queryString) # The JSON String 
        resultDict = self.string2dict(resultString) # JSON String converted to Dictionary for easier handling
        expectedFaces = ['green', 'yellow', 'blue', 'white', 'red', 'orange']
        actualResult = resultDict['cube']
        actualFaceIndex = 0
        for face in expectedFaces:
            for _ in range(0, 9):
                self.assertEqual(face, actualResult[actualFaceIndex])
                actualFaceIndex += 1
                
    def test200_133_ShouldCreateLongOptionsCubeValues(self):
        queryString="op=create\
            &f=ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\
            &r=rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr\
            &b=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\
            &l=llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll\
            &t=tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt\
            &u=uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu"
        resultString = self.httpGetAndResponse(queryString) # The JSON String 
        resultDict = self.string2dict(resultString) # JSON String converted to Dictionary for easier handling
        expectedFaces = ['ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', \
             'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr', \
             'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', \
             'llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll', \
             'tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt', \
             'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu']
        actualResult = resultDict['cube']
        actualFaceIndex = 0
        for face in expectedFaces:
            for _ in range(0, 9):
                self.assertEqual(face, actualResult[actualFaceIndex])
                actualFaceIndex += 1
            
    def test200_140_ShouldCreateOptionsCubeValue(self):
        queryString="op=create&r=r&l=l&t=t&u=u&f=f&b=b"
        resultString = self.httpGetAndResponse(queryString) # The JSON String 
        resultDict = self.string2dict(resultString) # JSON String converted to Dictionary for easier handling
        expectedFaces = ['f', 'r', 'b', 'l', 't', 'u'] #---Originally Tested with--- ['r', 'l', 't', 'u', 'f', 'b']
        actualResult = resultDict['cube']
        actualFaceIndex = 0
        for face in expectedFaces:
            for _ in range(0, 9):
                self.assertEqual(face, actualResult[actualFaceIndex])
                actualFaceIndex += 1
                
    def test200_150_ShouldCreateMultipleFaceCubeWithCustomAndDefaultValues(self):
        queryString="op=create&f=f&r=r&b=b&l=l&t=1"
        resultString = self.httpGetAndResponse(queryString) # The JSON String 
        resultDict = self.string2dict(resultString) # JSON String converted to Dictionary for easier handling
        expectedFaces = ['f', 'r', 'b', 'l', '1', 'orange'] 
        actualResult = resultDict['cube']
        actualFaceIndex = 0
        for face in expectedFaces:
            for _ in range(0, 9):
                self.assertEqual(face, actualResult[actualFaceIndex])
                actualFaceIndex += 1
                
    def test200_160_ShouldCreateMultipleFaceCubeWithCustomValueAndDefaultOrange(self):
        queryString="op=create&f=f&r=r&b=b&l=l&t=1&under=42"
        resultString = self.httpGetAndResponse(queryString) # The JSON String 
        resultDict = self.string2dict(resultString) # JSON String converted to Dictionary for easier handling
        expectedFaces = ['f', 'r', 'b', 'l', '1', 'orange'] 
        actualResult = resultDict['cube']
        actualFaceIndex = 0
        for face in expectedFaces:
            for _ in range(0, 9):
                self.assertEqual(face, actualResult[actualFaceIndex])
                actualFaceIndex += 1
                
    # ====== SAD PATHS =======
    def test200_170_ShouldCreateStatusErrorOnExplicitDuplicateCubeValues(self):
        queryString="op=create&f=red&r=red"
        resultString = self.httpGetAndResponse(queryString) # The JSON String 
        resultDict = self.string2dict(resultString) # {'status':'error: duplicate side values not allowed'}
        expectedResponse = 'error: at least two faces have the same color'
        actualResponse = resultDict['status']
        self.assertEqual(expectedResponse, actualResponse)
        
    def test200_180_ShouldCreateStatusErrorOnImplicitDuplicateCubeValues(self):
        queryString="op=create&f=red"
        resultString = self.httpGetAndResponse(queryString) # The JSON String 
        resultDict = self.string2dict(resultString) # {'status':'error: duplicate side values not allowed'}
        expectedResponse = 'error: at least two faces have the same color'
        actualResponse = resultDict['status']
        self.assertEqual(expectedResponse, actualResponse)
    
    def test200_191_ShouldCreateStatusErrorOnMissingFaceValue(self):
        queryString="op=create&f="
        resultString = self.httpGetAndResponse(queryString) # The JSON String 
        resultDict = self.string2dict(resultString) # {'status':'error: duplicate side values not allowed'}
        expectedResponse = 'error: face color is missing'
        actualResponse = resultDict['status']
        self.assertEqual(expectedResponse, actualResponse)
        


        
# Acceptance Tests ==============================================================
#
# 300 dispatch -- op-check
# Desired level of confidence is BVA
# Analysis 
#    inputs:     http:// ...myURL... /rcube?op=create<options>
#        where <options> can be zero or one of: 
#            f=<string>  String of length .GT. 0. Optional. Defaults to "green" Unvalidated.
#            r=<string>  String of length .GT. 0. Optional. Defaults to "yellow" Unvalidated.
#            b=<string>  String of length .GT. 0. Optional. Defaults to "blue" Unvalidated.
#            l=<string>  String of length .GT. 0. Optional. Defaults to "white" Unvalidated.
#            t=<string>  String of length .GT. 0. Optional. Defaults to "red" Unvalidated.
#            u=<string>  String of length .GT. 0. Optional. Defaults to "orange" Unvalidated.
#            cube=<string> String of colors, comm-separated.  Contains no extraneous white space.  
#                          The first 9 elements represent the colors on the front face, the second 9 elements 
#                          represent the colors on the right face, and so forth for the back, left, top, and under faces, respectively.   
#                          Each face's elements are arranged in row-major order, beginning with the upper left corner.  
#                          Each element's color comes from the designated set of colors. The "Support Info" tab illustrates the layout of the cube.  Mandatory.  
#                          Arrives unvalidated.  
#
# HAPPY PATHS 
    def test300_050_ShouldReturnCheckStatusFull(self):
        queryString = "op=check&f=f&r=r&b=b&l=l&t=t&u=u&cube=f,f,f,f,f,f,f,f,f,"\
                                                            "r,r,r,r,r,r,r,r,r,"\
                                                            "b,b,b,b,b,b,b,b,b,"\
                                                            "l,l,l,l,l,l,l,l,l,"\
                                                            "t,t,t,t,t,t,t,t,t,"\
                                                            "u,u,u,u,u,u,u,u,u"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('full', resultDict['status'])

    def test300_060_ShouldReturnCheckStatusCrosses(self):
        queryString = "op=check&f=w&r=g&b=y&l=b&t=r&u=o&cube=r,w,r,w,w,w,r,w,r,"\
                                                            "w,g,w,g,g,g,w,g,w,"\
                                                            "o,y,o,y,y,y,o,y,o,"\
                                                            "y,b,y,b,b,b,y,b,y,"\
                                                            "g,r,g,r,r,r,g,r,g,"\
                                                            "b,o,b,o,o,o,b,o,b"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('crosses', resultDict['status'])
        
    def test300_061_ShouldReturnCheckStatusCrossesOnMovedBorderElements(self):
        queryString = "op=check&f=r&r=w&b=o&l=y&t=g&u=b&cube=w,r,w,r,r,r,w,r,w,g,w,g,w,w,w,g,w,g,y,o,y,o,o,o,y,o,y,b,y,b,y,y,y,b,y,b,r,g,r,g,g,g,r,g,r,o,b,o,b,b,b,o,b,o"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('crosses', resultDict['status'])
        
    def test300_070_ShouldReturnCheckStatusSpots(self):
        queryString = "op=check&f=r&r=b&b=o&l=g&t=w&u=y&cube=y,y,y,y,r,y,y,y,y,"\
                                                            "o,o,o,o,b,o,o,o,o,"\
                                                            "w,w,w,w,o,w,w,w,w,"\
                                                            "r,r,r,r,g,r,r,r,r,"\
                                                            "b,b,b,b,w,b,b,b,b,"\
                                                            "g,g,g,g,y,g,g,g,g"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('spots', resultDict['status'])
        
    
    def test300_080_ShouldReturnCheckStatusUnknown(self):
        queryString = "op=check&f=o&r=b&b=r&l=g&t=y&u=w&cube=y,y,b,b,o,g,o,b,w,"\
                                                            "r,b,b,r,b,w,b,w,r,"\
                                                            "o,g,g,o,r,g,g,b,b,"\
                                                            "y,y,o,y,g,o,o,o,g,"\
                                                            "r,w,w,r,y,r,g,o,y,"\
                                                            "w,y,r,g,w,r,y,w,w"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('unknown', resultDict['status']) 


# SAD PATHS 
    def test300_010_ShouldReturnErrorOnMissingCube(self):
        queryString = "op=check"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error: cube must be specified', resultDict['status'])

    def test300_020_ShouldReturnErrorOnMissingOpValue(self):
        queryString = "op="
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error: op code is missing', resultDict['status'])
        
    def test300_030_ShouldReturnErrorOnNonexistentOpValue(self):
        queryString = "op=noSuchOp"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error: op code is missing', resultDict['status'])
        
    def test300_040_ShouldReturnErrorOnInvalidCubeLength(self):
        queryString = "op=check&f=2&r=o&b=g&l=r&t=b&u=y&cube=y,y,b,b,o,g,o,b,w,r"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertIn('status', resultDict)
        self.assertEquals('error: cube is not sized properly', resultDict['status'])
        
    def test300_041_ShouldReturnErrorOnIllegalCube(self):
        queryString = "op=check&f=f&r=r&b=b&l=l&t=t&u=u&cube=f,f,f,f,f,b,f,f,f,"\
                                                            "r,r,r,r,r,r,r,r,r,"\
                                                            "f,b,b,b,b,b,b,b,b,"\
                                                            "l,l,l,l,l,l,l,l,l,"\
                                                            "t,t,t,t,t,t,t,t,t,"\
                                                            "u,u,u,u,u,u,u,u,u"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('error: unsolvable cube configuration', resultDict['status'])

    def test300_042_ShouldReturnErrorOnRepeatingMiddleElements(self):
        queryString = "op=check&f=f&r=r&b=b&l=l&t=t&u=u&cube=f,f,f,f,f,f,f,f,f,\
                                                             r,r,r,r,r,r,r,r,r,\
                                                             b,b,b,b,u,b,b,b,b,\
                                                             l,l,l,l,l,l,l,l,l,\
                                                             t,t,t,t,t,t,t,t,t,\
                                                             u,u,u,u,u,u,u,u,u"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('error: unsolvable cube configuration', resultDict['status'])
        
    def test300_090_ShouldReturnErrorOnUnsolvableCubeCustomerExample(self):
        queryString = "op=check&f=f&r=r&b=b&l=l&t=t&u=u&cube=f,f,f,f,f,b,f,f,f,\
                                                             r,r,r,r,r,r,r,r,r,\
                                                             f,b,b,b,b,b,b,b,b,\
                                                             l,l,l,l,l,l,l,l,l,\
                                                             t,t,t,t,t,t,t,t,t,\
                                                             u,u,u,u,u,u,u,u,u"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('error: unsolvable cube configuration', resultDict['status'])
        
    def test300_091_ShouldReturnErrorOnIllegalEdges(self):
        queryString = "op=check&f=f&r=r&b=b&l=l&t=t&u=u&cube=f,f,f,f,f,b,f,f,f,r,r,r,r,r,f,r,r,r,b,b,b,b,b,r,b,b,b,l,l,l,l,l,l,l,l,l,t,t,t,t,t,t,t,t,t,u,u,u,u,u,u,u,u,u"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('error: unsolvable cube configuration', resultDict['status'])
        
    def test300_092_ShouldReturnErrorOnIllegalCorners(self):
        queryString = "op=check&f=f&r=r&b=b&l=l&t=t&u=u&cube=f,f,f,f,f,f,t,f,f,r,r,r,r,r,r,r,r,r,f,b,b,b,b,b,b,b,b,l,l,l,l,l,l,l,l,l,t,t,t,t,t,t,t,t,b,u,u,u,u,u,u,u,u,u"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('error: unsolvable cube configuration', resultDict['status'])
        
# Acceptance Tests ==============================================================
#
# 400 dispatch -- op-rotate
# Desired level of confidence is BVA
# Analysis 
#    inputs:     http:// ...myURL... /rcube?op=rotate<options>
#        where <options> can be zero or one of: 
#            f=<string>  String of length .GT. 0. Optional. Defaults to "green" Unvalidated.
#            r=<string>  String of length .GT. 0. Optional. Defaults to "yellow" Unvalidated.
#            b=<string>  String of length .GT. 0. Optional. Defaults to "blue" Unvalidated.
#            l=<string>  String of length .GT. 0. Optional. Defaults to "white" Unvalidated.
#            t=<string>  String of length .GT. 0. Optional. Defaults to "red" Unvalidated.
#            u=<string>  String of length .GT. 0. Optional. Defaults to "orange" Unvalidated.
#            cube=<string> String of colors, comm-separated.  Contains no extraneous white space.  
#                          The first 9 elements represent the colors on the front face, the second 9 elements 
#                          represent the colors on the right face, and so forth for the back, left, top, and under faces, respectively.   
#                          Each face's elements are arranged in row-major order, beginning with the upper left corner.  
#                          Each element's color comes from the designated set of colors. The "Support Info" tab illustrates the layout of the cube.  Mandatory.  
#                          Arrives unvalidated.  
#            face=<string> Specifies the face to rotate.  It is a string having one of the values listed below.  Mandatory.  Arrives unvalidated.        
#                 Value of "face"    Meaning    
#                     f    Turn the front face such that the top moves to the right.    
#                     F    Turn the front face such that the top moves to the left.    
#                     r     Turn the right face such that the top moves to the back    
#                     R     Turn the right face such that the top moves to the front    
#                     b    Turn the back face such that the top moves to the left    
#                     B    Turn the back face such that the top moves to the right    
#                     l    Turn the left face such that the top moves to the front    
#                     L    Turn the left face such that the top moves to the back    
#                     t    Turn the top face such that the front moves to the left    
#                     T    Turn the top face such that the front moves to the right    
#                     u    Turn the bottom face such that the front moves to the right.    
#                     U    Turn the bottom face such that the front moves to the left.    
#
# HAPPY PATHS 
    def test400_040_ShouldReturnCubeRotatedF(self):
        queryString = "op=rotate&f=g&r=r&b=b&l=o&t=w&u=y&cube=g,g,g,g,g,g,g,g,g,\
                                                              r,r,r,r,r,r,r,r,r,\
                                                              b,b,b,b,b,b,b,b,b,\
                                                              o,o,o,o,o,o,o,o,o,\
                                                              w,w,w,w,w,w,w,w,w,\
                                                              y,y,y,y,y,y,y,y,y&face=F"
        expectedFacelets = ['g','g','g','g','g','g','g','g','g', 
                            'y','r','r','y','r','r','y','r','r', 
                            'b','b','b','b','b','b','b','b','b', 
                            'o','o','w','o','o','w','o','o','w', 
                            'w','w','w','w','w','w','r','r','r',
                            'o','o','o','y','y','y','y','y','y']        
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        actualFacelets = resultDict['cube']
        self.assertEquals('rotated', resultDict['status'])
        for i in range(54):
            self.assertEquals(expectedFacelets[i], actualFacelets[i])
         
    def test400_045_ShouldReturnCubeRotatedf(self):
        queryString = "op=rotate&f=g&r=r&b=b&l=o&t=w&u=y&cube=g,g,g,g,g,g,g,g,g,\
                                                              r,r,r,r,r,r,r,r,r,\
                                                              b,b,b,b,b,b,b,b,b,\
                                                              o,o,o,o,o,o,o,o,o,\
                                                              w,w,w,w,w,w,w,w,w,\
                                                              y,y,y,y,y,y,y,y,y&face=f"
        expectedFacelets = ['g','g','g','g','g','g','g','g','g',
                            'w','r','r','w','r','r','w','r','r',
                            'b','b','b','b','b','b','b','b','b',
                            'o','o','y','o','o','y','o','o','y',
                            'w','w','w','w','w','w','o','o','o',
                            'r','r','r','y','y','y','y','y','y']       
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        actualFacelets = resultDict['cube']
        self.assertEquals('rotated', resultDict['status'])
        for i in range(54):
            self.assertEquals(expectedFacelets[i], actualFacelets[i])
            
    def test400_050_ShouldReturnCubeRotatedR(self):
        queryString = "op=rotate&f=g&r=r&b=b&l=o&t=w&u=y&cube=g,g,g,g,g,g,g,g,g,\
                                                              r,r,r,r,r,r,r,r,r,\
                                                              b,b,b,b,b,b,b,b,b,\
                                                              o,o,o,o,o,o,o,o,o,\
                                                              w,w,w,w,w,w,w,w,w,\
                                                              y,y,y,y,y,y,y,y,y&face=R"
        expectedFacelets = ['g','g','w','g','g','w','g','g','w',
                            'r','r','r','r','r','r','r','r','r',
                            'y','b','b','y','b','b','y','b','b',
                            'o','o','o','o','o','o','o','o','o',
                            'w','w','b','w','w','b','w','w','b',
                            'y','y','g','y','y','g','y','y','g']       
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        actualFacelets = resultDict['cube']
        self.assertEquals('rotated', resultDict['status'])
        for i in range(54):
            self.assertEquals(expectedFacelets[i], actualFacelets[i])

    def test400_055_ShouldReturnCubeRotatedr(self):
        queryString = "op=rotate&f=g&r=r&b=b&l=o&t=w&u=y&cube=g,g,g,g,g,g,g,g,g,\
                                                              r,r,r,r,r,r,r,r,r,\
                                                              b,b,b,b,b,b,b,b,b,\
                                                              o,o,o,o,o,o,o,o,o,\
                                                              w,w,w,w,w,w,w,w,w,\
                                                              y,y,y,y,y,y,y,y,y&face=r"
        expectedFacelets = ['g','g','y','g','g','y','g','g','y',
                            'r','r','r','r','r','r','r','r','r',
                            'w','b','b','w','b','b','w','b','b',
                            'o','o','o','o','o','o','o','o','o',
                            'w','w','g','w','w','g','w','w','g',
                            'y','y','b','y','y','b','y','y','b']       
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        actualFacelets = resultDict['cube']
        self.assertEquals('rotated', resultDict['status'])
        for i in range(54):
            self.assertEquals(expectedFacelets[i], actualFacelets[i])
             
    def test400_060_ShouldReturnCubeRotatedB(self):
        queryString = "op=rotate&f=g&r=r&b=b&l=o&t=w&u=y&cube=g,g,g,g,g,g,g,g,g,\
                                                              r,r,r,r,r,r,r,r,r,\
                                                              b,b,b,b,b,b,b,b,b,\
                                                              o,o,o,o,o,o,o,o,o,\
                                                              w,w,w,w,w,w,w,w,w,\
                                                              y,y,y,y,y,y,y,y,y&face=B"
        expectedFacelets = ['g','g','g','g','g','g','g','g','g',
                            'r','r','w','r','r','w','r','r','w',
                            'b','b','b','b','b','b','b','b','b',
                            'y','o','o','y','o','o','y','o','o',
                            'o','o','o','w','w','w','w','w','w',
                            'y','y','y','y','y','y','r','r','r']    
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        actualFacelets = resultDict['cube']
        self.assertEquals('rotated', resultDict['status'])
        for i in range(54):
            self.assertEquals(expectedFacelets[i], actualFacelets[i])
            
    def test400_065_ShouldReturnCubeRotatedb(self):
        queryString = "op=rotate&f=g&r=r&b=b&l=o&t=w&u=y&cube=g,g,g,g,g,g,g,g,g,\
                                                              r,r,r,r,r,r,r,r,r,\
                                                              b,b,b,b,b,b,b,b,b,\
                                                              o,o,o,o,o,o,o,o,o,\
                                                              w,w,w,w,w,w,w,w,w,\
                                                              y,y,y,y,y,y,y,y,y&face=b"
        expectedFacelets = ['g','g','g','g','g','g','g','g','g',
                            'r','r','y','r','r','y','r','r','y',
                            'b','b','b','b','b','b','b','b','b',
                            'w','o','o','w','o','o','w','o','o',
                            'r','r','r','w','w','w','w','w','w',
                            'y','y','y','y','y','y','o','o','o']       
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        actualFacelets = resultDict['cube']
        self.assertEquals('rotated', resultDict['status'])
        for i in range(54):
            self.assertEquals(expectedFacelets[i], actualFacelets[i])
             
    def test400_070_ShouldReturnCubeRotatedL(self):
        queryString = "op=rotate&f=g&r=r&b=b&l=o&t=w&u=y&cube=g,g,g,g,g,g,g,g,g,\
                                                              r,r,r,r,r,r,r,r,r,\
                                                              b,b,b,b,b,b,b,b,b,\
                                                              o,o,o,o,o,o,o,o,o,\
                                                              w,w,w,w,w,w,w,w,w,\
                                                              y,y,y,y,y,y,y,y,y&face=L"
        expectedFacelets = ['y','g','g','y','g','g','y','g','g',
                            'r','r','r','r','r','r','r','r','r',
                            'b','b','w','b','b','w','b','b','w',
                            'o','o','o','o','o','o','o','o','o',
                            'g','w','w','g','w','w','g','w','w',
                            'b','y','y','b','y','y','b','y','y']      
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        actualFacelets = resultDict['cube']
        self.assertEquals('rotated', resultDict['status'])
        for i in range(54):
            self.assertEquals(expectedFacelets[i], actualFacelets[i])
             
    def test400_075_ShouldReturnCubeRotatedl(self):
        queryString = "op=rotate&f=g&r=r&b=b&l=o&t=w&u=y&cube=g,g,g,g,g,g,g,g,g,\
                                                              r,r,r,r,r,r,r,r,r,\
                                                              b,b,b,b,b,b,b,b,b,\
                                                              o,o,o,o,o,o,o,o,o,\
                                                              w,w,w,w,w,w,w,w,w,\
                                                              y,y,y,y,y,y,y,y,y&face=l"
        expectedFacelets = ['w','g','g','w','g','g','w','g','g',
                            'r','r','r','r','r','r','r','r','r',
                            'b','b','y','b','b','y','b','b','y',
                            'o','o','o','o','o','o','o','o','o',
                            'b','w','w','b','w','w','b','w','w',
                            'g','y','y','g','y','y','g','y','y']       
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        actualFacelets = resultDict['cube']
        self.assertEquals('rotated', resultDict['status'])
        for i in range(54):
            self.assertEquals(expectedFacelets[i], actualFacelets[i])
             
    def test400_080_ShouldReturnCubeRotatedT(self):
        queryString = "op=rotate&f=g&r=r&b=b&l=o&t=w&u=y&cube=g,g,g,g,g,g,g,g,g,\
                                                              r,r,r,r,r,r,r,r,r,\
                                                              b,b,b,b,b,b,b,b,b,\
                                                              o,o,o,o,o,o,o,o,o,\
                                                              w,w,w,w,w,w,w,w,w,\
                                                              y,y,y,y,y,y,y,y,y&face=T"
        expectedFacelets = ['o','o','o','g','g','g','g','g','g',
                            'g','g','g','r','r','r','r','r','r',
                            'r','r','r','b','b','b','b','b','b',
                            'b','b','b','o','o','o','o','o','o',
                            'w','w','w','w','w','w','w','w','w',
                            'y','y','y','y','y','y','y','y','y']       
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        actualFacelets = resultDict['cube']
        self.assertEquals('rotated', resultDict['status'])
        for i in range(54):
            self.assertEquals(expectedFacelets[i], actualFacelets[i])
             
    def test400_085_ShouldReturnCubeRotatedt(self):
        queryString = "op=rotate&f=g&r=r&b=b&l=o&t=w&u=y&cube=g,g,g,g,g,g,g,g,g,\
                                                              r,r,r,r,r,r,r,r,r,\
                                                              b,b,b,b,b,b,b,b,b,\
                                                              o,o,o,o,o,o,o,o,o,\
                                                              w,w,w,w,w,w,w,w,w,\
                                                              y,y,y,y,y,y,y,y,y&face=t"
        expectedFacelets = ['r','r','r','g','g','g','g','g','g',
                            'b','b','b','r','r','r','r','r','r',
                            'o','o','o','b','b','b','b','b','b',
                            'g','g','g','o','o','o','o','o','o',
                            'w','w','w','w','w','w','w','w','w',
                            'y','y','y','y','y','y','y','y','y']       
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        actualFacelets = resultDict['cube']
        self.assertEquals('rotated', resultDict['status'])
        for i in range(54):
            self.assertEquals(expectedFacelets[i], actualFacelets[i])
             
    def test400_090_ShouldReturnCubeRotatedU(self):
        queryString = "op=rotate&f=g&r=r&b=b&l=o&t=w&u=y&cube=g,g,g,g,g,g,g,g,g,\
                                                              r,r,r,r,r,r,r,r,r,\
                                                              b,b,b,b,b,b,b,b,b,\
                                                              o,o,o,o,o,o,o,o,o,\
                                                              w,w,w,w,w,w,w,w,w,\
                                                              y,y,y,y,y,y,y,y,y&face=U"
        expectedFacelets = ['g','g','g','g','g','g','r','r','r',
                            'r','r','r','r','r','r','b','b','b',
                            'b','b','b','b','b','b','o','o','o',
                            'o','o','o','o','o','o','g','g','g',
                            'w','w','w','w','w','w','w','w','w',
                            'y','y','y','y','y','y','y','y','y']       
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        actualFacelets = resultDict['cube']
        self.assertEquals('rotated', resultDict['status'])
        for i in range(54):
            self.assertEquals(expectedFacelets[i], actualFacelets[i])
             
    def test400_095_ShouldReturnCubeRotatedu(self):
        queryString = "op=rotate&f=g&r=r&b=b&l=o&t=w&u=y&cube=g,g,g,g,g,g,g,g,g,\
                                                              r,r,r,r,r,r,r,r,r,\
                                                              b,b,b,b,b,b,b,b,b,\
                                                              o,o,o,o,o,o,o,o,o,\
                                                              w,w,w,w,w,w,w,w,w,\
                                                              y,y,y,y,y,y,y,y,y&face=u"
        expectedFacelets = ['g','g','g','g','g','g','o','o','o',
                            'r','r','r','r','r','r','g','g','g',
                            'b','b','b','b','b','b','r','r','r',
                            'o','o','o','o','o','o','b','b','b',
                            'w','w','w','w','w','w','w','w','w',
                            'y','y','y','y','y','y','y','y','y']       
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        actualFacelets = resultDict['cube']
        self.assertEquals('rotated', resultDict['status'])
        for i in range(54):
            self.assertEquals(expectedFacelets[i], actualFacelets[i])
 
#     def test400_100_ShouldReturnCubeRotatedCrosses(self):
#         queryString = "op=rotate&f=w&r=g&b=y&l=b&t=r&u=o&cube=r,w,r,w,w,w,r,w,r,\
#                                                               w,g,w,g,g,g,w,g,w,\
#                                                               o,y,o,y,y,y,o,y,o,\
#                                                               y,b,y,b,b,b,y,b,y,\
#                                                               g,r,g,r,r,r,g,r,g,\
#                                                               b,o,b,o,o,o,b,o,b&face=t"
#         expectedFacelets = ['w','g','w','w','w','w','r','w','r',
#                             'o','y','o','g','g','g','w','g','w',
#                             'y','b','y','y','y','y','o','y','o',
#                             'r','w','r','b','b','b','y','b','y',
#                             'g','r','g','r','r','r','g','r','g',
#                             'b','o','b','o','o','o','b','o','b']       
#         resultString = self.httpGetAndResponse(queryString)
#         resultDict = self.string2dict(resultString)
#         actualFacelets = resultDict['cube']
#         self.assertEquals('rotated', resultDict['status'])
#         for i in range(54):
#             self.assertEquals(expectedFacelets[i], actualFacelets[i])
#              
#     def test400_105_ShouldReturnCubeRotatedSpots(self):
#         queryString = "op=rotate&f=r&r=b&b=o&l=g&t=w&u=y&cube=y,y,y,y,r,y,y,y,y,\
#                                                               o,o,o,o,b,o,o,o,o,\
#                                                               w,w,w,w,o,w,w,w,w,\
#                                                               r,r,r,r,g,r,r,r,r,\
#                                                               b,b,b,b,w,b,b,b,b,\
#                                                               g,g,g,g,y,g,g,g,g&face=t"
#         expectedFacelets = ['o','o','o','y','r','y','y','y','y',
#                             'w','w','w','o','b','o','o','o','o',
#                             'r','r','r','w','o','w','w','w','w',
#                             'y','y','y','r','g','r','r','r','r',
#                             'b','b','b','b','w','b','b','b','b',
#                             'g','g','g','g','y','g','g','g','g']       
#         resultString = self.httpGetAndResponse(queryString)
#         resultDict = self.string2dict(resultString)
#         actualFacelets = resultDict['cube']
#         self.assertEquals('rotated', resultDict['status'])
#         for i in range(54):
#             self.assertEquals(expectedFacelets[i], actualFacelets[i])
             
    def test400_110_ShouldReturnCubeRotatedUnknown(self):
        queryString = "op=rotate&f=o&r=b&b=r&l=g&t=y&u=w&cube=y,y,b,b,o,g,o,b,w,r,b,b,r,b,w,b,w,r,o,g,g,o,r,g,g,b,b,y,y,o,y,g,o,o,o,g,r,w,w,r,y,r,g,o,y,w,y,r,g,w,r,y,w,w&face=t"
        expectedFacelets = ['r','b','b','b','o','g','o','b','w',
                            'o','g','g','r','b','w','b','w','r',
                            'y','y','o','o','r','g','g','b','b',
                            'y','y','b','y','g','o','o','o','g',
                            'g','r','r','o','y','w','y','r','w',
                            'w','y','r','g','w','r','y','w','w']       
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        actualFacelets = resultDict['cube']
        self.assertEquals('rotated', resultDict['status'])
        for i in range(54):
            self.assertEquals(expectedFacelets[i], actualFacelets[i])

# SAD PATHS
    def test400_010_ShouldReturnStatusErrorOnUnspecifiedCube(self):
        queryString = "op=rotate"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('error: cube must be specified', resultDict['status'])
        
    def test400_020_ShouldReturnStatusErrorOnUnknownFace(self):
        queryString = "op=rotate&f=g&r=r&b=b&l=o&t=w&u=y&cube=g,g,g,g,g,g,g,g,g,\
                                                              r,r,r,r,r,r,r,r,r,\
                                                              b,b,b,b,b,b,b,b,b,\
                                                              o,o,o,o,o,o,o,o,o,\
                                                              w,w,w,w,w,w,w,w,w,\
                                                              y,y,y,y,y,y,y,y,y&face=w"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('error: face is unknown', resultDict['status'])
        
    def test400_030_ShouldReturnStatusErrorOnMissingFace(self):
        queryString = "op=rotate&f=g&r=r&b=b&l=o&t=w&u=y&cube=g,g,g,g,g,g,g,g,g,\
                                                              r,r,r,r,r,r,r,r,r,\
                                                              b,b,b,b,b,b,b,b,b,\
                                                              o,o,o,o,o,o,o,o,o,\
                                                              w,w,w,w,w,w,w,w,w,\
                                                              y,y,y,y,y,y,y,y,y"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('error: face is missing', resultDict['status'])        
        
# Acceptance Tests ==============================================================
#
# 500 dispatch -- op-scramble
# Desired level of confidence is BVA
# Analysis 
#    inputs:     http:// ...myURL... /rcube?op=scramble<options>
# Analysis 
#    inputs:     http:// ...myURL... /rcube?op=scramble<options>
#        where <options> can be zero or one of: 
#            method=<string>  String of length .GT. 0. Optional. Defaults to "random" Unvalidated.
#            n=<string>  String of length .GE. 0. Optional. Defaults to '0' Unvalidated. 
#            face=<string> Specifies the face to rotate.  It is a string having one of the values listed below.  Mandatory.  Arrives unvalidated.        
#                 Value of "face"    Meaning    
#                     f    Turn the front face such that the top moves to the right.    
#                     F    Turn the front face such that the top moves to the left.    
#                     r     Turn the right face such that the top moves to the back    
#                     R     Turn the right face such that the top moves to the front    
#                     b    Turn the back face such that the top moves to the left    
#                     B    Turn the back face such that the top moves to the right    
#                     l    Turn the left face such that the top moves to the front    
#                     L    Turn the left face such that the top moves to the back    
#                     t    Turn the top face such that the front moves to the left    
#                     T    Turn the top face such that the front moves to the right    
#                     u    Turn the bottom face such that the front moves to the right.    
#                     U    Turn the bottom face such that the front moves to the left.  
# HAPPY PATHS
    def test500_030_ShouldReturnScrambled100(self):
        queryString = "op=scramble"      
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('scrambled 100', resultDict['status'])
        self.assertEquals([], resultDict['rotations'])
        
    def test500_035_ShouldReturnScrambled67(self):
        queryString = "op=scramble&n=1"      
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('scrambled 67', resultDict['status'])
        #self.assertEquals(['f'], resultDict['random'])
        

# SAD PATHS
    def test500_010_ShouldReturnStatusErrorOnMethodNotGiven(self):
        queryString = "op=scramble&method="
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('error: method is unknown', resultDict['status'])
         
    def test500_015_ShouldReturnStatusErrorOnMethodUnknown(self):
        queryString = "op=scramble&method=none"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('error: method is unknown', resultDict['status'])
         
    def test500_020_ShouldReturnStatusErrorOn_N_NotGiven(self):
        queryString = "op=scramble&n="
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('error: n is invalid', resultDict['status'])   
         
    def test500_025_ShouldReturnStatusErrorOn_N_Invalid(self):
        queryString = "op=scramble&n=999"
        resultString = self.httpGetAndResponse(queryString)
        resultDict = self.string2dict(resultString)
        self.assertEquals('error: n is invalid', resultDict['status']) 

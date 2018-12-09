#===============================================================================
# Created on Sep 25, 2018
# 
# @author: zedtran
# 
# Course:         COMP5710
# Assignment:     4
# Date:           09/22/18
# AUBGID:         DZT0021
# Name:           Tran, Don
# 
# Description:    Non dev or test code. Just figuring Pyhon out.
#===============================================================================




def switch_faces(argument):
    parm_options = {
        'f': 'green',
        'r': 'yellow',
        'b': 'blue',
        'l': 'white',
        't': 'red',
        'u': 'orange'
    }
    print parm_options.get(argument, "Invalid Face")
    
    
#======== Can add this after assigning faces in createCube and before populating the cube ======
#    
#     cubeValues = {1:faceF, 2:faceR, 3:faceB, 4:faceL, 5:faceT, 6:faceU}
#     for key in sorted(cubeValues.keys()):
#         for i in range(1, key):
#             if key[i] == key.value():
#                 # This means we have >= 2 faces with the same color
# 
#         for i in range(key+1, 6):
#             if key[i] == key.value():
#                 # This means we have >= 2 faces with the same color
#================================================================================================


# How to check length of query string -- Place into dispatch



# How list slices work
a = [1, 2, 3, 4, 5, 6, 7, 8]

print(a[1:4])
# >>> [2, 3, 4]

print(a[1:4:2])
# >>> [2, 4] << Increment by 2

print(a[::-1])
# >>> 'a' in reverse -- Vanilla Python lets you negative index 




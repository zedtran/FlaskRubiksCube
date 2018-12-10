# Flask Microservice Rubik's Cube 

![alt text](https://github.com/zedtran/FlaskRubiksCube/blob/master/RCube/Images/Screen%20Shot%202018-12-10%20at%203.32.50%20PM.png)

Notes:
1)  Pull this code to GitHub Classroom
2)  Change "manifest.yml" to reflect your AU username
    Line 6:  is -> name: umphrda-rcube    should be -> name: username-rcube
 	Line 7:  is -> host: umphrda-rcube    should be -> host: username-rcube
3)  "dispatch.py" is your starting point
	It is the dispatching function for the microservice.
	It is passed the query string portion of the URL in Python dictionary format.
	For example, an HTTP request consisting the URL below
	     http://abc0001-rcube/mybluemix.net/rcube?op=init
	will result in {'op':'init'} being passed as the value of "parm"
4)  Place your production code in the body of the "RCube" directory.
5)  Place your test code in the "test" directory




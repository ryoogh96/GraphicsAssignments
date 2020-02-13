from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
WINDOW_POSITION_X = 0
WINDOW_POSITION_Y = 0

# start from right
angle = 150.0 

angleMoveSpeed = 360.0 / math.pi / 2

earthRotationAngle = 0
earthRotationIncrease = 360.0 # 지구의 하루는 지구가 한바퀴 자전하는 날이다.
earthRevolveAngle = 0
earthRevolveIncrease = 360.0 / 4 # 지구의 1년은 4일이다. 즉 태양을 한번 도는데 지구는 4번의 자전을 한다.
earthLeftAxis = 15.0
earthEyear = 1
earthEday = 1



plutoRotationAngle = 180.0 # 명왕성은 3시 방향에서 시작한다.
plutoRotationIncrease = earthRotationIncrease / 4 # 명왕성의 1년은 지구의 4년과 동일하다.
plutoRevolveAngle = 90.0 
plutoRevolveIncrease = plutoRotationIncrease / 8 # 명왕성의 1년은 명왕성의 8일마다 명왕성 1년이 돌아온다.
plutoPyear = 1
plutoPday = 1
plutoADistance = 15.0
plutoBDistance = 10.0
plutoX = 0.0
plutoZ = 0.0


settleLightAngle = 270.0 # 인공위성의 처음 위치는 적도와 평행한 평면상에 12시 방향에서 시작한다.
settleLightIncrease = 360.0
settleLightSlope = 0

lookView = 60.0
isStop = True # 처음에는 정지된 상태로 화면에 표시된다. 
isToggle = False 

def drawPlanet(distance, planetRadius, planet , slope):

    global earthRotationAngle,earthRevolveAngle,settleLightAngle,plutoRotationAngle,plutoRevolveAngle,settleLightSlope
    global plutoADistance,plutoBDistance,earthEyear,earthEday,plutoPyear,plutoPday

    if(planet == "pluto"):
        glRotatef(slope,1,0,0)
        glBegin(GL_LINE_STRIP)
        for i in range(0, 361):
            theta = 2.0 * 3.141592 * i / 360.0
            x = distance * math.cos(theta)
            y = distance * math.sin(theta)
            glVertex3f(x, 0, y)
        glEnd()
        glRotatef(plutoRotationAngle, 0, 1, 0) # 자전
        glTranslatef(distance, 0, 0)
        glRotatef(plutoRevolveAngle, 0, 0, 1) # 공전
        if(plutoRotationAngle > 360.0  * plutoPday):
            plutoPday += 1
        if(plutoPday % 8 == 0):
            plutoPyear = (plutoPday / 4) + 1
        glutSolidIcosahedron()   
    elif(planet == "settlelight"):
        glRotatef(slope,1,0,0)
        glBegin(GL_LINE_STRIP)
        for i in range(0, 361):
            theta = 2.0 * 3.141592 * i / 360.0
            x = distance * math.cos(theta)
            y = distance * math.sin(theta)
            glVertex3f(x, 0, y)
        glEnd()
        if(settleLightAngle > 360.0): # 인공위성은 매번 한 번씩 공전할 때마다 30도씩 기울기를 높이면서 지구를 회전한다.
            settleLightAngle = 0.0
            settleLightSlope += 30
        if(settleLightSlope >= 180): # 인공위성이 6바퀴를 다 돌면 다시 원래 기울기로 회복된다.
            settleLightSlope = 0
        glRotatef(settleLightAngle, 0, 1, 0)
        glTranslatef(distance, 0, 0)
        glutSolidCone(0.8,1.0,100,100)
    elif(planet == "earth"):
        glRotatef(slope,1,0,0) # 지구의 세로축은 수직에서 15도 기울어져 있다.
        glBegin(GL_LINE_STRIP)
        for i in range(0, 361):
            theta = 2.0 * 3.141592 * i / 360.0
            x = distance * math.cos(theta)
            y = distance * math.sin(theta)
            glVertex3f(x, 0, y)
        glEnd()        
        glRotatef(earthRotationAngle, 0, 1, 0) # 자전
        glTranslatef(distance, 0, 0)
        glRotatef(earthRevolveAngle, 0, 0, 1) # 공전
        glutSolidCube(1.0)
        if(earthRotationAngle > (360.0 / 4) * earthEday):
            earthEday += 1
        if(earthEday % 4 == 0):
            earthEyear = (earthEday / 4) + 1 
    
    
    
 
def drawScene() :
    
    global settleLightSlope
    
    # drawing
    # sun
    glPushMatrix()
    glColor3f(1,0,0)
    glutSolidSphere(1.0, 20, 20)
    glPopMatrix()
    # earth
    glPushMatrix()
    glColor3f(0,0.5,1.0)
    drawPlanet(5.0, 0.5, "earth",15)
    # settlelight
    glColor3f(0.0,0.0,0.0)
    drawPlanet(3.0, 0.5, "settlelight", settleLightSlope)
    glPopMatrix()
    # pluto
    glPushMatrix()
    glColor3f(0.7, 0.5, 0.5)
    drawPlanet(15.0, 0.5, "pluto", 0)
    glPopMatrix()
    
def disp() :

    global lookView,plutoRotationAngle,plutoRevolveAngle,earthRotationAngle,earthRevolveAngle,settleLightAngle
    global plutoRotationIncrease,plutoRevolveIncrease,earthRotationIncrease,earthRevolveIncrease,settleLightIncrease
    global earthEyear, earthEday, plutoPyear, plutoPday

    if(isStop == False):
        plutoRotationAngle += plutoRotationIncrease / 500
        plutoRevolveAngle += plutoRevolveIncrease / 500
        earthRotationAngle += earthRotationIncrease / 500
        earthRevolveAngle += earthRevolveIncrease / 500
        settleLightAngle += settleLightIncrease / 100




    # reset buffer
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(1.0,1.0,1.0,1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30, 1.0, 0.1, 1000)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Screen 2 All vision
    glViewport(WINDOW_POSITION_X, int(WINDOW_POSITION_Y+WINDOW_HEIGHT/2), int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2))
    glPushMatrix()
    gluLookAt(0, lookView, 0, 0, 0, 0, 0, 0, 1)
    EYear = "EYear = " + str(earthEyear) + " Eday = " + str(earthEday)
    PYear = "PYear = " + str(plutoPyear) + " Pday = " + str(plutoPday)
    renderBitmapCharacter(16,0,-16,EYear) # 지구 Year Day
    renderBitmapCharacter(-16,0,-16,PYear) # 명왕성 Year Day
    drawScene()
    glPopMatrix()

    # Screen 1 sun's vision
    glViewport(int(WINDOW_POSITION_X+WINDOW_WIDTH/2), int(WINDOW_POSITION_Y+WINDOW_HEIGHT/2), int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2))
    glPushMatrix()
    gluLookAt(1,1,1, 0,-1,4, 0,1,0) # 태양에서는 12시 방향으로만 본다.
    drawScene()
    glPopMatrix()


    theta = 2.0 * 3.141592 * settleLightAngle / 360.0
    x = 3.0
    z = 3.0
    
    settleLightXPrime = math.cos(theta) * x + math.sin(theta) * z 
    settleLightZPrime = -(math.sin(theta) * x) + math.cos(theta) * z

    #theta = 2.0 * 3.141592 *  earthRevolveAngle / 360.0
    #x = 5.0*math.cos(theta)
    #y = 5.0*math.sin(theta)
    
    #xPrime = math.cos(earthRevolveAngle) * x - math.sin(earthRevolveAngle) * y 
    #yPrime = math.sin(earthRevolveAngle) * x + math.cos(earthRevolveAngle) * y


    theta = 2.0 * 3.141592 * earthRotationAngle / 360.0
    
    x = 5.0
    z = 5.0


    earthXPrime = math.cos(theta) * x + math.sin(theta) * z 
    earthZPrime = -(math.sin(theta) * x) + math.cos(theta) * z    

 

    # Screen 4 earth's vision
    glViewport(int(WINDOW_POSITION_X+WINDOW_WIDTH/2), WINDOW_POSITION_Y, int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2))
    glPushMatrix()
    # settleLight's vision
    if(isToggle == True):
        gluLookAt(settleLightXPrime , 0 , settleLightZPrime, earthXPrime , 0, earthZPrime, 0, 1, 0) # eyex,z 4.5
    elif(isToggle == False):
        gluLookAt(earthXPrime , 0 , earthZPrime, 0 , 0, 0, 0, 1, 0) # eyex,z 4.5
    #EYear = "EYear = " + str(earthEyear) + " Eday = " + str(earthEday)
    #renderBitmapCharacter(5,3.5,5,EYear)
    drawScene()
    glPopMatrix()

    theta = 2.0 * 3.141592 * plutoRotationAngle / 360.0
    x = 15.0
    z = 15.0
    
    plutoXPrime = math.cos(theta) * x + math.sin(theta) * z 
    plutoZPrime = -(math.sin(theta) * x) + math.cos(theta) * z

    # Screen 3 pluto's vision
    glViewport(WINDOW_POSITION_X, WINDOW_POSITION_Y, int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2))
    glPushMatrix()
    gluLookAt(plutoXPrime, 0, plutoZPrime, earthXPrime, 0, earthZPrime, 0, 1, 0) # eyex,z 15.0
    #PYear = "PYear = " + str(plutoPyear) + " Pday = " + str(plutoPday)
    #renderBitmapCharacter(-10,5,-10,PYear)
    drawScene()
    glPopMatrix()



    glFlush()
    glutSwapBuffers()

def renderBitmapCharacter(x,y,z,string):
    glRasterPos3f(x,y,z)
    for c in string:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c));
    
def keyboardInputs(key, x, y):

    global lookView, isToggle, isStop
 
    if(key == b'-' and lookView <= 100.0): # No.10
        lookView += 1.0
    elif(key == b'+' and lookView > 10.0): # No.11
        lookView -= 1.0
    elif(key == b't'): # No.12
        if(isToggle == True):   
            isToggle = False
        elif(isToggle == False):
            isToggle = True
    elif(key == b'h'): #h를 치면 toggle로 움직인다.
        if(isStop == True):
            isStop = False
        elif(isStop == False):
            isStop = True
    elif(key == b'q'): # No.14
        sys.exit()
        
        

def main():
    # windowing
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH,WINDOW_HEIGHT)
    glutInitWindowPosition(WINDOW_POSITION_X,WINDOW_POSITION_Y)
    glutCreateWindow(b"Simple Solar System")


    # register callbacks
    glutDisplayFunc(disp)
    glutIdleFunc(disp)
    glutKeyboardFunc(keyboardInputs)

    # enter main infinite-loop
    glutMainLoop()

if __name__ == "__main__":
    main()




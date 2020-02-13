from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random
import math
from PIL import Image


Ld = [0.6,0.6,0.6,1] # 광원 확산반사
Ls = [1,1,1,1] # 광원 경면반사
La = [0.1,0.1,0.1,1] # 광원 주변반사
Lp = [0,7,2,1] # 광원의 위치 
Md = [1,1,1,1] # 확산반사 입사광 색깔
#Ma = [0,0,0,1] # 주변반사 입사광 색깔 
Ms = [1,1,1,1] # 경면반사 입사광 색깔
shininess = [127.0] # 광원의 빛의 세기 

t = 0

camDist = 8.6
camLookAt = ([8.6, 6.6, 5]) # 카메라 atX, atY, atZ
camFront = ([0, 0, 1])
camSpeed = 0.1
radius = 0.1

ballLoc = ([5.5, 3, 4])

fov = 60 # Field of View

pitch = 360 # x 축 기준 회전
yaw = 360 # y 축 기준 회전
roll = 360 # z 축 기준 회전

deltaTime = 0.0 # Time between current frame and last frame
lastFrame = 0.0 # Time of last frame

isLightOn = True # 조명 on/off 판별
isBallMove = False # 당구공 랜덤 이동 판별
isRotateTog = False # 카메라 회전 판별


def loadMesh(filename):
    print(filename)
    with open(filename, "rt") as mesh :
        nV = int(next(mesh))
        verts = [[0,0,0] for idx in range(nV)]
        for i in range(0, nV) :
            verts[i][0], verts[i][1], verts[i][2] = [float(x) for x in
next(mesh).split()]
        nF = int(next(mesh))
        faces = [[0,0,0] for idx in range(nF)]
        for i in range(0, nF) :
            faces[i][0], faces[i][1], faces[i][2] = [int(x) for x in
next(mesh).split()]
    return verts, faces

V, F = loadMesh("Hexahedron.msh")

def computeNormal(p1, p2, p3) :
    u = np.array([p2[i]- p1[i] for i in range(0, 3)])
    v = np.array([p3[i]- p1[i] for i in range(0, 3)])
    N = np.cross(u,v)
    N = N / np.linalg.norm(N)
    return N


def drawVerts(v, f):
    glBegin(GL_TRIANGLES)
    for i in range(len(f)) :
        p1, p2, p3 = f[i][0], f[i][1], f[i][2]
        N = computeNormal(v[p1], v[p2], v[p3])
        glNormal3fv(N)
        glVertex3fv(v[p1])
        glVertex3fv(v[p2])
        glVertex3fv(v[p3])
    glEnd()
    
def loadImage(imageName) :
    img = Image.open(imageName)
    img_data = np.array(list(img.getdata()), np.uint8)
    return img.size[0], img.size[1], img_data


def setTexture(imageName) :
    imgW, imgH, myImage = loadImage(imageName)
    # print(imgW, imgH, myImage)
     
    # texture image 생성
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 imgW, imgH, 0, GL_RGB,
                 GL_UNSIGNED_BYTE, myImage)
    # texture 매핑 옵션 설정
    glTexParameterf(GL_TEXTURE_2D,
    GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D,
    GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D,
    GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    # 2d texture 매핑을 활성화
    glEnable(GL_TEXTURE_2D)


def drawWallandFloor() :

    glColor3fv([1,1,1])

        

    
    # 뒷쪽 벽면
    setTexture("wallSurface.jpg")
    glBegin(GL_QUADS)
    glTexCoord2f(1,0)
    glVertex3fv([0, 0, 0])
    glTexCoord2f(1,1)
    glVertex3fv([0, 10, 0])
    glTexCoord2f(0,1)
    glVertex3fv([0, 10, 10])
    glTexCoord2f(0,0)
    glVertex3fv([0 , 0, 10])
    glEnd()



    # 오른쪽 벽면
    glBegin(GL_QUADS)
    glTexCoord2f(1,0)
    glVertex3fv([10, 0, 0])
    glTexCoord2f(1,1)
    glVertex3fv([10, 10, 0])
    glTexCoord2f(0,1)
    glVertex3fv([0, 10, 0])
    glTexCoord2f(0,0)
    glVertex3fv([0 , 0, 0])
    glEnd()


    
    # 앞쪽 벽면
    glBegin(GL_QUADS)
    glTexCoord2f(1,0)
    glVertex3fv([10, 0, 0])
    glTexCoord2f(1,1)
    glVertex3fv([10, 10, 0])
    glTexCoord2f(0,1)
    glVertex3fv([10, 10, 10])
    glTexCoord2f(0,0)
    glVertex3fv([10 , 0, 10])
    glEnd()

    

    # 왼쪽 벽면
    glBegin(GL_QUADS)
    glTexCoord2f(1,0)
    glVertex3fv([10, 0, 10])
    glTexCoord2f(1,1)
    glVertex3fv([10, 10, 10])
    glTexCoord2f(0,1)
    glVertex3fv([0, 10, 10])
    glTexCoord2f(0,0)
    glVertex3fv([0 , 0, 10])
    glEnd()

    setTexture("floorSurface.jpg")
    # 바닥면
    glBegin(GL_QUADS)
    glTexCoord2f(1,0)
    glVertex3fv([10, 0, 10])
    glTexCoord2f(1,1)
    glVertex3fv([10, 0, 0])
    glTexCoord2f(0,1)
    glVertex3fv([0, 0, 0])
    glTexCoord2f(0,0)
    glVertex3fv([0 , 0, 10])
    glEnd()

def drawBall() :
    global ballLoc, isBallMove

    if(isBallMove == True):
        random.random()


    
    
    glPushMatrix()
    glColor3fv([1,0,0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, np.array([1,0,0,0])) # 확산반사 입사광 조명 설정
    glMaterialfv(GL_FRONT, GL_SPECULAR, np.array([1,0,0,0])) # 경면반사 입사광 조명 설정
    glNormal3f(ballLoc[0], ballLoc[1], ballLoc[2])
    glTranslatef(ballLoc[0], ballLoc[1], ballLoc[2])
    glutSolidSphere(0.1, 20, 20)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_DIFFUSE, Md) # 확산반사 입사광 조명 설정
    glMaterialfv(GL_FRONT, GL_SPECULAR, Ms) # 경면반사 입사광 조명 설정 

def curFrameSet() :
    global deltaTime, lastFrame

    currentFrame = glutGet(GLUT_ELAPSED_TIME)
    deltaTime = currentFrame - lastFrame
    lastFrame = currentFrame

    

def LightSet():
    # 광원 설정
    glLightfv(GL_LIGHT0, GL_DIFFUSE, Ld) # 0번 광원 확산반사 특성 할당
    glLightfv(GL_LIGHT0, GL_AMBIENT, La) # 0번 광원 주변반사 특성 할당
    glLightfv(GL_LIGHT0, GL_SPECULAR, Ls) # 0번 광원 경면반사 특성 할당
    

    # 질감 설정
    glMaterialfv(GL_FRONT, GL_DIFFUSE, Md) # 확산반사 입사광 조명 설정
    #glMaterialfv(GL_FRONT, GL_AMBIENT, Ma) # 주변반사 입사광 조명 설정
    glMaterialfv(GL_FRONT, GL_SPECULAR, Ms) # 경면반사 입사광 조명 설정 
    glMaterialfv(GL_FRONT, GL_SHININESS, shininess) # 빛의세기 조명 설정 


def camSet() :
    global camDist, camLookAt, camFront, camSpeed
    global deltaTime, lastFrame, isRotateTog
    global pitch, yaw, roll, radius

    #theta = radius * 3.141592 / 360.0
    camSpeed = deltaTime / 20

    yaw += camSpeed

    # 카메라가 회전하는 상태면
    if(isRotateTog == True) :
        camLookAt[0] = 8.6 + math.cos(math.radians(pitch)) * math.cos(math.radians(yaw))
        camLookAt[1] = 6.6 + math.sin(math.radians(pitch))
        camLookAt[2] = 5 + math.cos(math.radians(pitch)) * math.sin(math.radians(yaw))
        
    gluLookAt(camLookAt[0], camLookAt[1], camLookAt[2], 5,0,5, 0,1,0)
    



def myReshape(w, h) :

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspRatio = w / h
    gluPerspective(fov, aspRatio, 0.1, 10)
    glViewport(0, 0, w, h)


def myDisplay():
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, 1280 / 720, 0.1, 10) # 카메라 Zoom in / out
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, Lp) # 0번 광원 위치 설정
    curFrameSet() # 현재 프레임 설정
    camSet() # 카메라 이동,회전 설정
    drawWallandFloor() # 벽면과 바닥을 그림
    drawVerts(V,F) # 당구장을 그림
    drawBall()
    glFlush()
    return


def keyboardInputs(key, x, y):

    global camDist, camLookAt, camFront, camSpeed, fov
    global isLightOn, isBallMove, isRotateTog

    if(key == b'n' or key == b'N') : # no.4 조명 on
        if(isLightOn == False):
            glEnable(GL_LIGHT0) 
            isLightOn = True
    elif(key == b'f' or key == b'F') : # no.4 조명 off
        if(isLightOn == True):
            glDisable(GL_LIGHT0) 
            isLightOn = False
    elif(key == b'i' or key == b'I') : # no.14 카메라 zoom in
            if(fov >= 48.0) :
                fov -= 1.0
                camDist -= 1.0
            #print (fov)
        #if(camLookAt[0] > 7.7) :
        
            #camLookAt += camSpeed * camFront;
            #camLookAt[0] -= camSpeed
            #camLookAt[1] -= camSpeed
            #print (camLookAt[0],camLookAt[1])
    elif(key == b'o' or key == b'O') : # no.14 카메라 zoom out
            if(fov < 60.0) :
                fov += 1.0
                camDist += 1.0
            #print (fov)
        #if(camLookXAt[0] < 8.6) : # zoom out 은 원래 위치(camLookX == 8.6)로 돌아가면 변하지 않는다.

            #camLookAt -= camSpeed * camFront;
            #camLookAt[0] += camSpeed
            #camLookAt[1] += camSpeed
            #print (camLookAt[0],camLookAt[1])
    elif(key == b'h' or key == b'H') : # no.9 당구공 랜덤 이동
        if(isBallMove == False): 
            isBallMove = True
        elif(isBallMove == True):
            isBallMove = False
    elif(key == b'r' or key == b'R') : # no.13 카메라 회전
        if(isRotateTog == False) :
            isRotateTog = True
        elif(isRotateTog == True) :
            isRotateTag = False



# initialization
def GLInit() :
    # clear color setting
    glClearColor(1, 1, 1, 1)
    glEnable(GL_DEPTH_TEST) # 물체 깊이 활성화 
    glEnable(GL_LIGHTING) # 조명 활성화
    glEnable(GL_LIGHT0) # 0번 광원 활성화
    LightSet() # 조명 설정

    
def main(arg) :
    # opengl glut initialization
    glutInit(arg)
    # window setting
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1280,720)
    glutInitWindowPosition(100, 50)
    glutCreateWindow(b"Billiard room")
    GLInit()
    glutKeyboardFunc(keyboardInputs)
    glutReshapeFunc(myReshape)
    glutDisplayFunc(myDisplay)
    glutIdleFunc(myDisplay)
    glutMainLoop()

if __name__ == "__main__" :
    main(sys.argv)



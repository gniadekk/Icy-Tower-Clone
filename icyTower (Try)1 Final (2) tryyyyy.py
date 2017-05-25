from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import sys
from PIL import Image
from PIL.Image import *
#-------------------------------------------------

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
windowBottom = 0

texNum = 7

barrier_width = 150
barrier_hieght = 30

dTime = 0.2
j = False
iyVelocity = 55
yVelocity = iyVelocity
onBar = False

time_interval = 10  # try  2,5,7 msec
gameStart = False

class RECTA:
    def __init__(self, left, bottom, right, top):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top

randList = []
for i in range(0, 100):
    randList.append(random.randrange(0, WINDOW_WIDTH - barrier_width, 1))

wall = RECTA(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
gameO = RECTA(50, 200, 550, 600)
icyPic = RECTA(0, 0, 600, 800)
startPlay = RECTA(150, 170, 450, 270)
exitGame = RECTA(150, 50, 450, 150)

moveX = 0
playerLeft = 200
playerRight = 230
playerBottom = 0
player = RECTA(playerLeft, playerBottom, playerRight, playerBottom + 60)  # initial position of the bat


ixVelocity = 2
xVelocity = ixVelocity

incs = False

def LoadBarriersTexture():
    global BarsTexture
    image = open("icy2.png")
    
    ix = image.size[0]
    iy = image.size[1]
    image = image.tobytes("raw", "RGBA", 0, -1)
    
    # Create Texture
    BarsTexture = glGenTextures(texNum)
    glBindTexture(GL_TEXTURE_2D, int(BarsTexture[0]))   # 2d texture (x and y size)
    
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

man = "icyMan1.png"
right = False
def LoadIcymanTexture():
    global manTexture, man, right
    if keystates[1]:
        man = "icyMan2.png"
        right = True
        if right:
            man = "icyMan3.png"
            right = False


    image = open(man)
    
    ix = image.size[0]
    iy = image.size[1]
    image = image.tobytes("raw", "RGBA", 0, -1)
    
    # Create Texture
    manTexture = glGenTextures(texNum)
    glBindTexture(GL_TEXTURE_2D, int(manTexture[1]))   # 2d texture (x and y size)
    
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 4, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


def LoadBackgroundTexture():
    global bkgTexture
    image = open("bk3.png")
    
    ix = image.size[0]
    iy = image.size[1]
    image = image.tobytes("raw", "RGBA", 0, -1)
    
    # Create Texture
    bkgTexture = glGenTextures(texNum)
    glBindTexture(GL_TEXTURE_2D, int(bkgTexture[2]))   # 2d texture (x and y size)
    
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


def LoadGameoverTexture():
    global gameOverTexture
    image = open("gameover.png")
    
    ix = image.size[0]
    iy = image.size[1]
    image = image.tobytes("raw", "RGBA", 0, -1)
    
    # Create Texture
    gameOverTexture = glGenTextures(texNum)
    glBindTexture(GL_TEXTURE_2D, int(gameOverTexture[3]))   # 2d texture (x and y size)
    
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

def LoadBeginTexture():
    global BeginTexture
    image = open("icyT.png")
    
    ix = image.size[0]
    iy = image.size[1]
    image = image.tobytes("raw", "RGBA", 0, -1)
    
    # Create Texture
    BeginTexture = glGenTextures(texNum)
    glBindTexture(GL_TEXTURE_2D, int(BeginTexture[4]))   # 2d texture (x and y size)
    
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


def LoadStartTexture():
    global startPlayTexture
    image = open("startPlay.png")
    
    ix = image.size[0]
    iy = image.size[1]
    image = image.tobytes("raw", "RGBA", 0, -1)
    
    # Create Texture
    startPlayTexture = glGenTextures(texNum)
    glBindTexture(GL_TEXTURE_2D, int(startPlayTexture[5]))   # 2d texture (x and y size)
    
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


def LoadExitTexture():
    global exitTexture
    image = open("exitGame.png")
    
    ix = image.size[0]
    iy = image.size[1]
    image = image.tobytes("raw", "RGBA", 0, -1)
    
    # Create Texture
    exitTexture = glGenTextures(texNum)
    glBindTexture(GL_TEXTURE_2D, int(exitTexture[6]))   # 2d texture (x and y size)
    
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

# Initialization
def init():
    global windowBottom
    LoadBarriersTexture()
    LoadIcymanTexture()
    LoadBackgroundTexture()
    LoadGameoverTexture()
    LoadBeginTexture()
    LoadStartTexture()
    LoadExitTexture()
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.0, 0.0, 0.0, 0.0)

    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, windowBottom, windowBottom + WINDOW_HEIGHT, 0, 1)  # l,r,b,t,n,f

    glMatrixMode(GL_MODELVIEW)


def reshape(w, h):
        WINDOW_WIDTH = w
        WINDOW_HEIGHT = h
        glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

def animate():
    glutPostRedisplay()

moveWindow = False
def DrawRectangle(rect):
    glLoadIdentity()
    glBindTexture(GL_TEXTURE_2D, int(BarsTexture[0]))
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex(rect.left, rect.bottom, 0)  # Left - Bottom
    glTexCoord2f(1.0, 0.0); glVertex(rect.right, rect.bottom, 0)
    glTexCoord2f(1.0, 1.0); glVertex(rect.right, rect.top, 0)
    glTexCoord2f(0.0, 1.0); glVertex(rect.left, rect.top, 0)
    glEnd()


def DrawPlayerRectangle(rect):
    #glColor4f(0, 0, 0, 1)
    glLoadIdentity()
    glBindTexture(GL_TEXTURE_2D, int(manTexture[1]))
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex(rect.left, rect.bottom, 0)  # Left - Bottom
    glTexCoord2f(1.0, 0.0); glVertex(rect.right, rect.bottom, 0)
    glTexCoord2f(1.0, 1.0); glVertex(rect.right, rect.top, 0)
    glTexCoord2f(0.0, 1.0); glVertex(rect.left, rect.top, 0)
    glEnd()

def DrawBackGRectangle(rect):
    glLoadIdentity()
    glBindTexture(GL_TEXTURE_2D, int(bkgTexture[2]))
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex(rect.left, rect.bottom, 0)  # Left - Bottom
    glTexCoord2f(1.0, 0.0); glVertex(rect.right, rect.bottom, 0)
    glTexCoord2f(1.0, 1.0); glVertex(rect.right, rect.top, 0)
    glTexCoord2f(0.0, 1.0); glVertex(rect.left, rect.top, 0)
    glEnd()

def DrawGameOverRectangle(rect):
    glLoadIdentity()
    glBindTexture(GL_TEXTURE_2D, int(gameOverTexture[3]))
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex(rect.left, rect.bottom, 0)  # Left - Bottom
    glTexCoord2f(1.0, 0.0); glVertex(rect.right, rect.bottom, 0)
    glTexCoord2f(1.0, 1.0); glVertex(rect.right, rect.top, 0)
    glTexCoord2f(0.0, 1.0); glVertex(rect.left, rect.top, 0)
    glEnd()


def DrawIcyRectangle(rect):
    glLoadIdentity()
    glBindTexture(GL_TEXTURE_2D, int(BeginTexture[4]))
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex(rect.left, rect.bottom, 0)  # Left - Bottom
    glTexCoord2f(1.0, 0.0); glVertex(rect.right, rect.bottom, 0)
    glTexCoord2f(1.0, 1.0); glVertex(rect.right, rect.top, 0)
    glTexCoord2f(0.0, 1.0); glVertex(rect.left, rect.top, 0)
    glEnd()


def DrawStartRectangle(rect):
    glLoadIdentity()
    glBindTexture(GL_TEXTURE_2D, int(startPlayTexture[5]))
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex(rect.left, rect.bottom, 0)  # Left - Bottom
    glTexCoord2f(1.0, 0.0); glVertex(rect.right, rect.bottom, 0)
    glTexCoord2f(1.0, 1.0); glVertex(rect.right, rect.top, 0)
    glTexCoord2f(0.0, 1.0); glVertex(rect.left, rect.top, 0)
    glEnd()


def DrawExitRectangle(rect):
    glLoadIdentity()
    glBindTexture(GL_TEXTURE_2D, int(exitTexture[6]))
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex(rect.left, rect.bottom, 0)  # Left - Bottom
    glTexCoord2f(1.0, 0.0); glVertex(rect.right, rect.bottom, 0)
    glTexCoord2f(1.0, 1.0); glVertex(rect.right, rect.top, 0)
    glTexCoord2f(0.0, 1.0); glVertex(rect.left, rect.top, 0)
    glEnd()

# Key Board Messages
def keyboard(key, x, y):
    global barScore, barBottom, barCount, valDecRatio, gameStart, downBars, gameOver

    if key == b"q":
        sys.exit(0)

    if gameStart == False:

        if key == b"s":
            gameStart = True
        
        if key == b"r":
            randList.clear()
            for i in range(0, 100):
                randList.append(random.randrange(0, WINDOW_WIDTH - barrier_width, 1))
            barsTopList.clear()

            downBars = False
            gameOver = False

            barScore = 0
            barBottom = 110
            barCount = 0
            valDecRatio = 0.2


def Timer(v):
    Display()
    glutTimerFunc(time_interval, Timer, 1)


increaseF = False
keystates = []
for i in range(0,5):
    keystates.append(False)
def arrow_keys(key, x, y):
    global j
    global increaseF
    global keystates

    if gameStart:

        if player.left > 0:
            if key == GLUT_KEY_LEFT:
                keystates[0] = True
        
        if player.right < WINDOW_WIDTH:
            if key == 102:
                keystates[1] = True
                
        if keystates[0] == True or keystates[1] == True:
            increaseF = True
            
        if key == GLUT_KEY_UP:
            keystates[2] = True
            if keystates[2] == True:
                j = True


def keys_up(key,x,y):
    global keystates
    global increaseF

    if key == GLUT_KEY_LEFT:
            keystates[0] = False
            increaseF = False
    if key == 102:
            keystates[1] = False
            increaseF = False
    if key == GLUT_KEY_UP:
            keystates[2] = False

def mouseMotion(key, state, x, y):
    global barScore, barBottom, barCount, valDecRatio, gameStart, downBars, gameOver
    mouse_x = x
    mouse_y = WINDOW_HEIGHT - y
    if gameStart == False and gameOver == False:
        if key == GLUT_LEFT_BUTTON and state == GLUT_DOWN :
            print(x,mouse_y)
        if (mouse_x >= 150 and x <= 450) and (mouse_y >= 250 and mouse_y <= 340) :
            if key == GLUT_LEFT_BUTTON and state == GLUT_DOWN :
                gameStart = True
        if (mouse_x >= 150 and x <= 450) and (mouse_y >= 200 and mouse_y <= 280) :
            if key == GLUT_LEFT_BUTTON and state == GLUT_DOWN :
                sys.exit(0)
    if gameOver:
        if key == GLUT_LEFT_BUTTON and state == GLUT_DOWN :
            randList.clear()
            for i in range(0, 100):
                randList.append(random.randrange(0, WINDOW_WIDTH - barrier_width, 1))
            barsTopList.clear()

            downBars = False
            gameOver = False

            barScore = 0
            barBottom = 110
            barCount = 0
            valDecRatio = 0.2


barLeft = 0
barRight = 0
barScore = 0
ig = 9.8
g = ig
highScore = 0
searchRng = 15
def jump():
    
    global yVelocity
    global playerBottom
    global j
    global player
    global onBar
    global barLeft
    global barRight
    global barsTopList
    global barCount
    global barScore
    global g
    global dTime
    global highScore

    onBar = False
    if player.bottom > 220:
        yVelocity -= 1.85*valDecRatio
    if factor >= 30 or factor <= -30:
        g = 2
        dTime = 0.3
    else:
        g = ig
        dTime = 0.2
    yVelocity -= g * dTime
    playerBottom += yVelocity * dTime

    for i in range(barCount, barCount+searchRng):
        if yVelocity < 0:
            if player.bottom >= barsTopList[i] and (player.left <= (randList[i] + barrier_width) and player.right >= randList[i]):
                if playerBottom <= barsTopList[i]:
                    playerBottom = barsTopList[i]
                    onBar = True
                    barScore = (i + 1) * 10
                    print(barScore)
                    barLeft = randList[i]
                    barRight = randList[i] + barrier_width
                    yVelocity = iyVelocity
                    j = False

    if highScore < barScore:
        highScore = barScore
    

    if playerBottom <= 0:
        playerBottom = 0
        yVelocity = iyVelocity
        j = False
    barsTopList.clear() # important for dropping down the Barriers



barsTopList = []
downBars = False
val = 0
valDecRatio = 0.2
barCount = 0
moveX = 0
factor = 2
gameOver = False
def Display():
    global playerLeft
    global playerRight
    global playerBottom
    global player
    global j
    global moveWindow
    global windowBottom
    global barsTopList
    global onBar
    global yVelocity
    global barLeft
    global barRight
    global downBars
    global val
    global valDecRatio
    global barCount
    global moveX
    global incMoveXR
    global incMoveXL
    global factor
    global gameStart
    global randList
    global restartGame
    global gameOver
    global highScore

    barBottom = 110

    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glColor(1, 1, 1)  # White color
    glLoadIdentity()

    DrawBackGRectangle(wall)

    if gameOver:
        DrawGameOverRectangle(gameO)

    if gameStart == False and gameOver == False:
        DrawIcyRectangle(icyPic)
        DrawStartRectangle(startPlay)
        DrawExitRectangle(exitGame)
    
    if gameStart:
        for i in range(0, randList.__len__()):
            left = randList[i]
            barrier = RECTA(left, barBottom, left + barrier_width, barBottom + barrier_hieght)
            if downBars: # drop down the Barriers
                if player.bottom <= 0:
                    val = 0
                    gameStart = False
                    gameOver = True
                barrier.bottom -= val
                barrier.top -= val
            if barsTopList.__len__() < randList.__len__():
                barsTopList.append(barrier.top)
            DrawRectangle(barrier)
            barBottom += 110


        if onBar:  # When out of bar left and right edges
            if player.left > barRight or player.right < barLeft:
                playerBottom -= 9
                for i in range(barCount, barCount+searchRng):
                    if player.bottom >= barsTopList[i] and (player.left <= (randList[i] + barrier_width) and player.right >= randList[i]):
                        if playerBottom <= barsTopList[i]:
                            playerBottom = barsTopList[i]
                if playerBottom <= 0:
                    playerBottom = 0


    # drop down the Barriers
        if player.top >= barsTopList[1]:
            val += valDecRatio
            if player.top >= (0.9*WINDOW_HEIGHT):
                val += 3
        if val != 0:
            downBars = True
            if onBar and player.top >= barsTopList[1]:
                playerBottom -= valDecRatio
                for i in range(0,barsTopList.__len__()):
                    if barsTopList[i] < 0:
                        if i > barCount:
                            barCount = i
                            print(barCount)
                            if (barCount % 3) == 0:
                                valDecRatio *= 1.25
                                print(valDecRatio)
                barsTopList.clear()


        score = "Score"
        Text(score,20,640)
        scoreNum = str(barScore)
        Text(scoreNum,50,600)

        HighScore = "High Score"
        Text(HighScore,20,710)
        HighScoreNum = str(highScore)
        Text(HighScoreNum,50,670)
        
        if j:
            jump()

        if increaseF:
            factor += 1
        else:
            factor = 2

        if keystates[1]:
            if player.right < WINDOW_WIDTH:
                moveX += factor*0.25
        
        if keystates[0]:
            if player.left > 0:
                moveX -= factor*0.25
    
        glLoadIdentity()
        DrawPlayerRectangle(player)
        player = RECTA(playerLeft + moveX, playerBottom, playerRight + moveX, playerBottom + 60)

    
    
    glutSwapBuffers()
def Text(string ,x,y):
    glLineWidth(3)
    glColor(1,1,1)
    glLoadIdentity()
    glTranslate(x,y,0)
    glScale(0.19,0.19,1)
    string = string.encode()
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN,c)
        
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Egyptian Icy Tower :D");
    glutDisplayFunc(Display)
    glutReshapeFunc(reshape)
    #glutIdleFunc(animate)
    glutTimerFunc(time_interval, Timer, 1)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(arrow_keys)
    glutSpecialUpFunc(keys_up)
    glutMouseFunc(mouseMotion)
    init()
    glutMainLoop()
main()

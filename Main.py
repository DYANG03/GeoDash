#Final Project - Geometry Dash - Main.py
#Daniel Yang and Devin Feng
#This game is based off of the widely known game Geometry Dash. We tried to copy it as much as we could
#To play the user simply clicks the mouse or taps the space bar to perform an action
#The goal is to dodge the incoming obstacles and make it alive to the end of the stage
#There are 4 different player modes that can change in game
#The first is the cube, the cube will perform a jump when the mouse is clicked
#Another mode is the ship, the ship will fly up when the mouse is clicked and all down when the mouse is not clicked
#Another mode is the ball, the ball will have a gravity switch when the mouse is clicked
#The final mode is the wave, the wave will travel dowards at an angle when the mouse is not clicked and will travel at an upwards angle when it is clicked
#To change from one mode into the other, there will be portals for each mode that will be in game
#The player can only land on platforms
#The player will die if it touches anything other than landing on a platform
#We made a pause function that pauses the game, you can then quit, resume, or go to level select from pause
#We have a main menu where you can go for help, level select, and others
#For the level select menu, we made it so it can infinitely loop around
#After you win, a win menu will pop up and you can choose to replay the level or go to level select
#-----------------------------

#Libraries
from pygame import *
from random import *
from math import *
import os
import copy
mixer.pre_init(44100,16,2,4096)
init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (120,30)
#-----------------------------

#Functions
def running(pList): #this is the running function for each level
    global count 
    global mouseHold
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == MOUSEBUTTONUP:
            mouseHold = False #mouse is not being held anymore if mouse button is released
    if not lose(pInfo):
        return True #if not lose keeping running
    else:
        pList[pLost] = True
        pList[pVely] = 0
        if count<len(explosionImages)-1: #adds to count so it can loop through the death animation
            count+=1
            return True
        else:
            count = 0
            time.wait(500) #waits a bit after death
            return False #stops running the level
    
def loadImages(imageList): #this function will load images according to their names and will resize them
    for i in range(len(imageList)):
        loadedImage = image.load("images/"+imageList[i]+".png")
        if imageList[i][0] == "c":
            size1,size2 = 60,60
        if imageList[i][0] == "s":
            size1,size2 = 113,60
        if imageList[i][0] == "b":
            size1,size2 = 60,60
        if imageList[i][0] == "w":
            size1,size2 = 60,49
        if imageList[i][0] == "P":
            size1,size2 = 120,120
        if imageList[i][0] == "G":
            size1,size2 = 6471,201
        if imageList[i][0] == "H":
            size1,size2 = 900,600
        if imageList[i][0] == "B":
            size1,size2 = 1280,600
        if imageList[i][0] == "S":
            size1,size2 = 40,60
        if imageList[i] == "Spike1" or imageList[i] == "USpikes1":
            size1,size2 = 65,65
        if imageList[i] == "Spike2" or imageList[i] == "USpikes2":
            size1,size2 = 130,65
        if imageList[i] == "Spike3" or imageList[i] == "USpikes3":
            size1,size2 = 195,65
        if imageList[i] == "Spike4" or imageList[i] == "USpikes4":
            size1,size2 = 260,65
        if imageList[i][4:10] == "Portal":
            size1,size2 = 48,120
        if imageList[i][-3:] == "Big":
            size1,size2 = 240,600
        if imageList[i] == "block1":
            size1,size2 = 60,60
        if imageList[i] == "endPortal":
            size1,size2 = 280,600
        try:
            scaledImage = transform.smoothscale(loadedImage,(size1,size2))
        except:
            scaledImage = loadedImage
        imageList[i] = scaledImage
            
def moveMap(pList,mapList): #this moves the map which creates the illusion of the player moving
    for j in range(len(mapList)): #it takes the mapList which has all the rect object and moves it by a certain amount each frame
        for i in range(len(mapList[j])):
            if mapList[j][i] == 0:
                break
            mapList[j][i] = mapList[j][i].move(pList[pVelx],0)
            
def notlanded(pList): #this check if the player is in the air by checking if there are any collisions with platforms
    check = Rect(pList[pPosX],pList[pPos],pList[pSize],pList[pSize]) #each mode has a different hitbox
    if pList[pMode] == "ship":
        check = Rect(pList[pPosX],pList[pPos]+1,pList[pSize],int(pList[pSize]/1.875))
    if pList[pMode] == "wave":
        check = Rect(pList[pPosX],pList[pPos],pList[pSize],int(pList[pSize]/1.23))
    if check.collidelist(platforms[:platforms.index(0)]) == -1:
        return True
    else:
        return False
        
def movePlayer(pList,gravityJump,viJump,iconList): #this is the function that determines how the player moves depending on the mode
    keys = key.get_pressed()
    mb = mouse.get_pressed()
    if pList[pMode] == "cube":
        moveCube(pList,iconList,keys,mb,viJump,gravityJump)
    if pList[pMode] == "ship":
        moveShip(pList,iconList,keys,mb)        
    if pList[pMode] == "ball":
        moveBall(pList,iconList,keys,mb,viJump,gravityJump)
    if pList[pMode] == "wave":
        moveWave(pList,iconList,keys,mb)   

def moveCube(pList,iconList,keys,mb,viJump,gravityJump): #this function controls how the cube moves
    pList[pImage] = iconList[0] #changes image to cube
    pList[pImageIndex] = 0
    pList[pSize] = 60
    if (keys[K_SPACE] or mb[0] == 1) and pList[pLanded]: #if the cube is landed it can perfor a jump
        pList[pVely] = viJump
        pList[pLanded] = False
        pList[pAction] = True #keeps track of the cubes state, if it is still jumping
    if notlanded(pList) and pList[pAction]:
        jump(pList,pList[pVely],iconList) #this is how the cube jumps
        pList[pVely] += gravityJump #add gravity
    elif notlanded(pList) and not pList[pAction]: #if cube is not jumping and not landed it is falling
        jump(pList,pList[pVely]+2,iconList)
        pList[pVely] += gravityJump

def moveShip(pList,iconList,keys,mb): #this is how the ship moves
    pList[pImage] = iconList[1]
    pList[pImageIndex] = 1
    pList[pSize] = 113
    dy = rotateShip(pList,iconList) #used to reset displacement after image rotates
    if keys[K_SPACE] or mb[0] == 1: #if clicked ship will fly
        pList[pAction] = True
    else:
        pList[pAction] = False
    if pList[pAction]:
        if pList[pRship] > -45: #maximum rotation of image
            pList[pRship] += -2.3
        if pList[pVely] > -13: #maximim speed
            if pList[pVely] == 1:
                pList[pVely] += -2 #so that velocity will not be 0
            else:
                pList[pVely] += -1 #gravity 
    if not pList[pAction]: #same as above ut opposite direction
        if pList[pRship] < 45:
            pList[pRship] += 2.3
        if pList[pVely] < 13:
            if pList[pVely] == -1:
                pList[pVely] += 2
            else:
                pList[pVely] += 1
    dist = abs(pList[pVely])
    direct = pList[pVely]//dist
    for i in range(dist): #checks one pixel ahead for collision
        check = Rect(pList[pPosX],pList[pPos]+direct,pList[pSize],int(pList[pSize]/1.875))
        if check.collidelist(platforms[:platforms.index(0)]) == -1:
            pList[pPos] += direct
        else:
            pList[pAction] = False #if collides stop moving and reset rotation of image
            pList[pVely] = 0
            pList[pRship] = 0
    pList[pImagePosY] = pList[pPos] + dy #keeps the center of the image the same as center of hitbox
        
def moveBall(pList,iconList,keys,mb,viJump,gravityJump): #moves the ball
    global ballOrb #used for when the ball jumps on a orb, if this flag is true the ball will use the same movement mechanics as the cube
    pList[pImage] = iconList[2]
    pList[pImageIndex] = 2
    pList[pSize] = 60
    pList[pImagePosX] = pList[pPosX]
    dy = spinBall(pList,iconList) #offset of center of image and hitbox
    if (keys[K_SPACE] or mb[0] == 1) and pList[pLanded] and not ballOrb: #regular ball movement
        pList[pVely] = 0
        pList[pLanded] = False
        pList[pAction] = True
        pList[pClickCount]+=1 #used to keep track of what gravity the ball is subjected to, positive/negative
    if (keys[K_SPACE] or mb[0] == 1) and pList[pLanded] and ballOrb: #ball when it jumps on a orb
        if pList[pClickCount]%2 == 0: #the ball will jump depending on the direction of gravity
            pList[pVely] = int(viJump//1.5)
        else:
            pList[pVely] = int(-viJump//1.5)
        pList[pLanded] = False
        pList[pAction] = True
    if not ballOrb: #regular ball movement
        if not pList[pLanded] and pList[pAction]: #the ball is moving and not landed
            if pList[pClickCount]%2 == 0: #direction the ball is moving in
                pList[pImagePosY] = pList[pPos] + dy #makes the center of image and hitbox the same after rotation
                for i in range(abs(pList[pVely])): #checks one pixel ahead for collision
                    check = Rect(pList[pPosX],pList[pPos]+1,pList[pSize],pList[pSize])
                    if check.collidelist(platforms[:platforms.index(0)]) == -1:
                        pList[pPos] += 1
                    else:
                        pList[pLanded] = True
                        pList[pAction] = False
                        pList[pVely] = 0
                        pList[pImagePosY] = pList[pPos] + dy
                pList[pVely] += gravityJump//2 #the ball has a smaller gravity than the cube
            else:
                pList[pImagePosY] = pList[pPos] + dy #same as above but in opposite direction
                for i in range(abs(pList[pVely])):
                    check = Rect(pList[pPosX],pList[pPos]-1,pList[pSize],pList[pSize])
                    if check.collidelist(platforms[:platforms.index(0)]) == -1:
                        pList[pPos] -= 1
                    else:
                        pList[pLanded] = True
                        pList[pAction] = False
                        pList[pVely] = 0
                        pList[pImagePosY] = pList[pPos] + dy
                pList[pVely] -= gravityJump//2
        elif notlanded(pList) and not pList[pAction]: #falling for the ball same as falling for the cube but the ball has two gravities
            if pList[pClickCount]%2 == 0: #falling for the ball when gravity is negative
                pList[pImagePosY] = pList[pPos] + dy
                for i in range(abs(pList[pVely])):
                    check = Rect(pList[pPosX],pList[pPos]+1,pList[pSize],pList[pSize])
                    if check.collidelist(platforms[:platforms.index(0)]) == -1:
                        pList[pPos] += 1
                    else:
                        pList[pLanded] = True
                        pList[pAction] = False
                        pList[pVely] = 0
                        pList[pImagePosY] = pList[pPos] + dy
                pList[pVely] += gravityJump//2
            else: #falling movement for the ball when gravity is positive
                pList[pImagePosY] = pList[pPos] + dy
                for i in range(abs(pList[pVely])):
                    check = Rect(pList[pPosX],pList[pPos]-1,pList[pSize],pList[pSize])
                    if check.collidelist(platforms[:platforms.index(0)]) == -1:
                        pList[pPos] -= 1
                    else:
                        pList[pLanded] = True
                        pList[pAction] = False
                        pList[pVely] = 0
                        pList[pImagePosY] = pList[pPos] + dy
                pList[pVely] -= gravityJump//2
    if ballOrb: #if the ball movement is jumping on a orb it will do the following which is the same as the cubes code
        if notlanded(pList) and pList[pAction]:
            jump(pList,pList[pVely],iconList)
            if pList[pClickCount]%2 == 0:
                pList[pVely] += gravityJump//2
            else:
                pList[pVely] -= gravityJump//2
            
def moveWave(pList,iconList,keys,mb): #movement of the wave
    pList[pImage] = iconList[3]
    pList[pImageIndex] = 3
    pList[pVely] = pList[pVelx] #moves at 45 degree angles
    pList[pSize] = 60
    pList[pImagePosX] = pList[pPosX]
    if keys[K_SPACE] or mb[0] == 1: #if pressed the wave will move up
        pList[pLanded] = False
        pList[pImage] = transform.rotate(iconList[pList[pImageIndex]],40)
        for i in range(abs(pList[pVely])): #checks one pixel ahead for collision
            check = Rect(pList[pPosX],pList[pPos]-1,pList[pSize],int(pList[pSize]/1.23))
            if check.collidelist(platforms[:platforms.index(0)]) == -1:
                pList[pPos] -= 1
            else:
                pList[pVely] = 0
                pList[pLanded] = True
        pList[pImagePosY] = pList[pPos] - 20 #reset center of image and hitbox
    else: #wave will move down if mouse not pressed, same as above but in opposite direction
        pList[pLanded] = False
        pList[pImage] = transform.rotate(iconList[pList[pImageIndex]],-40)
        for i in range(abs(pList[pVely])):
            check = Rect(pList[pPosX],pList[pPos]+1,pList[pSize],int(pList[pSize]/1.23))
            if check.collidelist(platforms[:platforms.index(0)]) == -1:
                pList[pPos] += 1
            else:
                pList[pVely] = 0
                pList[pLanded] = True
        pList[pImagePosY] = pList[pPos] - 10
    if pList[pLanded]: #if the wave is sliding on a platform rest the image
        pList[pImage] = iconList[pList[pImageIndex]]
        pList[pImagePosY] = pList[pPos]
        
def jump(pList,Vy,iconList): #this is used for the jumping of the cube
    global ballOrb
    if Vy == 0: #so that we will not get a 0/0
        Vy = 1
    dist = abs(Vy)
    direct = Vy//dist
    for i in range(dist): #checks one pixel ahead for collision
        check = Rect(pList[pPosX],pList[pPos]+direct,pList[pSize],pList[pSize])
        center = check.center
        if check.collidelist(platforms[:platforms.index(0)]) == -1:
            pList[pPos] += direct
            pList[pImage] = transform.rotate(iconList[pList[pImageIndex]],-pList[pAng]*180//165) #how much the cube rotates
            offcenter = pList[pImage].get_rect().center # the following code until else is all to reset the center of the image with the hit box, offcenter gets the rect of the image
            dx = 30 - offcenter[0] #gets the x displacement of the image by subtracting the position of the image rect and the hitbox rect
            dy = 30 - offcenter[1] #gets the y displacement of the image
            pList[pImagePosX] = pList[pPosX] + dx
            pList[pImagePosY] = pList[pPos] + dy
            pList[pAng] += 1 #keeps track of how much rotation is done
        else:
            pList[pLanded] = True #resets everything to default
            pList[pAction] = False
            pList[pVely] = 0
            pList[pImage] = iconList[pList[pImageIndex]]
            pList[pImagePosX] = pList[pPosX]
            pList[pImagePosY] = pList[pPos]
            pList[pAng] = 0
            ballOrb = False
            
def spinBall(pList,iconList): #spins the ball images
    global rotateCount
    if pList[pClickCount]%2 != 0: #ball will spin different directions when under different gravities
        pList[pImage] = transform.rotate(iconList[pList[pImageIndex]],-rotateCount*7)
    else:
        pList[pImage] = transform.rotate(iconList[pList[pImageIndex]],rotateCount*7)
    center = Rect(pList[pPosX],pList[pPos],pList[pSize],pList[pSize]).center #centers the image and hitbox
    offcenter = pList[pImage].get_rect().center
    dx = 30 - offcenter[0]
    dy = 30 - offcenter[1]
    pList[pImagePosX] = pList[pPosX] + dx
    rotateCount -= 1 #keeps track of rotation
    return dy

def rotateShip(pList,iconList): #used for rotating image of ship uses same logic as the other image rotations
    pList[pImage] = transform.rotate(iconList[pList[pImageIndex]],-pList[pRship])
    center = Rect(pList[pPosX],pList[pPos],pList[pSize],int(pList[pSize]/1.875))
    offcenter = pList[pImage].get_rect().center
    dx = 113//2 - offcenter[0]
    dy = int(113/1.875)//2 - offcenter[1]
    pList[pImagePosX] = pList[pPosX] + dx
    return dy

def playerRect(pList): #gets the rect for the different modes
    if pList[pMode] == "cube":
        return Rect(pList[pPosX],pList[pPos],60,60)
    if pList[pMode] == "ship":
        return Rect(pList[pPosX],pList[pPos],113,60)
    if pList[pMode] == "wave":
        return Rect(pList[pPosX],pList[pPos],60,49)
    if pList[pMode] == "ball":
        return Rect(pList[pPosX],pList[pPos],60,60)
    
def portals(cPort,sPort,bPort,wPort,pList): #changes the player mode when the player collides with a respective portal 
    if playerRect(pList).collidelist(cPort[:cPort.index(0)]) != -1: #changes mode to cube
        if pList[pMode] == "wave":
            pList[pPos] -= 12 #wave has different dimensions than the others
        if pList[pMode] == "ship":
            pList[pPosX] += 53 #ship also has different dimensions than others
        pList[pAction] = False #stops doing the previous modes action
        pList[pVely] = 0
        pList[pMode] = "cube"
    if playerRect(pList).collidelist(sPort[:sPort.index(0)]) != -1:#changes mode to ship
        if pList[pMode] == "wave":
            pList[pPos] -= 12
        pList[pAction] = False
        pList[pVely] = 0
        pList[pMode] = "ship"
    if playerRect(pList).collidelist(bPort[:bPort.index(0)]) != -1:#changes mode to ball
        if pList[pMode] == "wave":
            pList[pPos] -= 12
        pList[pMode] = "ball"
    if playerRect(pList).collidelist(wPort[:wPort.index(0)]) != -1:#changes mode to wave
        if pList[pMode] == "ship":
            pList[pPosX] += 53
        pList[pMode] = "wave"

def autoJump(pList,jumpPads,jumpPadValues,viJump,gJump): #this is how all the modes move when they hit a jump pad
    global changeWave
    if playerRect(pList).collidelist(jumpPads[:jumpPads.index(0)]) != -1:
        if pList[pMode] == "ship":
            pList[pVely] = int(0.75*viJump*jumpPadValues[playerRect(pList).collidelist(jumpPads[:jumpPads.index(0)])]) #will launch the player up
        if pList[pMode] == "cube":
            pList[pLanded] = False
            pList[pVely] = int(1.5*viJump*jumpPadValues[playerRect(pList).collidelist(jumpPads[:jumpPads.index(0)])])-1

def jumpRing(pList,jumpOrbs,jumpOrbValues,viJump,gJump,mb): #used to move player when they jump on a jump orb
    global ballOrb
    global mouseHold #used to keep track of if the mouse is being held
    if not mouseHold: #the jump orb will only let you jump on it if you are not holding down your mouse, you must let go and reclick
        if playerRect(pList).collidelist(jumpOrbs[:jumpOrbs.index(0)]) != -1 and mb[0] == 1:
            if pList[pMode] == "ship": #same as autoJump but with different values
                pList[pVely] = int(0.7*viJump*jumpOrbValues[playerRect(pList).collidelist(jumpOrbs[:jumpOrbs.index(0)])])
                print(playerRect(pList).collidelist(jumpPads[:jumpPads.index(0)]))
            if pList[pMode] == "cube":
                pList[pAction] = True
                pList[pVely] = int(1.2*viJump*jumpOrbValues[playerRect(pList).collidelist(jumpOrbs[:jumpOrbs.index(0)])])
            if pList[pMode] == "ball":
                pList[pLanded] = True
                ballOrb = True #will make the ball jump like the cube
            mouseHold = True #once mouse is pressed mouseHold will be true until the event loop detects a mousebuttonup
            

def speed(pList,speedRects,speedValues): #changes the velocity x of the game when you collide with these speed changers
    if playerRect(pList).collidelist(speedRects) != -1:
        pList[pVelx] = -10*speedValues[playerRect(pList).collidelist(speedRects)]
        
def lose(pList): #checks to see if the player has lost
    check = Rect(pList[pPosX],pList[pPos],pList[pSize],pList[pSize])
    if pList[pMode] == "ship":
        check = Rect(pList[pPosX],pList[pPos],pList[pSize],int(pList[pSize]/1.875))
    if pList[pMode] == "wave":
        check = Rect(pList[pPosX],pList[pPos],pList[pSize],int(pList[pSize]/1.23))
    if check.collidelist(walls[:walls.index(0)]) == -1: #checks collision with walls, which includes everything the player cannot touch
        return False
    else:
        deathSFX.play() #plays sound effect if player loses
        mixer.music.stop() #stops the music
        pList[pVelx] = 0 #stops the movement of the player
        pList[pVely] = 0 #stops the movement of the map
        return True
def changeColour(colourList): #changes the background colour gradually
    colourList[4]+=1
    if colourList[4]%3 == 0: #makes it so that the colour changes slower
        if colourList[3]:
            if colourList[0] < 250: #increases each rgb by 1 until they are all 250
                colourList[0]+=1
            elif colourList[1] < 250:
                colourList[1]+=1
            elif colourList[2] < 250:
                colourList[2]+=1
            else:
                colourList[3] = False
        else:
            if colourList[0] > 10: #decreases each rgb by 1 until they are all 10
                colourList[0]-=1
            elif colourList[1] > 10:
                colourList[1]-=1
            elif colourList[2] > 10:
                colourList[2]-=1
            else:
                colourList[3] = True

def groundImagePos(groundPos): #determines the position of the ground images, the position of the ground images loops
    if groundPos[0] < 1400:
        groundPos[0] += 10
    else:
        groundPos[0] = 0    
    
def drawScene(screen,pList,offset): #draws everything
    if not lose(pInfo):
        if backgroundColour[4]%2 == 0: #draws every other frame so that game doesn't lag
            screen.fill((backgroundColour[0],backgroundColour[1],backgroundColour[2]))            
            screen.blit(backgroundImages[0],(0,0))
            screen.blit(pList[pImage],(pList[pImagePosX],pList[pImagePosY]))
            for i in range(len(spikePos[:spikePos.index(0)])):
                screen.blit(spikes[spikeType[i]-1],(spikePos[i][0]-offset,spikePos[i][1]))
            screen.blit(groundImages[0],(-groundPos[0],600))
            for i in range(len(jumpPads)):
                if jumpPads[i] == 0:
                    break
                if jumpPadValues[i] == 1:
                    colour = (255,255,0)
                else:
                    colour = (212,0,255)
                draw.rect(screen,colour,jumpPads[i])
            for i in range(len(jumpOrbs)):
                if jumpOrbs[i] == 0:
                    break
                if jumpOrbValues[i] == 1:
                    colour = (255,255,0)
                else:
                    colour = (212,0,255)
                draw.rect(screen,colour,jumpOrbs[i])
            screen.blit(pauseButton,(1180,0))
    else: #however if the player loses must draw every frame for the death animation
        screen.fill((backgroundColour[0],backgroundColour[1],backgroundColour[2]))        
        screen.blit(backgroundImages[0],(0,0))
        for i in range(len(spikePos[:spikePos.index(0)])):
            screen.blit(spikes[spikeType[i]-1],(spikePos[i][0]-offset,spikePos[i][1]))
        screen.blit(groundImages[0],(-groundPos[0],600))
        for i in range(len(jumpPads)):
            if jumpPads[i] == 0:
                break
            if jumpPadValues[i] == 1:
                colour = (255,255,0)
            else:
                colour = (212,0,255)
            draw.rect(screen,colour,jumpPads[i])  
        for i in range(len(jumpOrbs)):
            if jumpOrbs[i] == 0:
                break
            if jumpOrbValues[i] == 1:
                colour = (255,255,0)
            else:
                colour = (212,0,255)
            draw.rect(screen,(255,255,0),jumpOrbs[i])
        screen.blit(pauseButton,(1180,0))
        screen.blit(explosionImages[count],(pList[pImagePosX]-25,pList[pImagePosY]-30))
    display.flip()

def readFile(fileList,maxNum): #organizes data that was read from a txt file, adds everyline into a list as a Rect object
    newList = [] #makes a list
    for entry in fileList:
        tempList = entry.strip().split()
        for i in range(len(tempList[:4])):
            tempList[i] = int(tempList[i]) #converts every values to integer
        newList.append(Rect(tempList[:4])) #makes it into a Rect and adds it to the list
    for i in range(maxNum - len(newList)): #adds 0's until the list is at the right size
        newList.append(0)
    return newList

def getSpike(Filelist,numSpikes): #same as above funtion but saves the first two entries of each line as a tuple and the last as a single value to a different list
    newList = []
    newlst = []
    for entry in Filelist:
        tempList = entry.strip().split()
        for i in range(len(tempList)):
            tempList[i] = int(tempList[i])
        newList.append((tempList[0],tempList[1]))
        newlst.append(tempList[2])
    for i in range(numSpikes - len(newList)):
        newList.append(0)
        newlst.append(0)
    return newList,newlst

def menu():#
    running = True
    myClock = time.Clock()
    
    global menuImages1,menuImages2,musicVol,sfxVol,previousPage#variables that are defined globally
    buttons = [Rect(553,412,164,164),Rect(241,412,170,170),Rect(853,412,170,170),Rect(565,750,150,50)]#these are all the positions of the buttons that are going to be used in this menu. Each button in this list brings you to a different page
    values = ["levels","stats","info","credit"]#these values correspond to each rect above. once the button is presses it returns the corresponding value which then brings you to the right page
    
    if previousPage!= "levels" and previousPage!= "credit" and previousPage!= "info" and previousPage!= "stats":#all the "previous pages" mentioned here are pages that don't have any music specifically for them so when visiting those pages the music continues to play.
        #additionally when returning from those pages to the main menu you don't want the music to restart so, it only plays the music from the beggining when the previous page has a different song playing.
        mixer.music.load("songs/menu.mp3")#loads themenu songs
        mixer.music.set_volume(musicVol)#uses global music variable
        mixer.music.play(-1)#this ensures the song loops
    buttonSFX.set_volume(sfxVol)#uses global volume variable
    

    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "exit"

        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        
        screen.blit(menuBG,(0,0))
        screen.blit(Title,(100,150))
        for i in range(len(buttons)):#this loop is to utilize the list with all the button variables
            screen.blit(menuImages1[i],(buttons[i][0],buttons[i][1]))#blits all of them
            if buttons[i].collidepoint(mpos):
                screen.blit(menuImages2[i],(buttons[i][0]-4,buttons[i][1]-4))#blits the larger image on top to give user feedback that they can click the button
                if mb[0]==1:
                    buttonSFX.play()
                    time.wait(100)
                    previousPage="menu" #if the player were to choose to go view the levels the song wouldn't play again
                    return values[i]#returns the value that corresponds with the rect the player clicked on
        display.flip()
        
def info():# this screen teaches the player how to play
    running = True
    myClock = time.Clock()
    global menuImages
    global helpImagesa
    global helpImagesb
    global previousPage
    previousPage="info"#sets the previous page variable so music doesn't loop
    index=0#this index is used as the list index
    buttonClose=Rect(187,74,83,95)#this button makes the player return to the main menu
    arrowPos=[Rect(225,440,75,150),Rect(1005,440,75,150)]#list of the buttons used view each picture
    menuPos1=[(541,400),(241,410),(855,410)]#positions corresponding to the menu images in the back because this page doesn't cover the full screen
    for i in range(len(menuPos1)):#blits the main menu buttons
        screen.blit(menuImages1[i],menuPos1[i])
    screen.blit(Title,(100,150))
    
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "exit"
        screen.blit(menuBG,(0,0))    
        index=index%3#modulus so when the index exceeds 3 it goes back to 0
        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        screen.blit(helpImages[index],(190,75))#blits the slkide corresponding to the index
        for i in range(2):#this loop is to blit and check each button Rect
            screen.blit(helpImagesa[i],(arrowPos[i][0],arrowPos[i][1]))
            if arrowPos[i].collidepoint(mpos):
                screen.blit(helpImagesb[i],(arrowPos[i][0]-4,arrowPos[i][1]-4))
        if mb[0]==1 and arrowPos[0].collidepoint(mpos):#if the player clicks on the arrow on the left you subtract from the index by one to play the image on the left of the current one
            index-=1
            time.wait(100)
        if mb[0]==1 and arrowPos[1].collidepoint(mpos):#same thing as the one above however it adds to the index and it shows the picture on the right
            index+=1
            time.wait(100)
        if buttonClose.collidepoint(mpos):#exiting this menu
            screen.blit(closeButton,(183,70))
            if mb[0]==1:
                buttonSFX.play()
                return "menu"        
        display.flip()
        
def credit():#page giving credit to the creators
    global previousPage#setting previous page variable so music does not replay when returning to the menu
    previousPage="credit"
    running = True
    myClock = time.Clock()
    statsBG=transform.smoothscale(image.load("images/statsPage.png"),(1280,800))#loading the image for this page and adjusting to the right dimensions so it fills the page
    exitButtonRect=Rect(4,4,124,142)
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "exit"
        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        screen.blit(statsBG,(0,0))
        screen.blit(exitButton1,(4,4))
        if exitButtonRect.collidepoint(mpos):#when colliding with the exit button it blits the larger one
            screen.blit(exitButton2,(0,0))
            if mb[0]==1:#brings you back to the main menu if clicked
                buttonSFX.play()
                return "menu"           
        display.flip()
    return "credit"

def stats():
    global previousPage, levelsCompleted,totalAttempts,totalDeaths#setting previous page variable so music does not replay when returning to the menu
    stats=[levelsCompleted,totalAttempts,totalDeaths]#Puts the values that are going to be presented into the list
    digitPosY=[-540,-410,-290]#these are the coordinates that are going to changes so it appears the numbers drop with the statcard
    oneDigit=[(620,270),(620,400),(620,510)]#coordinates for blit if it is 1 digit
    twoDigits=[(600,270),(600,400),(600,510)]#coordinate for first digit if it is 2 digits long
    twoDigitsb=[(640,270),(640,400),(640,510)]#coordinate for second digit if it is 2 digits long
    previousPage="stats"
    running = True
    myClock = time.Clock()
    exitButtonRect=Rect(4,4,124,142)
    statscardPosY=-691#the stat cards y position when initially blit
    displacement=0
    statsCard=image.load("images/statsCard.png")
    digits=0#they are temporary variables used to store the sperated digits
    digits1=0
    digits2=0
    #using the numbers list as a keyboard and it's index lines up with the numbers
    
    while running:
        for evnt in event.get():        
            if evnt.type == QUIT:
                return "exit"
        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        screen.blit(menuBG,(0,0))
        screen.blit(exitButton1,(4,4))
        if displacement<800:#using the same method as mvoeRIght and left however vertically and one time use
            for i in range(len(digitPosY)):
                digitPosY[i]+=40
                oneDigit[i]=(620,digitPosY[i])#applying the changed y coordinate to the coordinate list
                twoDigits[i]=(600,digitPosY[i])
                twoDigitsb[i]=(640,digitPosY[i])
            statscardPosY+=40
            displacement+=40
        screen.blit(statsCard,(247,statscardPosY))
        for i in range(len(stats)):
            if len(str(stats[i]))==1:
                    screen.blit(numbers[stats[i]],(oneDigit[i]))
            if len(str(stats[i]))==2:#converting the int into a string and then splicing it
                digits=str(stats[i])
                digits1=int(digits[0])
                digits2=int(digits[1])
                screen.blit(numbers[digits1],(twoDigits[i]))
                screen.blit(numbers[digits1],(twoDigitsb[i]))
                            
                
            
        if exitButtonRect.collidepoint(mpos):#when colliding with the exit button it blits the larger one
            screen.blit(exitButton2,(0,0))
            if mb[0]==1:#brings you back to the main menu if clicked
                buttonSFX.play()
                return "menu"           
        display.flip()
        
def levels():
    moveRight=False#flags for when the level images move to the left or right
    moveLeft=False
    running = True
    index=0
    displacement=0#how much the level moves
    global menuImages1,menuImages2,sfxVol,previousPage#imports variables defined in the variable list below
    buttonSFX.set_volume(sfxVol)#sfx level
    movebuttons1=[Rect(290,300,700,200),Rect(1570,300,700,200),Rect(2850,300,700,200)]#rect objects for each level button
    exitButton=Rect(0,0,124,142)#rect object for the exit button
    values = ["level1","level2","level3"]#corresponding values to the level buttons to bring you to the right level when clicking on one
    arrow1=Rect(1080,290,107,220)#rect for arrows both sides
    arrow2=Rect(93,290,107,200)#^
    if previousPage!="menu":#makes it so music doesn't replay
        mixer.music.load("songs/menu.mp3")#
        mixer.music.set_volume(musicVol)#
        mixer.music.play(-1)#
        
    while running:
        for evnt in event.get():      
            if evnt.type == QUIT:
                return "exit"
        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        index=index%3#allows to loops through the 3 level
        #blitting the stagnant images
        screen.fill((50,150,50))
        screen.blit(levelTop,(140,0))
        screen.blit(levelCorners1,(0,527))
        screen.blit(levelCorners2,(1004,527))
        #LEVELS sliding left and right
        if moveRight and displacement>-1280:#when the move right flag is true it will displace the titles to the right until it has moved one full page to the right so the previous menu is out of the screen. thus revealing the the title on the left
            for i in range(len(movebuttons1)):#this loop allows me to apply the transform command to all three level buttons
                movebuttons1[i]=movebuttons1[i].move(80,0)#
            displacement-=80#keeps subtracting the same number as the number of pixels moved per loop until it reaches -1280
        elif displacement==-1280:#once the title has fuilly moved 1280 pixels it resets the displacement
            index-=1
            moveRight=False#stops the movement
            displacement=0
        if moveLeft and displacement<1280:#same thing as move right but now to the left
            for i in range(len(movebuttons1)):
                movebuttons1[i]=movebuttons1[i].move(-80,0)
            displacement+=80        
        elif displacement==1280:
            index+=1
            moveLeft=False
            displacement=0
        #these loops blits each button, check for collision and plays SFX when clicked 
        for i in range(len(movebuttons1)):
            if movebuttons1[i][0]<-910:#
                movebuttons1[i]=Rect(2850,300,700,200)#
            if movebuttons1[i][0]>2850:#
                movebuttons1[i]=Rect(-910,300,700,200)#
            screen.blit(levelImages1[i],(movebuttons1[i][0],movebuttons1[i][1]))
            if movebuttons1[i].collidepoint(mpos):
                screen.blit(levelImages2[i],(movebuttons1[i][0]-4,movebuttons1[i][1]-4))
                if mb[0]==1 and displacement==0:#
                    buttonSFX.play()
                    return values[i]
        #blitting the arrows above the level images-> blitting the arrows here make it appear that the level buttons slide behind them
        screen.blit(levelArrows2,(93,290))
        screen.blit(levelArrows1,(1080,290))    
        if arrow1.collidepoint(mpos):
            screen.blit(levelArrows1b,(1076,286))
            if mb[0]==1:
                moveLeft=True#sets the flag to true to begin moving
        
        if arrow2.collidepoint(mpos):
            screen.blit(levelArrows2b,(89,286))
            if mb[0]==1:
                moveRight=True#sets the flag to be true to begin moving
        screen.blit(exitButton1,(exitButton[0],exitButton[1]))
        if exitButton.collidepoint(mpos):
            screen.blit(exitButton2,(exitButton[0]-4,exitButton[1]-4))
            if mb[0]==1:
                buttonSFX.play()
                previousPage="levels"
                return "menu"            
        display.flip()
        
def pause():#when this is called within the level loops, so it the level loop stops running until this loop is broken out of
    paused=True#initially sets the condition the loop
    slider=False
    global previousValue,pauseIndex,musicVol,musicSliderRect,sfxVol,sfxSliderRect#variables defined in the variable section
    running = True
    screen.blit(pauseBG,(0,0))#blits transparent image to make background darken
    pauseMenu=screen.copy()#screen shots where the level stops at
    mixer.music.pause()#pauses level music
    posButton=[Rect(565,450,150,150),Rect(885,450,150,150),Rect(170,450,150,150)]#button Rects
    pauseValues=[False,"levels","quit"]#values corresponding to Rects
    screen.blit(pauseBG,(0,0))
    while paused:#when pause is false then the pause function will stop looping
        for evnt in event.get():      
            if evnt.type == QUIT:
                quit()
        buttonSFX.set_volume(sfxVol)
        screen.blit(pauseMenu,(0,0))
        screen.blit(musicSlider,(226,620))
        screen.blit(sfxSlider,(646,620))
        (mx,my) = mouse.get_pos()
        mb = mouse.get_pressed()
        draw.ellipse(screen,(255,255,255),musicSliderRect)#the button within the slider
        draw.ellipse(screen,(255,255,255),sfxSliderRect)
        if musicSliderRect.collidepoint(mx,my) and mb[0]==1:#checks for collision
            if mx<=616 and mx>=226 and my<=693 and my>=653:#this sets the condition that the button within the slider can only move up to certain points so it doens't go off the slider
                musicSliderRect=Rect(mx-15,656,30,30)#only changing the x coordinate
                musicVol=round((((mx-15)-217)/400),1)#since the volume is from 0-1.0 it subtracts the difference between where my mouse is and the beggining of the slider and divides by 400 giving a value between 0 and 1.0
        if sfxSliderRect.collidepoint(mx,my) and mb[0]==1:#samething but for the sfxSlide
            if mx<=1041 and mx>=646 and my<=693 and my>=653:
                sfxSliderRect=Rect(mx-15,656,30,30)
                sfxVol=round((((mx-15)-637)/400),1)           
        draw.ellipse(screen,(255,255,255),musicSliderRect)        
        for i in range(len(pauseImages1)):#drawing,checking for collision for the pause buttons, and returning corresponding values to bring you to the designated page you clicked on
            screen.blit(pauseImages1[i],(posButton[i][0],posButton[i][1]))
            if posButton[i].collidepoint(mx,my):
                screen.blit(pauseImages2[i],(posButton[i][0]-4,posButton[i][1]-4))
                if mb[0]==1:
                    buttonSFX.play()
                    pauseIndex=i #so it will keep track of which button was pressed
                    paused=False#stops the pause
        if posButton[0].collidepoint(mx,my) and mb[0]==1:
            buttonSFX.play()
            mixer.music.unpause()
            paused=False#this resumes your level
        display.flip()
        
def win():
    #vars
    global previousPage,levelsCompleted
    levelsCompleted += 1 #adds a win to be recorded for the stats page
    running=True
    myClock = time.Clock()
    winImages1=[]#list of regular sized buttons
    winImages2=[]#list of larger verson of the buttons
    winImagePos=[Rect(312,-411,100,100),Rect(869,-411,100,100)]#rects of all the buttons
    winValues=["","levels"]
    endcardPosY=-691#only moving the y coordinate
    displacement=0#like the moveRight and moveLeft checks displacement
    #loading images
    endCard=image.load("images/endcard.png")
    replayButton=image.load("images/replay.png")
    replayButton1=transform.smoothscale(replayButton,(100,100))
    replayButton2=transform.smoothscale(replayButton,(108,108))
    returnlevels=image.load("images/levelmenuButton.png")
    returnlevels1=transform.smoothscale(returnlevels,(100,100))
    returnlevels2=transform.smoothscale(returnlevels,(108,108))
    
    #adding to a list
    winImages1.append(replayButton1)
    winImages2.append(replayButton2)
    winImages1.append(returnlevels1)
    winImages2.append(returnlevels2)
    #blitting stagnant ones and screenshotting
    screen.blit(pauseBG,(0,0))
    screen.blit(pauseBG,(0,0))
    winBg=screen.copy()#screenshots where you left off with darkened background just like pause()
    screen.blit(winBg,(0,0))
    screen.blit(endCard,(247,109))#
    winSFX1.play()#
    winSFX2.play()#
    endCard=image.load("images/endcard.png")
    replayButton=image.load("images/replay.png")
    replayButton1=transform.smoothscale(replayButton,(100,100))
    replayButton2=transform.smoothscale(replayButton,(108,108))
    mixer.Channel(0).play(winSFX1)
    mixer.Channel(1).play(winSFX2)
    while running:
        for evnt in event.get():      
            if evnt.type == QUIT:
                return "exit"
            
        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        if displacement<800:
            winImagePos[0]=winImagePos[0].move(0,40)#slides the images down by adding to their y value
            winImagePos[1]=winImagePos[1].move(0,40)
            endcardPosY+=40
            displacement+=40
        screen.blit(winBg,(0,0))
        screen.blit(endCard,(247,endcardPosY))
        for i in range(len(winImages1)):#blits buttons,checks for collisiona and returns designated value if clicked on
            screen.blit(winImages1[i],(winImagePos[i][0],winImagePos[i][1]))
            if winImagePos[i].collidepoint(mpos):
                screen.blit(winImages2[i],(winImagePos[i][0]-4,winImagePos[i][1]-4))
        if mb[0]==1 and winImagePos[0].collidepoint(mpos):
            buttonSFX.play()
            return previousPage
        if mb[0]==1 and winImagePos[1].collidepoint(mpos):
            buttonSFX.play()
            time.wait(100)
            mixer.music.stop()
            return "levels"
        display.flip()
    return "win"

def level1(): #this is the level 1 function
    global count,pauseIndex,musicVol,sfxVol,previousPage,ballOrb,totalAttempts,totalDeaths
    totalAttempts += 1 #adds an attempt to be recorded for the stats page
    previousPage = "level1" #sets the current page to previous page
    for i in range(len(pInfo)): #changes the player information to the level 1 player info
        pInfo[i] = pInfo1[i]
    pauseRect=Rect(1180,0,100,100)
    pauseValues=[False,"levels","quit"]
    mixer.music.load("songs/lvl1.mp3") #loads and plays the music for level 1
    mixer.music.set_volume(0.5)
    mixer.music.play()
    for i in range(len(lvl1platforms)): #changes the information of all the default lists into the level 1 info
        platforms[i] = lvl1platforms[i]
    for i in range(len(lvl1walls)):
        walls[i] = lvl1walls[i]
    for i in range(len(lvl1cubePortals)):
        cubePortals[i] = lvl1cubePortals[i]
    for i in range(len(lvl1shipPortals)):
        shipPortals[i] = lvl1shipPortals[i]
    for i in range(len(lvl1ballPortals)):
        ballPortals[i] = lvl1ballPortals[i]
    for i in range(len(lvl1wavePortals)):
        wavePortals[i] = lvl1wavePortals[i]
    for i in range(len(lvl1jumpPads)):
        jumpPads[i] = lvl1jumpPads[i]
        jumpPadValues[i] = lvl1jumpPadValues[i]
    for i in range(len(lvl1jumpOrbs)):
        jumpOrbs[i] = lvl1jumpOrbs[i]
        jumpOrbValues[i] = lvl1jumpOrbValues[i]
    for i in range(len(backgroundColour)):
        backgroundColour[i] = backgroundColour1[i]
    for i in range(len(spikePos)):
        spikePos[i] = lvl1spikePos[i]
        spikeType[i] = lvl1spikeType[i]
    time.wait(100)
    offset = 0 #keeps track of how far the map has moved so we know where to blit the images
    while running(pInfo):
        if offset>31960: #if the player reaches this point it means they have won
            break
        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        mixer.music.set_volume(musicVol) #this is so that the player can control the music loudness within the game, they can change it when they pause
        deathSFX.set_volume(sfxVol) #same as music, sound effects also have a volume control
        if lose(pInfo):
            mixer.music.play()
        changeColour(backgroundColour) #changes the colour of background
        moveMap(pInfo,level) #moves the map
        if not pInfo[pLost]: #only do these if we haven't lost yet, makes sure that all images stop moving after the player loses
            movePlayer(pInfo,gJump,viJump,iconImages)
            groundImagePos(groundPos)
            offset+=10
        portals(cubePortals,shipPortals,ballPortals,wavePortals,pInfo) #checks for portal collision and performs mode changes
        jumpRing(pInfo,jumpOrbs,jumpOrbValues,viJump,gJump,mb) #checks for jump orb activations
        autoJump(pInfo,jumpPads,jumpPadValues,viJump,gJump) #checks for jump pad activations
        drawScene(screen,pInfo,offset) #draws everything
        if pauseRect.collidepoint(mpos) and mb[0]==1:#if the player clicks pause
            pause()#pauses the game
            if pauseIndex!=0:#
                return pauseValues[pauseIndex]#
        myClock.tick(60)
    if offset > 31960: #if they hit this point they will win
        previousPage = "level1"
        return "win"
    totalDeaths+=1
    return "level1" #if they didn't win they lost so returns level 1 again to auto restart

def level2(): #level 2 function is exact same as level1 but for level 2
    global count,pauseIndex,musicVol,sfxVol,previousPage,ballOrb,totalAttempts,totalDeaths
    totalAttempts+=1
    previousPage = "level2"
    for i in range(len(pInfo)):
        pInfo[i] = pInfo2[i]
    pauseRect=Rect(1180,0,100,100)#
    pauseValues=[False,"levels","quit"]
    mixer.music.load("songs/lvl2.mp3")
    mixer.music.play()
    for i in range(len(lvl2platforms)):
        platforms[i] = lvl2platforms[i]
    for i in range(len(lvl2walls)):
        walls[i] = lvl2walls[i]
    for i in range(len(lvl2cubePortals)):
        cubePortals[i] = lvl2cubePortals[i]
    for i in range(len(lvl2shipPortals)):
        shipPortals[i] = lvl2shipPortals[i]
    for i in range(len(lvl2ballPortals)):
        ballPortals[i] = lvl2ballPortals[i]
    for i in range(len(lvl2wavePortals)):
        wavePortals[i] = lvl2wavePortals[i]
    for i in range(len(lvl2jumpPads)):
        jumpPads[i] = lvl2jumpPads[i]
        jumpPadValues[i] = lvl2jumpPadValues[i]
    for i in range(len(lvl2jumpOrbs)):
        jumpOrbs[i] = lvl2jumpOrbs[i]
        jumpOrbValues[i] = lvl2jumpOrbValues[i]
    for i in range(len(spikePos)):
        spikePos[i] = lvl2spikePos[i]
        spikeType[i] = lvl2spikeType[i]
    time.wait(100)
    offset = 0
    while running(pInfo):
        if offset>22000:
            break
        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        mixer.music.set_volume(musicVol)#
        deathSFX.set_volume(sfxVol)
        if lose(pInfo):
            mixer.music.play()
        changeColour(backgroundColour)
        moveMap(pInfo,level)
        if not pInfo[pLost]:
            movePlayer(pInfo,gJump,viJump,iconImages)
            groundImagePos(groundPos)
            offset+=10
        portals(cubePortals,shipPortals,ballPortals,wavePortals,pInfo)
        jumpRing(pInfo,jumpOrbs,jumpOrbValues,viJump,gJump,mb)
        autoJump(pInfo,jumpPads,jumpPadValues,viJump,gJump)
        drawScene(screen,pInfo,offset)
        if pauseRect.collidepoint(mpos) and mb[0]==1:
            pause()
            if pauseIndex!=0:
                return pauseValues[pauseIndex]    
        myClock.tick(60)
    if offset>22000:
        previousPage = "level2"
        return "win"
    totalDeaths+=1
    return "level2"

def level3(): #level 3 function is exact same as level1 and level2
    global count,pauseIndex,musicVol,sfxVol,previousPage,ballOrb,totalAttempts,totalDeaths
    totalAttempts += 1
    previousPage = "level3"
    for i in range(len(pInfo)):
        pInfo[i] = pInfo3[i]
    pauseRect=Rect(1180,0,100,100)
    pauseValues=[False,"levels","quit"]
    mixer.music.load("songs/lvl3.mp3")
    mixer.music.play()
    for i in range(len(lvl3platforms)):
        platforms[i] = lvl3platforms[i]
    for i in range(len(lvl3walls)):
        walls[i] = lvl3walls[i]
    for i in range(len(lvl3cubePortals)):
        cubePortals[i] = lvl3cubePortals[i]
    for i in range(len(lvl3shipPortals)):
        shipPortals[i] = lvl3shipPortals[i]
    for i in range(len(lvl3ballPortals)):
        ballPortals[i] = lvl3ballPortals[i]
    for i in range(len(lvl3wavePortals)):
        wavePortals[i] = lvl3wavePortals[i]
    for i in range(len(lvl3jumpPads)):
        jumpPads[i] = lvl3jumpPads[i]
        jumpPadValues[i] = lvl3jumpPadValues[i]
    for i in range(len(lvl3jumpOrbs)):
        jumpOrbs[i] = lvl3jumpOrbs[i]
        jumpOrbValues[i] = lvl3jumpOrbValues[i]
    for i in range(len(spikePos)):
        spikePos[i] = lvl3spikePos[i]
        spikeType[i] = lvl3spikeType[i]
    time.wait(100)
    offset = 0
    while running(pInfo):
        if offset>12600:
            break
        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        mixer.music.set_volume(musicVol)
        deathSFX.set_volume(sfxVol)
        if lose(pInfo):
            mixer.music.play()
        changeColour(backgroundColour)
        moveMap(pInfo,level)
        if not pInfo[pLost]:
            movePlayer(pInfo,gJump,viJump,iconImages)
            groundImagePos(groundPos)
            offset+=10
        portals(cubePortals,shipPortals,ballPortals,wavePortals,pInfo)
        jumpRing(pInfo,jumpOrbs,jumpOrbValues,viJump,gJump,mb)
        autoJump(pInfo,jumpPads,jumpPadValues,viJump,gJump)
        drawScene(screen,pInfo,offset)
        if pauseRect.collidepoint(mpos) and mb[0]==1:
            pause()
            if pauseIndex!=0:
                return pauseValues[pauseIndex]    
        myClock.tick(61)
    if offset>12600:
        previousPage = "level3"
        return "win"
    totalDeaths+=1
    return "level3"
#-----------------------------
#screen
screenSize = screenWidth,screenHeight = 1280,800 #size of the screen
screen = display.set_mode(screenSize)
page = "menu" #first page shown is menu

#InGameImages
iconImages = ["cube1","ship1","ball1","wave1"] #stores the image of the player
loadImages(iconImages)

explosionImages = [] #stores the death animation sequence
for i in range(1,10):
    explosionImages.append("PE"+str(i))
    explosionImages.append("PE10")
loadImages(explosionImages)

backgroundImages = ["Background1"] #stores the background image
loadImages(backgroundImages)
for i in range(len(backgroundImages)):
    backgroundImages[i] = backgroundImages[i].convert_alpha()
    
groundImages = ["Ground1"] #stores the ground image
groundPos = [0]
loadImages(groundImages)
for i in range(len(groundImages)):
    groundImages[i] = groundImages[i].convert_alpha()

spikes = ["Spike1","Spike2","Spike3","Spike4","USpikes1","USpikes2","USpikes3",
          "USpikes4","cubePortal","shipPortal","wavePortal","ballPortal",
          "block1","endPortal","cubePortalBig"] #stores the images of spikes, and a few other items that appear on the map
loadImages(spikes)
for i in range(len(spikes)):
    spikes[i] = spikes[i].convert_alpha()

numbers=[] #stores the digits from 0-9 to be blitted onto the stats page
for i in range(0,10):
    numbers.append("S"+str(i))
loadImages(numbers)

#MenuImages
menuImages1=[]#regular sized buttons for the menu
menuImages2=[]#larger buttons that are larger by 8 pixels

menuBG=image.load("images/menuBG.jpg")
menuBG=transform.smoothscale(menuBG,(1280,800))

Title=image.load("images/Title.png")
Title=transform.smoothscale(Title,(1080,100))

playbutton1=image.load("images/playbutton.png")

playbutton1=transform.smoothscale(playbutton1,(188,188))
menuImages1.append(playbutton1)

playbutton2=transform.smoothscale(playbutton1,(196,196)) #everything here is loading images and adding to the above lists
menuImages2.append(playbutton2)

statsbutton1=image.load("images/stats.png")

statsbutton1=transform.smoothscale(statsbutton1,(170,170))
menuImages1.append(statsbutton1)

statsbutton2=transform.smoothscale(statsbutton1,(178,178))
menuImages2.append(statsbutton2)

infobutton1=image.load("images/info.png")

infobutton1=transform.smoothscale(infobutton1,(170,170))
menuImages1.append(infobutton1)

infobutton2=transform.smoothscale(infobutton1,(178,178))
menuImages2.append(infobutton2)

creditButton=image.load("images/credits.png")#
creditButton1=transform.smoothscale(creditButton,(150,50))#
menuImages1.append(creditButton1)#

creditButton2=transform.smoothscale(creditButton,(158,58))#
menuImages2.append(creditButton2)#

#level select menu
levelImages1=[]#smaller buttons for the level page
levelImages2=[]#larger buttons for the level page
levelTop=image.load("images/levelsTop.png")
levelTop=transform.smoothscale(levelTop,(1000,100))

levelCorners1=image.load("images/levelsCorner.png")

levelCorners2=transform.flip(levelCorners1,True,False)

levelArrows1=image.load("images/levelArrow.png")
levelArrows1b=transform.smoothscale(levelArrows1,(115,228))
                                     

levelArrows2=transform.flip(levelArrows1,True,False)
levelArrows2b=transform.flip(levelArrows1b,True,False)

lvl1menu1=image.load("images/menulvl1.png")
lvl1menu1=transform.smoothscale(lvl1menu1,(700,200))
levelImages1.append(lvl1menu1)

lvl1menu2=transform.smoothscale(lvl1menu1,(708,208)) #loading and adding to lists
levelImages2.append(lvl1menu2)

lvl2menu=image.load("images/menulvl2.png")
lvl2menu1=transform.smoothscale(lvl2menu,(700,200))
levelImages1.append(lvl2menu1)

lvl2menu2=transform.smoothscale(lvl2menu,(708,208))
levelImages2.append(lvl2menu2)

lvl3menu=image.load("images/menulvl3.png")
lvl3menu1=transform.smoothscale(lvl3menu,(700,200))
levelImages1.append(lvl3menu1)

lvl3menu2=transform.smoothscale(lvl3menu,(708,208))
levelImages2.append(lvl3menu2)

exitButton1=image.load("images/exitbutton.png")
exitButton2=transform.smoothscale(exitButton1,(132,150))

#Help Menu
helpImages=[]#help images slideshow pages
helpImagesa=[]#smaller buttons
helpImagesb=[]#larger buttons
for i in range(1,4):
    helpImages.append("Help"+str(i))
loadImages(helpImages)
helpArrow1=image.load("images/levelArrow.png")
helpArrow1=transform.smoothscale(helpArrow1,(75,150))
helpArrow2=helpArrow1
helpArrow2b=transform.smoothscale(helpArrow2,(83,150))
helpArrow1=transform.flip(helpArrow2,True,False)
                                 
helpArrow1b=transform.smoothscale(helpArrow1,(83,150))
helpImagesa.append(helpArrow1)
helpImagesb.append(helpArrow1b)
helpImagesa.append(helpArrow2)
helpImagesb.append(helpArrow2b)

closeButton=image.load("images/close.png")
closeButton=transform.smoothscale(closeButton,(91,103))

closeButton=image.load("images/close.png")
closeButton=transform.smoothscale(closeButton,(91,103))

#pause
pauseImages1=[]#small buttons for pause menu
pauseImages2=[]#large buttons for pause menu
pauseBG=image.load('images/pauseBg.png')
pauseButton=image.load("images/pauseButton.png")
pauseButton=transform.smoothscale(pauseButton,(100,100))

resumeButton=image.load("images/resumeButton.png")
resumeButton1=transform.smoothscale(resumeButton,(150,150))
pauseImages1.append(resumeButton1)
resumeButton2=transform.smoothscale(resumeButton1,(158,158))
pauseImages2.append(resumeButton2)

levelsButton=image.load("images/levelmenuButton.png")
levelsButton1=transform.smoothscale(levelsButton,(150,150))
pauseImages1.append(levelsButton1)                              #loading, scaling, and adding images to lists

levelButton2=transform.smoothscale(levelsButton,(158,158))
pauseImages2.append(levelButton2)

quitButton=image.load("images/quitButton.png")
quitButton1=transform.smoothscale(quitButton,(150,150))
pauseImages1.append(quitButton1)

quitButton2=transform.smoothscale(quitButton,(158,158))
pauseImages2.append(quitButton2)

musicSlider=image.load("images/musicSlider.png")

sfxSlider=image.load("images/sfxSlider.png")

#----------------------------------------

#sfx
sfxVol = 1#universal sfx volume for the music sliders
#loading all the sfx
deathSFX = mixer.Sound("sfx/death.wav")
deathSFX.set_volume(sfxVol)
buttonSFX = mixer.Sound("sfx/button.wav")
buttonSFX.set_volume(sfxVol)
winSFX1=mixer.Sound("sfx/winSFX1.wav")#
winSFX1.set_volume(sfxVol)#
winSFX2=mixer.Sound("sfx/winSFX2.wav")#
winSFX2.set_volume(sfxVol)#

#----------------------------------------

#stats
levelsCompletedFile = open("levelsCompleted.txt") #opens the file for each type of statistic and sets the statistic variable equal to it
levelsCompleted=int(levelsCompletedFile.readline().strip())
totalAttemptsFile = open("totalAttempts.txt")
totalAttempts=int(totalAttemptsFile.readline().strip())
totalDeathsFile = open("totalDeaths.txt")
totalDeaths=int(totalDeathsFile.readline().strip())



#Variables and Lists
#global variables
count = 0#used for the death animation to ensure correct number of loops
pauseIndex = 0#used to transfer the values from the pause function into the level functions
musicVol = 1
musicSliderRect=Rect(611,656,30,30)#rect for the music slider button
sfxSliderRect=Rect(1031,656,30,30)#rect for the sfx slider button
ballOrb = False #keeps track of when the ball hits a jump orb
mouseHold = False #keeps track of when the mouse is held
backgroundColour = [0,0,0,0,0]
previousPage = "menu"#used to check what the previous page is so correct measure can be taken for each function
#player
pMode = 0
pPos = 1
pVelx = 2
pVely = 3
pSize = 4
pLanded = 5
pAction = 6
pImage = 7
pImageIndex = 8
pAng = 9
pImagePosX = 10
pImagePosY = 11
pClickCount = 12
pRship = 13
pPosX = 14
pLost = 15
pInfo = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
gJump = 2 #gravity of cube
viJump = -23 #intial velocity of the cube when it jumps
rotateCount = 0 #used for keeping track of rotation of ball

numPlats = 250 #these are all the maximum number compared between all levels of each type of object
numWalls = 300
numCubePortals = 3
numShipPortals = 3
numBallPortals = 3
numWavePortals = 3
numJumpPads = 21
numJumpOrbs = 10
numSpikes = 402
#level1
backgroundColour1 = [255,105,180,True,0] #background colour of lvl1
pInfo1 = ["cube",540,-10,0,60,True,False,iconImages[2],0,1,450,640,0,0,450,False] #intial information of player for lvl1

lvl1platformFile = open("lvl1/lvl1platforms.txt").readlines() #reads and organizes level information in this case the platforms
lvl1platforms = readFile(lvl1platformFile,numPlats)

lvl1wallsFile = open("lvl1/lvl1walls.txt").readlines()
lvl1walls = readFile(lvl1wallsFile,numWalls)

lvl1cubePortalsFile = open("lvl1/lvl1cubePortals.txt").readlines()
lvl1cubePortals = readFile(lvl1cubePortalsFile,numCubePortals)

lvl1shipPortalsFile = open("lvl1/lvl1shipPortals.txt").readlines()
lvl1shipPortals = readFile(lvl1shipPortalsFile,numShipPortals)

lvl1jumpPadsFile = open("lvl1/lvl1jumpPads.txt").readlines()        #this is all reading and organizig level information
lvl1jumpPads = readFile(lvl1jumpPadsFile,numJumpPads)               #stores the info into the lvl1 lists
lvl1jumpPadValues = []
for jumpPad in lvl1jumpPadsFile:
    tempList = jumpPad.strip().split()
    jumpPadValue = float(tempList[-1])
    lvl1jumpPadValues.append(jumpPadValue)
for i in range(numJumpPads-len(lvl1jumpPadValues)):
    lvl1jumpPadValues.append(0)

lvl1jumpOrbsFile = open("lvl1/lvl1jumpOrbs.txt").readlines()
lvl1jumpOrbs = readFile(lvl1jumpOrbsFile,numJumpOrbs)
lvl1jumpOrbValues = []
for jumpOrb in lvl1jumpOrbsFile:
    tempList = jumpOrb.strip().split()
    jumpOrbValue = float(tempList[-1])
    lvl1jumpOrbValues.append(jumpOrbValue)
for i in range(numJumpOrbs-len(lvl1jumpOrbValues)):
    lvl1jumpOrbValues.append(0)

lvl1spikesFile = open("lvl1/lvl1spikePos.txt")
lvl1spikePos,lvl1spikeType = getSpike(lvl1spikesFile,numSpikes)

lvl1ballPortals = [0 for i in range(numBallPortals)]    #lvl1 doesn't have any of these object but the list is still needed 
lvl1wavePortals = [0 for i in range(numWavePortals)]    #to overwrite the other levels if level 1 were to be selected after playing another level

#level2
pInfo2 = ["cube",540,-10,0,60,True,False,iconImages[2],0,1,450,640,0,0,450,False] #initial info for level 2
#everything under here is same as level 1 but for level 2
lvl2platformFile = open("lvl2/lvl2platforms.txt").readlines()
lvl2platforms = readFile(lvl2platformFile,numPlats)

lvl2wallsFile = open("lvl2/lvl2walls.txt")
lvl2walls = readFile(lvl2wallsFile,numWalls)

lvl2cubePortalsFile = open("lvl2/lvl2cubePortals.txt").readlines()
lvl2cubePortals = readFile(lvl2cubePortalsFile,numCubePortals)

lvl2shipPortalsFile = open("lvl2/lvl2shipPortals.txt").readlines()
lvl2shipPortals = readFile(lvl2shipPortalsFile,numShipPortals)

lvl2ballPortalsFile = open("lvl2/lvl2ballPortals.txt").readlines()
lvl2ballPortals = readFile(lvl2ballPortalsFile,numBallPortals)

lvl2wavePortalsFile = open("lvl2/lvl2wavePortals.txt").readlines()
lvl2wavePortals = readFile(lvl2wavePortalsFile,numWavePortals)

lvl2jumpPadsFile = open("lvl2/lvl2jumpPads.txt").readlines()
lvl2jumpPads = readFile(lvl2jumpPadsFile,numJumpPads)
lvl2jumpPadValues = []
for jumpPad in lvl2jumpPadsFile:
    tempList = jumpPad.strip().split()
    jumpPadValue = float(tempList[-1])
    lvl2jumpPadValues.append(jumpPadValue)
for i in range(numJumpPads-len(lvl2jumpPadValues)):
    lvl2jumpPadValues.append(0)

lvl2jumpOrbsFile = open("lvl2/lvl2jumpOrbs.txt").readlines()
lvl2jumpOrbs = readFile(lvl2jumpOrbsFile,numJumpOrbs)
lvl2jumpOrbValues = []
for jumpOrb in lvl2jumpOrbsFile:
    tempList = jumpOrb.strip().split()
    jumpOrbValue = float(tempList[-1])
    lvl2jumpOrbValues.append(jumpOrbValue)
for i in range(numJumpOrbs-len(lvl2jumpOrbValues)):
    lvl2jumpOrbValues.append(0)

lvl2spikesFile = open("lvl2/lvl2spikePos.txt")
lvl2spikePos,lvl2spikeType = getSpike(lvl2spikesFile,numSpikes)

#level3
pInfo3 = ["cube",540,-10,0,60,True,False,iconImages[2],0,1,450,640,0,0,450,False] #initial info for level 3
#everything under here is same as level 1 and 2
lvl3platformFile = open("lvl3/lvl3platforms.txt").readlines()
lvl3platforms = readFile(lvl3platformFile,numPlats)

lvl3wallsFile = open("lvl3/lvl3walls.txt")
lvl3walls = readFile(lvl3wallsFile,numWalls)

lvl3cubePortalsFile = open("lvl3/lvl3cubePortals.txt").readlines()
lvl3cubePortals = readFile(lvl3cubePortalsFile,numCubePortals)

lvl3shipPortalsFile = open("lvl3/lvl3shipPortals.txt").readlines()
lvl3shipPortals = readFile(lvl3shipPortalsFile,numShipPortals)

lvl3ballPortalsFile = open("lvl3/lvl3ballPortals.txt").readlines()
lvl3ballPortals = readFile(lvl3ballPortalsFile,numBallPortals)

lvl3wavePortalsFile = open("lvl3/lvl3wavePortals.txt").readlines()
lvl3wavePortals = readFile(lvl3wavePortalsFile,numWavePortals)

lvl3jumpPadsFile = open("lvl3/lvl3jumpPads.txt").readlines()
lvl3jumpPads = readFile(lvl3jumpPadsFile,numJumpPads)
lvl3jumpPadValues = []
for jumpPad in lvl3jumpPadsFile:
    tempList = jumpPad.strip().split()
    jumpPadValue = float(tempList[-1])
    lvl3jumpPadValues.append(jumpPadValue)
for i in range(numJumpPads-len(lvl3jumpPadValues)):
    lvl3jumpPadValues.append(0)

lvl3jumpOrbsFile = open("lvl3/lvl3jumpOrbs.txt").readlines()
lvl3jumpOrbs = readFile(lvl3jumpOrbsFile,numJumpOrbs)
lvl3jumpOrbValues = []
for jumpOrb in lvl3jumpOrbsFile:
    tempList = jumpOrb.strip().split()
    jumpOrbValue = float(tempList[-1])
    lvl3jumpOrbValues.append(jumpOrbValue)
for i in range(numJumpOrbs-len(lvl3jumpOrbValues)):
    lvl3jumpOrbValues.append(0)

lvl3spikesFile = open("lvl3/lvl3spikePos.txt")
lvl3spikePos,lvl3spikeType = getSpike(lvl3spikesFile,numSpikes)  

#level lists
jumpPads = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #these are the lists that holds the level information for the level that is being played
jumpPadValues = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #all the functions use these lists and act on these lists
jumpOrbs = [0,0,0,0,0,0,0,0,0,0] #when a certain level is selected these 0's will be replaced by the rect objects for that level
jumpOrbValues = [0,0,0,0,0,0,0,0,0,0] #these 0's are just place holders to make the list the right size
cubePortals = [0,0,0]
wavePortals = [0,0,0]
shipPortals = [0,0,0]
ballPortals = [0,0,0]
spikePos = [0 for i in range(numSpikes)]
spikeType = [0 for i in range(numSpikes)]
platforms = [0 for i in range(numPlats)]
walls = [0 for i in range(numWalls)]
level = [platforms,walls,cubePortals,wavePortals,shipPortals,ballPortals,jumpPads,jumpOrbs] #stores every objectlist so that they can all be moved simultaneously

#miscellaneous
myClock = time.Clock()

#-----------------------------

#Main Game Loop
while page != "exit":
    if page == "menu": #displays the current page and runs the function for each page
        page = menu()
    if page == "stats":
        page = stats()
    if page == "info":
        page = info()
    if page == "levels":
        page = levels()
    if page == "level1":
        page = level1()
    if page == "level2":
        page = level2()
    if page == "quit":
        quit()
    if page == "win":
        page = win()
    if page == "credit":
        page = credit()
    if page == "level3":
        page = level3()
levelsCompletedFileOut = open("levelsCompleted.txt","w") #writes the stats as files, it will replace the old stats files
levelsCompletedFileOut.write(str(levelsCompleted))
levelsCompletedFileOut.close()
totalAttemptsFileOut = open("totalAttempts.txt","w")
totalAttemptsFileOut.write(str(totalAttempts))
totalAttemptsFileOut.close()
totalDeathsFileOut = open("totalDeaths.txt","w")
totalDeathsFileOut.write(str(totalDeaths))
totalDeathsFileOut.close()
quit()
    

    

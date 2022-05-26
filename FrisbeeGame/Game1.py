# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 17:52:38 2021

@author: Gabriel Rodriguez
"""

import pygame, sys, math
import numpy as np
import random as rd

def FrisbeeEulerFindX(veloIn,angle):
    

    #initial conditions
    angleI = angle #angle of inclination
    angleV = angle #initial angle of velocity
    velo = veloIn #initial velocity
    
    #Defining values
    TMAX = 30  # End time of simulation
    DT = 0.01   # Time step
    STEPS = int((TMAX/DT)) #Total number of time steps
    g = 9.8  # gravity
    mass = 0.175 #mass of frisbee in kg
    airD = 1.23 #air density in kg/m^3
    crsecF = math.pi * (0.135**2) #Area of cross section of frisbee in m^2


    #Defining arrays
    t = np.zeros(STEPS)  # Array with time values
    y = np.zeros(STEPS)  # Array with Y position
    x = np.zeros(STEPS)  # Array with X position
    vy = np.zeros(STEPS)  # Array with Y speed
    vx = np.zeros(STEPS)  # Array with X speed

    t[0] = 0
    y[0] = 0
    x[0] = 0
    vy[0] = velo*math.sin(math.radians(angleV))
    vx[0] = velo*math.cos(math.radians(angleV))

    #Drag and Lift coefficient functions
    def coefD(angA):
        return 0.085 + ( 3.30 * ((angA + 0.052)**2) )

    def coefL(angA):
        return 0.13 + (3.09 * angA)
    

    #Lift and drag functions
    def liftX(veloX, veloY):
        vel = math.sqrt(( (veloX**2) + (veloY**2) ))
        angV = math.atan(veloY/veloX)
        angA = math.radians(angleI) - angV
        liftx = -( (1/2) * airD * crsecF * coefL(angA) * (vel**2) ) * math.sin(angV)
        #print("liftX: ", liftx)
        #print("gravity:",-g*mass)
        #print("-")
        return liftx

    def liftY(veloX, veloY):
        vel = math.sqrt(( (veloX**2) + (veloY**2) ))
        angV = math.atan(veloY/veloX)
        angA = math.radians(angleI) - angV
        lifty = ( (1/2) * airD * crsecF * coefL(angA) * (vel**2) ) * math.cos(angV)
        #print("liftY: ",lifty)
        return lifty

    def dragX(veloX, veloY):
        vel = math.sqrt(( (veloX**2) + (veloY**2) ))
        angV = math.atan(veloY/veloX)
        angA = math.radians(angleI) - angV
        dragx = -( (1/2) * airD * crsecF * coefD(angA) * (vel**2) ) * math.cos(angV)
        #print("dragX: ",dragx)
        return dragx

    def dragY(veloX, veloY):
        vel = math.sqrt(( (veloX**2) + (veloY**2) ))
        angV = math.atan(veloY/veloX)
        angA = math.radians(angleI) - angV
        dragy = -( (1/2) * airD * crsecF * coefD(angA) * (vel**2) ) * math.sin(angV)
        #print("dragY: ",dragy)
        return dragy



    #Euler's loop
    for i in range(0, STEPS-1):

        y[i+1] = y[i] + vy[i]*DT 
        x[i+1] = x[i] + vx[i]*DT
    
        vy[i+1] = vy[i] + (  (1/mass) * ( (-1 * mass * g) + (dragY(vx[i],vy[i])) + (liftY(vx[i],vy[i])) )  ) * DT
        vx[i+1] = vx[i] + (  (1/mass) * ( (dragX(vx[i],vy[i])) + (liftX(vx[i],vy[i])) )  ) * DT
    
        t[i+1] = t[i] + DT
    
    #removing the coordiantes with thenegative values of Y
    # while y[len(y)-1] < 0:
    #     y = np.delete(y,len(y)-1)
    #     x = np.delete(x,len(x)-1)
    #     t = np.delete(t,len(t)-1)
        
    return x,y

def rotate_frisbee(frisbee,angle):
    new_frisbee = pygame.transform.rotozoom(frisbee,angle,1)
    return new_frisbee


def angle_speed_display(x,y,ypos):

    dx = x
    dy = -(y - ypos)
    
    speed = round(((dx**2+dy**2)**(1/2))/17-10,1)
    angle = math.degrees(math.tan(dy/dx))
    angle = round(angle,2)
    
    if angle > 80:
        angle = 80
    if angle < - 80:
        angle = -80
    
    strspeed = str(speed) + 'm/s'
    strangle = str(angle) + '*'

    angle_surface = game_font.render(strspeed,True,(255,255,255))
    angle_rect = angle_surface.get_rect(center = (950,50))
    
    speed_surface = game_font.render(strangle,True,(255,255,255))
    speed_rect = speed_surface.get_rect(center = (500,50))
    
    screen.blit(angle_surface,angle_rect)
    screen.blit(speed_surface,speed_rect)
    
    return float(angle)

def display_start():
    start_surface = game_font.render('Press SPACE to start', True, (255,255,255))
    start_rect = start_surface.get_rect(center = (500,300))
    
    instruction_surface = game_font.render('Move Your Mouse to Aim and Click to Launch the Frisbee at Your Target || Press SPACE to Reset the Level', True, (255,255,255))
    instruction_rect = instruction_surface.get_rect(center = (500,50))
    
    screen.blit(instruction_surface,instruction_rect)
    screen.blit(start_surface,start_rect)

def display_score(score):
    strscore = 'Score: ' + str(score)
    score_surface = game_font.render(strscore,True,(255,255,255))
    score_rect = score_surface.get_rect(center = (100,100))
    screen.blit(score_surface,score_rect)
    
    
    
    
pygame.init()





## Variables
WIDTH = 1000
HEIGHT = 600
FrameRate = 120
WHITE = (255,255,255)
BGcolor = (0,0,0)
angle = 0

frisbY = 500





screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Frisbee Game")
clock = pygame.time.Clock()
game_font = pygame.font.SysFont('arial',20)


frisbee_surface = pygame.image.load('Assets/orange_frisbee_2.jpg').convert_alpha()
frisbee_surface = pygame.transform.smoothscale(frisbee_surface, (50,7))
frisbee_rect = frisbee_surface.get_rect(center = (25,frisbY))

def pole(x,y):
    pole_rect = pygame.Rect(x,y,5,80)
    pygame.draw.rect(screen,WHITE,pole_rect)
    pygame.draw.polygon(screen, WHITE, [(x,y),(x,y+10),(x+15,y+5)])
    pygame.draw.polygon(screen, WHITE, [(x-15,y+78),(x+18,y+78),(x+18,y+80),(x-15,y+80)])
    
    return pole_rect





def main():
    # Main Game Loop
    Startbool = False
    Clickbool = False
    Flybool = False
    i = 0
    polex = 900
    poley = 500
    obstaclex = 500
    obstacley = 500
    score = 0
    while True:
        clock.tick(FrameRate)
        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        if Mouse_x <= 200:
            Mouse_x = 200
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Startbool = not Startbool
                    Flybool = False
                    frisbee_rect.centerx = 25
                    frisbee_rect.centery = frisbY
                    i = 0
                    polex = rd.randint(700,950)
                    poley = rd.randint(100,500)
                    obstaclex = rd.randint(350,650)
                    obstacley = poley - 40 + rd.randint(0,80)
                    
                    
            if event.type == pygame.MOUSEBUTTONUP:
                Clickbool = True

        screen.fill(BGcolor)
        
        
        if Startbool == True:
            dx = Mouse_x 
            dy = -(Mouse_y - frisbY)
            
            speed = round(((dx**2+dy**2)**(1/2))/17-10,1)

            angle = math.degrees(math.tan(dy/dx))
            angle = round(angle,2)
            angle_speed_display(Mouse_x,Mouse_y,frisbY)
            
            if angle > 80:
                angle = 80
            if angle < - 80:
                angle = -80
            
            pygame.draw.line(screen,WHITE,(200,0),(200,600))
            
            rotated_frisbee = rotate_frisbee(frisbee_surface,angle)
            screen.blit(rotated_frisbee,frisbee_rect)
            pole(polex,poley)
            obstacle = pygame.Rect(obstaclex,obstacley,5,120)
            pygame.draw.rect(screen,WHITE,obstacle)
            
            display_score(score)
            
            if Clickbool == True:
                Startbool = False
                Flybool = True
                currentangle = angle
                currentspeed = speed
                frisbeeCords = FrisbeeEulerFindX(currentspeed,currentangle)
                Clickbool = False
        elif Flybool == True:
            i += 1

            frisbee_rect.centerx = 25 + frisbeeCords[0][i]*15
            frisbee_rect.centery = frisbY - frisbeeCords[1][i]*20

            rotated_frisbee = rotate_frisbee(frisbee_surface,angle)
            screen.blit(rotated_frisbee,frisbee_rect)
            pole(polex,poley)
            obstacle = pygame.Rect(obstaclex,obstacley,5,120)
            pygame.draw.rect(screen,WHITE,obstacle)
            
            if frisbee_rect.colliderect(pole(polex,poley)):
                score += 1
                Startbool = not Startbool
                Flybool = False
                frisbee_rect.centerx = 25
                frisbee_rect.centery = frisbY
                i = 0
                polex = rd.randint(700,950)
                poley = rd.randint(100,500)
                obstaclex = rd.randint(350,650)
                obstacley = poley - 40 + rd.randint(0,80)
            
            if frisbee_rect.colliderect(obstacle) or frisbee_rect.centerx > WIDTH or frisbee_rect.centery > HEIGHT:
                Startbool = not Startbool
                Flybool = False
                frisbee_rect.centerx = 25
                frisbee_rect.centery = frisbY
                i = 0
            


                
        else:
            display_start()
        


        pygame.display.update()
        Clickbool = False

    
    
if __name__ == '__main__':
    main()
            









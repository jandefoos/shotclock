import sys, os
import time
import pygame
from pygame.locals import *
if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

Screen = max(pygame.display.list_modes())
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("[Program] - [Author] - [Version] - [Date]")
Surface = pygame.display.set_mode(Screen,FULLSCREEN)

Click = pygame.mixer.Sound("snd.ogg")
buzzer = pygame.mixer.Sound("nba-buzzer.ogg")

Font = pygame.font.Font("font.ttf", 700)

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

Time = [0,10,00]
#OriginalTime = list(Time)

test = Font.render("0",True,(255,0,0))
width = test.get_width() 
height = test.get_height()
totalwidth = 5 * width


mode = "stopped"

def quit():
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    pygame.quit(); sys.exit()

def GetInput():
    global mode, Time
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: quit()
            if event.key == K_h:                            # reset 5
                if Time == [0,0,0]:
                    mode = 'counting'
                    pygame.mixer.pause()
                Time = [0,5,00]
            if event.key == K_f:                            # reset 15
                if Time == [0,0,0]:
                    mode = 'counting'
                    pygame.mixer.pause()
                Time = [0,15,00]
            if event.key == K_j:                            # reset 10
                if Time == [0,0,0]:
                    mode = 'counting'
                    pygame.mixer.pause()
                Time = [0,10,00]
            if event.key == K_t:                            # time-out 30
                pygame.mixer.pause()
                buzzer.play()
                if Time == [0,0,0]:
                    mode = 'counting'
                    pygame.mixer.pause()
                Time = [0,30,00]
            if event.key == K_y:                            # game break 90
                if Time == [0,0,0]:
                    mode = 'counting'
                    pygame.mixer.pause()
                Time = [0,90,00]
            if event.key == K_SPACE: # stop
                mode = 'stopped'
            if event.key == K_RETURN:  # start
                mode = 'counting'

def Update():
    global mode, Time
    if mode == "counting":
        Time[2] -= 1
        #if Time[2] == 15: Click.play()                      # Click sound
        if Time[2] < 0:
            Time[2] = 99
            Time[1] -= 1
            if Time[1] < 0:
                Time[1] = 59
                Time[0] -= 1
                if Time[0] < 0:
                    Time = [0,0,0]
                    mode = "stopped"
                    #Click.play()
                    buzzer.play()

def Draw():
    Surface.fill((0,0,0))
    t2 = str(Time[1])
    if len(t2) == 1: t2 = "0"+t2
    t3 = str(Time[2])
    if len(t3) == 1: t3 = "0"+t3
    string = t2+":"+t3
    start_pos = (Screen[0]/2)-(totalwidth/2)
    for character in string:
        if character != "1":
            pos = [start_pos,(Screen[1]/2)-(height/2)]
        else:
            pos = [start_pos+int(round((51.0/99.0)*width)),(Screen[1]/2)-(height/2)]
        Surface.blit(Font.render(character,True,(255,255,0)),pos)
        start_pos += width
    pygame.display.flip()

def main():
    global mode
    Clock = pygame.time.Clock()
    while True:
        #GetInput()
        Draw()
        if mode == "stopped":
            GetInput()
            time.sleep(0.01)
        elif mode == "counting":
            GetInput()
            Update()
            Clock.tick(100)

if __name__ == '__main__': main()

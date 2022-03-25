import pygame as py
import tkinter
import tkinter.filedialog
from math import sqrt
from math import acos
from calc import *

WINDOW_SIZE = (1040, 720)
map = py.image.load("map.bmp")

py.init()

screen = py.display.set_mode(WINDOW_SIZE, py.RESIZABLE)

#values about points
pointsX = []
pointsY = []

#converted points
pointsXc = []
pointsYc = []

circleRadius = 7

#values aboutrendering engine
updateBg = False
updatePts = False
updateRec = False
recPos = (0, 0)

#overall values
leftShift = False
leftCtrl = False
pressing = False

def export():
    top = tkinter.Tk()
    top.withdraw()
    fileName = tkinter.filedialog.asksaveasfilename(parent = top, filetypes=(("Text files", "*.txt"), ("Prolog files", "*.pl *.pro"), ("All files", "*.*")))
    top.destroy()
    file = open(fileName, "w")

    pointsXc = []
    pointsYc = []
    for i in range(0, len(pointsX)):
        pointsXc.append((pointsX[i]-75)/3.75)
        pointsYc.append(abs(pointsY[i]-553)/3.75)

    direction = 0
    for i in range(1, len(pointsXc)):
        posA = [pointsXc[i], pointsYc[i]]
        posC = [pointsXc[i-1], pointsYc[i-1]]
        posB = [posC[0] + GetPosition(1, direction)[0], posC[1] + GetPosition(1, direction)[1]]
        a = 1
        b = ((posA[0] - posC[0]) **2) + ((posA[1] - posC[1]) **2)
        c = ((posA[0] - posB[0]) **2) + ((posA[1] - posB[1]) **2)
        angle = acos(round((b + a - c) / (2 * sqrt(b) * sqrt(a)), 4)) * 57.29579
        if round(pointsXc[i-1] + GetPosition(sqrt(b), direction + angle)[0], 1) == round(pointsXc[i], 1) and round(pointsYc[i-1] + GetPosition(sqrt(b), direction + angle)[1], 1) == round(pointsYc[i], 1):
            file.write("turn("+str(round(-angle, 2))+")\n")
            file.write("straight("+ str(-(round(sqrt(b), 3) * 10))+ ")\n")
            direction += round(angle, 2)
        else:
            file.write("turn("+str(round(angle, 2))+")\n")
            file.write("straight("+ str(-(round(sqrt(b), 3) * 10))+ ")\n")
            direction -= round(angle, 2)

def render(updateBackground, updatePoints, updateRectangle):
    if updateBackground:
        screen.blit(map, (0, 0))
    if updatePoints:
        for i in range(0, len(pointsX)):
            py.draw.circle(screen, (108, 92, 231), (pointsX[i], pointsY[i]), circleRadius)
        for i in range(1, len(pointsX)):
            py.draw.aaline(screen, (108, 92, 231), (pointsX[i-1], pointsY[i-1]), (pointsX[i], pointsY[i]))
    if updateRec:
        rect = py.Rect(recPos, (200, 400))
        py.draw.rect(screen, (0, 206, 201), rect)

    py.display.flip()

running = True

render(True, False, False)

while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        
        if event.type == py.VIDEORESIZE:
            updateBg = True
            updatePts = True

        #On key first press down
        if event.type == py.KEYDOWN:
            if event.key == py.K_LSHIFT:
                leftShift = True
            if event.key == py.K_LCTRL:
                leftCtrl = True

        #On key release
        if event.type == py.KEYUP:
            if event.key == py.K_LSHIFT:
                leftShift = False
            if event.key == py.K_LCTRL:
                leftCtrl = False
            if leftCtrl:
                if event.key == py.K_e:
                    export()

    if py.mouse.get_pressed(3)[0] and not pressing:
        pressing = True
        if leftShift and not leftCtrl:
            print("Not working")
        elif leftCtrl and not leftShift:
            print("Not working")
        elif not leftCtrl and not leftShift:
            pointsX.append(py.mouse.get_pos()[0])
            pointsY.append(py.mouse.get_pos()[1])
            updatePts = True
    elif py.mouse.get_pressed(3)[2] and not pressing:
        pressing = True
        for i in range(0, len(pointsX)):
            if py.mouse.get_pos()[0] > pointsX[i]-circleRadius and py.mouse.get_pos()[0] < pointsX[i]+circleRadius:
                if py.mouse.get_pos()[1] > pointsY[i]-circleRadius and py.mouse.get_pos()[1] < pointsY[i]+circleRadius:
                    updateRec = True
                    recPos = py.mouse.get_pos()

    elif not py.mouse.get_pressed(3)[0]:
        pressing = False

    render(updateBg, updatePts, updateRec)
    updateBg = False
    updatePts = False
    updateRec = False


py.quit()
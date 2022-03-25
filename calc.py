from math import sin
from math import cos
from math import radians

def GetPosition(distance, angle):
    if(angle/360 > 1):
        angle = angle%360
    locationNew = [0, 0]
    if(angle >= 0):
        if(not angle == 0 and not angle == 180 and not angle == 90 and not angle == 270):
            locationNew[0] = sin(radians(angle)) * distance
            locationNew[1] = cos(radians(angle)) * distance
        elif(angle == 0 or angle == 180):
            if(angle == 0):
                locationNew[0] = 0
                locationNew[1] = distance
            else:
                locationNew[0] = 0
                locationNew[1] = distance * -1
        else:
            if(angle == 90):
                locationNew[0] = distance
                locationNew[1] = 0
            else:
                locationNew[0] = distance * -1
                locationNew[1] = 0
    else:
        if(not angle == -180 and not angle == -90 and not angle == -270):
            locationNew[0] = (sin(radians(angle)) * distance)
            locationNew[1] = (cos(radians(angle)) * distance)
        elif(angle == -180):
                locationNew[0] = 0
                locationNew[1] = distance * -1
        else:
            if(angle == -90):
                locationNew[0] = distance * -1
                locationNew[1] = 0
            else:
                locationNew[0] = distance
                locationNew[1] = 0
    return(locationNew)
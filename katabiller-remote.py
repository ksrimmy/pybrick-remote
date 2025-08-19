from pybricks.tools import wait
from pybricks.hubs import TechnicHub
from pybricks.parameters import Color
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Direction, Stop, Button
from pybricks.pupdevices import *
from pybricks.parameters import *
from pybricks.tools import wait
#print(Color.RED.h, Color.RED.s, Color.RED.v)
#https://www.profinerd.de/2022/03/24/pybricks-tutorial-42140-mit-lego-fernbedienung-aber-ohne-handy-steuern-wie-genial-ist-das-denn/

## Initialize the hub.
hub = TechnicHub()
battstand = hub.battery.current()
battstand = str(battstand)
print("-----------------------------------------")
print("-- Profinerd Edition --")
print("-----------------------------------------")
print("19-03-2022 | Aktueller Batteriestand " + battstand + "%")
print("-----------------------------------------")
print("Credits an Technicmaster0 für die komplette Steuerung!")
print("-----------------------------------------")
print("Sein Quellcode für Steuerung per Remote Control")
print("Optimierung und Kleinigkeiten verbessert durch Profinerd")
print("-----------------------------------------")

#----------------------------------------------
#Variablen
#----------------------------------------------
#Millisekunden für Drehung um 180 grad / 600 standard
halfturnms = 550
#Profinerd-Blink-Farben in MS / 500 Standard / 0=aus
blinkstartms = 500
#----------------------------------------------

#Blinken in den Farben des Profinerd :)
for i in range(3):

    hub.light.on(Color.VIOLET)
    wait(blinkstartms)
    hub.light.on(Color.BLUE)
    wait(blinkstartms)

## ------------------------------------------
## From now on: THANKS to technicmaster0
## He wrote this incredible code:
## ------------------------------------------
#Einbinden der Hardware
hub = TechnicHub()
motor1 = Motor(Port.B)
motor2 = Motor(Port.A)
remoteControl = Remote()


#main loop
while True:
   #update pressed buttons information
    pressed = remoteControl.buttons.pressed()
    #update orientation of the hub
    hubOrientation = hub.imu.up()





    #commands to drive forwards or backwards
    #they depend on the orientation of the hub
    #for one side, motors are reversed and switched
    if hubOrientation == Side.TOP:
        hub.light.on(Color.BLUE)
        if Button.LEFT_MINUS in pressed:
            motor2.dc(100)
        elif Button.LEFT_PLUS in pressed:
            motor2.dc(-100)
        else: 
            motor2.brake()
        
        if Button.RIGHT_MINUS in pressed:
            motor1.dc(-100)
        elif Button.RIGHT_PLUS in pressed:
            motor1.dc(100)
        else:
            motor1.brake()

        if (Button.LEFT in pressed):
           hub.light.on(Color.VIOLET)
           motor1.dc(-100)
           motor2.dc(-100)
           wait(halfturnms)

## ------------------------------------------
## Small edits from profinerd for 180° turn
## ------------------------------------------
#180° Turn
        if (Button.RIGHT in pressed):
           hub.light.on(Color.VIOLET)
           motor1.dc(100)
           motor2.dc(100)
           wait(halfturnms)

#Shutdown mit Grüner Mitteltaste
        if (Button.CENTER in pressed):
           hub.light.on(Color.RED)
           wait(1000)
           hub.system.shutdown()

## ------------------------------------------
## End profinerd of small Profinerd Edits
## ------------------------------------------

    elif hubOrientation == Side.BOTTOM:
        hub.light.on(Color.ORANGE)
        if Button.LEFT_MINUS in pressed:
            motor1.dc(100)
        elif Button.LEFT_PLUS in pressed:
            motor1.dc(-100)
        else: 
            motor1.brake()
        
        if Button.RIGHT_MINUS in pressed:
            motor2.dc(-100)
        elif Button.RIGHT_PLUS in pressed:
            motor2.dc(100)
        else:
            motor2.brake()
        
        if (Button.LEFT in pressed):
           hub.light.on(Color.VIOLET)
           motor1.dc(-100)
           motor2.dc(-100)
           wait(halfturnms)

## ------------------------------------------
## Small edits from profinerd for 180° turn
## ------------------------------------------
#180° Turn
        if (Button.RIGHT in pressed):
           hub.light.on(Color.VIOLET)
           motor1.dc(100)
           motor2.dc(100)
           wait(halfturnms)

#Shutdown mit Grüner Mitteltaste
        if (Button.CENTER in pressed):
           hub.light.on(Color.RED)
           wait(1000)
           hub.system.shutdown()

## ------------------------------------------
## End profinerd of small Profinerd Edits
## ------------------------------------------

    else:
        hub.light.on(Color.BLUE)
        if (Button.LEFT_PLUS not in pressed) and (Button.LEFT_MINUS not in pressed) and (Button.RIGHT_PLUS not in pressed) and (Button.RIGHT_MINUS not in pressed):
            motor1.brake()
            motor2.brake()

        if (Button.CENTER in pressed):
           hub.light.on(Color.RED)
           wait(1000)
           hub.system.shutdown()


    wait(100)
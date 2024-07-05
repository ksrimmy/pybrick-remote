from pybricks.parameters import Direction, Port, Stop
from pybricks.pupdevices import Motor, UltrasonicSensor
from pybricks.robotics import Car
from pybricks.tools import wait

# Standard MicroPython modules
from usys import stdin, stdout
from uselect import poll


# Set up all devices.
steering = Motor(Port.B, Direction.COUNTERCLOCKWISE)
motorL = Motor(Port.C, Direction.COUNTERCLOCKWISE)
motorR = Motor(Port.D, Direction.CLOCKWISE)

# Lower the acceleration so the car starts and stops realistically.
motorL.control.limits(acceleration=500)
motorR.control.limits(acceleration=500)


car = Car(steering, [motorL, motorR])


distanceSensor = UltrasonicSensor(Port.A)
# distanceSensor.lights.on()


# Optional: Register stdin for polling. This allows
# you to wait for incoming data without blocking.
keyboard = poll()
keyboard.register(stdin)

stdout.buffer.write(b"rdy")
data = ""
cmd_arr = []
while True:
    # Let the remote program know we are ready for a command.
  

    # Optional: Check available input.
    # while not keyboard.poll(0):
    #     # Optional: Do something here.
    #     wait(10)

    if keyboard.poll(0):
        #cmd = input()
        data += stdin.read(1)
    
        if data[-1] == "\n":
            cmd_arr = data[0:-1].split("|")
            data = ""

            # Control steering using the left - and + buttons.
            car.steer(50 if "lft" in cmd_arr else (-50 if "rgt" in cmd_arr else 0))
            # Control drive power using the right - and + buttons.
            car.drive_power(80 if "fwd" in cmd_arr else (-80 if "rev" in cmd_arr else 0))
    
    # stdout.buffer.write(data)
    wait(2)
    

stdout.buffer.write(b"END")
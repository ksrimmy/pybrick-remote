# Import required MicroPython libraries.
from pybricks.parameters import Direction, Port, Stop
from usys import stdin, stdout
from uselect import poll
from pybricks.tools import wait
from pybricks.pupdevices import Motor
from pybricks.robotics import Car

# Set up all devices.
motorH = Motor(Port.C, Direction.COUNTERCLOCKWISE)
motorL = Motor(Port.E, Direction.COUNTERCLOCKWISE)
motorR = Motor(Port.A, Direction.CLOCKWISE)

# Lower the acceleration so the car starts and stops realistically.
motorL.control.limits(acceleration=300)
motorR.control.limits(acceleration=300)
motorH.control.limits(acceleration=300)

motorL.run_target(200, 180, wait=False)
motorR.run_target(200, 180)
motorH.run_target(200, 0, wait=False)
wait(200)
motorL.reset_angle(0)
motorR.reset_angle(0)
motorL.run_target(200, 0, wait=False)
motorR.run_target(200, 0)
motorH.run_target(200, 0, wait=False)


# Register the standard input so we can read keyboard presses.
keyboard = poll()
keyboard.register(stdin)

stdout.buffer.write(b"rdy\r\n")
data = ""
cmd_arr = []

while True:
    # Check if a key has been pressed.
    if keyboard.poll(0):
        ch = stdin.read(1)
        data += ch
        
        if data[-1] == "\n":
            print("")
            cmd = data[0]
            try:
                angle = int(data[1:-1])
                data = ""
                # print("Command:", cmd)
                # print("Angle:", angle)

                if cmd == 'v':
                    motorL.run_target(200, angle, wait=False)
                    motorR.run_target(200, angle)
                if cmd == 'h':
                    motorH.run_target(200, angle, wait=False)
            except ValueError:
                print("Command not recognized.")
                data = ""
                continue
        else:
            stdout.buffer.write(ch)
    
    # stdout.buffer.write(data)


stdout.buffer.write(b"END")
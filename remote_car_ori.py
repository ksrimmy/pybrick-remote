from pybricks.parameters import Direction, Port, Stop
from pybricks.pupdevices import Motor, UltrasonicSensor
from pybricks.robotics import Car
from pybricks.tools import wait

# Standard MicroPython modules
from usys import stdin, stdout
from uselect import poll


# Set up all devices.
steering = Motor(Port.C, Direction.COUNTERCLOCKWISE)
motorL = Motor(Port.A, Direction.COUNTERCLOCKWISE)
motorR = Motor(Port.E, Direction.CLOCKWISE)
car = Car(steering, [motorL, motorR])

distanceSensor = UltrasonicSensor(Port.B)
# distanceSensor.lights.on()


# Optional: Register stdin for polling. This allows
# you to wait for incoming data without blocking.
keyboard = poll()
keyboard.register(stdin)

stdout.buffer.write(b"rdy")
data = ""
cmd_arr = []
last_cmd = []
cur_speed_val = 30
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
            last_cmd = cmd_arr
            cmd_arr = data[0:-1].split("|")
            data = ""

            if last_cmd == cmd_arr:
                if cur_speed_val < 100:
                    cur_speed_val += 2
            else:
                cur_speed_val = 30

            # Control steering using the left - and + buttons.
            car.steer(cur_speed_val if "lft" in cmd_arr else (cur_speed_val * -1 if "rgt" in cmd_arr else 0))
            # Control drive power using the right - and + buttons.
            car.drive_power(cur_speed_val if "fwd" in cmd_arr else (cur_speed_val * -1 if "rev" in cmd_arr else 0))
    
    # stdout.buffer.write(data)
    wait(2)
    

stdout.buffer.write(b"END")
from pybricks.parameters import Direction, Port, Color
from pybricks.pupdevices import Motor, UltrasonicSensor
from pybricks.robotics import Car
from pybricks.tools import wait, StopWatch
from pybricks.hubs import PrimeHub

# Standard MicroPython modules
from usys import stdin, stdout
from uselect import poll


# Set up all devices.
distanceSensor = UltrasonicSensor(Port.A)
steering = Motor(Port.B, Direction.COUNTERCLOCKWISE)
motorL = Motor(Port.C, Direction.COUNTERCLOCKWISE)
motorR = Motor(Port.D, Direction.CLOCKWISE)

hub = PrimeHub()


# Lower the acceleration so the car starts and stops realistically.
motorL.control.limits(acceleration=200)
motorR.control.limits(acceleration=200)


car = Car(steering, [motorL, motorR])
# car = Car(steering, [motorL, motorR], torque_limit=40)


# distanceSensor.lights.on()


# Optional: Register stdin for polling. This allows
# you to wait for incoming data without blocking.
keyboard = poll()
keyboard.register(stdin)

stdout.buffer.write(b"rdy")
data = ""
cmd_arr = []
collision_counter = -1
CAR_LENGTH = 130
stopWatch = StopWatch()
last_crash_time = 0
new_crash = False

AVERAGE_LEN = 10
average_values = [0] * AVERAGE_LEN

while True:
    # Let the remote program know we are ready for a command.
    full_speed_mode = False

    average_values = average_values[1:]
    average_values.append(distanceSensor.distance())
    average_dist = sum(average_values) / AVERAGE_LEN

    if average_dist < 50:
        full_speed_mode = True
    else:
        if average_dist < CAR_LENGTH:
            if not new_crash:
                new_crash = True
                crash_time = stopWatch.time()
                if crash_time > 1000:
                    collision_counter += 1
                    stopWatch.pause()
                    stopWatch.reset()
        elif average_dist >= CAR_LENGTH:
            new_crash = False
            stopWatch.resume()
            
            
 
        if collision_counter >= 0:
            hub.display.pixel(collision_counter/4, collision_counter%4, brightness=100)

    if keyboard.poll(0):
        #cmd = input()
        data += stdin.read(1)
         
        if data[-1] == "\n":
            cmd_arr = data[0:-1].split("|")
            data = ""

            if full_speed_mode:
                # Control steering using the left - and + buttons.
                car.steer(100 if "lft" in cmd_arr else (-100 if "rgt" in cmd_arr else 0))
                # Control drive power using the right - and + buttons.
                car.drive_power(100 if "fwd" in cmd_arr else (-100 if "rev" in cmd_arr else 0))
            else:
                # Control steering using the left - and + buttons.
                car.steer(60 if "lft" in cmd_arr else (-60 if "rgt" in cmd_arr else 0))
                # Control drive power using the right - and + buttons.
                car.drive_power(60 if "fwd" in cmd_arr else (-60 if "rev" in cmd_arr else 0))
        
    # stdout.buffer.write(data)
    wait(2)
    

stdout.buffer.write(b"END")
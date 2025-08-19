from pybricks.parameters import Direction, Port, Color
from pybricks.pupdevices import Motor, UltrasonicSensor
# from pybricks.robotics import Car
from pybricks.tools import wait, StopWatch
from pybricks.hubs import PrimeHub
from pybricks.robotics import DriveBase

# Standard MicroPython modules
from usys import stdin, stdout
from uselect import poll
from uerrno import ENODEV



def detectDistanceSensor(sensorPort = Port.A):
    try:
        # Try to initialize
        distanceSensor = UltrasonicSensor(sensorPort)
        distanceSensor.lights.on()

        # If all goes well, you'll see this message.
        stdout.buffer.write(b"Detected DistanceSensor.")
        return distanceSensor
    except OSError as ex:
        # If an OSError was raised, we can check what
        # kind of error this was, like ENODEV.
        if ex.errno == ENODEV:
            # ENODEV is short for "Error, no device."
            stdout.buffer.write(b"There is no sensor on this port.")
        else:
            stdout.buffer.write(b"Error occurred when detecting DistanceSensor.")
        return None

# Set up all devices.
distanceSensor = detectDistanceSensor(Port.A)
# distanceSensor = UltrasonicSensor(Port.A)
# distanceSensor.lights.on()
# steering = Motor(Port.B, Direction.COUNTERCLOCKWISE)
motorL = Motor(Port.C, Direction.COUNTERCLOCKWISE)
motorR = Motor(Port.D, Direction.CLOCKWISE)







hub = PrimeHub()


# Lower the acceleration so the car starts and stops realistically.
# motorL.control.limits(acceleration=200)
# motorR.control.limits(acceleration=200)

# Initialize the drive base. In this example, the wheel diameter is 56mm.
# The distance between the two wheel-ground contact points is 112mm.
car = DriveBase(motorL, motorR, wheel_diameter=56, axle_track=112)

# Optionally, uncomment the line below to use the gyro for improved accuracy.
# drive_base.use_gyro(True)



# Optional: Register stdin for polling. This allows
# you to wait for incoming data without blocking.
keyboard = poll()
keyboard.register(stdin)

stdout.buffer.write(b"rdy")
data = ""
cmd_arr = []
prev_cmd_arr = []
collision_counter = -1
CAR_LENGTH = 130
stopWatch = StopWatch()
# lastCommandWatch = StopWatch()
last_crash_time = 0
new_crash = False

FULL_SPEED_FWD = 500
FULL_SPEED_REV = -500
NORMAL_SPEED_FWD = 200
NORMAL_SPEED_REV = -200
# ANGLE_LFT = -90
# ANGLE_RGT = 90

AVERAGE_LEN = 10
average_values = [0] * AVERAGE_LEN

LASTCOMMANDTHRESHOLD = 1000

while True:
    # Let the remote program know we are ready for a command.
    full_speed_mode = False

    if distanceSensor is not None:
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

        

    
    # # Drive forward by 500mm (half a meter).
    # drive_base.straight(500)

    # # Turn around clockwise by 180 degrees.
    # drive_base.turn(180)

    # # Drive forward again to get back to the start.
    # drive_base.straight(500)

    # # Turn around counterclockwise.
    # drive_base.turn(-180)
    # # stdout.buffer.write(data)
    # wait(2)
        
    if keyboard.poll(LASTCOMMANDTHRESHOLD):
        #cmd = input()
        data += stdin.read(1)
         
        if data[-1] == "\n":
            prev_cmd_arr = cmd_arr
            cmd_arr = data[0:-1].split("|")
            data = ""

            # if full_speed_mode:
            #     # Control steering using the left - and + buttons.
            #     car.steer(100 if "lft" in cmd_arr else (-100 if "rgt" in cmd_arr else 0))
            #     # Control drive power using the right - and + buttons.
            #     car.drive_power(100 if "fwd" in cmd_arr else (-100 if "rev" in cmd_arr else 0))
            # else:
            # Control steering using the left - and + buttons.

            
            # angle = ANGLE_LFT if "lft" in cmd_arr else (ANGLE_RGT if "rgt" in cmd_arr else 0)
            if len(cmd_arr) >= 2:
                angle = float(cmd_arr[1])
            else:
                angle = 0.0

            # use braking, when switching directions, might not make a difference
            if ("fwd" in cmd_arr and "rev" in prev_cmd_arr) or ("rev" in cmd_arr and "fwd" in prev_cmd_arr):
                car.brake()
                wait(500)
            else:
                if full_speed_mode:
                     speed = FULL_SPEED_FWD if "fwd" in cmd_arr else (FULL_SPEED_REV if "rev" in cmd_arr else 0)
                else:
                    speed = NORMAL_SPEED_FWD if "fwd" in cmd_arr else (NORMAL_SPEED_REV if "rev" in cmd_arr else 0)
                car.drive(speed, angle)
    else:
        car.drive(0, 0.0)
    # wait(2)

    

stdout.buffer.write(b"END")
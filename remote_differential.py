from pybricks.pupdevices import Motor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.parameters import Port, Direction, Stop

# Standard MicroPython modules
from usys import stdin, stdout
from uselect import poll

motorSteering = Motor(Port.B)

motorL = Motor(Port.C)
motorR = Motor(Port.D)

distanceSensor = UltrasonicSensor(Port.A)
distanceSensor.lights.on()


# Lower the acceleration so the car starts and stops realistically.
# motorL.control.limits(acceleration=1000)
# motorR.control.limits(acceleration=1000)

# Optional: Register stdin for polling. This allows
# you to wait for incoming data without blocking.
keyboard = poll()
keyboard.register(stdin)

while True:

    # Let the remote program know we are ready for a command.
    stdout.buffer.write(b"rdy")

    # Optional: Check available input.
    while not keyboard.poll(0):
        # Optional: Do something here.
        
        if distanceSensor.distance() < 300:
            motorL.run_time(1000, 700, wait=False)
            motorR.run_time(-1000, 700)
            motorL.run(0)
            motorR.run_time(-1000, 700)

            motorL.run(-1000)
            motorR.run(1000)            

        wait(10)

    # Read three bytes.
    cmd = stdin.buffer.read(3)

    # Decide what to do based on the command.
    if cmd == b"fwd":
        motorL.run(-1000)
        motorR.run(1000)
    elif cmd == b"rev":
        motorL.run(500)
        motorR.run(-500)
    elif cmd == b"lft":
        motorL.run(-500)
        motorR.run(1000)
    elif cmd == b"rgt":
        motorL.run(-1000)
        motorR.run(500)
    elif cmd == b"sto":
        motorL.run(0)
        motorR.run(0)
    elif cmd == b"bye":
        break
    else:
        motorL.stop()
        motorR.stop()


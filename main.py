from __future__ import print_function
import time
from dronekit import Vehicle, connect
from source.mark1 import start_flame_on, flame_on

CONNECTION_STRING: str = "/dev/ttyAMA0"

BAUD_RATE: int = 921600
print("CONNECTING TO DRONE...")
drone: Vehicle = connect(CONNECTION_STRING, baud=BAUD_RATE, wait_ready=False)

# wait for at least one heartbeat to confirm life
while not drone.last_heartbeat:
    print("WAITING FOR HEARTBEAT...")
    time.sleep(1)

print("HEARTBEAT RECEIVED! CONNECTING TO PARAMETERS...")
drone.wait_ready("autopilot_version")
print("CONNECTED SUCCESSFULLY!")

while True:
    start_flame_on(drone)

print("CLOSING VEHICLE OBJECT")
drone.close()

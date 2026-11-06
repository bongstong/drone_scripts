from __future__ import print_function
import time
from dronekit import Vehicle, connect
from source.mark1 import start_flame_on

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


# using drone.channels doens't work so I fix it
@drone.on_message("RC_CHANNELS")
def rc_listener(self, name, message):
    global switch6
    # map mavlink message to dict
    switch6 = message.chan6_raw


try:
    while True:
        print(switch6)
        # start_flame_on(drone)
except KeyboardInterrupt:
    quit()

print("CLOSING VEHICLE OBJECT")
drone.close()

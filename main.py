import time
import collections
import collections.abc

collections.MutableMapping = collections.abc.MutableMapping
collections.MutableSequence = collections.abc.MutableSequence
collections.Mapping = collections.abc.Mapping
collections.Sequence = collections.abc.Sequence
from dronekit import Vehicle, connect
from source.mark1 import start_flame_check

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
switch6 = None


# using drone.channels doens't work so I fix it
drone.add_message_listener(
    "RC_CHANNELS",
    lambda self, name, msg: setattr(
        drone,
        "ch6_raw",
        msg.chan6_raw,
    ),
)


try:
    while True:
        ch6 = getattr(drone, 'ch6_raw', None)
        start_flame_check(drone, ch6)
except KeyboardInterrupt:
    quit()

print("CLOSING VEHICLE OBJECT")
drone.close()

from __future__ import print_function

import time
from dronekit import Vehicle, connect, VehicleMode  # , LocationGlobalRelative

CONNECTION_STRING = "/dev/ttyAMA0"


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


def arm_and_takeoff(TargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("BASIC PRE-ARM CHECKS")
    # Don't try to arm until autopilot is ready
    while not drone.is_armable:
        print("WAITING FOR VEHICLE TO INITIALISE...")
        time.sleep(1)

    print("ARMING MOTORS")
    # Copter should arm in GUIDED mode
    drone.mode = VehicleMode("GUIDED")
    drone.armed = True

    # Confirm vehicle armed before attempting to take off
    while not drone.armed:
        print("WAITING FOR ARMING...")
        time.sleep(1)

    print("DRONE ARMED")
    print("TAKING OFF!")
    drone.simple_takeoff(TargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).

    while drone.location.global_relative_frame.alt <= TargetAltitude * 0.95:
        print(" Altitude: ", drone.location.global_relative_frame.alt)
        time.sleep(1)
    print("REACHED TARGET ALTITUDE")


arm_and_takeoff(1)
print("CLOSING VEHICLE OBJECT")
drone.close()

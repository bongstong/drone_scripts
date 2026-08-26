from __future__ import print_function

import time
from dronekit import Vehicle, connect, VehicleMode, LocationGlobalRelative
from convert import dms2wgs
from camera import start_recording, stop_recording

CONNECTION_STRING = "/dev/ttyAMA0"


BAUD_RATE: int = 921600
print("CONNECTING TO DRONE...")
vehicle: Vehicle = connect(CONNECTION_STRING, baud=BAUD_RATE, wait_ready=False)

# wait for at least one heartbeat to confirm life
while not vehicle.last_heartbeat:
    print("WAITING FOR HEARTBEAT...")
    time.sleep(1)

print("HEARTBEAT RECEIVED! CONNECTING TO PARAMETERS...")
video_stream = start_recording()
vehicle.wait_ready("autopilot_version")
print("CONNECTED SUCCESSFULLY!")


def arm_and_takeoff(TargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("BASIC PRE-ARM CHECKS")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print("WAITING FOR VEHICLE TO INITIALISE...")
        time.sleep(1)

    print("ARMING MOTORS")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print("WAITING FOR ARMING...")
        time.sleep(1)

    print("DRONE ARMED")
    print("TAKING OFF!")
    vehicle.simple_takeoff(TargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).

    # while drone.location.global_relative_frame.alt <= TargetAltitude * 0.95:
    #     print(" Altitude: ", drone.location.global_relative_frame.alt)
    #     time.sleep(1)

    while True:
        if vehicle.location.global_relative_frame.alt >= TargetAltitude * 0.95:
            break
        time.sleep(1)
    print("REACHED TARGET ALTITUDE")


arm_and_takeoff(3)

print("SET DEFAULT/TARGET AIRSPEED TO 3")
vehicle.airspeed = 1

print("GOING TOWARDS FIRST POINT FOR 15 SECONDS ...")

# WGS coordinates of the waypoints
point1_coordinates = dms2wgs([[47, 13, 18.57, "N"], [1, 34, 48.61, "W"]])
# point2_coordinates = dms2wgs(
#     [],
# )

point1: LocationGlobalRelative = LocationGlobalRelative(
    point1_coordinates[0],
    point1_coordinates[1],
    10,
)
vehicle.simple_goto(point1)

# sleep so we can see the change in map
time.sleep(15)

# print("GOING TOWARDS SECOND POINT (GROUNDSPEED SET TO 10 M/S)")
# point2: LocationGlobalRelative = LocationGlobalRelative(
#     point2_coordinates[0],
#     point2_coordinates[1],
#     5,
# )
# drone.simple_goto(point2, groundspeed=10)

print("RETURNING TO lAUNCH")
vehicle.mode = VehicleMode("RTL")

stop_recording(video_stream)

# Close vehicle object before exiting script
print("CLOSING VEHICLE OBJECT")
vehicle.close()

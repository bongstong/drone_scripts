from __future__ import print_function
import time
from dronekit import Vehicle, VehicleMode  # , LocationGlobalRelative


def arm_and_takeoff(target_altitude, drone: Vehicle):
    """
    Arms vehicle and fly to target_altitude.
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
    drone.simple_takeoff(target_altitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).

    while drone.location.global_relative_frame.alt <= target_altitude * 0.95:
        print(" Altitude: ", drone.location.global_relative_frame.alt)
        time.sleep(1)
    print("REACHED TARGET ALTITUDE")

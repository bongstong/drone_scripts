from gpiozero import Servo, Device, OutputDevice
from gpiozero.pins.lgpio import LGPIOFactory
from time import sleep

# initialize servo pin 11 and ground is pin 9
Device.pin_factory = LGPIOFactory()
servo = Servo(17)


def flame_on() -> None:
    """coordinates the servo to press on the can and generate spark
    to start the flamethrower
    no return value"""
    spark_relay = OutputDevice(23, active_high=False, initial_value=False)
    print("sparks ON")
    spark_relay.on()

    servo.max()
    sleep(1)
    print("flame turned ON")
    servo.min()
    sleep(1)
    print("end of spark and flame OFF")
    return None


def start_flame_on(drone, rc_num: str = "6") -> None:
    """Listens to RC switch number _ and when high calls
    the flame_on function"""
    if drone.channels[rc_num] >= 1800:
        flame_on()


if __name__ == "__main__":
    flame_on()

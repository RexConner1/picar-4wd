import time
from enum import Enum
import picar_4wd as car

SERVO_OFFSET = -36  # To achieve a 0-degree ultrasonic sensor
DEFAULT_SPEED = 25  # Motor speed (0-100)
DEFAULT_WAIT_TIME = 1.0  # In seconds
DEFAULT_SLEEP_TIME = 0.1  # In seconds


class DIRECTION(Enum):
    LEFT = "left"
    RIGHT = "right"


def move_forward(speed=DEFAULT_SPEED, sleep_seconds=0.1):
    car.forward(speed)
    time.sleep(sleep_seconds)
    car.stop()


def move_backward(speed=DEFAULT_SPEED, sleep_seconds=0.1):
    car.backward(speed)
    time.sleep(sleep_seconds)
    car.stop()


def move_left():
    car.turn_left(DEFAULT_WAIT_TIME)


def move_right():
    car.turn_right(DEFAULT_WAIT_TIME)

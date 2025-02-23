import time
import picar_4wd.helpers as defaults
from enum import Enum
import picar_4wd as car

class MOVE(Enum):
    LEFT = 'left'
    RIGHT = 'right'


def stop():
    car.stop()


def move_forward(motor_speed=defaults.DEFAULT_SPEED, sleep_time=defaults.DEFAULT_SLEEP_TIME):
    car.forward(motor_speed)
    time.sleep(sleep_time)
    stop()


def move_backward(motor_speed=defaults.DEFAULT_SPEED, sleep_time=defaults.DEFAULT_SLEEP_TIME):
    car.backward(motor_speed)
    time.sleep(sleep_time)
    stop()


def move_left(wait_time = defaults.DEFAULT_WAIT_TIME):
    car.turn_left(wait_time)


def move_right(wait_time = defaults.DEFAULT_WAIT_TIME):
    car.turn_right(wait_time)


def get_speed():
    return car.speed_val()

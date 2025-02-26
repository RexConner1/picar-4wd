import time
import picar_4wd.helpers as defaults
from enum import Enum
import picar_4wd as car

TURN_TIME_PER_DEGREE = 0.1


class MOVE(Enum):
    LEFT = 'left'
    RIGHT = 'right'


def __convert_degrees_to_time(degrees):
    return abs(degrees) * TURN_TIME_PER_DEGREE


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


def move_left(degrees=45):
    time = __convert_degrees_to_time(degrees)
    car.turn_left(time)


def move_right(degrees=45):
    time = __convert_degrees_to_time(degrees)
    car.turn_right(time)


def get_speed():
    return car.speed_val()

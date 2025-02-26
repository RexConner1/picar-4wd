import picar_4wd as car


DEFAULT_SPEED = 25  # Motor speed (0-100)

DEFAULT_WAIT_TIME = 1.0  # In seconds
DEFAULT_SLEEP_TIME = 0.1  # In seconds

OBSTACLE_THRESHOLD = 15  # In cm
ANGLE_THRESHOLD = 5


def get_config(name):
    car.config.get(name)


def set_config(name, value):
    car.config.set(name, value)

import picar_4wd as car
import time


def get_distance_at(angle):
    distance = car.get_distance_at(angle)
    time.sleep(0.1)
    return distance


def get_flat_distance():
    return get_distance_at(0)

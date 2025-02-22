import matplotlib.pyplot as plt
import numpy as np
import time
import picar_4wd.helpers.navigation as car
import picar_4wd.helpers.visuals as scan
from enum import Enum
from picar_4wd.filedb import FileDB
from math import radians, cos, sin

config = FileDB('mapping')
GRID_SIZE = 100
SCAN_ANGLES = list(range(-60, 60, 15))
scan_map = np.zeros((GRID_SIZE, GRID_SIZE))
car_position = [GRID_SIZE // 2, GRID_SIZE // 2]


class DIRECTION(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)


def update_position():
    print('Updating position...')
    distance_moved = car.get_speed() * 0.1
    car_position[0] += int(distance_moved)
    car_position[1] += int(distance_moved)


def scan_environment():
    print("Scanning environment...")
    for angle in SCAN_ANGLES:
        distance = scan.get_distance_at(angle)

        if 0 < distance < GRID_SIZE:
            x = int(GRID_SIZE / 2 + distance * cos(radians(angle)))
            y = int(GRID_SIZE / 2 + distance * sin(radians(angle)))

            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                scan_map[y, x] = 1


def display_map():
    plt.imshow(scan_map, cmap='gray')
    plt.title("Environment Map")
    plt.show()


if __name__ == "__main__":
    print(f'Starting mapping...')

    while True:
        car.move_forward(50)
        update_position()
        scan_environment()
        display_map()

        time.sleep(1)
        car.stop()

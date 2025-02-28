import math
import matplotlib.pyplot as plt
import numpy as np
import picar_4wd.helpers as defaults
import picar_4wd.helpers.navigation as car
import picar_4wd.helpers.visuals as scan
from enum import Enum
from picar_4wd.filedb import FileDB

config = FileDB('mapping')
GRID_SIZE = 100
SCAN_ANGLES = list(range(-60, 60 + 1, 15))
GRID_CENTER = (GRID_SIZE // 2, GRID_SIZE // 2)
scan_map = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
current_position = GRID_CENTER
current_angle = 0


class DIRECTION(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)


# def update_position():
#     print('Updating position...')
#     distance_moved = car.get_speed() * 0.1
#     current_position[0] += int(distance_moved)
#     current_position[1] += int(distance_moved)


def scan_environment():
    data = []

    print("Scanning environment...")
    for angle in SCAN_ANGLES:
        distance = scan.get_distance_at(angle)
        print(f'{distance: .1f} cm at {angle} degrees')
        if 0 < distance < GRID_SIZE:
            data.append((angle, distance))
    
    return data


def build_grid():
    scan_data = scan_environment()

    for angle, distance in scan_data:
        distance = scan.get_distance_at(angle)
        print(f'Distance at angle {angle}: {distance} cm')
        if distance and 0 < distance < GRID_SIZE:
            angle = np.radians(angle)
            x = int(current_position[0] + distance * np.cos(angle)) 
            y = int(current_position[1] + distance * np.sin(angle))
            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                print(f'Obstacle at {x}, {y}')
                scan_map[y, x] = 1


def follow_path(path):
    current_position = GRID_CENTER
    for next_cell in path[1:]:
        dx = next_cell[0] - current_position[0]
        dy = GRID_CENTER[1] - next_cell[1]
        angle_desired = math.degrees(math.atan2(dy, dx))
        angle_difference = (angle_desired - current_angle + 180) % 360 - 180
        print(f'Current angle: {current_angle}, Desired angle: {angle_desired} ')

        if abs(angle_difference) > defaults.ANGLE_THRESHOLD:
            car.move_left(angle_difference) if angle_difference else car.move_right(angle_difference)
            current_angle = (current_angle + angle_difference) % 360
        car.move_forward()
        current_position = next_cell
        print(f'Moved to {current_position}')


def display_map():
    plt.imshow(scan_map, cmap='gray')
    plt.title("Environment Map")
    plt.show()


if __name__ == "__main__":
    print(f'Starting mapping...')

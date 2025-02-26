import cv2
import numpy as np
import time
import heapq
import picar_4wd.helpers as defaults
import picar_4wd.helpers.navigation as car
import advanced_mapping as mapping
import object_detection as detect
from types import SimpleNamespace

camera = cv2.VideoCapture(0)
GOAL = (75, 25)


def reconstruct_path(past, present):
    path = []
    while present in past:
        present = past[present]
        path.append(present)


def compute_a_star(start, goal):
    grid = mapping.scan_map
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_cell_list = []
    heapq.heappush(open_cell_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    visited = set()
    
    while open_cell_list:
        _, current = heapq.heappop(open_cell_list)

        if current == goal:
            reconstruct_path(came_from, current)

        for direction in mapping.DIRECTION:
            dx, dy = direction.value
            here = SimpleNamespace(x = current[0], y = current[1])
            neighbor = (here.x + dx, here.y + dy)
            there = SimpleNamespace(x = neighbor[0], y = neighbor[1])

            x_coord_within_grid = 0 <= there.x < mapping.GRID_SIZE
            y_within_grid = 0 <= there.y < mapping.GRID_SIZE
            neighbor_accessible = grid[there.y][there.x] == 1
            tentative_g_score = g_score[current] + 1
            neighbor_g_score = g_score[neighbor]
            neighbor_advantage = tentative_g_score < neighbor_g_score

            if x_coord_within_grid and y_within_grid:
                if neighbor_accessible or (neighbor in visited and not neighbor_advantage):
                    continue
                if neighbor_advantage:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_cell_list, (f_score[neighbor], neighbor))
    return None


print(f'Starting autonomous driving...')
while True:
    ret, frame = camera.read()
    if not camera.isOpened():
        print('Camera not detected.')
        break
    if not ret:
        print('Unable to capture frame.')
        continue

    mapping.build_grid()
    detect.detected_stop_sign()
    path = compute_a_star(tuple(mapping.current_position), GOAL)
    mapping.follow_path(path)

camera.release()
cv2.destroyAllWindows()
car.stop()
print("Full Autonomy Stopped.")

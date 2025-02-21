import cv2
import numpy as np
import time
import heapq
import picar_4wd.helpers as defaults
import picar_4wd.helpers.navigation as car
import picar_4wd.helpers.visuals as scan
from tools import advanced_mapping as mapping
from tools import object_detection as detect
from types import SimpleNamespace

cap = cv2.VideoCapture(0)
goal_position = (75, 75)


def compute_a_prime(start, goal, grid):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_list = [(0, start)]
    came_from, g_score, f_score = {}, {start: 0}, {start: heuristic(start, goal)}
    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            route = []
            while current in came_from:
                route.append(current)
                current = came_from[current]
            return route[::-1]

        for direction in mapping.DIRECTION:
            dx, dy = direction.value
            here = SimpleNamespace(x = current[0], y = current[1])
            neighbor = (here.x + dx, here.y + dy)
            there = SimpleNamespace(x = neighbor[0], y = neighbor[1])

            x_coord_within_grid = 0 <= there.x < mapping.GRID_SIZE
            y_within_grid = 0 <= there.y < mapping.GRID_SIZE
            neighbor_accessible = grid[neighbor[1]][neighbor[0]] == 0

            if x_coord_within_grid and y_within_grid and neighbor_accessible:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
    return []


print(f'Starting autonomous driving...')
while True:
    ret, frame = cap.read()

    if not ret:
        continue
    image = cv2.resize(frame, (detect.height, detect.width))
    image = np.expand_dims(image, axis=0).astype(np.float32)
    detect.interpreter.set_tensor(detect.images['index'], image)
    detect.interpreter.invoke()
    boxes, classes, scores, detections = (detect.interpreter.get_tensor(detect.output_details[i]['index']) for i in range(4))

    detected_stop = any(
        'stop sign' in detect.labels[int(classes[0][i])].lower() for i in range(len(scores[0])) if scores[0][i] > 0.5
    )

    for angle in mapping.SCAN_ANGLES:
        distance = scan.get_distance_at(angle)
        if 0 < distance < mapping.GRID_SIZE:
            x, y = int(mapping.car_position[0] + distance * np.cos(np.radians(angle))), int(
                mapping.car_position[1] + distance * np.sin(np.radians(angle)))
            if 0 <= x < mapping.GRID_SIZE and 0 <= y < mapping.GRID_SIZE:
                mapping.scan_map[y, x] = 1
                defaults.set_config(f'obstacle_{x}_{y}', 1)

    if scan.get_flat_distance() < 20:
        print('Obstacle detected! Stopping.')
        car.stop()
        time.sleep(2)
        car.move_forward(30)
    if detected_stop:
        print('Stopping for stop sign.')
        car.stop()
        time.sleep(3)
        car.move_forward(40)
    path = compute_a_prime(tuple(mapping.car_position), goal_position, mapping.scan_map)
    if path:
        mapping.car_position = list(path[0])
        car.move_forward(40)
    cv2.imshow('PiCar-4WD Autonomous Mode', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
car.stop()
print("Full Autonomy Stopped.")

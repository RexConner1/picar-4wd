import cv2
import heapq
from picar_4wd.helpers.navigation import stop
from advanced_mapping import Mapping, DIRECTION
from object_detection import Detect
from types import SimpleNamespace

GOAL = (75, 25)

class Drive:
    def __init__(self):
        self.mapping = Mapping()
        self.detect = Detect()
        self.detect.detect()


    def reconstruct_path(self, past, present):
        new_path = []
        while present in past:
            present = past[present]
            new_path.append(present)
        new_path.reverse()
        return new_path


    def compute_a_star(self, start, goal):
        a_star_path = None
        grid = self.mapping.scan_map
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
                a_star_path = self.reconstruct_path(came_from, current)

            for direction in DIRECTION:
                dx, dy = direction.value
                here = SimpleNamespace(x = current[0], y = current[1])
                neighbor = (here.x + dx, here.y + dy)
                there = SimpleNamespace(x = neighbor[0], y = neighbor[1])

                x_coord_within_grid = 0 <= there.x < self.mapping.GRID_SIZE
                y_within_grid = 0 <= there.y < self.mapping.GRID_SIZE

                if x_coord_within_grid and y_within_grid:
                    tentative_g_score = g_score[current] + 1
                    neighbor_g_score = g_score.get(neighbor, float('inf'))
                    neighbor_advantage = tentative_g_score < neighbor_g_score
                    neighbor_accessible = grid[there.y][there.x] == 1

                    if neighbor_accessible or (neighbor in visited and not neighbor_advantage):
                        continue
                    if neighbor_advantage:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        heapq.heappush(open_cell_list, (f_score[neighbor], neighbor))

        return a_star_path


if __name__ == '__main__':
    print(f'Starting autonomous driving...')

    car = Drive()

    while True:
        ret, frame = car.detect.camera.read()
        if not car.detect.camera.isOpened():
            print('Camera not detected.')
            break
        if not ret:
            print('Unable to capture frame.')
            continue

        car.mapping.build_grid()
        car.detect.detected_stop_sign()
        path = car.compute_a_star(tuple(car.mapping.current_position), GOAL)
        car.mapping.follow_path(path)

    car.detect.camera.release()
    cv2.destroyAllWindows()
    stop()

    print("Full Autonomy Stopped.")

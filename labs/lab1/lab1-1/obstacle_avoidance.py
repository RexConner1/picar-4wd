import time
import random
import picar_4wd as fc
from enum import Enum

SENSOR_ADJUST = -36  # To achieve a 0-degree ultrasonic sensor
OBSTACLE_THRESHOLD = 10  # In cm
BACKUP_TIME = 1.0  # In seconds
TURN_TIME = 1.0  # In seconds
FORWARD_SPEED = 25  # Motor speed (0-100)
BACKUP_SPEED = 25  # Reverse speed (0-100)


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"


def get_distance(degrees = SENSOR_ADJUST):
    return fc.get_distance_at(degrees)


def move_forward():
    fc.forward(FORWARD_SPEED)
    time.sleep(0.1)


def stop():
    fc.stop()


def move_backward():
    fc.backward(BACKUP_SPEED)
    time.sleep(BACKUP_TIME)
    stop()


def turn_random():
    direction = random.choice([Direction.LEFT, Direction.RIGHT])
    fc.turn_left(FORWARD_SPEED) if direction == Direction.LEFT else fc.turn_right(FORWARD_SPEED)
    time.sleep(TURN_TIME)
    stop()


def obstacle_avoidance():
    print("Starting obstacle avoidance...")

    while True:
        distance = get_distance()
        print(f"Distance: {distance:.2f} cm")

        if distance < OBSTACLE_THRESHOLD:
            print("Obstacle detected! Avoiding...")
            stop()
            move_backward()
            turn_random()

        move_forward()


if __name__ == "__main__":
    try:
        obstacle_avoidance()
    except KeyboardInterrupt:
        print("\nStopping obstacle avoidance ...")
        stop()

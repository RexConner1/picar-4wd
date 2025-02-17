import time
import random
import picar_4wd as car

OBSTACLE_THRESHOLD = 10  # In cm


def get_distance(degrees=car.SERVO_OFFSET):
    return car.get_distance_at(degrees)


def turn_random():
    direction = random.choice([car.DIRECTION.LEFT, car.DIRECTION.RIGHT])
    car.move_left() if direction == car.DIRECTION.LEFT else car.move_right()


def obstacle_avoidance():
    print("Starting obstacle avoidance...")

    while True:
        distance = get_distance()
        print(f"Distance: {distance:.2f} cm")

        if distance < OBSTACLE_THRESHOLD:
            print("Obstacle detected! Avoiding...")
            car.stop()
            car.move_backward()
            turn_random()

        car.move_forward()


if __name__ == "__main__":
    try:
        obstacle_avoidance()
    except KeyboardInterrupt:
        print("\nStopping obstacle avoidance ...")
        car.stop()

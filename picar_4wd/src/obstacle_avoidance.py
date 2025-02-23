import random
import picar_4wd.helpers as defaults
import picar_4wd.helpers.navigation as car
import picar_4wd.helpers.visuals as scan


def turn_random():
    direction = random.choice([car.MOVE.LEFT, car.MOVE.RIGHT])
    car.move_left() if direction == car.MOVE.LEFT else car.move_right()


def obstacle_avoidance():
    print("Starting obstacle avoidance...")

    while True:
        distance = scan.get_flat_distance()
        print(f"Distance: {distance:.2f} cm")

        if distance < defaults.OBSTACLE_THRESHOLD:
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

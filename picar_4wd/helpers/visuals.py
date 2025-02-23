import picar_4wd as car

def get_flat_distance():
    return get_distance_at(0)


def get_distance_at(angle):
    return car.get_distance_at(angle)

#uses matric rotation derivation to rotate passed cordinates into a local frame
#if the leg is mounted at an angle, then getting it to push the robot forward means the passed xy coordinates must be rotated. 

import math

def rotate_point(x, y, rotation_deg):
    angle_rad = math.radians(rotation_deg)

    x_prime = x * math.cos(angle_rad) - y * math.sin(angle_rad)
    y_prime = x * math.sin(angle_rad) + y * math.cos(angle_rad)

    return x_prime, y_prime
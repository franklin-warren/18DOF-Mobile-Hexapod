#uses matric rotation derivation to rotate passed cordinates into a local frame
#if the leg is mounted at an angle, then getting it to push the robot forward means the passed xy coordinates must be rotated. 

import math

def rotate_point(x, y, rotation_deg):
    angle_rad = math.radians(rotation_deg)
    cos = math.cos(angle_rad)
    sin = math.sin(angle_rad)

    x_prime = x * cos - y * sin
    y_prime = x * sin + y * cos

    return x_prime, y_prime
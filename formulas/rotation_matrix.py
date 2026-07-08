#uses matric rotation derivation to rotate passed cordinates into a local frame
#if the leg is mounted at an angle, then getting it to push the robot forward means the passed xy coordinates must be rotated. 

import math

def rotate_x(x, y, angle_deg):
    angle_rad = math.radians(angle_deg)
    x_prime = x * math.cos(angle_rad) - y * math.sin(angle_rad)
    
    return(x_prime)

def rotate_y(x, y, angle_deg):
    angle_rad = math.radians(angle_deg)
    y_prime = y * math.sin(angle_rad) + x * math.cos(angle_rad)

    return(y_prime)


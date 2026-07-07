import math 

def law_of_cosines_SAS(a, theta_c_degrees, b):
    #c^2 = a^2 + b^2 - 2ab·cosC
    theta_c_radians = math.radians(theta_c_degrees)

    c =  math.sqrt(math.pow(a, 2) + math.pow(b, 2) - 2 *a*b* math.cos(theta_c_radians))
    return c

def law_of_cosines_SSS(a, b, c):
    #theta_c = arccos((a^2 + b^2 -c^2)/(2ab))

    theta_c_radians = math.acos((math.pow(a, 2) + math.pow(b, 2) - math.pow(c, 2)) / (2*a*b))

    return theta_c_radians
import math
from law_of_cosines import law_of_cosines_SAS, law_of_cosines_SSS 

#see project journal for diagrams and derivations
#all numbers in mm, angles in radians, but converted to degrees at the end for servo movement. 

#link lengths
coxa = 50
femur= 85
tibia = 160

def inverse_kinematics_theta_c (x, y, z):
    theta_c = math.atan2 (y, x)
    theta_c_degrees = math.degrees(theta_c)
    if -70 <= theta_c_degrees <= 70:
        return theta_c_degrees
    else:
        return None
    
        

def inverse_kinematics_theta_f (x, y, z):
    R = math.sqrt(x**2 + y**2) #overall "radius"  ie straight line distance of entire leg. 
    f_t_hyp = math.sqrt((R-coxa)**2 + z**2) #d on derivation

    A = law_of_cosines_SSS(f_t_hyp, femur, tibia)
    alpha = math.atan2(z, (R-coxa))
    theta_f = A - alpha
    theta_f_degrees = math.degrees(theta_f)

    if -90<= theta_f_degrees <=90:
        return theta_f_degrees
    else:
        return None
    
    


def inverse_kinematics_theta_t (x, y, z):

    R = math.sqrt(x**2 + y**2) #overall "radius"  ie straight line distance of entire leg. 
    f_t_hyp = math.sqrt((R-coxa)**2 + z**2) #d on derivation
    beta = law_of_cosines_SSS (tibia, femur, f_t_hyp) #B on derivation

    theta_t = math.pi - beta #supplementary 
    theta_t_degrees = math.degrees(theta_t)

    if -100 <= theta_t_degrees <=100:
        return theta_t_degrees
    else:
        return None
    
    



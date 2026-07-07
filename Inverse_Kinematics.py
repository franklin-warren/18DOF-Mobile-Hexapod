import math
from law_of_cosines import law_of_cosines_SAS, law_of_cosines_SSS 

#see project journal for diagrams and derivations
#all numbers in mm, angles in radians, but converted to degrees at the end for servo movement. 

#link lengths
coxa = 50
femur= 85
tibia = 165

def get_leg_angles (x, y, z):

    #Step 1: COXA ANGLE 
    theta_c = math.atan2 (y, x)
    theta_c_degrees = math.degrees(theta_c)

    if not -70<= theta_c_degrees <= 70: # will break joint
        return None
    
    # R and D from derivation
    R = math.sqrt(x**2 + y**2) #overall "radius"  ie straight line distance of entire leg. 
    f_t_hyp = math.sqrt((R-coxa)**2 + z**2) #d on derivation    

    #check if the leg is inside itself or cant reach the point
    if f_t_hyp > (femur + tibia) or f_t_hyp < abs(femur-tibia):
        return None
    
    #Step 2: FEMUR ANGLE
    A = law_of_cosines_SSS(f_t_hyp, femur, tibia)
    alpha = math.atan2(abs(z), (R-coxa)) #forces alpha into a positive triangle

    if z > 0:
        theta_f = A + alpha #add when pointing UP
    else:
        theta_f = A-alpha #subtract when pointing DOWN
    
    theta_f_degrees = (math.degrees(theta_f))

    if not -90<= theta_f_degrees <=90: 
        return None

    #Step 3: TIBIA ANGLE
    beta = law_of_cosines_SSS (tibia, femur, f_t_hyp) #B on derivation

    theta_t = math.pi - beta #supplementary 

    theta_t_degrees = -abs(math.degrees(theta_t)) #makes knee bend properly


    if not -125 <= theta_t_degrees <=45: #mounted tibia at offset, so when the 180 degree servo is at 135 degrees leg is horizontal
        return None
    
    return theta_c_degrees, theta_f_degrees, theta_t_degrees 
    

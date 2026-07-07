import math
import time
from Inverse_Kinematics import get_leg_angles
from hexapod_servo_config import move_servo, RF_coxa, RF_femur, RF_tibia


def move_servo_xyz(x, y, z):

    angles = get_leg_angles(x, y, z) 

    if angles is not None:
        coxa, femur, tibia = angles

        move_coxa = (coxa)+135
        move_femur = (135 - (femur))
        move_tibia = (135  + (tibia))

        print("Position: ", "(", x,",", y,",", z, ")")

        print("Coxa angle: ", (coxa))
        move_servo(RF_coxa, move_coxa)
        print("Coxa moved to: ", move_coxa)

        print("Femur angle: ", (femur))
        move_servo(RF_femur, move_femur)
        print("Femur moved to: ", move_femur)

        print("Tibia angle: ", (tibia))
        move_servo(RF_tibia, move_tibia)
        print("Tibia moved to: ", move_tibia)
    else:
        print("Position: ", "(", x,",", y,",", z, ")")
        print("Out of Reach")

move_servo_xyz(300, -0, -0)

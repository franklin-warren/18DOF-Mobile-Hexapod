import time
from hexapod_servo_config import *

def home_servos():

    print("homing servos")
    move_servo(RM_coxa, 135)
    time.sleep_ms(150)

    move_servo(RM_femur, 135)
    time.sleep_ms(150)

    move_servo(RM_tibia, 135)
    time.sleep_ms(150)

    print("servos homed")

home_servos()
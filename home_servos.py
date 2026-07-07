import time
from hexapod_servo_config import move_servo, RF_coxa, RF_femur, RF_tibia

def home_servos():

    print("homing servos")
    move_servo(RF_coxa, 135)
    time.sleep_ms(150)

    move_servo(RF_femur, 135)
    time.sleep_ms(150)

    move_servo(RF_tibia, 135)
    time.sleep_ms(150)

    print("servos homed")

home_servos()
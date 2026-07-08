from hexapod_servo_config import *

def move_leg(leg_prefix, coxa_deg, femur_deg, tibia_deg):
    leg_joints = right_servos[leg_prefix]

    move_servo(leg_joints['coxa'], (coxa_deg)+135)
    move_servo(leg_joints['femur'], 135-femur_deg)
    move_servo(leg_joints['tibia'], tibia_deg+135)


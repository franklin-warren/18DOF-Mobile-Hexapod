import math
import time
from hexapod_servo_config import move_servo, RF_coxa, RF_femur, RF_tibia
from Inverse_Kinematics import get_leg_angles

#the goal: a straight line along z=0, y=0. movement in the x direction. 

#centre servos 
print("centering sevros")
move_servo(RF_coxa, 135) #greater than 135 left less right
time.sleep_ms(150)

move_servo(RF_femur, 135) #greater than 135 down less up 
time.sleep_ms(150)

move_servo(RF_tibia, 90) # greater than 90 up less down
time.sleep_ms(150)

print("servos centered")

for i in range (0, 20, 1):

    angles= get_leg_angles(295-i, 0, 0)

    if angles is None:
        print("skipping, out of reach")
        continue
    else:
        coxa, femur, tibia = angles

    coxa = round(coxa)
    femur = round(femur)
    tibia= round(tibia)

    print("Position:")
    print(295-i)
    print(coxa + 135)
    print(femur - 135)
    print(tibia + 90)
    move_servo(RF_coxa, coxa + 135)
    move_servo(RF_femur, femur - 135)
    move_servo(RF_tibia, tibia + 90)

    time.sleep_ms(300)

   
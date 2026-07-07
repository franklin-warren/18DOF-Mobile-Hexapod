import time
from hexapod_servo_config import RF_coxa, RF_femur, RF_tibia, move_servo
from home_servos import home_servos

home_servos()

#coxa: max= 135+70 right; min= 135-70 left. 
#femur: max = 135-90 up; min = 135+90 down. 
#tibia: max = 90 + 100 (90) up; min = 90-100 (90) down (servo limit is 90 degrees hardware is 100)

rest = 2
#coxa
for i in range (135, 205, 1):
    move_servo(RF_coxa, i)
    time.sleep_ms(rest)

for i in range (205, 65, -1):
    move_servo(RF_coxa, i)
    time. sleep_ms(rest)

for i in range (65, 135, 1):
    move_servo(RF_coxa, i)
    time.sleep_ms(rest)

#femur
for i in range (135, 45, -1):
    move_servo(RF_femur, i)
    time.sleep_ms(rest)

for i in range (45, 225, 1):
    move_servo(RF_femur, i)
    time. sleep_ms(rest)

for i in range (225, 135, -1):
    move_servo(RF_femur, i)
    time.sleep_ms(rest)

#tibia
for i in range (90, 180, 1):
    move_servo(RF_tibia, i)
    time.sleep_ms(rest)

for i in range (180, 0, -1):
    move_servo(RF_tibia, i)
    time. sleep_ms(rest)

for i in range (0, 90, 1):
    move_servo(RF_tibia, i)
    time.sleep_ms(rest)

#very cool leg stance
move_servo(RF_coxa, 135+15)
move_servo(RF_femur, 135-35)
move_servo(RF_tibia, 90-85)
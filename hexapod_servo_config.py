from machine import Pin, I2C
import pca9685
import servo
import time

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)

#right legs
right_board_270 = servo.Servos(i2c, address=0x40, freq=50, min_us=500, max_us=2500, degrees=270)

# #left legs
# left_board_270 = servo.Servos(i2c, address=0x41, freq=200, min_us=500, max_us=2500, degrees=270)

#leg setup. R= right, L= left, F= front, M= middle, B=back
RF_coxa = (right_board_270, 6)
RF_femur = (right_board_270, 7)
RF_tibia = (right_board_270, 8)

RM_coxa = (right_board_270, 3)
RM_femur = (right_board_270, 4)
RM_tibia = (right_board_270, 5)

RB_coxa = (right_board_270, 0)
RB_femur = (right_board_270, 1)
RB_tibia = (right_board_270, 2)

# LF_coxa = (left_board_270, 0)
# LF_femur = (left_board_270, 1)
# LF_tibia = (left_board_270, 2)

# LM_coxa = (left_board_270, 3)
# LM_femur = (left_board_270, 4)
# LM_tibia = (left_board_270, 5)

# LB_coxa = (left_board_270, 6)
# LB_femur = (left_board_270, 7)
# LB_tibia = (left_board_270, 8)

def move_servo(joint, degrees):
    board= joint[0] #left or right board
    channel= joint[1] #location of motor (0-15) on PCA
    board.position(channel, degrees=degrees)

right_servos = {
    'RF': {"coxa": (right_board_270, 6), "femur": (right_board_270, 7), "tibia": (right_board_270, 8)}, 
    'RM': {"coxa": (right_board_270, 3), "femur": (right_board_270, 4), "tibia": (right_board_270, 5)}, 
    'RB': {"coxa": (right_board_270, 0), "femur": (right_board_270, 1), "tibia": (right_board_270, 2)}
}
#eventually, I have to offload the math to a computer, as steps have to be calculated in real time. 
#for the sake of testing, I need two legs to trace the same path. THey must not interfere in standard gait
#To not absolutly cook my esp32, this program sets up nessesary joint angles ahead of time
#those angles are then simply called by the esp in the loop as it runs. 
#initial setup may take a while, but this should allow the legs to run quickly at a high freqency (200+ hz) for smoothness

from formulas.cycloid_formula import calculate_cycloid
from formulas.Inverse_Kinematics import get_leg_angles

from formulas.rotation_matrix import rotate_x, rotate_y
from hexapod_servo_config import *
from move_leg import move_leg

from move_servo_xyz import move_servo_xyz
step_time = 0.75 #T
half_step_time = step_time/2 #splits entire function into rise and fall
step_static_x_pos = 150

#resolution: MATCH TO SERVO CONFIG FREQ PARAMETER!!! Higher resolution increases compute time
resolution = int(half_step_time * 200) #number is freq
delay_time = half_step_time/resolution
delay_time_ns = int(delay_time * 1_000_000_000) 


step_z_naught_rise = -125
step_z_final = -125
H_rise = 30 #how big ar steps
s_final_rise = step_z_naught_rise + H_rise
step_z_naught_fall = s_final_rise

step_y_naught = -75
step_y_final  = 75
y_middle_step = (step_y_naught + step_y_final)/2

z_pos_rise = calculate_cycloid(step_z_naught_rise, s_final_rise, half_step_time, resolution)
z_pos_fall = calculate_cycloid(step_z_naught_fall, step_z_final, half_step_time, resolution)

#region calculate cycloid for each leg
#RB (rotation of -30 degrees)
RB_rot = -30
y_pos_rb_rise = calculate_cycloid(rotate_y(step_static_x_pos, step_y_naught, RB_rot), rotate_y(step_static_x_pos, y_middle_step, RB_rot), half_step_time, resolution)
y_pos_rb_fall = calculate_cycloid(rotate_y(step_static_x_pos, y_middle_step, RB_rot), rotate_y(step_static_x_pos, step_y_final, RB_rot), half_step_time, resolution)
y_pos_rb_stance = calculate_cycloid(rotate_y(step_static_x_pos, step_y_final, RB_rot), rotate_y(step_static_x_pos, step_y_naught, RB_rot), 2* half_step_time, 2 * resolution)

#RM (no rotation)
y_pos_rm_rise = calculate_cycloid(step_y_naught, y_middle_step, half_step_time, resolution)
y_pos_rm_fall = calculate_cycloid(y_middle_step, step_y_final, half_step_time, resolution)
y_pos_rm_stance = calculate_cycloid(step_y_final, step_y_naught, 2 * half_step_time, 2 * resolution)
#endregion

#region compute joint angles and save into list
rb_angles_rise = []
for i in range (len(y_pos_rb_rise)):
    x_prime = rotate_x(step_static_x_pos, y_pos_rb_rise[i], RB_rot)
    angles = get_leg_angles(x_prime, y_pos_rb_rise[i], z_pos_rise[i])
    rb_angles_rise.append(angles)

rb_angles_fall = []
for i in range (len(y_pos_rb_fall)):
    x_prime = rotate_x(step_static_x_pos, y_pos_rb_fall[i], RB_rot)
    angles = get_leg_angles(x_prime, y_pos_rb_fall[i], z_pos_fall[i])
    rb_angles_fall.append(angles)

rb_angles_stance = []
for i in range (len(y_pos_rb_stance)):
    x_prime = rotate_x(step_static_x_pos, y_pos_rb_stance[i], RB_rot)
    angles = get_leg_angles(x_prime, y_pos_rb_stance[i], step_z_final)
    rb_angles_stance.append(angles)

rm_angles_rise = []
for i in range (len(y_pos_rm_rise)):
    angles = get_leg_angles(step_static_x_pos, y_pos_rm_rise[i], z_pos_rise[i])
    rm_angles_rise.append(angles)

rm_angles_fall = []
for i in range (len(y_pos_rm_fall)):
    angles = get_leg_angles(step_static_x_pos, y_pos_rm_fall[i], z_pos_fall[i])
    rm_angles_fall.append(angles)

rm_angles_stance = []
for i in range (len(y_pos_rm_stance)):
    angles = get_leg_angles(step_static_x_pos, y_pos_rm_stance[i], step_z_final)
    rm_angles_stance.append(angles)
#endregion

rm_swing_angles = rm_angles_rise + rm_angles_fall
rb_swing_angles = rb_angles_rise + rb_angles_fall
substeps_per_phase = 2*resolution

tripod_A = [ #will be RF LM and RB
    ('RB', rb_swing_angles, rb_angles_stance),
]
tripod_B = [ #will be LF RM and LB
    ('RM', rm_swing_angles, rm_angles_stance)
]

current_phase = 'A_swing_B_stance'
substeps_taken = 0
while True:
    if current_phase == 'A_swing_B_stance':

        current_time = time.time_ns()
        if (current_time-last_time)>=delay_time_ns:

            for leg, swing, stance in tripod_A:
                move_leg(leg, *swing[substeps_taken])
            for leg, swing, stance in tripod_B:
                move_leg(leg, *stance[substeps_taken])
            last_time = current_time
            substeps_taken += 1

            if substeps_taken >= substeps_per_phase:
                substeps_taken = 0
                current_phase = 'A_stance_B_swing'
    
    elif current_phase == 'A_stance_B_swing':
        current_time = time.time_ns()
        if (current_time-last_time)>=delay_time_ns:

            for leg, swing, stance in tripod_A:
                move_leg(leg, *stance[substeps_taken])
            for leg, swing, stance in tripod_B:
                move_leg(leg, *swing[substeps_taken])
            last_time = current_time
            substeps_taken += 1

            if substeps_taken >= substeps_per_phase:
                substeps_taken = 0
                current_phase = 'A_swing_B_stance'

    








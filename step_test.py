import time
from Inverse_Kinematics import get_leg_angles
from move_servo_xyz import move_servo_xyz
from cycloid_formula import calculate_cycloid

time.sleep_ms(10) #allows servos to get to postion
step_time = 0.75 #T
half_step_time = step_time/2 #splits entire function into rise and fall
step_static_x_pos = 170

#resolution: (MUST be capped at 50hz ie steps per second is 50)
resolution = int(half_step_time * 50)
delay_time = half_step_time/resolution


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

y_pos_rise = calculate_cycloid(step_y_naught, y_middle_step, half_step_time, resolution)
y_pos_fall = calculate_cycloid(y_middle_step, step_y_final, half_step_time, resolution)

y_pos_stance = calculate_cycloid(step_y_final, step_y_naught, 2* half_step_time, 2 * resolution)

current_resolution_substep_rise = 0
current_resolution_substep_fall = 0
current_resolution_substep_stance = 0


move_servo_xyz(step_static_x_pos, y_pos_rise[current_resolution_substep_rise], z_pos_rise[current_resolution_substep_rise]) #puts leg at start of step
current_resolution_substep_rise = current_resolution_substep_rise + 1
last_time = time.ticks_ms()
current_time = time.ticks_ms()
step_stage = 'rise'

while True:
    current_time = time.ticks_ms()

    if step_stage == 'rise':
        if time.ticks_diff(current_time, last_time) >= delay_time:
            move_servo_xyz(step_static_x_pos, y_pos_rise[current_resolution_substep_rise], z_pos_rise[current_resolution_substep_rise]) 
            current_resolution_substep_rise = current_resolution_substep_rise + 1
            last_time = time.ticks_ms()
            
        if current_resolution_substep_rise >= len(z_pos_rise):
            step_stage = 'fall'
            current_resolution_substep_rise = 0
            #moves into zero position of next phase (elimiates double zero pause)
            move_servo_xyz(step_static_x_pos, y_pos_fall[current_resolution_substep_fall], z_pos_fall[current_resolution_substep_fall]) 
            current_resolution_substep_fall = current_resolution_substep_fall + 1
    
    if step_stage == 'fall':
        if time.ticks_diff(current_time, last_time) >= delay_time:
            move_servo_xyz(step_static_x_pos, y_pos_fall[current_resolution_substep_fall], z_pos_fall[current_resolution_substep_fall]) 
            current_resolution_substep_fall = current_resolution_substep_fall + 1
            last_time = time.ticks_ms()

        if current_resolution_substep_fall >= len(z_pos_fall):
            step_stage = 'stance'
            current_resolution_substep_fall = 0
            #moves into zero position of next phase (elimiates double zero pause)
            move_servo_xyz(step_static_x_pos, y_pos_stance[current_resolution_substep_stance], step_z_final)
            current_resolution_substep_stance = current_resolution_substep_stance + 1
            
    
    if step_stage == 'stance':
        if time.ticks_diff(current_time, last_time) >= delay_time:
            move_servo_xyz(step_static_x_pos, y_pos_stance[current_resolution_substep_stance], step_z_final)
            current_resolution_substep_stance = current_resolution_substep_stance + 1
            last_time = time.ticks_ms()
        if current_resolution_substep_stance >= len(y_pos_stance):
            step_stage = 'rise'
            current_resolution_substep_stance = 0
            #moves into zero position of next phase (elimiates double zero pause)
            move_servo_xyz(step_static_x_pos, y_pos_rise[current_resolution_substep_rise], z_pos_rise[current_resolution_substep_rise]) 
            current_resolution_substep_rise = current_resolution_substep_rise + 1





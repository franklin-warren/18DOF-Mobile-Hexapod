import time
from formulas.rotation_matrix import rotate_point
from formulas.cycloid_formula import calculate_cycloid
from formulas.Inverse_Kinematics import get_leg_angles
from move_leg import move_leg

#region SETUP
step_time = 0.75 #T
half_step_time = step_time/2 #splits entire function into rise and fall
step_static_x_pos = 150

#resolution: MATCH TO SERVO CONFIG FREQ PARAMETER!!! Higher resolution increases compute time
resolution = int(half_step_time * 50) #number is <=freq
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

RB_rot = -30
RB_comp = -RB_rot
#endregion

#region CYCLOIDS
z_pos_rise = calculate_cycloid(step_z_naught_rise, s_final_rise, half_step_time, resolution)
z_pos_fall = calculate_cycloid(s_final_rise, step_z_final, half_step_time, resolution)

y_pos_rise = calculate_cycloid(step_y_naught, y_middle_step, half_step_time, resolution)
y_pos_fall = calculate_cycloid(y_middle_step, step_y_final, half_step_time, resolution)
y_pos_stance = calculate_cycloid(step_y_final, step_y_naught, 2*half_step_time, 2*resolution)

z_pos_swing = z_pos_rise + z_pos_fall[1:]
y_pos_swing = y_pos_rise + y_pos_fall[1:]
y_pos_stance = y_pos_stance

# print(len(z_pos_swing)) #all should equal the same number
# print(len(y_pos_stance))
# print(len(y_pos_swing))

#endregion

#region INVERSE KINEMATICS
print("starting inverse kinematics")

#right middle: no rotation
RM_swing_angles = []
RM_stance_angles = []
for i in range(len(z_pos_swing)):
    angles = get_leg_angles(step_static_x_pos, y_pos_swing[i], z_pos_swing[i])
    if angles is not None:
        RM_swing_angles.append(angles)
    else:
        print("RM swing substep", i, "returned None at position (", step_static_x_pos, y_pos_swing[i], z_pos_swing[i], ")")
        RM_swing_angles.append(RM_swing_angles[-1]) #makes copy so final lists are equal in length: avoids phase shifting #EDGE CASE IF FIRST SUBSTEP FAILS INDEX ERROR WILL HAPPEN
for i in range (len(y_pos_stance)):
    angles = get_leg_angles(step_static_x_pos, y_pos_stance[i], step_z_final)
    if angles is not None:
        RM_stance_angles.append(angles)
    else: 
        print("RM stance substep", i, "returned None at position (", step_static_x_pos, y_pos_stance[i], step_z_final, ")")
        RM_stance_angles.append(RM_stance_angles[-1])#makes copy so final lists are equal in length: avoids phase shifting

#right back: rotated RB_angle. To compensate, the positions must be rotated -RB angle
RB_rotated_x_swing = []
RB_rotated_y_swing = []
RB_rotated_x_stance = []
RB_rotated_y_stance = []
RB_swing_angles = []
RB_stance_angles = []

local_delta_x = 0 #unrotated, x should change by this much over the course of the step. If cycloid list for x, local_delta_x = list[i]
y_offset = 0
for i in range(len(y_pos_swing)):
    target_x, target_y = rotate_point(local_delta_x, y_pos_swing[i], RB_comp)
    RB_rotated_x_swing.append(target_x + step_static_x_pos)
    RB_rotated_y_swing.append (target_y + y_offset)

for i in range (len(y_pos_stance)):
    target_x, target_y = rotate_point(local_delta_x, y_pos_stance[i], RB_comp)
    RB_rotated_x_stance.append(target_x + step_static_x_pos)
    RB_rotated_y_stance.append (target_y + y_offset)

for i in range (len(RB_rotated_x_swing)):
    angles = get_leg_angles(RB_rotated_x_swing[i], RB_rotated_y_swing[i], z_pos_swing[i])
    if angles is not None:
        RB_swing_angles.append(angles)
    else:
        print("RB swing substep", i, "returned None at position (", RB_rotated_x_swing[i], RB_rotated_y_swing[i], z_pos_swing[i], ")")
        RB_swing_angles.append(RB_swing_angles[-1])

for i in range (len(RB_rotated_x_stance)):
    angles = get_leg_angles(RB_rotated_x_stance[i], RB_rotated_y_stance[i], step_z_final)
    if angles is not None:
        RB_stance_angles.append(angles)
    else:
        print("RB stance substep", i, "returned None at position (", RB_rotated_x_stance[i], RB_rotated_y_stance[i], step_z_final, ")")
        RB_swing_angles.append(RB_swing_angles[-1])

#endregion

#region MAIN LOOP

substeps_per_phase = len(y_pos_stance)
current_phase = 'A_swing_B_stance'
substeps_taken = 0
last_time = time.time_ns()

#tripod: leg prefix (RF RM RB LF LM LB), swing angles (as tuple), stance angles (as tuple)
tripod_A = [ #will be RF LM and RB
    ('RB', RB_swing_angles, RB_stance_angles),
]
tripod_B = [ #will be LF RM and LB
    ('RM', RM_swing_angles, RM_stance_angles)
]

while True:
    if current_phase == 'A_swing_B_stance':

        current_time = time.time_ns()
        if (current_time-last_time)>=delay_time_ns:

            for leg, swing, stance in tripod_A:
                target_angles = swing[substeps_taken]
                if target_angles is not None:
                    move_leg(leg, *target_angles)
                else: 
                    print("leg ", leg, "out of reach! skipping substep ", substeps_taken)
    
            for leg, swing, stance in tripod_B:
                target_angles = stance[substeps_taken]
                if target_angles is not None:
                    move_leg(leg, *target_angles)
                else: 
                    print("leg ", leg, "out of reach! skipping substep ", substeps_taken)
            last_time = current_time
            substeps_taken += 1

            if substeps_taken >= substeps_per_phase:
                substeps_taken = 0
                current_phase = 'A_stance_B_swing'
    
    elif current_phase == 'A_stance_B_swing':
        current_time = time.time_ns()
        if (current_time-last_time)>=delay_time_ns:

            for leg, swing, stance in tripod_A:
                target_angles = stance[substeps_taken]
                if target_angles is not None:
                    move_leg(leg, *target_angles)
                else:
                    print("leg ", leg, "out of reach! skipping substep ", substeps_taken)
            
            for leg, swing, stance in tripod_B:
                target_angles = swing[substeps_taken]
                if target_angles is not None:
                    move_leg(leg, *target_angles)
                else:
                    print("leg ", leg, "out of reach! skipping substep ", substeps_taken)

            last_time = current_time
            substeps_taken += 1

            if substeps_taken >= substeps_per_phase:
                substeps_taken = 0
                current_phase = 'A_swing_B_stance'

#endregion
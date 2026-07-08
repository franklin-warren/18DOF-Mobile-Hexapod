import time
from formulas.cycloid_formula import calculate_cycloid
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
z_rise = z_pos_rise + z_pos_fall [1:]
#region calculate cycloid for each leg
y_pos_stance = calculate_cycloid(step_y_final, step_y_naught, 2 * half_step_time, 2 * resolution)

print('z rise:', len(z_pos_rise))
print('z fall', len(z_pos_fall))
print("z rise", len(z_rise))
print("stance", len(y_pos_stance))
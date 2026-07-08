import time
import csv
from Inverse_Kinematics import get_leg_angles

max_reach = 600 #600mm a side cube, for +-300mm
resolution_mm = 3 #3mm/point
output_file = "hexapod_leg_workspace.csv" 

start_value = -max_reach
end_value = max_reach+1

reachable_count = 0
checked_count = 0

print("finding valid points")
print("checking with", resolution_mm, "mm resolution")
print("outputting sucsessful points to ", output_file)

start_time = time.time()

with open(output_file, mode ="w", newline= "") as f:
    writer = csv.writer(f)
    writer.writerow(["X", "Y", "Z"])

    for x in range(start_value, end_value, resolution_mm):
        for y in range(start_value, end_value, resolution_mm):
            for z in range(start_value, end_value, resolution_mm):
    
                checked_count = checked_count + 1

                result = get_leg_angles(x, y, z)

                if result is not None:
                    writer.writerow([x, y, z])
                    reachable_count = reachable_count + 1

end_time = time.time()
total_time = end_time - start_time
print("Finished")
print("Evaluated ", checked_count, "points in ", total_time, "seconds. ", reachable_count, "reachable points saved.") 









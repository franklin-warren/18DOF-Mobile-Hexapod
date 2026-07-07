import math

def calculate_cycloid(s_naught, s_final, T, resolution):
    positions = []
    if resolution != 0 and T != 0:
        for i in range(resolution+1):

            H = s_final-s_naught
            t= i * (T/resolution)
            s_current = s_naught + (H * ((t/T)-(1/(2*math.pi))*math.sin(((2*math.pi)/T)*t)))
            positions.append(s_current)

        return positions
    else:
        print("resolution or T cannot be zero")
        return []


def errorCalc(Tw, current_temp, tp, ti):
    error_sum = 0
    new_error = Tw - current_temp #Tw - t[n]
    error_sum += new_error
    e = (tp / ti) * error_sum


def heat_calculation(tp,ti):
    t = []
    e = []
    Tw = 1

    for n in range(10000) # in czas próbkowania
        new_error, I_term = errorCalc(Tw, t[-1], tp, ti)
        e.append(new_error)
        x = (Pw * I_term * tp) / (cv * d * s * h) + (1 - (Qout / (s * h))) * t[-1]
        t.append(x)








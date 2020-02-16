import numpy as np

"""Dynamic Time Warping Algorithm"""


def dynamicTime(s,t):
    n = len(s)
    m = len(t)
    DTW = np.empty((n,m))
    for i in range(1, n):
        cost = np.abs((s[i]-t[0]))
        DTW[i, 0] = cost + DTW[i-1, 0]
    for i in range(1, m):
        cost = np.abs((s[0]-t[i]))
        DTW[0, i] = cost + DTW[0, i-1]
    DTW[0, 0] = 0

    for i in range(1, n):
        for j in range(1, m):
            cost = np.abs((s[i]-t[j]))
            DTW[i, j] = cost + min(DTW[i-1, j], DTW[i, j-1], DTW[i-1, j-1])
    return DTW


def dtwdistance(array):
    r, c = array.shape
    r = r-1
    c = c-1
    cost = 0
    while r >= 0 and c >= 0:
        c_min = [array[r, c-1], array[r-1, c], array[r-1, c-1]]
        value = min(c_min)
        min_index = c_min.index(min(c_min))
        cost = cost + value
        if min_index == 0:
            c = c - 1
        if min_index == 1:
            r = r - 1
        if min_index == 2:
            r = r - 1
            c = c - 1
    return cost


def dynamicTimeWrappingCost(first_signal,second_signal):
    dtw = dynamicTime(first_signal,second_signal)
    cost = dtwdistance(dtw)
    return cost


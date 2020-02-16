import numpy as np
from scipy.fftpack import fft
from scipy.fftpack import ifft
import matplotlib.pyplot as plt
from peakdetect import peakdetect
from peakdetect import peakdetect
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter as savgf
import math as math
import dynamicTimeWarping as dynamicTW

"""Cost Signal"""
def dynamicTimeWrappingCost(array1, array2):
    cost = dynamicTW.dynamicTimeWrappingCost(array1, array2)
    return cost

"""Changing the list to 2D Array"""
def change_data(array):
    data = np.empty((len(array), 2), dtype=object)
    for i in range(len(data)):
        data[i][0] = array[i][0]
        data[i][1] = array[i][1]
    return data

"""absolute"""
def abs_return(array):
    for idx in range(len(array)):
        array[idx] = abs(array[idx])
    return array

"""Removing Spikes"""
def data_removal(array, remove_threshold = 10):
    array = np.array(array)
    r, c = array.shape
    array_new = []
    for idx in range(c - 1):
        temp = np.array(array[:, idx])
        max_val, min_val = peakdetect(temp, lookahead=31)
        max_data = change_data(max_val)
        min_data = change_data(min_val)
        max_pos = max_data[:, 0].astype(np.int)
        min_pos = min_data[:, 0].astype(np.int)
        max_value = max(max_data[:, 1])
        min_value = min(min_data[:, 1])
        # print(max_value)
        # print(min_value)
        max_average = sum(max_data[:, 1]) / len(max_data[:, 1])
        min_average = sum(min_data[:, 1]) / len(min_data[:, 1])
        # print('MAX_AVG::',max_average)
        # print('MIN_AVG::',min_average)
        idx_max = []
        idx_min = []
        r, k = array.shape
        for idx1 in range(r):
            if array[idx1, idx] >= remove_threshold * max_average:
                idx_max.append(idx1)
        for idx2 in range(r):
            if array[idx2, idx] <= remove_threshold * min_average:
                idx_min.append(idx2)

        #print('IDX_MAX::',idx_max)
        #print('IDX_MIN::', idx_min)
        if idx_max.__len__() > 0:
            for data in idx_max:
                temp[data] = max_average

        if idx_min.__len__() > 0:
            for data in idx_min:
                temp[data] = min_average

        array_new.append(temp)
        """
        if len(idx_max)!= 0:
            idx_max = np.array(idx_max)
            for data in idx_max:
                temp[data] = max_average
        if len(idx_min)!= 0:
            idx_min = np.array(idx_min)
            for data in idx_min:
                temp[data] = min_average
        """

   # print(np.array(array_new).shape)
    r1 , c1 = np.array(array_new).shape
    array_final = np.empty((c1, r1), dtype=float)
    for i in range(r1):
        array_final[:, i] = array_new[i][:]

    # plt.plot(np.arange(0,len(array[:,idx])),array[:,idx])
    # plt.scatter(max_pos,temp[max_pos],c="r")
    # plt.scatter(min_pos,temp[min_pos], c="g")

    # plt.figure(2)
    # plt.plot(np.arange(0, len(array[:, idx])), array[:,idx])
    # plt.show()

    return array

"""RMS"""
def rms(array):
    square_array = np.square(array)
    temp_array = np.sum(square_array)
    rms_val = temp_array / len(array)
    return rms_val

"""Crest Factor"""
def crest_feature(array, bmi):
    array = np.array(array)
    array = array * bmi
    r, c = array.shape
    cf = np.empty(c, dtype=float)
    for idx in range(c):
        rms_temp = rms(array[:, idx])
        abs_array = abs_return(array[:, idx])
        max_temp = max(abs_array)
        temp = max_temp / rms_temp
        if np.isnan(temp) != True or np.isinf(temp) != True:
            cf[idx] = temp
        else:
            print('0Inserted')
            cf[idx] = 0
    return cf

def single_crest_feature(array):
    array = np.array(array)
    r = array.size
    rms_temp = rms(array)
    abs_array = abs_return(array)
    max_temp = max(abs_array)
    cf = max_temp / rms_temp
    return cf

"""Correlation Feature"""
def correlation_feature(array1, array2):
    array1 = np.array(array1)
    array2 = np.array(array2)
    mean_array1 = np.mean(array1, axis=0)
    mean_array2 = np.mean(array2, axis=0)
    num1 = np.empty(len(array1), dtype=float)
    num2 = np.empty(len(array2), dtype=float)

    for idx in range(len(array1)):
        num1[idx] = array1[idx] - mean_array1
    for idx in range(len(array2)):
        num2[idx] = array2[idx] - mean_array2
    num = 0
    for idx in range(len(array1)):
        num = num + (num1[idx] * num2[idx])
    den1 = 0
    for idx in range(len(num1)):
        den1 = den1 + (num1[idx] ** 2)
    den2 = 0
    for idx in range(len(num2)):
        den2 = den2 + (num2[idx] ** 2)
    r_sum = num / ((den1 ** 0.5) * (den2 ** 0.5))
    return r_sum

"""Linear Interpolation"""
def filter_data(array):
    r, c = np.array(array).shape
    print(r, c)
    x_pos = np.linspace(0, r, num=r)
    x_pos.astype(int)
    for idx in range(c - 1):
        f = interp1d(x_pos, array[:, idx], kind='linear')
        y = f(x_pos)
        # plt.plot(x_pos,array[:,idx])
        array[:, idx] = savgf(y, polyorder=5, window_length=29)
        # plt.figure(3)
        # plt.plot(x_pos,array[:,idx])
        # plt.show()

    return array

"""Finding the MAX in 2D Array and corresponding IDX"""
def max_finder_change(array):
    max_data = max(array[:, 1])
    for i in range(len(array)):
        if array[i, 1] == max_data:
            max_idx = array[i, 0]
    return max_idx


""" IDX Finder is to Find the First Harmonic Wave"""
def idx_finder(array1):
    data = []
    print('array:', array1)
    [max_value, min_value] = peakdetect(array1, lookahead=1, delta=0)
    max_value = change_data(max_value)
    min_value = change_data(min_value)
    if len(min_value) == 0:
        min_value = [[0, array1[0]], [50, array1[50]]]
    print('max value: ', max_value)
    print('min value: ', min_value)
    max_value_idx = max_finder_change(max_value)
    data.append(max_value_idx)
    print((np.abs(min_value[:, 0] - max_value_idx)))
    temp = ((np.abs(min_value[:, 0] - max_value_idx)).argmin())
    min_vale_idx1 = min_value[temp - 1, 0]
    min_vale_idx2 = min_value[temp, 0]
    min_vale_idx1 = 0
    data.append(min_vale_idx1)
    data.append(min_vale_idx2)
    # else:
    #    print(array1)
    return data

def idx_finder_fft(array):
    data = []
    [max_value, min_value] = peakdetect(array, lookahead=25, delta=0)
    print('Max Vale:', max_value)
    print('Min Vale:', min_value)

# Returns Convolution in Frequency Domain
def freq_convolution(walk_data):
    """Getting the length of the two signals"""
    n = len(walk_data[:, 0])
    m = len(walk_data[:, 1])
    """Getting the length of the Convolution Size"""
    nConv = n + m - 1
    """50 is selected as the sampling Freq is 100 and needs to be divided by 2"""
    plot_x = np.linspace(0, 50, int(np.math.floor((nConv / 2) + 1)))
    """FFT of the ACCX Data as input to the Convolution"""
    fft_accx = fft(walk_data[:, 0], n=nConv)
    """Creating the Window"""
    fft_accy = fft(walk_data[:, 1], n=nConv)
    window_accy = fft_accy / max(fft_accy)
    data = fft_accx * window_accy
    data_out = abs(data[0:len(plot_x)])
    del fft_accy
    del fft_accx
    del window_accy
    del data

    return data_out

# Return Convolution in  Time Domain
def time_convolution(walk_data):
    """Getting the length of the two signals"""
    n = len(walk_data[:, 0])
    m = len(walk_data[:, 1])
    """Getting the length of the Convolution Size"""
    nConv = n + m - 1
    """50 is selected as the sampling Freq is 100 and needs to be divided by 2"""
    plot_x = np.linspace(0, 50, int(np.math.floor((nConv / 2) + 1)))
    """FFT of the ACCX Data as input to the Convolution"""
    fft_accx = fft(walk_data[:, 0], n=nConv)
    """Creating the Window"""
    fft_accy = fft(walk_data[:, 1], n=nConv)
    window_accy = fft_accy / max(fft_accy)
    data = fft_accx * window_accy
    size_con = math.floor(len(data) / 2.0) + 1
    data_temp = ifft(data)
    data_inv = data_temp[1:size_con + 1]
    data_inv = data_inv.real
    del fft_accy
    del fft_accx
    del window_accy
    del data

    return data_inv

# Returns the Maximum Value
def return_max(array):
    max_value = max(array)

    return max_value

# Returns the Mean Value for First Harmonics
def return_mean(array):
    data = idx_finder(array)
    mean_array = np.array(array[data[1]:data[2] + 1])
    mean = np.mean(mean_array)

    return mean

# Calculate the STD for First Harmonics
def return_std(array):
    stddev = np.std(array)

    return stddev

# Calculate Y-MIN absolute difference between two Y-Min found in the first Harmonic.
def return_ymin_absolute(array):
    data = idx_finder(array)
    ymin1 = array[data[1]]
    ymin2 = array[data[2]]
    ymin_abs = np.abs((ymin1 - ymin2))

    return ymin_abs

# Calculate the area between Y-Min 1 Y-Max and Y-min 2. This like computing a triangle inside the First Harmonic Curve
def return_area_triangle(array):
    data = idx_finder(array)
    height = array[data[0]]
    base_x1 = data[1]
    base_x2 = data[2]
    base_y1 = array[data[1]]
    base_y2 = array[data[2]]
    base = math.sqrt(((base_x2 - base_x1) ** 2) + ((base_y2 - base_y1) ** 2))
    area = 0.5 * base * height

    return area

# Calculate Average variation
def return_averageVaration(array):
    sumation = 0
    for i in range(len(array) - 1):
        temp = (array[i + 1] - array[i]) / len(array)
        sumation = sumation + temp

    return sumation

def pitch_calculation(array):
    x = array[:, 0]
    y = np.array(np.power(array[:, 1], 2))
    z = np.array(np.power(array[:, 2], 2))
    den = np.sqrt(y + z)
    res = np.empty(len(x), dtype=float)
    for i in range(len(x)):
        res[i] = (180 * math.atan(x[i] / den[i])) / math.pi
    pitch = np.std(res, axis=0)

    return pitch

def roll_calculation(array):
    x = array[:, 1]
    y = np.array(np.power(array[:, 0], 2))
    z = np.array(np.power(array[:, 2], 2))
    den = np.sqrt(y + z)
    res = np.empty(len(x), dtype=float)
    for i in range(len(x)):
        res[i] = (180 * math.atan(x[i] / den[i])) / math.pi
    roll = np.std(res, axis=0)

    return roll

def yaw_calculation(array):
    x = array[:, 2]
    y = np.array(np.power(array[:, 0], 2))
    z = np.array(np.power(array[:, 2], 2))
    den = np.sqrt(y+z)
    res = np.empty(len(x), dtype=float)
    for i in range(len(x)):
        res[i] = (180 * math.atan(x[i] / den[i])) / math.pi
    yaw = np.std(res, axis=0)

    return yaw

def anglefinderacc(array, bmi):

    x = np.array(array[:, 0])
    x = x * bmi
    y = np.array(array[:, 1])
    y = y * bmi
    z = np.array(array[:, 2])
    z = z * bmi
    h1 = np.sqrt(np.power(x, 2) + np.power(y, 2))
    h2 = np.sqrt(np.power(y, 2) + np.power(z, 2))
    h3 = np.sqrt(np.power(z, 2) + np.power(x, 2))

    theta1 = np.empty(len(h1), dtype=float)
    theta2 = np.empty(len(h1), dtype=float)
    theta3 = np.empty(len(h1), dtype=float)
    theta4 = np.empty(len(h1), dtype=float)
    theta5 = np.empty(len(h1), dtype=float)
    theta6 = np.empty(len(h1), dtype=float)
    #theta7 =[]
    theta7 = np.empty(len(h1), dtype=float)
    for i in range(len(x)):
        theta1[i] = math.degrees(math.acos((x[i] / h1[i])))
        theta2[i] = math.degrees(math.asin((y[i] / h1[i])))
        #theta3[i] = math.degrees(math.acos((y[i] / h2[i])))
        #theta4[i] = math.degrees(math.asin((z[i] / h2[i])))
        #theta5[i] = math.degrees(math.acos((z[i] / h3[i])))
        #theta6[i] = math.degrees(math.asin((x[i] / h3[i])))
    '''
    theta7.append(theta1)
    theta7.append(theta2)
    theta7.append(theta3)
    theta7.append(theta4)
    theta7.append(theta5)
    theta7.append(theta6)
    theta = np.array(theta7)
    theta_mean = np.mean(theta, axis=0)
    '''

    theta7 = theta1 + theta2
    theta_mean = np.mean(theta7)

    return theta_mean

def anglefindergyro(array):

    x = np.array(array[:, 3])
    y = np.array(array[:, 4])
    z = np.array(array[:, 5])
    h1 = np.sqrt(np.power(x, 2) + np.power(y, 2))
    h2 = np.sqrt(np.power(y, 2) + np.power(z, 2))
    h3 = np.sqrt(np.power(z, 2) + np.power(x, 2))

    theta1 = np.empty(len(h1), dtype=float)
    theta2 = np.empty(len(h1), dtype=float)
    theta3 = np.empty(len(h1), dtype=float)
    theta4 = np.empty(len(h1), dtype=float)
    theta5 = np.empty(len(h1), dtype=float)
    theta6 = np.empty(len(h1), dtype=float)
    # theta7 =[]
    theta7 = np.empty(len(h1), dtype=float)
    for i in range(len(x)):
        theta1[i] = math.degrees(math.acos((x[i] / h1[i])))
        theta2[i] = math.degrees(math.asin((y[i] / h1[i])))
        theta3[i] = math.degrees(math.acos((y[i] / h2[i])))
        theta4[i] = math.degrees(math.asin((z[i] / h2[i])))
        theta5[i] = math.degrees(math.acos((z[i] / h3[i])))
        theta6[i] = math.degrees(math.asin((x[i] / h3[i])))
    '''
    theta7.append(theta1)
    theta7.append(theta2)
    theta7.append(theta3)
    theta7.append(theta4)
    theta7.append(theta5)
    theta7.append(theta6)
    theta = np.array(theta7)
    print(theta)
    theta_mean = np.mean(theta, axis=0)
    '''
    theta7 = theta1 + theta2 + theta3 + theta4 + theta5 + theta6
    theta_mean = np.mean(theta7)

    return theta_mean

def anglefinder(array):
    x = np.array(array[:, 0])
    y = np.array(array[:, 1])
    z = np.array(array[:, 2])
    gx = np.array(array[:, 3])
    gy = np.array(array[:, 4])
    gz = np.array(array[:, 5])

    h1 = np.sqrt(np.power(x, 2) + np.power(y, 2))
    h2 = np.sqrt(np.power(y, 2) + np.power(z, 2))
    h3 = np.sqrt(np.power(z, 2) + np.power(x, 2))
    h4 = np.sqrt(np.power(gx, 2) + np.power(gy, 2))
    h5 = np.sqrt(np.power(gy, 2) + np.power(gz, 2))
    h6 = np.sqrt(np.power(gz, 2) + np.power(gx, 2))

    theta1 = np.empty(len(h1), dtype=float)
    theta2 = np.empty(len(h1), dtype=float)
    theta3 = np.empty(len(h1), dtype=float)
    theta4 = np.empty(len(h1), dtype=float)
    theta5 = np.empty(len(h1), dtype=float)
    theta6 = np.empty(len(h1), dtype=float)

    theta7 = []

    for i in range(len(x)):
        theta1[i] = math.degrees(math.acos((x[i] / h1[i]))) + math.degrees(math.asin((y[i] / h1[i])))
        theta2[i] = math.degrees(math.acos((y[i] / h2[i]))) + math.degrees(math.asin((z[i] / h2[i])))
        theta3[i] = math.degrees(math.acos((z[i] / h3[i]))) + math.degrees(math.asin((x[i] / h3[i])))
        theta4[i] = math.degrees(math.acos((gx[i] / h4[i]))) + math.degrees(math.asin((gy[i] / h4[i])))
        theta5[i] = math.degrees(math.acos((gy[i] / h5[i]))) + math.degrees(math.asin((gz[i] / h5[i])))
        theta6[i] = math.degrees(math.acos((gz[i] / h6[i]))) + math.degrees(math.asin((gx[i] / h6[i])))

    theta7.append(theta1)
    theta7.append(theta2)
    theta7.append(theta3)
    theta7.append(theta4)
    theta7.append(theta5)
    theta7.append(theta6)
    theta = np.array(theta7)
    theta_mean = np.mean(theta, axis=0)
    #theta7 = theta1 + theta2 + theta3 + theta4 + theta5 + theta6
    #theta_mean = np.mean(theta7)
    return theta_mean

def data_removal_trial(array, remove_threshold):
    array = np.array(array)
    r, c = array.shape
    array_new = []
    for idx in range(c):# - 1
        temp = np.array(array[:, idx])
        max_val, min_val = peakdetect(temp, lookahead=31)
        max_data = change_data(max_val)
        min_data = change_data(min_val)
        idx_max = []
        idx_min = []
        #max_average = []
        #min_average = []
        r, k = array.shape

        if max_data.size > 0:
            max_pos = max_data[:, 0].astype(np.int)
            max_value = max(max_data[:, 1])
            max_average = sum(max_data[:, 1]) / len(max_data[:, 1])
            for idx1 in range(r):
                if array[idx1, idx] >= remove_threshold * max_average:
                    idx_max.append(idx1)

        if min_data.size > 0:
            min_value = min(min_data[:, 1])
            min_pos = min_data[:, 0].astype(np.int)
            min_average = sum(min_data[:, 1]) / len(min_data[:, 1])
            for idx2 in range(r):
                if array[idx2, idx] <= remove_threshold * min_average:
                    idx_min.append(idx2)

        if idx_max.__len__() > 0:
            #row = len(array[:, 0]) - len(idx_max)
            #temp_array = np.empty((row, 7), dtype=float)
            for i in range(c):

                if i == 0:
                    row = len(np.delete(array[:, i].copy(), idx_max))
                    temp_array = np.empty((row, c), dtype=float)
                temp_array[:, i] = np.delete(array[:, i], idx_max)
            array = temp_array

        if idx_min.__len__() > 0:
            #row = len(array[:, 0]) - len(idx_min)
            #print(len(array[:, 0]), len(idx_min), row)
            #temp_array1 = np.empty((row, 7), dtype=float)
            for i in range(c):
                #print(np.delete(array[:, i], idx_min).shape)
                if i == 0:
                    row = len(np.delete(array[:, i].copy(), idx_min))
                    temp_array1 = np.empty((row, c), dtype=float)

                temp_array1[:, i] = np.delete(array[:, i], idx_min)
            array = temp_array1

    return array

































#end

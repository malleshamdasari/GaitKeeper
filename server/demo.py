import time
import numpy as np
from utils import *
from model import model
from preprocessing import preprocessing
import matplotlib.pyplot as plt

#keys = ['acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'trust_score']
keys = ['acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z']
sampling_frequency = 10
num_cycle_per_second = 1
guard_range_proportion = 0.4
target_cycle_length = 30

threshold = 2
valid_threshold = 4
boundary = 0.7

initial_learning_rate = 10**(-4)
num_steps = 2*10**(2)
model_save_path = 'model'
keep_prob = 0.7

num_sample = 5

json_list = get_json()
data = data_load(json_list, keys)

'''
#fig, axes = plt.subplots(6)

#for idx, ax in enumerate(axes):

#    ax.plot(data[:, idx][:5000])
#    ax.vlines(3100, ymax = 50, ymin = -50, linestyle = '--')
#plt.tight_layout()
#plt.show()
'''

pp = preprocessing(sampling_frequency, num_cycle_per_second, guard_range_proportion, target_cycle_length)
data = pp.process(data)

while(1):

    json_list = get_json()
    #print(json_list)
    data = data_load(json_list, keys)
    print(data.shape)

    pp = preprocessing(sampling_frequency, num_cycle_per_second, guard_range_proportion, target_cycle_length)
    data = pp.process(data)
    print(data.shape)
    _, cycle_length, num_features = data.shape
    data = data[-num_sample:]

    num_cycle, cycle_length, num_features = data.shape
    num_col = cycle_length*num_features

    mm = model(initial_learning_rate, num_steps, model_save_path, num_col)

    prediction = mm.predict(data.reshape(-1, num_col))
    #print(prediction)
    send(int(prediction.mean()*100))

    print(prediction.mean()*100)
    time.sleep(5)














#end

import numpy as np
from utils import *
from model import model
from preprocessing import preprocessing
import tensorflow as tf

'''
1. Read Data from Server
'''
keys = ['acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z']

json_list = get_json()
data = data_load(json_list, keys)

'''
2. Preprocessing
'''
sampling_frequency = 100
num_cycle_per_second = 1
guard_range_proportion = 0.4
target_cycle_length = 200

pp = preprocessing(sampling_frequency, num_cycle_per_second, guard_range_proportion, target_cycle_length)
data = pp.process(data)
num_cycle, cycle_length, num_features = data.shape
label = [1 for _ in range(num_cycle)]

false_data_path = 'data/anomaly.pkl'
false_data, false_label = labeling(false_data_path)

data = np.concatenate([data, false_data], axis = 0)
label = np.array(label + false_label).reshape(-1, 1)

_, cycle_length, num_features = data.shape

train_x_data, train_y_data, test_x_data, test_y_data = train_test_divide(data, label)
train_x_data, test_x_data = train_x_data.reshape(-1, cycle_length*num_features), test_x_data.reshape(-1, cycle_length*num_features)

'''
4. Create Model Object
'''
#parameters for object initialization
initial_learning_rate = 10**(-4)
num_steps = 2*10**(2)
model_save_path = 'model'
keep_prob = 0.7
num_col = cycle_length*num_features

mm = model(initial_learning_rate, num_steps, model_save_path, num_col)

'''
5. Train Model
'''
mm.build()
mm.train(train_x_data, train_y_data, keep_prob)


'''
6. Test Model
'''
prediction = mm.predict(test_x_data)
print(prediction)
accuracy = mm.acc(test_x_data, test_y_data)
print(accuracy)

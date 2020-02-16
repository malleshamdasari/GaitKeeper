import os
import json
from datetime import datetime
import platform
import numpy as np
import firstHarmonicsAnalysis as fh
from os import environ,getcwd
from dateutil.tz import tzlocal
from sklearn.utils import shuffle
from influxdb import InfluxDBClient
from scipy.interpolate import interp1d

##############  CONNECTION STRING VARIABLES ##########
INFLUX_HOST="influx-cewit.netsmartdev.com"
INFLUX_DATABASE="db_team_69"
INFLUX_USER="user_team_69"
INFLUX_PASS="J9sdscUlGImEzBEP"
######################################################

class Ntst_Influx_Payload:
    def __init__(self, measurementName,tagKvDict,datestamp, fieldKvDict):
        self.measurement = measurementName
        self.tags = tagKvDict
        self.time = datestamp
        self.fields = fieldKvDict

getUser = lambda: environ["USERNAME"] if "C:" in getcwd() else environ["USER"]
USERNAME = getUser()

tags = {"component":"primary_web_app","type":'method_timer',"hostname":platform.uname()[1],"os":platform.uname()[2],"user":USERNAME}

client = InfluxDBClient(INFLUX_HOST, 443, INFLUX_USER, INFLUX_PASS, INFLUX_DATABASE,True,False)

#json structure
'''
 {'time': '2020-02-15T17:24:20.421Z', 'trust_score' : 750,
 'acc_x': 3.83203125, 'acc_y': 3.90264892578125, 'acc_z': 8.356124877929688,
 'gyro_x': 0.0291290283203125, 'gyro_y': -0.156402587890625, 'gyro_z': -0.3584442138671875}
'''
# Get current user running your process
getUser = lambda: environ["USERNAME"] if "C:" in getcwd() else environ["USER"]
USERNAME = getUser()


def send(data):

    fields = {'heimdall_score':data}
    isoDate = datetime.now(tzlocal()).isoformat()

    newPointObject = Ntst_Influx_Payload("model_data",tags,isoDate,fields)
    # Influx requires an interable collection of dictionaries
    pointsArray=[newPointObject.__dict__]
    resultBool = client.write_points(pointsArray)


def get_json():
    # Add various tags (meta data) to 'group by' in the charts, providing many ways to filter and group on your measurements.
    tags = {"component":"primary_web_app","type":'method_timer',"hostname":platform.uname()[1],"os":platform.uname()[2],"user":USERNAME}
    client_data = client.query('SELECT * from sensor_data')

    return client_data

def json_parse(json_data, keys):

    result = []
    #del json_data['time']
    for value in json_data:

        sub_result = []

        for key in keys:
            sub_result.append(value[key])
        result.append(sub_result)

    return np.array(result)

def data_load(json_list, keys):

    data_list = []

    for idx, json_object in enumerate(json_list):

        data = json_parse(json_object, keys)
        data_list.append(data)

    return np.concatenate(data_list, axis = 0)

def peak_removal(data):
    return fh.data_removal_trial(data, threshold = 2)

def filter(data):
    data[data == None] = 0
    return fh.filter_data(data)

def cycle_detection(data, sampling_frequency, num_cycle_per_second, guard_range_proportion):

    unit_cycle_length = sampling_frequency // num_cycle_per_second
    gyro_z_data = data[:, -1]

    num_cycle = len(gyro_z_data) // unit_cycle_length

    guard_size = int(guard_range_proportion*unit_cycle_length)

    user_cycle_list = []
    slice_start_idx = 0

    for cycle_idx in range(num_cycle):

        #print('%d/%d'%(cycle_idx+1, num_cycle))

        target_start_idx = slice_start_idx + unit_cycle_length - guard_size
        target_end_idx = slice_start_idx + unit_cycle_length + guard_size

        #find the local minima
        if len(gyro_z_data[target_start_idx : target_end_idx]):
            #print(gyro_z_data[target_start_idx : target_end_idx])
            local_min_idx = np.argmin(gyro_z_data[target_start_idx : target_end_idx])

            #define the end idx for slicing a valid period
            slice_end_idx = target_start_idx + local_min_idx
            user_cycle_list.append(data[slice_start_idx:slice_end_idx, :])

            slice_start_idx = slice_end_idx

    return user_cycle_list

def interpolation(cycle_data, target_cycle_length):

    interpolated_result = []

    for cycle in cycle_data:

        cycle_length, num_col = cycle.shape
        new_cycle = []

        for col_idx in range(num_col):

            x = range(cycle_length)
            f = interp1d(x, cycle[:, col_idx], kind = 'linear')

            new_x = np.linspace(0, cycle_length-1, num = target_cycle_length)
            interpolated_cycle = f(new_x)
            new_cycle.append(interpolated_cycle.reshape(-1, 1))

        new_cycle = np.concatenate(new_cycle, axis = 1)
        interpolated_result.append(new_cycle)

    return np.array(interpolated_result)

def labeling(data_path):

    data = np.load(data_path, allow_pickle = True)

    label = []

    for user_data in data:

        for _ in user_data:
            label.append(0)

    return np.concatenate(data, axis = 0), label

def train_test_divide(x_data, y_label, ratio = 0.8):

    if len(x_data.shape) == 3:
        num_sample, period_len, num_type = x_data.shape
    else:
        num_sample, num_feature = x_data.shape

    x_data, y_label = shuffle(x_data, y_label)

    train_size = int(num_sample*ratio)
    train_x_data = x_data[:train_size, :]
    test_x_data = x_data[train_size:, :]

    train_y_data = y_label[:train_size]
    test_y_data = y_label[train_size:]

    return train_x_data, train_y_data, test_x_data, test_y_data
























#end

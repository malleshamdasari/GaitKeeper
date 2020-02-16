from utils import *

class preprocessing():

    def __init__(self, sampling_frequency = 100, num_cycle_per_second = 1, guard_range_proportion = 0.4, target_cycle_length = 200):

        self.sampling_frequency = sampling_frequency
        self.num_cycle_per_second = num_cycle_per_second
        self.guard_range_proportion = guard_range_proportion
        self.target_cycle_length = target_cycle_length

    def process(self, data, peak = False):

        if peak:
            data = peak_removal(data)
        data = filter(data)

        user_cycle_list = cycle_detection(data, self.sampling_frequency, self.num_cycle_per_second, self.guard_range_proportion)
        interpolated_cycle_list = interpolation(user_cycle_list, self.target_cycle_length)

        return interpolated_cycle_list


















































#end

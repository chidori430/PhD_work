# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 11:59:15 2018

@author: micha
"""
import math
import matplotlib.pyplot as plt


def pipe_line_len(base_voltage, threshold_voltage, voltage, base_length, alpha):
    length = base_length * ((pow(base_voltage - threshold_voltage, alpha) * voltage) / (
                pow(voltage - threshold_voltage, alpha) * base_voltage))

    return length


def num_of_pipe_stages(voltage, alpha, base_voltage, threshold_voltage):
    n = ((voltage * pow(base_voltage - threshold_voltage, alpha)) / (
                base_voltage * pow(voltage - threshold_voltage, alpha))) - 1

    return n


def max_frequency(voltage, threshold_voltage, alpha):
    max_freq = pow(voltage - threshold_voltage, alpha) / voltage
    return max_freq


def alpha_power(dyn_power_base, voltage, base_voltage, frequency, stat_pwr_base, n, dyn_pwr_latch, stat_pwr_latch):
    a_pwr = (dyn_power_base * ((pow(voltage, 2)) / (pow(base_voltage, 2))) * frequency)
    + ((voltage / base_voltage) * stat_pwr_base) + n * (((pow(voltage, 2) / pow(base_voltage, 2)) * frequency)
                                                        + ((voltage / base_voltage) * stat_pwr_latch))

    return a_pwr


base_voltage = 1.8 #should never be above 1.8 volts for the i9 processor and 1.2 for i7
voltage = 1.6 #should never be above 1.8 volts but should be lower than the base voltage
threshold_voltage = 0.2 # has to be lower then voltage
alpha = 2.0 # can vary

n = num_of_pipe_stages(voltage, alpha, base_voltage, threshold_voltage)
print(n)
freq = max_frequency(voltage,threshold_voltage,alpha)
print(freq)

# plt.plot([1, 2, 3, 4])
# plt.ylabel('some numbers')
# plt.xlabel('wat')
# plt.show()

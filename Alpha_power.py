# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 11:59:15 2018

@author: micha
"""

""" X-series core voltage ranges from 1.55 to 1.8 volts
    X-series inclues the: i7-7740X,i7-7800X,i7-7820X,i9-7900X,i9-7920X
    static and dynamic power consumption found here https://www.techspot.com/review/1442-intel-kaby-lake-x/page4.html
"""
    
"""All of the values generated are factors, not absolute values so if you get
   a power consumption of 2 this means it is 2 * (original power consumption)

"""
import math
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from IPython import get_ipython
import itertools
from mpl_toolkits.mplot3d import Axes3D
#length of the pipeline which includes all stages
def pipe_line_len(base_voltage, threshold_voltage, voltage, base_length, alpha):
    length = base_length * ((pow((base_voltage - threshold_voltage), alpha) * voltage) 
    / (pow((voltage - threshold_voltage), alpha) * base_voltage))

    return length

# number of additional pipeline stages needed
def num_of_pipe_stages(voltage, alpha, base_voltage, threshold_voltage):
    n = ((voltage * pow((base_voltage - threshold_voltage), alpha)) / (
                base_voltage * pow(voltage - threshold_voltage, alpha))) - 1

    return n


def max_frequency(voltage, threshold_voltage, alpha):
    max_freq = pow((voltage - threshold_voltage), alpha) / voltage
    return max_freq


def alpha_power(dyn_power_base, voltage, base_voltage, frequency, stat_pwr_base, n, dyn_pwr_latch, stat_pwr_latch):
    a_pwr = (dyn_power_base * ((pow(voltage, 2)) / (pow(base_voltage, 2))) * frequency)
    + ((voltage / base_voltage) * stat_pwr_base) + (n * (((pow(voltage, 2) / pow(base_voltage, 2)) * frequency * dyn_pwr_latch)
                                                        + ((voltage / base_voltage) * stat_pwr_latch)))

    return a_pwr

base_length = 1
base_voltage = 1.8 
tbv = base_voltage
bv_list = []
voltage = 1.7
tv = voltage 
v_list = [] 
threshold_voltage = 0.2 # has to be lower then voltage
ttv = threshold_voltage
tv_list = []
alpha = 1.3 # can vary
# base pwr ratio = 888/323 with 888 being dynamic and 323 being static 
# This was the average across the x series chips 
dyn_pwr_base = 888/(888+323)
print(dyn_pwr_base)
stat_pwr_base = 323/(888+323)
dyn_pwr_latch = 0.9
stat_pwr_latch = 0.1 
n = 1.0
frequency =1.0


freq_list = []
p_length = []
stage_num = []
a_pwr = []


freq_list1 =[]
p_length1 = []
stage_num1 = []
a_pwr1 = []

freq_list2 =[]
p_length2 = []
stage_num2 = []
a_pwr2 = []


v_list = np.linspace(1,voltage,25,endpoint = False)
tv_list = np.linspace(threshold_voltage,0.99,25,endpoint = False)

X =[]
Y =[]
n =[]
for x in itertools.product(v_list,tv_list):
    
    X.append(x[0])
    Y.append(x[1])
    n.append(num_of_pipe_stages(x[0],alpha,base_voltage,x[1]))
X, Y = np.meshgrid(X, Y)
p_length = (pipe_line_len(base_voltage, Y, X, base_length, alpha))   
freq_list = (max_frequency(X,Y,alpha))
stage_num = (num_of_pipe_stages(X,alpha,base_voltage,Y))       

n = np.meshgrid(n)
#print(n)
a_pwr = (alpha_power(dyn_pwr_base, X, base_voltage, frequency, stat_pwr_base, stage_num, dyn_pwr_latch, stat_pwr_latch))


    

   
p_len_xmin, p_len_ymin = np.unravel_index(np.argmin(p_length), p_length.shape)
p_len_xmax, p_len_ymax = np.unravel_index(np.argmax(p_length), p_length.shape)

p_len_mi = (X[p_len_xmin,p_len_ymin], Y[p_len_xmin,p_len_ymin], p_length.min(),'Minimum Value for Pipeline length')
p_len_ma = (X[p_len_xmax, p_len_ymax], Y[p_len_xmax, p_len_ymax], p_length.max(),'Maximum Value for Pipeline length')
print(p_len_mi,'\n',p_len_ma,'\n')



a_pwr_xmin, a_pwr_ymin = np.unravel_index(np.argmin(a_pwr), a_pwr.shape)
a_pwr_xmax, a_pwr_ymax = np.unravel_index(np.argmax(a_pwr), a_pwr.shape)

a_pwr_mi = (X[a_pwr_xmin,a_pwr_ymin], Y[a_pwr_xmin,a_pwr_ymin], a_pwr.min(),'Minimum Value for Power Consumption')
a_pwr_ma = (X[a_pwr_xmax, a_pwr_ymax], Y[a_pwr_xmax, a_pwr_ymax], a_pwr.max(),'Maximum Value for Power Consumption')
print(a_pwr_mi,'\n',a_pwr_ma,'\n')


freq_xmin, freq_ymin = np.unravel_index(np.argmin(freq_list), freq_list.shape)
freq_xmax, freq_ymax = np.unravel_index(np.argmax(freq_list), freq_list.shape)

freq_mi = (X[freq_xmin,freq_ymin], Y[freq_xmin,freq_ymin], freq_list.min(),'Minimum Value for Frequency')
freq_ma = (X[freq_xmax, freq_ymax], Y[freq_xmax, freq_ymax], freq_list.max(),'Maximum Value for Frequency')
print(freq_mi,'\n',freq_ma,'\n')

stage_num_xmin, stage_num_ymin = np.unravel_index(np.argmin(stage_num), stage_num.shape)
stage_num_xmax, stage_num_ymax = np.unravel_index(np.argmax(stage_num), stage_num.shape)

stage_num_mi = (X[stage_num_xmin,stage_num_ymin], Y[stage_num_xmin,stage_num_ymin], stage_num.min(),'Minimum Value for Number of stages')
stage_num_ma = (X[stage_num_xmax, stage_num_ymax], Y[stage_num_xmax, stage_num_ymax], stage_num.max(),'Maximum Value for Number of stages')
print(stage_num_mi,'\n',stage_num_ma,'\n')

# frequency plots   
fig = plt.figure()
fig.set_size_inches(18.5, 10.5, forward=True)
ax = fig.add_subplot(2, 2, 1, projection='3d')
# Plot the surface.
surf = ax.plot_surface(X, Y, freq_list, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_xlabel('Voltage', fontsize=10)
ax.set_ylabel('Threshold Voltage', fontsize=10)
ax.set_zlabel('Frequency', fontsize=10)
ax.set_title('Frequency')
### Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()


# alpha power plots   
ax = fig.add_subplot(2, 2, 2, projection='3d')
# Plot the surface.
surf = ax.plot_surface(X, stage_num, a_pwr, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_xlabel('Voltage', fontsize=10)
ax.set_ylabel('Pipeline depth factor', fontsize=10)
ax.set_zlabel('Alpha Power', fontsize=10)
ax.set_title('Power Consumption')
### Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()


# Stage number plots   
ax = fig.add_subplot(2, 2, 3, projection='3d')
# Plot the surface.
surf = ax.plot_surface(X, Y, stage_num, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_xlabel('Voltage', fontsize=10)
ax.set_ylabel('Threshold Voltage', fontsize=10)
ax.set_zlabel('Pipeline depth Factor', fontsize=10)
ax.set_title('Pipeline depth Factor')
### Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()

# Pipeline length plots   
ax = fig.add_subplot(2, 2, 4, projection='3d')
# Plot the surface.
surf = ax.plot_surface(X, Y, p_length, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_xlabel('Voltage', fontsize=10)
ax.set_ylabel('Threshold Voltage', fontsize=10)
ax.set_zlabel('Pipeline delay factor', fontsize=10)
ax.set_title('Pipeline delay factor')
### Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()

fig.tight_layout()

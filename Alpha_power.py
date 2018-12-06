# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 11:59:15 2018

@author: micha
"""

""" X-series core voltage ranges from 1.55 to 1.8 volts
    X-series inclues the: i7-7740X,i7-7800X,i7-7820X,i9-7900X,i9-7920X
    static and dynamic powre consumption found here https://www.techspot.com/review/1442-intel-kaby-lake-x/page4.html
"""
    
import math
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from IPython import get_ipython

#length of the pipeline which includes all stages
def pipe_line_len(base_voltage, threshold_voltage, voltage, base_length, alpha):
    length = base_length * ((pow(base_voltage - threshold_voltage, alpha) * voltage) 
    / (pow(voltage - threshold_voltage, alpha) * base_voltage))

    return length

# number of additional pipeline stages needed
def num_of_pipe_stages(voltage, alpha, base_voltage, threshold_voltage):
    n = ((voltage * pow(base_voltage - threshold_voltage, alpha)) / (
                base_voltage * pow(voltage - threshold_voltage, alpha))) - 1

    return n


def max_frequency(voltage, threshold_voltage, alpha):
    max_freq = pow(voltage - threshold_voltage, alpha) / voltage
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
alpha = 2.0 # can vary
# base pwr ratio = 888/323 with 888 being dynamic and 323 being static 
# This was the average across the x series chips 
dyn_pwr_base = 888/(888+323)
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


#while tv > 1.0 :
#    tv = tv - (1/10)
#    freq = max_frequency(tv,threshold_voltage,alpha)
#    p_len = pipe_line_len(base_voltage,threshold_voltage,tv,base_length,alpha) 
#    nps = num_of_pipe_stages(tv, alpha,base_voltage,threshold_voltage)
#    pwr = alpha_power(dyn_pwr_base,tv,base_voltage,frequency,stat_pwr_base,n,dyn_pwr_latch,stat_pwr_latch)
#    v_list.append(tv)
#    p_length.append(p_len)
#    freq_list.append(freq)
#    stage_num.append(nps)
#    a_pwr.append(pwr)
#
#plt.figure(1)
#plt.subplot(411)
#plt.plot(v_list,freq_list, marker ='o', color = 'r')
#plt.tight_layout()
#plt.ylabel('Frequency')
#plt.xlabel('Voltage')
#
#plt.subplot(412)
#plt.plot(v_list,p_length,marker ='o', color ='g')
#plt.tight_layout()
#plt.ylabel('Pipe Line Length')
#plt.xlabel('Voltage')
#
#plt.subplot(413)
#plt.plot(v_list,stage_num, marker ='o',color ='b')
#plt.tight_layout()
#plt.ylabel('# of Pipeline stages')
#plt.xlabel('Voltage')
#
#plt.subplot(414)
#plt.plot(v_list,a_pwr, marker ='o',color ='c')
#plt.tight_layout()
#plt.ylabel(' Alpha Power')
#plt.xlabel('Voltage')
#
#
#plt.show()
#
#
#counter  =0
#
#while ttv < 1 :
#    tv_list.append(ttv)
#    ttv = ttv + (1/10)
#    freq1 = max_frequency(voltage,ttv,alpha)
#    p_len1 = pipe_line_len(base_voltage,ttv,voltage,base_length,alpha) 
#    nps1 = num_of_pipe_stages(voltage, alpha,base_voltage,ttv)
#    
#    p_length1.append(p_len1)
#    freq_list1.append(freq1)
#    stage_num1.append(nps1)
#
#plt.figure(2)
#plt.subplot(311)
#plt.plot(tv_list,freq_list1, marker ='o', color = 'r')
#plt.tight_layout()
#plt.ylabel('Frequency')
#plt.xlabel('Threshold Voltage')
#
#plt.subplot(312)
#plt.plot(tv_list,p_length1,marker ='o', color ='g')
#plt.tight_layout()
#plt.ylabel('Pipe Line Length')
#plt.xlabel('Threshold Voltage')
#
#plt.subplot(313)
#plt.plot(tv_list,stage_num1, marker ='o',color ='b')
#plt.tight_layout()
#plt.ylabel('# of Pipeline stages')
#plt.xlabel('Threshold Voltage')
#
#plt.show()
v_list = np.linspace(1,voltage,50,endpoint = False)
tv_list = np.linspace(threshold_voltage,0.99,50,endpoint = False)
i = 0
while i < len(v_list):
    p_length.append(pipe_line_len(base_voltage, tv_list[i], v_list[i], base_length, alpha))   
    a_pwr.append(alpha_power(dyn_pwr_base, v_list[i], base_voltage, frequency, stat_pwr_base, n, dyn_pwr_latch, stat_pwr_latch))
    max_frequency(v_list[i],tv_list[i],alpha)
    stage_num.append(num_of_pipe_stages(v_list[i],alpha,base_voltage,tv_list[i]))
    i = i +1






#while tbv > 1.0 :
#    tbv = tbv - 0.1
#
#    p_len2 = pipe_line_len(tbv,threshold_voltage,voltage,base_length,alpha) 
#    nps2 = num_of_pipe_stages(voltage, alpha,tbv,threshold_voltage)
#    pwr2 = alpha_power(dyn_pwr_base,voltage,tbv,frequency,stat_pwr_base,n,dyn_pwr_latch,stat_pwr_latch)
#    bv_list.append(tbv)
#    p_length2.append(p_len2)
#    stage_num2.append(nps2)
#    a_pwr2.append(pwr2)
#
#
#plt.figure(3)
#plt.subplot(311)
#plt.plot(bv_list,p_length2,marker ='o', color ='g')
#plt.tight_layout()
#plt.ylabel('Pipe Line Length')
#plt.xlabel('Base Voltage')
#
#plt.subplot(312)
#plt.plot(bv_list,stage_num2, marker ='o',color ='b')
#plt.tight_layout()
#plt.ylabel('# of Pipeline stages')
#plt.xlabel('Base Voltage')
#
#plt.subplot(313)
#plt.plot(bv_list,a_pwr2, marker ='o',color ='c')
#plt.tight_layout()
#plt.ylabel(' Alpha Power')
#plt.xlabel('Base Voltage')


#plt.show()

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 11:59:15 2018

@author: micha
"""
import math

def pipe_line_len(base_voltage,threshold_voltage,voltage,base_length,alpha):
    
    length = base_length*((pow(base_voltage - threshold_voltage,alpha)*voltage)/(pow(voltage-threshold_voltage,alpha)*base_voltage))
    
    return length

def num_of_pipe_stages(voltage,alpha,base_voltage,threshold_voltage):

    n = ((voltage*pow(base_voltage-threshold_voltage,alpha))/(base_voltage*pow(voltage - threshold_voltage,alpha))) - 1
         
    return n

def max_frequency(voltage,threshold_voltage,alpha):
    max_freq = pow(voltage - threshold_voltage,alpha)/voltage
    return max_freq

def alpha_power(dyn_power_base,voltage,base_voltage,frequency,stat_pwr_base,n,dyn_pwr_latch,stat_pwr_latch):
    
    a_pwr = (dyn_power_base*((pow(voltage,2))/(pow(base_voltage,2)))*frequency) 
    + ((voltage/base_voltage)*stat_pwr_base) + n*(((pow(voltage,2)/pow(base_voltage,2))*frequency) 
    + ((voltage/base_voltage)*stat_pwr_latch))

    return a_pwr



print(max_frequency(1.2,0.6,2))

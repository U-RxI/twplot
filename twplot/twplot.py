# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 11:56:50 2022

@author: Asmus Graumann Moser
"""

import matplotlib.pyplot as plt
from comtrade import Comtrade


import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt

def sine_generator(fs, sinefreq, duration):
    T = duration
    n = fs * T
    w = 2. * np.pi * sinefreq
    t_sine = np.linspace(0, T, n, endpoint = False)
    y_sine = np.sin(w * t_sine)
    result = pd.DataFrame({"data" : y_sine} ,index = t_sine)
    return result

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype = "high", analog = False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=9):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y


# Access to TW data
import os
cwd = os.getcwd()
pwd = os.path.dirname(cwd)


record = Comtrade()
record.load(pwd+"\\tests\\TWdata\\TW_Local.CFG", pwd+"\\tests\\TWdata\\TW_Remote.DAT")

print("Trigger time = {}s".format(record.trigger_time))

IA = np.array(record.analog[0])
IB = np.array(record.analog[1])
IC = np.array(record.analog[2])
# Clarke A
TWIAalpha = 1/3*(2*IA-1*IB-1*IC)
TWIAbeta = 1/3*(0*IA+3**(1/2)*IB-3**(1/2)*IC)
TWIAzero = 1/3*(1*IA+1*IB+1*IC)
# Clarke B
TWIBalpha = 1/3*(-1*IA+2*IB-1*IC)
TWIBbeta = 1/3*(-3**(1/2)*IA+0*IB+3**(1/2)*IC)
TWIBzero = 1/3*(1*IA+1*IB+1*IC)
# Clarke C
TWICalpha = 1/3*(-1*IA-1*IB+2*IC)
TWICbeta = 1/3*(3**(1/2)*IA-3**(1/2)*IB+0*IC)
TWICzero = 1/3*(1*IA+1*IB+1*IC)

fps = 30
filtered_sine = butter_highpass_filter(record.analog[0], 50000, 5000000)

plt.figure()
plt.plot(record.time, TWIAalpha)
plt.plot(record.time, TWIBalpha)
plt.plot(record.time, TWICalpha)
#plt.plot(record.time, record.analog[1])
#plt.plot(record.time, record.analog[2])
plt.legend([record.analog_channel_ids[0], record.analog_channel_ids[1], record.analog_channel_ids[2]])
plt.show()




'''
rec = Comtrade()
rec.load(pwd+"\\tests\\TWdata/SUB A TW.CFG", pwd+"\\tests\\TWdata\\411L SUB A FILTERED.cff")
print("Trigger time = {}s".format(rec.trigger_time))

plt.figure()
plt.plot(rec.time, rec.analog[0])
plt.plot(rec.time, rec.analog[1])
plt.legend([rec.analog_channel_ids[0], rec.analog_channel_ids[1]])
plt.show()
'''



'''
fps = 30
sine_fq = 10
duration = 10
sine_5Hz = sine_generator(fps,sine_fq,duration)
sine_fq = 1
duration = 10
sine_1Hz = sine_generator(fps,sine_fq,duration)
sine = sine_5Hz + sine_1Hz
'''









# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 18:07:12 2019

@author: Juan
"""
import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
import adquisicion

def callback(task_handle, every_n_samples_event_type, number_of_samples,
             callback_data):
        global data
        global time
        global last
        samples = task.read(number_of_samples_per_channel=number_of_samples)
        data[last:last+number_of_samples] = samples
        print(samples[-1])
        last += number_of_samples
        return 0


# %%
fs = 200
tmax = 2
dtcall = 1
data = np.zeros(tmax*fs)
time = np.zeros_like(data)
last = 0
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")

    task.timing.cfg_samp_clk_timing(rate=fs, samps_per_chan=tmax*fs)

    task.register_every_n_samples_acquired_into_buffer_event(
        dtcall*fs, callback)

    task.start()
    input('fin')
plt.plot(data)

# %% Set trigger
dev = nidaqmx.system.device.Device('Dev1')
channels = {'sound': 'ai0', 'vs': 'ai1'}

fs = 44150
tmax = 1
adquisicion.set_trigger(dev, channels, tmax, fs)
time, med = adquisicion.medicion_finita(dev, channels, tmax=tmax, fs=fs)

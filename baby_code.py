# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 18:07:12 2019

@author: Juan
"""
import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
import adquisicion
from nidaqmx.constants import AcquisitionType
from utils import gen_trigger
from trigger_functions import abs_value, integral, modulo


#def callback(task_handle, every_n_samples_event_type, number_of_samples,
#             callback_data):
#        global data
#        global time
#        global last
#        samples = task.read(number_of_samples_per_channel=number_of_samples)
#        data[last:last+number_of_samples] = samples
#        print(samples[-1])
#        last += number_of_samples
#        return 0
#
#
## %%
#fs = 200
#tmax = 2
#dtcall = 1
#data = np.zeros(tmax*fs)
#time = np.zeros_like(data)
#last = 0
#with nidaqmx.Task() as task:
#    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
#
#    task.timing.cfg_samp_clk_timing(rate=fs, samps_per_chan=tmax*fs)
#
#    task.register_every_n_samples_acquired_into_buffer_event(
#        dtcall*fs, callback)
#
#    task.start()
#    input('fin')
#plt.plot(data)
#
## %% Set trigger
#dev = nidaqmx.system.device.Device('Dev1')
#channels = {'sound': 'ai0', 'vs': 'ai1'}
#
#fs = 44150
#tmed = 1
#adquisicion.set_trigger(dev, channels, tmed, fs)
#time, med = adquisicion.medicion_finita(dev, channels, tmed=tmed, fs=fs)
# %% Medir posta
def callback(task_handle, every_n_samples_event_type, number_of_samples,
             callback_data):
    global samples
    global channels
    global fs
    ncanales = len(channels_dict)
    if ncanales > 1:
        new_samples = task.read(number_of_samples_per_channel=number_of_samples)
    else:
        new_samples = [task.read(number_of_samples_per_channel=number_of_samples)]
    array_samples = np.asarray(new_samples)
    samples = np.concatenate((samples[:, number_of_samples:], array_samples),
                             axis=1)
    time = np.arange(0, max(samples.shape))/fs
    fig, ax = plt.subplots(ncols=ncanales, squeeze=False,
                           figsize=(4*ncanales, 4))
    for ix, chan in enumerate(samples):
        ax[0, ix].plot(time, chan)
        ax[0, ix].set_title(list(channels_dict.keys())[ix])
    plt.show()
#    playback...
#    if check_trigger_condition:
#        if not folder ok:
#            get_day
#            create_folder
#        get_file_info
#        write_log
#        save_data
#        plot
    return 0
    

fs = 44150
tmed = 3
dtcall = 1
channels_dict = {'sound': 'ai0', 'vs': 'ai1'}
functions_dict = {abs_value: {}, integral: {'dt_integral': 0.1},modulo: {}}
functions_thresholds = {abs_value: 0, integral: 1, modulo: 1}
trigger = gen_trigger(44150, functions_dict, functions_thresholds)
dev = nidaqmx.system.device.Device('Dev1')
samples = np.zeros((len(channels_dict), int(fs*tmed)))
with nidaqmx.Task() as task:
    adquisicion.add_channels(task, dev, channels_dict)
    task.timing.cfg_samp_clk_timing(rate=fs,
                                    sample_mode=AcquisitionType.CONTINUOUS)
    task.in_stream.input_buf_size = int(fs*dtcall*10)
    task.register_every_n_samples_acquired_into_buffer_event(
        int(dtcall*fs), callback)
    task.start()
    while input('q = fin\n') != 'q':
        1
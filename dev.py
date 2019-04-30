# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 13:58:09 2019

@author: lsd
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import adquisicion
import nidaqmx

#%%
def set_trigger(dev, channels, tmed=1, fs=44150):
    def create_update(axis, hline):
        def update(val):
            hline.set_ydata(val)
            lines = axis.get_lines() 
            if len(lines) > 2:
                lines[-1].remove()
            data_line = axis.get_lines()[0]
            xdata = data_line.get_xdata()
            ydata = data_line.get_ydata()
            crossings, = np.where(np.logical_and(ydata[1:] > val,
                                                 ydata[:-1] < val))
            if len(crossings) > 0:
                axis.plot(xdata[crossings], ydata[crossings], 'x', color='g')
            fig.canvas.draw_idle()
        return update
    time, med = adquisicion.medicion_finita(dev=dev, channels=channels,
                                            tmed=tmed, fs=fs)
    channel_names = list(channels.keys())
    nplots = len(channels)
    fig, ax = plt.subplots(nrows=1, ncols=nplots, figsize=(6*nplots, 4),
                           squeeze=False)
    plt.subplots_adjust(bottom=0.25)
    sliders = []
    updates = []
    for nchannel in range(nplots):
        ch_name = channel_names[nchannel]
        ncol = nchannel
        ax[0, ncol].plot(time, med[ncol], lw=2, color='red',
                      label='{}'.format(ch_name))
        axumbral = plt.axes([ncol/nplots+0.1, 0.0, 1/nplots-0.15, 0.03])
        umbral = np.mean(med[nchannel])
        sliders.append(Slider(axumbral, 'Umbral {}'.format(ch_name),
                              min((0.0, min(med[ncol]))),
                              max((0.5, max(med[ncol]))),
                              valinit=umbral))
        hline = ax[0, ncol].axhline(umbral, ls='dashed')
        update_func = create_update(axis=ax[0, ncol], hline=hline)
        sliders[-1].on_changed(update_func)
        updates.append(update_func)
    fig.tight_layout()
    plt.show()
    return fig, ax, sliders, updates

channels = {'sound': 'ai0', 'vs': 'ai1'}
fs = 44150
tmed = 1
dev = nidaqmx.system.device.Device('Dev1')
fig, ax, sliders, updates = set_trigger(dev, channels)

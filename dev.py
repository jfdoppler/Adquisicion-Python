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
    def create_update(line):
        def update(val):
            line.set_ydata(val)
            fig.canvas.draw_idle()
        return update
    time, med = adquisicion.medicion_finita(dev=dev, channels=channels,
                                            tmax=tmed, fs=fs)
    channel_names = list(channels.keys())
    nplots = len(channels)
    fig, ax = plt.subplots(nrows=1, ncols=nplots, figsize=(6*nplots, 4),
                           squeeze=False)
    plt.subplots_adjust(bottom=0.25)
    hlines = []
    umbrales = []
    sliders = []
    updates = []
    for ncol in range(nplots):
        ch_name = channel_names[ncol]
        ax[0, ncol].plot(time, med[ncol], lw=2, color='red',
                      label='{}'.format(ch_name))
        axumbral = plt.axes([ncol/nplots+0.1, 0.0, 1/nplots-0.15, 0.03])
        umbral = np.mean(med[ncol])
        umbrales.append(umbral)
        sliders.append(Slider(axumbral, 'Umbral {}'.format(ch_name), 0.0, 1.,
                              valinit=umbral))
        line = ax[0, ncol].axhline(umbral)
        hlines.append(line)
        update_func = create_update(line)
        sliders[-1].on_changed(update_func)
        updates.append(update_func)
    fig.tight_layout()
    plt.show()
    return fig, ax, sliders, updates

channels = {'sound': 'ai0', 'vs': 'ai1'}
fs = 44150
tmed = 1
dev = nidaqmx.system.device.Device('Dev1')
set_trigger(dev, channels)

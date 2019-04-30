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
import pandas as pd

#%%
def integral(data, fs, dt_integral):
    window = int(fs*dt_integral)
    series = pd.Series(data)
    value = series.rolling(window=window, min_periods=1, center=True).sum()/fs
    return value


def set_trigger(dev, channels, tmed=1, fs=44150, funciones=[integral],
                **kwargs):
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
    ncols = len(channels)
    nrows = 1+len(funciones)
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols,
                           figsize=(6*ncols, 3*nrows),
                           squeeze=False)
    plt.subplots_adjust(bottom=0.25)
    sliders = []
    updates = []
    for nchannel in range(ncols):
        ch_name = channel_names[nchannel]
        ncol = nchannel
        for nrow in range(nrows):
            if nrow == 0:
                variable = med[ncol]
            else:
                variable = funciones[nrow-1](med[ncol], fs=fs, **kwargs)
            ax[nrow, ncol].plot(time, variable, lw=2, color='red',
                                label='{}'.format(ch_name))
            axumbral = plt.axes([ncol/ncols+0.1, nrow/nrows, 1/ncols-0.15, 
                                 0.03])
            umbral = np.mean(med[ncol])
            sliders.append(Slider(axumbral, 'Umbral {}'.format(ch_name),
                                  min((0.0, min(variable))),
                                  max((0.5, max(variable))),
                                  valinit=umbral))
            hline = ax[nrow, ncol].axhline(umbral, ls='dashed')
            update_func = create_update(axis=ax[nrow, ncol], hline=hline)
            sliders[-1].on_changed(update_func)
            updates.append(update_func)
#    fig.tight_layout()
    plt.show()
    return fig, ax, sliders, updates

channels = {'sound': 'ai0', 'vs': 'ai1'}
fs = 44150
tmed = 1
dev = nidaqmx.system.device.Device('Dev1')
fig, ax, sliders, updates = set_trigger(dev, channels, tmed=tmed, fs=fs,
                                        dt_integral=0.1)

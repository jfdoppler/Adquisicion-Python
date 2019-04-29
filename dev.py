# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 13:58:09 2019

@author: lsd
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import adquisicion


def set_trigger(dev, channels, variables=[], method='umbral', tmax=1, fs=44150):
    def update(val):
    #    amp = samp.val
    #    freq = sfreq.val
    #    l.set_ydata(amp*np.sin(2*np.pi*freq*t))
        fig.canvas.draw_idle()
        print(l.get_ydata())
        
    time, med = adquisicion.medicion_finita(dev=dev, channels=channels, tmax=tmax, fs=fs)
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    ax.plot(time, med[0], lw=2, color='red')
    axcolor = 'lightgoldenrodyellow'
    axumbral = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    umbral = 0
    sumbral = Slider(axumbral, 'Umbral', 0.0, 5, valinit=umbral)
    l = ax.axhline(umbral)
    sumbral.on_changed(update)
    plt.show()
    return fig, ax, sumbral, update

channels = {'sound': 'ai0', 'vs': 'ai1'}
fs = 44150
tmax = 1
set_trigger(nidaqmx.system.device.Device('Dev1'), channels)

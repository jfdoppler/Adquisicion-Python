# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 12:27:10 2019

@author: lsd
"""
import nidaqmx
import matplotlib.pyplot as plt
import numpy as np


def medicion_finita(dev, channels, tmax=1, fs=44150, show=False):
    """
    Hace una medicion por un tiempo determinado
    
    Parametros
    ----------
    dev : nidaqmx.system.device.Device
        Objeto que representa a la placa y contiene sus atributos (por ejemplo,
        su nombre: dev.name). Debe ser creado usando:
        dev = nidaqmx.system.device.Device('Dev1')
        El nombre 'Dev1' es el asignado a la placa y puede conocerse usando
        el NI MAX.
    
    channels : dict
        Diccionario que contiene los nombres y canales físicos a medir. Tanto
        los nombres como los canales en string.
        {'sonido': 'ai4; 'vs': 'ai0'}
    
    tmax : float
        Tiempo de medicion
    
    fs : float
        Frecuencia de adquisición
    
    show : bool
        Si True muestra un grafico con las mediciones de cada canal
    
    Returns
    -------
    time : np.array
        Vector de tiempo
    
    med : list
        Lista de mediciones. Cada elemento es una lista que corresponde a las
        mediciones de un canal
    """
    nsamples = int(fs*tmax)
    time = np.arange(0, tmax, 1/fs)
    with nidaqmx.Task() as task:
        for name, phys_channel in channels.items():
            task.ai_channels.add_ai_voltage_chan('{}/{}'.format(dev.name,
                                                 phys_channel),
                                                 name_to_assign_to_channel=name)
        task.timing.cfg_samp_clk_timing(rate=fs, samps_per_chan=nsamples)
        if len(channels) == 1:
            med = [task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE)]
        else:
            med = task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE)
    if show:
        plt.figure()
        for ch_med in med:
            plt.plot(time, ch_med)
    return time, med



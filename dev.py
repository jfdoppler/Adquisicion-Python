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
from trigger_functions import integral, modulo


# %%
def set_trigger(dev, channels, tmed=1, fs=44150,
                funciones={integral: {'dt_integral': 0.1}}):
    """
    Funcion para setear el (los) trigger(s). Hace una medción y grafica los
    resultados y variables de interés en subplots para todos los canales.
    Los graficos tienen sliders asociados que permiten definir los valores
    de umbral para cada variable.

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
    tmed : float
        Tiempo de medicion
    fs : float
        Frecuencia de adquisición
    funciones : dict
        Diccionario con las funciones que queremos evaluar para decidir si
        triggerear o no, con sus parametros particulares. Todas las funciones
        deben tomar como parametros time, data pero pueden pedir otros
        adicionales. Este diccionario se construye de la siguiente manera:
        >>> funciones = {funcion_1: {par_1_1: val_1_1, par_1_2: val_1_2},
        >>>              funcion_2: {par_2_1: val_2_1}}
        Cada key de este diccionario es el nombre de una funcion a evaluar. El
        value asociado a cada key es un diccionario. Este tiene como keys los
        nombres (strings) de los parametros adicionales y como value los
        valores.

    Ejemplo
    -------
    Queremos evaluar las siguientes funciones en el trigger:

    >>> def integral(time, data, dt_integral):
    >>>     fs = 1/(time[1]-time[0])
    >>>     window = int(fs*dt_integral)
    >>>     series = pd.Series(np.abs(data))
    >>>     value = series.rolling(window=window, min_periods=1,
    >>>                            center=True).sum()/fs
    >>> return value
    >>> def modulo(time, data):
    >>>     value = np.abs(data)
    >>> return value

    A "integral" tenemos que pasarle el argumento adicional "dt_integral",
    mientras que a modulo no tenemos que pasarle argumentos adicionales:

    >>> funciones = {integral: {"dt_integral": 0.5}, modulo: {}}

    Returns
    -------
    fig : ~.figure.Figure
    ax : array of Axes objects.
        Array de Axes objects (creados con plt.subplots, squeeze=False)
    sliders : array of Slider objects
        Cada Slider está asociado a un subplot distinto.
    updates : array of update functions
        Cada update function esta asociada a un subplot y Slider distinto.
    """
    def create_update(axis, hline):
        """
        Crea un update asociado a un eje y una línea

        Parametros
        ----------
        axis : Axes object
            Creado con plt.subplots sin squeeze
        hline : Line2D
            Línea horizontal, creada con axhline

        Returns
        -------
        update : function
        """
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
                axis.axvline(xdata[crossings[0]], color='g')
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
    fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.98,
                        wspace=0.25, hspace=0.25)
    sliders = []
    updates = []
    for nchannel in range(ncols):
        ch_name = channel_names[nchannel]
        ncol = nchannel
        for nrow in range(nrows):
            if nrow == 0:
                variable = med[ncol]
                label = ch_name
            else:
                funcion = list(funciones.keys())[nrow-1]
                kwargs_for_f = funciones[funcion]
                variable = funcion(time, med[ncol], **kwargs_for_f)
                label = funcion.__name__
            ax[nrow, ncol].plot(time, variable, lw=2, color='red')
            ax[nrow, ncol].set_ylabel(label)
            axumbral = plt.axes([ncol/ncols+0.1, 1.01-(nrow+1)/nrows,
                                 1/ncols-0.2, 0.02])
            umbral = np.mean(variable)
            sliders.append(Slider(axumbral, 'umbral',
                                  min((0.0, min(variable))),
                                  max((0.5, max(variable))),
                                  valinit=umbral))
            hline = ax[nrow, ncol].axhline(umbral, ls='dashed')
            update_func = create_update(axis=ax[nrow, ncol], hline=hline)
            sliders[-1].on_changed(update_func)
            updates.append(update_func)
    plt.show()
    return fig, ax, sliders, updates


channels = {'sound': 'ai0', 'vs': 'ai1', 'presion': 'ai5'}
fs = 44150
tmed = 1
dev = nidaqmx.system.device.Device('Dev1')
fig, ax, sliders, updates = set_trigger(dev, channels, tmed=tmed, fs=fs,
                                        funciones={integral: {'dt_integral': 0.1},
                                                   modulo: {}})

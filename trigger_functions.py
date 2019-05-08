#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 11:14:46 2019

@author: juan
"""
import numpy as np
import pandas as pd


def abs_value(time, data):
    return np.abs(data)


def integral(time, data, dt_integral):
    fs = 1/(time[1]-time[0])
    window = int(fs*dt_integral)
    series = pd.Series(np.abs(data))
    value = series.rolling(window=window, min_periods=1, center=True).sum()/fs
    return value


def modulo(time, data):
    value = np.abs(data)
    return value

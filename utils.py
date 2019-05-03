#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 11:16:58 2019

@author: juan
"""
from datetime import datetime, timedelta
from scipy.io import wavfile
import os


# Todo esto no quedaria mejor en una clase donde iriamos actualizando self. ?
class FileManager:
    def __init__(self, birdname, base_path, night_start=20, night_end=6,
                 duracion_night=15, duracion_day=10,
                 datefmt='%Y-%m-%d_%H.%M.%S', fname_sep='_'):
        self.night_start = night_start
        self.night_end = night_end
        self.duracion_night = duracion_night
        self.duracion_day = duracion_day
        self.duracion_med = 0
        self.isDay = True
        self.fdatetime = ''
        self.folder = ''
        self.fnames = []

    def isDay_update(self):
        date = datetime.now()
        current_hour = date.hour
        if current_hour >= self.night_start or current_hour < self.night_end:
            self.isDay = False
        else:
            self.isDay = True

    def 

    def fdatetime_update(self):
        current_datetime = datetime.now()
        file_datetime = current_datetime-timedelta(seconds=duracion_med)
        formatted_datetime = format_datetime(file_datetime, fmt=fmt)
        return file_datetime, formatted_datetime

# %%
# SOLO FILE MANAGEMENT
def is_day(night_from=20, night_to=6):
    date = datetime.now()
    current_hour = date.hour
    if current_hour >= night_from or current_hour < night_to:
        return False
    else:
        return True


def format_datetime(datetime, fmt='%Y-%m-%d_%H.%M.%S'):
    return datetime.strftime(fmt)


def get_file_datetime(duracion_med, fmt='%Y-%m-%d_%H.%M.%S'):
    current_datetime = datetime.now()
    file_datetime = current_datetime-timedelta(seconds=duracion_med)
    formatted_datetime = format_datetime(file_datetime, fmt=fmt)
    return file_datetime, formatted_datetime


def get_folder(base_path, duracion_med):
    file_datetime, _ = get_file_datetime(duracion_med=duracion_med)
    current_hour = file_datetime.hour
    isDay = is_day()
    if isDay:
        folder_date = format_datetime(file_datetime, fmt='%Y-%m-%d')
        folder_name = folder_date + '-day'
    elif current_hour < 12:
        folder_datetime = file_datetime - timedelta(days=1)
        folder_date = format_datetime(folder_datetime, fmt='%Y-%m-%d')
        folder_name = folder_date + '-night'
    folder = os.path.join(base_path, folder_name)
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def get_fname(channel_name, birdname, dtime):
    fname = '_'.join([channel_name, birdname, dtime])
    fname += '.wav'
    return fname

# Esto no viene aca! Guardar datos y escribir log tienen que estar separados
def save_file(folder, fname):
    full_path = folder + fname
    wavfile.write(full_path)


def write_log_line():
    return 0


def init_log():
    return 0

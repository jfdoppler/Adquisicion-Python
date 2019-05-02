#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 11:16:58 2019

@author: juan
"""
from datetime import datetime, timedelta


# Todo esto no quedaria mejor en una clase donde iriamos actualizando self. ?
# class FileManag:
#     def __init__(self, birdname, base_path, name_fmt):
#         self.isDay =
#         self.date =
#         self.current_folder =


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


def folder_path():
    return 0


def file_full_name():
    return 0


def save_file():
    return 0


def write_log_line():
    return 0


def init_log():
    return 0

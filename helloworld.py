#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 11:38:12 2019

@author: juan
"""

import tkinter as tk
import pygubu


class Application:
    def __init__(self, master):
        self.master = master
#        1: Create a builder
        self.builder = builder = pygubu.Builder()

#        2: Load an ui file
        builder.add_from_file('helloworld.ui')

#        3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('mainwindow', master)
        builder.connect_callbacks(self)

    def on_quit_button_click(self):
        self.master.quit()


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

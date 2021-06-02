# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 12:43:29 2020

@author: FDemircan
"""

import serial as s
arduino = s.Serial('COM3', 115200)
val = 0

while True:
    val = input("Thrust:")
    v = str(val)
    arduino.write(v.encode())
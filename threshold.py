# -*- coding: utf-8 -*-
"""
Created on Sat Apr 08 23:56:59 2017

@authors: LJY, YH

"""

import csv
import matplotlib.pyplot as plt
import numpy
import time
import math
import socket
import sys

plt.ion()
data_array_x = []
data_array1_y = []
data_array2_y = []
data_array3_y = []
f, axarr = plt.subplots(2)
# axarr[0].xlabel('Timestep [s]')
bar_width = 0.35
opacity = 0.4
axarr[0].set_ylabel('Measurement')
axarr[0].set_xlabel('Timestep [s]')
axarr[1].set_ylabel('Measurement')
axarr[1].set_xlabel('Temp                                         Humidity [%]                                         Pressure [kPa]')
# axarr[1].set_xticks([1+0.35/2, 2+0.35/2, 3+0.35/2], ('Temp', 'Humidity', 'Pressure'))
legend_flag = 0
i = 0

def threshold(temp,humi,press,age,oxygen,heart):
    maximum = 207-0.7*age-((temp-66)**2)*0.01-abs(humi-0.5)-(press-1000)
    if oxygen <= 0.7 * maximum:
        print("Keep pushing it!")
        return 1
    elif oxygen <= 0.9 * maximum:
        print("Time to cool it")
        return 2
    else: 
        print("Take a break")
        return 3

with open('./SampleData.csv', 'r') as csvfile:
    csvfile = csv.reader(csvfile)
    for row in csvfile:
        level = (threshold(float(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5])))
        s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_out.connect(("127.0.0.1", 8001))
        s_out.send(bytes(str(level), encoding='utf-8'))
        s_out.close()

        if len(data_array_x) > 11:
            data_array_x.pop(0)
            data_array1_y.pop(0)
            data_array2_y.pop(0)
        data_array_x.append(i)
        data_array1_y.append(float(row[5]))
        data_array2_y.append(float(row[4]))
        # update_line(hl, [i, i**2])
        axarr[0].axis([i-10,i+10,50,200])
        axarr[0].plot(data_array_x, data_array1_y, 'r-o', label='Blood O2')
        axarr[0].plot(data_array_x, data_array2_y, 'b-o', label='HR')
        if legend_flag == 0:
            legend = axarr[0].legend()
            legend_flag = legend_flag + 1
                     
        # axarr[0].draw()
        # axarr[0].pause(0.01)
        # time.sleep(0.2)

        rects1 = axarr[1].bar(1, float(row[0]), bar_width,
                         alpha=opacity,
                         color='b',
                         label='Temp')

        rects2 = axarr[1].bar(2, float(row[1])*100, bar_width,
                         alpha=opacity,
                         color='r',
                         label='Humid')

        rects3 = axarr[1].bar(3, float(row[2])/10, bar_width,
                         alpha=opacity,
                         color='g',
                         label='Pressure')

        # axarr[1].tight_layout()
        plt.draw()
        plt.pause(0.01)
        # axarr[1].pause(0.01)
        i = i+1

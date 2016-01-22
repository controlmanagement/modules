#! /usr/bin/env python
#-*- coding: utf-8 -*-


# necopt
"""
import m4
import abs

ret1 = m4.start_m4_server()
ret2 = abs.start_abs_server()

"""
# necctrl

import time
import antenna_enc
import antenna_nanten_controller
import dome_pos
import dome
import weather
import subprocess as sub

ret3 = antenna_enc.start_enc_server()
time.sleep(3.)
ret4 = antenna_nanten_controller.start_antenna_server()

ret5 = dome_pos.start_dome_pos_server()
time.sleep(3.)
ret6 = dome.start_dome_server()
ret7 = weather.start_weather_server()

ret8 = antenna_enc.enc_client('172.20.0.11',8001)
ret9 = dome_pos.dome_pos_client('172.20.0.11',8005)
ret10 = weather.weather_client('172.20.0.11',3001)

p = sub.Popen("/home/amigos/NECST/soft/server/server_stop.py", shell = "True")

ret10.get_weather()
t = t_w = time.time()

while(1):
	ret = ret8.get_azel()
	ret = ret9.dome_encoder_acq()
	if t-t_w >= 1.0:
		ret = ret10.get_weather()
		t_w = time.time()
	t = time.time()
# necrx


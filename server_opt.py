#! /usr/bin/env python
#-*- coding: utf-8 -*-


# necopt

import time
import m4
import abs
import geomech

ret1 = m4.start_m4_server()
ret2 = abs.start_abs_server()
ret3 = geomech.start_geomech_server()

time.sleep(1)
ret4 = geomech.geomech_client('172.20.0.12',8100)

while(1):
    ret = ret4.get_geomech_col()
    print("server_opt.py : main_loop")
    time.sleep(0.1)


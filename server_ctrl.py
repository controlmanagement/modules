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
#import dome_pos
import dome
import os
import subprocess as sub


#for kill server
pid = os.getpid()
f = open("server_ctrl.pid", "w")
f.write(pid)
f.close()


ret3 = antenna_enc.start_enc_server()
time.sleep(3.)
ret4 = antenna_nanten_controller.start_antenna_server()

ret6 = dome.start_dome_server()

ret8 = antenna_enc.enc_client('172.20.0.11',8001)
#ret9 = dome.dome_client('172.20.0.11',8007)

while(1):
    time.sleep(0.1)
    print('server_ctrl.py : main_loop')
    ret = ret8.get_azel()
    #ret = ret9.dome_encoder_acq()
# necrx


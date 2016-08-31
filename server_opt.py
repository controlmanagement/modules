#! /usr/bin/env python
#-*- coding: utf-8 -*-


# necopt

import time
import m2
import m4
import abs
import geomech
import datetime
import ccd
import os


pid = os.getpid()
f = open("server_opt.pid", "w")
f.write(str(pid))
f.close()

ret1 = m4.start_m4_server()
ret2 = abs.start_abs_server()
ret3 = geomech.start_geomech_server()

time.sleep(1)
ret4 = geomech.geomech_client('172.20.0.12',8100)
date = datetime.date.today()
b_day = date.day
ret5 = ccd.start_ccd_server()
ret6 = m2.start_m2_server()

while(1):
    try:
        date = datetime.date.today()
        ret = ret4.get_geomech_col()
        print("server_opt.py : main_loop")
        
        if b_day != date.day:
            ret4.record_log()
            b_day = date.day
        
        time.sleep(0.1)
    
    except Exception as e:
        f = open("error.txt","a")
        timestmp = time.strftime('%Y%m%d_%H%M%S')
        f.write(timestmp+"\n")
        f.write('type:' + str(type(e))+"\n")
        f.write('args:' + str(e.args)+"\n")
        f.write('message:' + e.message+"\n")
        f.write(str(e)+"\n")
        f.write("\n")
        f.close()
        
        while 1:
            print("================geomech error================")
            time.sleep(0.1)
        


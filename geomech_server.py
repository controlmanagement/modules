#! /usr/bin/env python
#-*- coding: utf-8 -*-

import time
import geomech

ret0 = geomech.start_geomech_server()
time.sleep(1)
ret1 = geomech.geomech_client('172.20.0.12',8100)

while(1):
    re1 = ret1.get_geomech_col()
    re2 = ret1.read_geomech_col()
    tv = time.time()
    print (tv, re2)
    time.sleep(0.1)

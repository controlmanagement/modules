#! /usr/bin/env python
#-*- coding: utf-8 -*-

import time
import geomech

ret0 = geomech.start_geomech_server()
ret1 = geomech.geomech_client('172.20.0.12',8100)

while(1):
    ret = ret1.get_geomech_col()
    geomech_col = ret1.read_geomech()
    tv = time.time()
    print (tv, geomech_col)
    time.sleep(0.1)

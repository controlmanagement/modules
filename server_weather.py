#! /usr/bin/env python
#-*- coding: utf-8 -*-

import time
import os
import weather


#for server kill
pid = os.getpid()
f = open("server_weather.pid", "w")
f.write(pid)
f.close()


ret6 = weather.start_weather_server()

time.sleep(.1)

ret7 = weather.weather_client('172.20.0.11',3001)

while(1):
    ret = ret7.get_weather()
    time.sleep(10)

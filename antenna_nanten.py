#! /usr/bin/env python
# coding:utf-8

"""
望遠鏡及びdomeの制御
"""

import math
import time
import core.controller

class antenna_nanten(core.controller.antenna):
    def __init__(self):
        import telescope_nanten.antenna_nanten_controller
        import telescope_nanten.dome
        import pymeasure.weather
        self.antenna = telescope_nanten.antenna_nanten_controller.antenna_client('172.20.0.11',8003)
        self.dome = telescope_nanten.dome.dome_client('172.20.0.11',8007)
        self.weather = pymeasure.weather.weather_monitor_client('172.20.0.11',3002)
        self.start_limit_check()
        #self.start_domestatus_check()
        pass 
    
    def drive_on(self):
        """drive_on"""
        self.antenna.contactor_on()
        self.antenna.drive_on()
        return
    
    def drive_off(self):
        """drive_off"""
        self.antenna.drive_off()
        self.antenna.contactor_off()
        return
    
    def test_move(self,az_speed,el_speed,dist_arcsec = 5 * 3600):
        self.antenna.test_move(az_speed,el_speed,dist_arcsec)
        return
    
    def azel_move(self, az_arcsec, el_arcsec, az_rate = 12000, el_rate =12000):
        """antennaを(Az, El)に動かす"""
        self.antenna.azel_move_start(az_arcsec, el_arcsec, az_rate, el_rate)
        return
    
    def azel_stop(self):
        """antennaのazel駆動を止める"""
        self.antenna.azel_stop()
        return
    
    def radec_move(self, ra, dec, code_mode, off_x = 0, off_y = 0, hosei = 'hosei_230.txt',offcoord = "HORIZONTAL", lamda=2600, az_max_rate=16000, el_max_rate=12000,dcos=1):
        """antennaを(Ra, Dec)に動かす
        ra,dec は degreeで
        code_mode → 'J2000' or 'B1950'"""
        
        gx = ra*math.pi/180.
        gy = dec*math.pi/180.
        condition = self.weather.read_weather()
        temp = float(condition[6])+273.
        press = float(condition[12])
        humid = float(condition[9])/100.
        self.antenna.thread_start('EQUATRIAL', 0, gx, gy, 0, 0, code_mode, temp, press, humid, lamda, dcos, hosei, offcoord, off_x, off_y, az_max_rate, el_max_rate)
        return
    
    def galactic_move(self, l, b, off_x = 0, off_y = 0, hosei = 'hosei_230.txt', offcoord = "HORIZONTAL", lamda=2600, az_max_rate=16000, el_max_rate=12000,dcos=0):
        """antennaを(l, b)に動かす"""
        gx = l*math.pi/180.
        gy = b*math.pi/180.
        condition = self.weather.read_weather()
        temp = float(condition[6])+273.
        press = float(condition[12])
        humid = float(condition[9])/100.
        self.antenna.thread_start('GALACTIC', 0, gx, gy, 0, 0, 0, temp, press, humid, lamda, dcos, hosei, offcoord, off_x, off_y, az_max_rate, el_max_rate)
        return
    
    def planet_move(self, number, off_x = 0, off_y = 0, hosei = 'hosei_230.txt', offcoord = "HORIZONTAL", lamda=2600, az_max_rate=16000, el_max_rate=12000, dcos=0):
        """antennaをplanetに動かす
        1.Mercury 2.Venus 3. 4.Mars 5.Jupiter 6.Saturn 7.Uranus 8.Neptune, 9.Pluto, 10.Moon, 11.Sun"""
        ##debug
        #print('planet_move!!!, {number}'.format(**locals()))
        #print('planet_move!!!, %s, %s'%(self.antenna, self.antenna.thread_start))
        ##debug-end
        condition = self.weather.read_weather()
        temp = float(condition[6])+273.
        press = float(condition[12])
        humid = float(condition[9])/100.
        self.antenna.thread_start('PLANET', number, 0, 0, 0, 0, 0, temp, press, humid, lamda, dcos, hosei, offcoord, off_x, off_y, az_max_rate, el_max_rate)
        return
    
    def set_offset(self, off_x, _off_y, off_coord = "HORIZONTAL"):
        self.antenna.set_offset(off_coord, off_x, off_y)
        return
    
    def tracking_end(self):
        """trackingの終了"""
        self.antenna.tracking_end()
        return
    
    def otf_start(self, sx, sy, dcos, coord_sys, dx, dy, dt, n, rampt, delay, lamda, hosei, code_mode, ntarg=0, off_coord = "HORIZONTAL", off_x=0, off_y=0):
        condition = self.weather.read_weather()
        temp = float(condition[6])+273.
        press = float(condition[12])
        humid = float(condition[9])/100.
        
        start_x = sx-float(dx)/2.-float(dx)/float(dt)*rampt
        start_y = sy-float(dy)/2.-float(dy)/float(dt)*rampt
        total_t = rampt + dt * n
        end_x = sx + dx * (n - 0.5)
        end_y = sy + dy * (n - 0.5)
        mjd = 40587 + time.time()/(24.*3600.)
        
        self.antenna.otf_thread_start(mjd+delay/24./3600., start_x, start_y, mjd+(delay+total_t)/24./3600., end_x, end_y, dcos, coord_sys, hosei,temp, press, humid, lamda, code_mode, ntarg, off_coord, off_x, off_y)
        return mjd+(delay+rampt)/24./3600.
    
    def otf_tracking_end(self):
        self.antenna.otf_tracking_end()
        return
    
    def otf_end(self):
        self.antenna.otf_stop()
        return
    
    def read_track(self):
        ret = self.antenna.read_track()
        return ret
    
    def clear_error(self):
        """errorのclear"""
        self.antenna.clear_error()
        return
    
    def start_limit_check(self):
        self.antenna.start_limit_check()
        return
    
    def stop_limit_check(self):
        self.antenna.stop_limit_check()
        return
    
    def read_error(self):
        ret = self.antenna.read_error()
        return ret
    
# for dome
    
    def start_domestatus_check(self):
        self.dome.start_status_check()
        return
    
    def stop_domestatus_check(self):
        self.dome.stop_status_check()
        return
    
    def dome_open(self):
        self.dome.dome_open()
        return
    
    def dome_close(self):
        self.dome.dome_close()
        return
    
    def memb_open(self):
        self.dome.memb_open()
        return
    
    def memb_close(self):
        self.dome.memb_close()
        return
    
    def dome_move(self, dome_az):
        self.dome.move(dome_az)
        return
    
    def dome_stop(self):
        self.dome.dome_stop()
        return
    
    def dome_track(self):
        self.dome.start_thread()
        return
    
    def dome_track_end(self):
        self.dome.end_thread()
        return
    

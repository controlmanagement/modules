#! /usr/bin/env python
# coding:utf-8

"""
望遠鏡及びdomeの制御
1/15現在 望遠鏡のみ
"""

import math

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
		self.start_domestatus_check()
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
	
	def azel_move(self, az_arcsec, el_arcsec, az_rate = 12000, el_rate =12000):
		"""antennaを(Az, El)に動かす"""
		self.antenna.azel_move(az_arcsec, el_arcsec, az_rate, el_rate)
		return
	
	def radec_move(self, ra, dec, code_mode, off_x = 0, off_y = 0, hosei = 'hosei_230.txt',offcoord = "HORIZONTAL"):
		"""antennaを(Ra, Dec)に動かす"""
		"""ra,dec は degreeで"""
		"""code_mode → 'J2000' or 'B1950'"""
		
		gx = ra*math.pi/180.
		gy = dec*math.pi/180.
		condition = self.weather.read_weather()
		temp = float(condition[6])+273.
		press = float(condition[12])
		humid = float(condition[9])/100.
		self.antenna.thread_start('EQUATRIAL', 0, gx, gy, 0, 0, code_mode, temp, press, humid, 2600, 0, hosei, offcoord, off_x, off_y)
		return
	
	def planet_move(self, number,hosei,offcoorde = "HORIZONTAL", off_x =0, off_y = 0):
		"""antennaをplanetに動かす"""
		"""1.Mercury 2.Venus 3.Moon 4.Mars 5.Jupiter 6.Saturn 7.Uranus 8.Neptune, 9.Pluto, 10.Sun"""
		condition = self.weather.read_weather()
		temp = float(condition[6])+273.
		press = float(condition[12])
		humid = float(condition[9])/100.
		self.antenna.thread_start('PLANET', 0, 0, 0, 0, 0, 0, temp, press, humid, 2600, 0, hosei, offcoorde, off_x, off_y)
		return
	
	def set_offset(self, off_x, _off_y, off_coord = "HORIZONTAL"):
		self.antenna.set_offset(off_coord, off_x, off_y)
		return
	
	def tracking_end(self):
		"""trackingの終了"""
		self.antenna.tracking_end()
		return
	
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
	
	def dome_track(self):
		self.dome.start_thread()
		return
	
	def dome_track_end(self):
		self.dome.end_thread()
		return



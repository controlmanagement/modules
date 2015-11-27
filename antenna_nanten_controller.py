import time
import math
import coord
from pyslalib import slalib
import nanten_main_controller
import pyinterface





class antenna_nanten_controller(object):
	
	longitude = -67.70308139*math.pi/180
	latitude = -22.96995611*math.pi/180
	height = 4863.85
	#temporary dut1
	dut1 = 0.14708  #delta UT:  UT1-UTC (UTC seconds)
	
	# for socket
	instruction = ''
	dx = dy = dt = n = rampt = delay = 0
	
	
	def __init__(self):
		self.coord = coord.coord_calc()
		self.nanten = nanten_main_controller.nanten_main_controller()
		pass
	
	def move_azel(self, real_az, real_el, dcos, hosei = 'hosei_230.txt', off_az = 0, off_el = 0):
		if dcos == 0:
			real_el += off_el
			real_az += off_az
		else:
			real_el += off_el
			real_az = real_az+off_az/math.cos(real_el) # because of projection
		
		"""
		if set_coord == "HORIZONTAL":
			ret = self.coord.apply_kisa(real_az, real_el, hosei)
			target_az = real_az+ret[0]
			target_el = real_el+ret[1]
		else:
			target_az = real_az
			target_el = real_el
		"""
		ret = self.coord.apply_kisa(real_az, real_el, hosei) # until define the set_coord
		target_az = real_az+ret[0]
		target_el = real_el+ret[1]
		
		#track = self.nanten.move_azel(target_az, target_el, az_max_rate, el_max_rate)
		track = self.nanten.move_azel(target_az, target_el) #until define the set_coord
		return track
	
	def move_radec(self, gx, gy, gpx, gpy, code_mode, temp, pressure, humid, lamda, dcos, hosei = 'hosei_230.txt', off_x = 0, off_y = 0):
		#lamda not equals lambda
		# Calculate current MJD
		tv = time.time()
		tv_sec = int(tv)
		tv_usec = tv - tv_sec
		mjd = (tv_sec + tv_usec/1000000.)/24./3600. + 40587.0 # 40587.0 = MJD0
		tai_utc = 36.0 # tai_utc=TAI-UTC  2015 July from ftp://maia.usno.navy.mil/ser7/tai-utc.dat

		# lamda is wavelength(not lambda)
		if code_mode == "B1950":
			ret = slalib.sla_fk425(gx, gy, gpx, gpy, 0, 0)
			gaJ2000 = ret[0]
			gdJ2000 = ret[1]
			gpaJ2000 = ret[2]
			gpdJ2000 = ret[3]
		else: # code mode == "J2000"
			gaJ2000 = gx # for check
			gdJ2000 = gy # for check
			gpaJ2000 = gpx # for check
			gpdJ2000 = gpy # for check
		
		ret = slalib.sla_map(gaJ2000, gdJ2000, gpaJ2000, gpdJ2000, 0, 0, 2000, mjd + (tai_utc + 32.184)/(24.*3600.))
		"""
		ret[0] = apparent_ra
		ret[1] = apparent_dec
		"""
		if dcos == 0:
			new_dec = ret[1] + off_y
			new_ra = ret[0] + off_x
		else:
			new_dec = ret[1] + off_y
			new_ra = ret[0] + off_x/math.cos(new_dec)
			dcos = 0
		
		ret = slalib.sla_aop(ret[0], ret[1], mjd, self.dut1, self.longitude, self.latitude, self.height, 0, 0, temp, pressure, humid, lamda, tlr=0.0065)
		"""
		ret[0] = azimath(radian, N=0, E=90)
		ret[1] = zenith(radian)
		"""
		#From zenith angle to elevation 
		real_az = ret[0]
		real_el = math.pi/2. - ret[1]
		
		track = self.move_azel(real_az, real_el, dcos, hosei)
		return track
	
	def move_lb(self, gx, gy, temp, pressure, humid, lamda, dcos, hosei = 'hosei_230.txt', off_x = 0, off_y = 0):
		if dcos == 0:
			gy += off_y
			gx += off_x
		else:
			gy += off_y
			gx = gx+off_x/math.cos(gy)
		
		ret = slalib.sla_galeq(gx, gy)
		"""
		gaJ2000 = ret[0]
		gdj2000 = ret[1]
		gpaJ2000 = gpdJ2000 = 0
		"""
		
		track = self.move_radec(ret[0], ret[1], 0, 0, "J2000", temp, pressure, humid, lamda, dcos, hosei)
		return track
	
	def move_planet(self, ntarg,code_mode, temp, pressure, humid, lamda, dcos, hosei = 'hosei_230.txt', off_x = 0, off_y = 0):
		ret = self.coord.calc_planet_coordJ2000(ntarg)
		if len(ret) == 1:
			print(ret) #error
			return
			
		ret = self.coord.planet_J2000_geo_to_topo(ret[0], ret[1], ret[2], ret[3], self.dut1, self.longitude, self.latitude, self.height)
		
		#ret[2] = ra, ret[3] = dec
		self.move_radec(ret[2], ret[3], 0, 0,code_mode, temp, pressure, humid, lamda, dcos, hosei  , off_x , off_y )
		return
	
	def calc_otf(self, x, y, dcos, coord_sys, dx, dy, dt, n, rampt, delay, temp = 0, pressure = 0, humid = 0, lamda = 0, hosei = 'hosei_230.txt', code_mode = 'J2000'):
		start_x = x-float(dx)/2.-float(dx)/float(dt)*rampt
		start_y = y-float(dy)/2.-float(dy)/float(dt)*rampt
		total_t = rampt + dt * n
		end_x = x + dx * (n - 0.5)
		end_y = y + dy * (n - 0.5)
		
		Az_track_flag = El_track_flag = 'TRUE'
		while Az_track_flag == 'TRUE' or El_track_flag == 'TRUE':
			if coord_sys == 'HORIZONTAL':
				ret = self.move_azel(start_x, start_y,dcos)
				Az_track_flag = ret[0]
				El_track_flag = ret[1]
			elif coord_sys == 'EQUATORIAL':				
				# ret = self.move_radec(start_x, start_y, gpx, gpy, code_mode, temp, pressure, humid, lamda, dcos, hosei)
				# gpx,gpy => 0 for radio observation or planet observation
				# change this when you do optical observation
				ret = self.move_radec(start_x, start_y, 0, 0, code_mode, temp, pressure, humid, lamda, dcos, hosei)

				Az_track_flag = ret[0]
				El_track_flag = ret[1]
			else:
				ret = self.move_lb(start_x, start_y, temp, pressure, humid, lamda, dcos, hosei)
				Az_track_flag = ret[0]
				El_track_flag = ret[1]
		mjd = 40587 + time.time()/(24.*3600.)
		self.otf(mjd+delay/24./3600., start_x, start_y, mjd+(delay+total_t)/24./3600., end_x, end_y, dcos, coord_sys, hosei)
		return
	
	def otf(self, mjd_start, start_x, start_y, mjd_end, end_x, end_y, dcos, coord_sys, hosei,temp = 0, pressure = 0, humid = 0, lamda = 0, code_mode = 'J2000'):
		otf_end_flag = 0
		
		while otf_end_flag == 0:
			mjd = 40587 + time.time()/(24.*3600.)
			if mjd >= mjd_start and mjd <= mjd_end:
				off_x = (end_x - start_x) / (mjd_end - mjd_start) * (mjd - mjd_start) + start_x
				off_y = (end_y - start_y) / (mjd_end - mjd_start) * (mjd - mjd_start) + start_y
				
				if coord_sys == 'HORIZONTAL':
					self.move_azel(off_x, off_y,dcos)
				elif coord_sys == 'EQUATORIAL':
					self.move_radec(off_x, off_y, 0, 0, code_mode, temp, pressure, humid, lamda, hosei)
				elif coord_sys == 'GALACTIC':
					self.move_lb(off_x, off_y, temp, pressure, humid, lamda,dcos)
			
			if mjd > mjd_end:
				otf_end_flag = 1
		return

def antenna_client(host, port):
	client = pyinterface.server_client_wrapper.control_client_wrapper(antenna_nanten_controller, host, port)
	return client

def antenna_monitor_client(host, port):
	client = pyinterface.server_client_wrapper.monitor_client_wrapper(antenna_nanten_controler, host, port)
	return client

def start_antenna_server(port1 = 5925, port2 = 5926):
	antenna = antenna_nanten_controller()
	server = pyinterface.server_client_wrapper.server_wrapper(antenna, '', port1, port2)
	server.start()
	return server

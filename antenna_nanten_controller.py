import time
import math
import coord
from pyslalib import slalib
import nanten_main_controller




class antenna_nanten_controller(object):
	
	longitude = -67.70308139*math.pi/180
	latitude = -22.96995611*math.pi/180
	height = 4863.85
	#temporary dut1
	dut1 = 0.14708  #delta UT:  UT1-UTC (UTC seconds)
	
	
	def __init__(self):
		self.coord = coord.coord_calc()
		self.nanten = nanten_main_controller.nanten_main_controller()
		pass
	
	def move_azel(self, az, el, hosei, off_az = 0, off_el = 0):
		
		real_el += off_el
		real_az += off_az # greal_az = (goffazeldcos == 0)? (greal_az + goffaz): (greal_az + goffaz / cos(greal_el));
		
		if set_coord == "HORIZONTAL":
			ret = self.coord.apply_kisa(real_az, real_el, hosei)
			target_az = real_az+ret[0]
			target_el = real_el+ret[1]
		else:
			target_az = real_az
			target_el = real_el
		
		self.nanten.move_azel(target_az, target_el, az_max_rate, el_max_rate)
		return
	
	def move_radec(self, gx, gy, gpx, gpy, code_mode, temp, pressure, humid, lamda, hosei):
		#lamda not equals lambda
		# Calculate current MJD
		tv = time.time()
		tv_sec = int(tv)
		tv_usec = tv - tv_sec
		mjd = (tv_sec + tv_usec/1000000.)/24./3600. + 40587.0 # 40587.0 = MJD0
		
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
		
		ret = slalib.sla_aap(gaJ2000, gdJ2000, gpaJ2000, gpdJ2000, 0, 0, 2000, mjd + (tai_utc + 32.184)/(24.*3600.))
		"""
		ret[0] = apparent_ra
		ret[1] = apparent_dec
		"""
		ret = slalib.sla_aop(ret[0], ret[1], mjd, self.dut1, self.longitude, self.latitude, self.height, 0, 0, temp, pressure, humid, lamda, tlr)
		"""
		ret[0] = azimath(radian, N=0, E=90)
		ret[1] = zenith(radian)
		"""
		#From zenith angle to elevation 
		real_az = ret[0]
		real_el = math.pi/2. - ret[1]
		
		self.move_azel(real_az, real_el, hosei)
		return
	
	def move_lb(self, gx, gy, temp, pressure, humid, lamda, hosei):
		ret = self.sla.slaGaleq(gx, gy)
		"""
		gaJ2000 = ret[0]
		gdj2000 = ret[1]
		gpaJ2000 = gpdJ2000 = 0
		"""
		
		self.move_radec(ret[0], ret[1], 0, 0, "J2000", temp, pressure, humid, lamda, hosei)
		return
	
	def move_planet(self, ntarg):
		
		ret = self.coord.calc_planet_coordJ2000(ntarg)
		if len(ret) == 1:
			print(ret) #error
			return
			
		ret = self.coord.planet_J2000_geo_to_topo(ret[0], ret[1], ret[2], ret[3], self.dut1, self.longitude, self.latitude, self.height)
		
		#ret[2] = ra, ret[3] = dec
		self.move_radec(ret[2], ret[3], 0, 0)
		return
		

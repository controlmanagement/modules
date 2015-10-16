import time
import math
import coord
import slalib
import nanten_main_controller




class antenna_nanten_controller(object):
	
	longitude = -67.70308139*math.pi/180
	latitude = -22.96995611*math.pi/180
	height = 4863.85
	#temporary dut1
	dut1 = 0.14708  #delta UT:  UT1-UTC (UTC seconds)
	
	
	
	
	
	
	def __init__(self):
		self.coord = coord.coord_calc()
		self.sla = slalib.slalib_controller()
		
		
		
		
		
	def move_azel(self, ):
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	def move_radec(self, gx, gy, gpx, gpy, code_mode = "J2000", temp, pressure, humid, lamda = 1300, off_az, off_el):
		# Calculate current MJD
		tv = time.time()
		tv_sec = int(tv)
		tv_usec = tv - tv_sec
		mjd = (tv_sec + tv_usec/1000000.)/24./3600. + 40587.0 # 40587.0 = MJD0
		
		# lamda is wavelength
		if code_mode == "B1950":
			ret = self.sla.slaFk425(gx, gy, gpx, gpy, 0, 0)
			gaJ2000 = ret[0]
			gdJ2000 = ret[1]
			gpaJ2000 = ret[2]
			gpdJ2000 = ret[3]
		elif code_mode == "J2000":
			gaJ2000 = gx # for check
			gdJ2000 = gy # for check
			gpaJ2000 = gpx # for check
			gpdJ2000 = gpy # for check
		else:
			print("??????????") #?
			return
		
		ret = self.sla.slaMap(gaJ2000, gdJ2000, gpaJ2000, gpdJ2000, 0, 0, 2000, gmjd + (tai_utc + 32.184)/(24.*3600.))
		"""
		ret[0] = apparent_ra
		ret[1] = apparent_dec
		"""
		ret = self.sla.slaAop(ret[0], ret[1], mjd, self.dut1, self.longitude, self.latitude, self.height, 0, 0, temp, pressure, humid, lambda, tlr)
		"""
		ret[0] = azimath(radian, N=0, E=90)
		ret[1] = zenith(radian)
		"""
		#From zenith angle to elevation 
		real_el = math.pi/2. - ret[1]
		
		real_el += off_el
		real_az += off_az # greal_az = (goffazeldcos == 0)? (greal_az + goffaz): (greal_az + goffaz / cos(greal_el));
		
		self.move_azel()
		
		
		
		
		
		
		
	def move_lb(self, gx, gy):
		ret = self.sla.slaGaleq(gx, gy)
		"""
		gaJ2000 = ret[0]
		gdj2000 = ret[1]
		gpaJ2000 = gpdJ2000 = 0
		"""
		
		self.move_radec(ret[0], ret[1], 0, 0)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	def move_planet(self, ephem, jd_utc, tai_utc, ntarg):
		
		
		ret = self.coord.calc_planet_coordJ2000(ephem, jd_utc, tai_utc, ntarg)
		if len(ret) == 1:
			print(ret) #error
			return
			
		ret = self.coord.planet_J2000_geo_to_topo(ret[0], ret[1], ret[2], ret[3], jd_utc, self.dut1, tai_utc, self.longitude, self.latitude, self.height)
		
		self.move_radec(ret[2], ret[3], 0, 0)
		
		




















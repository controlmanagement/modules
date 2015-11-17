import telescope_nanten.antenna_nanten_controller
#import core.file_manager
#import core.controller
#import dome

class antenna_nanten(object):
	
	"""
	coord_dict = {"J2000"       : telescope_nanten.motor.COORD_J2000,
				  "B1950"       : telescope_nanten.motor.COORD_B1950,
				  "LB"          : telescope_nanten.motor.COORD_LB,
				  "GALACTIC"    : telescope_nanten.motor.COORD_LB,
				  "APPARENT"    : telescope_nanten.motor.COORD_APP,
				  "HORIZONTAL"  : telescope_nanten.motor.COORD_HORIZONTAL,
				  "SAME"        : telescope_nanten.motor.COORD_SAME}
	"""

	def __init__(self):
		self.antenna = telescope_nanten.antenna_nanten_controller.antenna_client('192.168.100.187', 5930)
		#self.dev = core.file_manager.dev_manager()
		#self.d = dome.dome_controller()
		return
		
	"""
	def use_radio(self):
		self.m.kisa()
		self.m.set_radio()
		self.m.set_lambda(float(self.dev["LIGHT_SPEED"]) / float(self.dev['1stLO1'])*1000.)
		return


	def use_opt(self):
		self.m.kisa()
		self.m.set_opt()
		return
	

	def set_condition(self, pressure, humidity, temperature_C):
		self.m.set_pressure(pressure)
		self.m.set_humidity(humidity)
		self.m.set_temperature(temperature_C)
		return
	"""
	

	def move(self, x, y, coord_sys, offset_x, offset_y, dcos, hosei, temp = 0, pressure = 0, humid = 0, lamda = 0, planet = 0, px = 0, py = 0, code_mode = 'J2000'):
		# offset_coord is not temporary available
		
		
		if planet:
			self.antenna.move_planet(planet, temp, pressure, humid, lamda)
			pass
		else:
			if coord_sys == 'HORIZONTAL':
				self.antenna.move_azel(x, y, dcos, hosei, offset_x, offset_yl)
			elif coord_sys == 'ECLIPTIC' :
				self.antenna.move_radec(x, y, px, py, code_mode, temp, pressure, humid, lamda, dcos, hosei, offset_x, offset_y)
			elif coord_sys == 'GALACTIC':
				self.antenna.move_lb(x, y, temp, pressure, humid, lamda, dcos, hosei, offset_x, offset_y)
		return
	
	
	
	
	def move_track(self, x, y, coord_sys, offset_x, offset_y, offset_dcos, temp = 0, pressure = 0, humid = 0, lamda = 0, planet = 0):
		stop_flag = 0
		while stop_flag == 0:
			self.move(x, y, coord_sys, offset_x, offset_y, offset_dcos, temp = 0, pressure = 0, humid = 0, lamda = 0, planet = 0)
			f = open('','r')
			line = f.readline()
			stop_flag = line
			f.close()
			return
	
	def move_opt(self, x, y, px, py, coord, acc):
		#self.m.move_opt(x, y, px, py, self.coord_dict[coord.upper()], acc)
		return


	def scan(self, sx, sy, coord, dcos, dx, dy, dt, n, ramp, delay, temp, pressure, humid, lamda):
		self.antenna.calc_otf(sx, sy, dcos, coord, dx, dy, dt, n, ramp, delay, temp, pressure, humid, lamda)
		return


	def get_status(self):
		#az, el = self.m.get_azel()
		#dome_az = self.d.get_count()
		#return az, el, dome_az
		
		
	def finalize(self):
		self.antenna.stop_tracking()
		return

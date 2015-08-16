import time
import math
import threading
import pyinterface


class dome_get_status():
	touchsensor_pos = [0,-197,-391,-586,-780,-974,-1168,-1363,-1561,-1755,-1948,-2143]
	dome_encoffset = 10000
	dome_enc1loop = 2343
	dome_enc_tel_offset = 1513*360
	dome_enc2arcsec = (3600.0*360/dome_enc1loop)




	def __init__(self):
		self.dio_2 = pyinterface.create_gpg2724(1)
		self.dio_2.initialize()
		self.dio_6 = pyinterface.create_gpg6204(1)
		self.dio_6.initialize()
		pass
	
	def print_msg(self,msg):
		print(msg)
		return

	def print_error(self,msg):
		self.error.append(msg)
		self.print_msg('!!!!ERROR!!!!')
		return

	def get_action(self):
		ret = [0]
		self.dio_2.di_input(ret, ?, ?)
		if ret == 0:
			move_status = ''
		else:
			move_status = ''
		return ret

	def get_door_status(self):
		ret = [0,0,0,0,0,0]
		self.dio_2.di_input(ret, ?, ?)
		if ret[0] == 0:
			right_act = 'off'
		else:
			right_act = 'drive'
		
		if ret[1] == 0:
			if ret[2] == 0:
				right_pos = 'move'
			else:
				right_pos = 'close'
		else:
			right_pos = 'open'
		
		if ret[3] == 0:
			left_act = 'off'
		else:
			left_act = 'drive'
		
		if ret[4] == 0:
			if ret[5] = 0:
				left_pos = 'move'
			else:
				left_pos = 'close'
		else:
			left_pos = 'open'
		return right_act,right_pos,left_act,left_pos
		
	def get_memb_status(self):
		ret = [0,0,0]
		self.dio_2.di_input(ret, ?, ?)
		if ret[0] == 0:
			memb_act = 'off'
		else:
			memb_act = 'drive'
		
		if ret[1] == 0:
			if ret[2] == 0:
				memb_pos = 'move'
			else:
				memb_pos = 'close'
		else:
			memb_pos = 'open'
		return memb_act,memb_pos

	def get_remote_status(self):
		ret = [0]
		self.dio_2.di_input(ret, ?, ?)
		if ret == 0:
			status = 'remote'
		else:
			status = 'local'
		return ret

	def error_check(self):
		ret = [0,0,0,0,0,0]
		self.dio_2.di_input(ret, ?, ?)
		return ret

	def limit_check(self):
		limit = [0,0,0,0]
		self.dio_2.di_input(ret, ?, ?)
		if limit == [0,0,0,0]:
			ret = 0
		elif limit == [1,0,0,0]:
			ret = 1
		elif limit == [0,1,0,0]:
			ret = 2
		elif limit == [1,1,0,0]:
			ret = 3
		elif limit == [0,0,1,0]:
			ret = 4
		elif limit == [1,0,1,0]:
			ret = 5
		elif limit == [0,1,1,0]:
			ret = 6
		elif limit == [1,1,1,0]:
			ret = 7
		elif limit == [0,0,0,1]:
			ret = 8
		elif limit == [1,0,0,1]:
			ret = 9
		elif limit == [0,1,0,1]:
			ret = 10
		elif limit == [1,1,0,1]:
			ret = 11
		elif limit == [0,0,1,1]:
			ret = 12
		return ret

	def dome_limit(self):
		limit = self.limit_check()
		if limit != 0:
			self.dio_6.set_counter(1, self.touchsensor_pos[limit-1]+dome_encoffset)
		return limit
	
	def dome_encoder_acq(self):
		counter = self.dio_6.get_counter(1)
		dome_enc_arcsec = -((counter-dome_encoffset) * dome_enc2arcsec)-dome_enc_tel_offset
		




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
		self.dio_2.di_input(ret, 0, 1)
		if ret == 0:
			move_status = 'OFF'
		else:
			move_status = 'DRIVE'
		return ret

	def get_door_status(self):
		ret = [0,0,0,0,0,0]
		self.dio_2.di_input(ret, 1, 6)
		if ret[0] == 0:
			right_act = 'OFF'
		else:
			right_act = 'DRIVE'
		
		if ret[1] == 0:
			if ret[2] == 0:
				right_pos = 'MOVE'
			else:
				right_pos = 'CLOSE'
		else:
			right_pos = 'OPEN'
		
		if ret[3] == 0:
			left_act = 'OFF'
		else:
			left_act = 'DRIVE'
		
		if ret[4] == 0:
			if ret[5] = 0:
				left_pos = 'MOVE'
			else:
				left_pos = 'CLOSE'
		else:
			left_pos = 'OPEN'
		return right_act,right_pos,left_act,left_pos
		
	def get_memb_status(self):
		ret = [0,0,0]
		self.dio_2.di_input(ret, ?, ?)
		if ret[0] == 0:
			memb_act = 'OFF'
		else:
			memb_act = 'DRIVE'
		
		if ret[1] == 0:
			if ret[2] == 0:
				memb_pos = 'MOVE'
			else:
				memb_pos = 'CLOSE'
		else:
			memb_pos = 'OPEN'
		return memb_act,memb_pos

	def get_remote_status(self):
		ret = [0]
		self.dio_2.di_input(ret, 7, 3)
		if ret == 0:
			status = 'REMOTE'
		else:
			status = 'LOCAL'
		return ret

	def error_check(self):
		ret = [0,0,0,0,0,0]
		self.dio_2.di_input(ret, 15, 6)
		if ret[0] == 1:
			self.print_error('controll board sequencer error')
		if ret[1] == 1:
			self.print_error('controll board inverter error')
		if ret[2] == 1:
			self.print_error('controll board thermal error')
		if ret[3] == 1:
			self.print_error('controll board communication error')
		if ret[4] == 1:
			self.print_error('controll board sequencer(of dome_door or membrane) error')
		if ret[5] == 1:
			self.print_error('controll board inverter(of dome_door or membrane) error')
		return

	def limit_check(self):
		limit = [0,0,0,0]
		self.dio_2.di_input(ret, 11, 4)
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
		dome_enc_arcsec = -((counter-dome_encoffset)*dome_enc2arcsec)-dome_enc_tel_offset
		while(dome_enc_arcsec>1800.*360):
			dome_enc_arcsec-=3600.*360;
		while(dome_enc_arcsec<=-1800.*360):
			dome_param.dome_enc_arcsec+=3600.*36
		return dome_enc_arcsec



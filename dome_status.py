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
	error = []



	def __init__(self):
		pass
	
	def open(self, ndev1 = 1, ndev2 = 2):
		self.dio_2 = pyinterface.create_gpg2000(ndev1)
		self.dio_6 = pyinterface.create_gpg6204(ndev2)
		return
	
	def print_msg(self,msg):
		print(msg)
		return

	def print_error(self,msg):
		self.error.append(msg)
		self.print_msg('!!!!ERROR!!!!'+ msg)
		return

	def get_action(self):
		ret = self.dio_2.di_check(1, 1)
		if ret == 0:
			move_status = 'OFF'
		else:
			move_status = 'DRIVE'
		return move_status

	def get_door_status(self):
		ret = self.dio_2.di_check(2, 6)
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
			if ret[5] == 0:
				left_pos = 'MOVE'
			else:
				left_pos = 'CLOSE'
		else:
			left_pos = 'OPEN'
		return [right_act, right_pos, left_act, left_pos]
		
	def get_memb_status(self):
		ret = self.dio_2.di_check(8, 3)
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
		return [memb_act, memb_pos]

	def get_remote_status(self):
		ret = self.dio_2.di_check(11, 1)
		if ret[0] == 0:
			status = 'REMOTE'
		else:
			status = 'LOCAL'
		return status

	def error_check(self):
		ret = self.dio_2.di_check(16, 6)
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

	def limit_check(self,ret=13):
		limit = self.dio_2.di_check(12, 4)
		if limit[0:4] == [0,0,0,0]:
			ret = 0
		elif limit[0:4] == [1,0,0,0]:
			ret = 1
		elif limit[0:4] == [0,1,0,0]:
			ret = 2
		elif limit[0:4] == [1,1,0,0]:
			ret = 3
		elif limit[0:4] == [0,0,1,0]:
			ret = 4
		elif limit[0:4] == [1,0,1,0]:
			ret = 5
		elif limit[0:4] == [0,1,1,0]:
			ret = 6
		elif limit[0:4] == [1,1,1,0]:
			ret = 7
		elif limit[0:4] == [0,0,0,1]:
			ret = 8
		elif limit[0:4] == [1,0,0,1]:
			ret = 9
		elif limit[0:4] == [0,1,0,1]:
			ret = 10
		elif limit[0:4] == [1,1,0,1]:
			ret = 11
		elif limit[0:4] == [0,0,1,1]:
			ret = 12
		else :
			self.print_error('at limit_check()')
			return
		
		return ret

	def dome_limit(self):
		limit = self.limit_check()
		if limit != 0:
			self.dio_6.ctrl.set_counter(self.touchsensor_pos[limit-1]+self.dome_encoffset)
		return limit
	
	def dome_encoder_acq(self):
		counter = self.dio_6.get_position()
		dome_enc_arcsec = -((counter-self.dome_encoffset)*self.dome_enc2arcsec)-self.dome_enc_tel_offset
		while(dome_enc_arcsec>1800.*360):
			dome_enc_arcsec-=3600.*360;
		while(dome_enc_arcsec<=-1800.*360):
			dome_enc_arcsec+=3600.*360
		return dome_enc_arcsec



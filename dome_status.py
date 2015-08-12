import time
import math
import threading
import pyinterface


class dome_get_status():



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

	def get_action():
		ret = [0]
		self.dio_2.di_input(ret, ?, ?)
		if ret == 0:
			move_status = ''
		else:
			move_status = ''
		return ret

	def get_door_status():
		ret = [0,0,0,0,0,0]
		self.dio_2.di_input(ret, ?, ?)
		if ret[0] == 0:
			right_act = 'stop'
		else:
			right_act = 'move'
		
		if ret[1] == 0:
			if ret[2] == 0:
				right_pos = 'move'
			else:
				right_pos = 'close'
		else:
			right_pos = 'open'
		
		if ret[3] == 0:
			left_act = 'stop'
		else:
			left_act = 'move'
		
		if ret[4] == 0:
			if ret[5] = 0:
				left_pos = 'move'
			else:
				left_pos = 'close'
		else:
			left_pos = 'open'
		
		







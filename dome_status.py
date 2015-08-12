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

	def get_move_status():
		ret = [0]
		dome_param = self.dio.di_input(ret, ?, ?)
		if ret == 0:
			move_status = ''
		else:
			move_status = ''
		return ret

	def

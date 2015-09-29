import time
import threading
import pyinterface

class abs_controller(object):
	buff = 0x00
	error = []
	
	position = ''
	
	
	def __init__(self, move_org=True):
		self.dio = pyinterface.create_gpg2000(1)
		pass
		
	def print_msg(self, msg):
		print(msg)
		return
		
	def print_error(self, msg):
		self.error.append(msg)
		self.print_msg('!!!! ERROR !!!! ' + msg)
		return
	
	def get_pos(self):
		ret = self.position = self.dio.ctrl.in_byte('FBIDIO_IN1_8')
		if ret == 0x09:
			self.position = 'IN'
		elif ret == 0x05:
			self.position = 'OUT'
		else:
			self.position = 'MOVE'
		return

	def move(self, dist, lock=True):
		self.get_pos()
		if dist == 'IN':
			self.buff = 0x00
		else:
			self.buff = 0x01
		while dist != self.position:
			self.dio.ctrl.out_byte('FBIDIO_OUT1_8', self.buff)
			self.get_pos()
		return
	
	def read_pos(self):
		return self.position

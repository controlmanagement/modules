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
		ret = self.position = self.dio.in_byte(FBIDIO_IN1_8)
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
		while dist == self.position:
			self.dio.out_byte(FBIDIO_OUT1_8, buff)
			self.get_pos()
		return
	
	def read_position(self):
		return self.position
	
	def slider():
		client = pyinterface.server_client_wrapper.control_client_wrapper(
			slider_controller, '192.168.40.13', 4004)
		return client
	
	def slider_monitor():
		client = pyinterface.server_client_wrapper.monitor_client_wrapper(
			slider_controller, '192.168.40.13', 4104)
		return client

	def start_slider_server():
		slider = slider_controller()
		server = pyinterface.server_client_wrapper.server_wrapper(slider,
				'', 4004, 4104)
		server.start()
		return server

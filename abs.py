
import time
import threading
import pyinterface

class abs_controller(object):
	pro = 0x00
	buff = 0x00
	error = []
	
	position = ''
	
	
	def __init__(self, ndev = 3):
		self.dio = pyinterface.create_gpg2000(ndev)
		self.get_pos()
		pass
	
	def print_msg(self, msg):
		print(msg)
		return
	
	def print_error(self, msg):
		self.error.append(msg)
		self.print_msg('!!!! ERROR !!!! ' + msg)
		return
	
	def get_pos(self):
		ret = self.dio.ctrl.in_byte('FBIDIO_IN1_8')
		if ret == 0x02:
			self.position = 'IN'
		elif ret == 0x01:
			self.position = 'OUT'
		elif ret == 0x03:
			self.position = 'MOVE'
		else:
			self.print_error('limit error')
			return
		return self.position

	def move(self, dist):
		pos = self.get_pos()
		if pos == dist:
			print('m4 is already ' + dist)
			return
		if dist == 'IN':
			self.pro = 0x00
			self.buff = 0x01
		elif dist == 'OUT':
			self.pro = 0x02
			self.buff = 0x03
		self.dio.ctrl.out_byte('FBIDIO_OUT1_8', self.pro)
		time.sleep(1)
		self.dio.ctrl.out_byte('FBIDIO_OUT1_8', self.buff)
		time.sleep(5)
		self.get_pos()
		return
	
	def move_r(self):
		self.move('IN')
		return
	
	def move_sky(self):
		self.move('OUT')
		return
		
	def stop(self):
		self.buff = 0x04
		self.dio.ctrl.out_byte('FBIDIO_OUT1_8', self.buff)
		return
	
	def read_pos(self):
		return self.position

def abs_client(host, port):
	client = pyinterface.server_client_wrapper.control_client_wrapper(abs_controller, host, port)
	return client

def abs_monitor_client(host, port):
	client = pyinterface.server_client_wrapper.monitor_client_wrapper(abs_controller, host, port)
	return client

def start_abs_server(port1 = 6001, port2 = 6002):
	abs = abs_controller()
	server = pyinterface.server_client_wrapper.server_wrapper(abs,'', port1, port2)
	server.start()
	return server

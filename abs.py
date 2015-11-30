import time
import threading
import pyinterface
import threading

class abs_controller(object):
	buff = 0x00
	error = []
	
	position = ''
	
	
	def __init__(self):
		pass
	
	def start_server(self):
		ret = self.start_abs_server()
		return
	
	def open(self, ndev=1):
		self.dio = pyinterface.create_gpg2000(ndev)
		return

	def print_msg(self, msg):
		print(msg)
		return
	
	def print_error(self, msg):
		self.error.append(msg)
		self.print_msg('!!!! ERROR !!!! ' + msg)
		return
	
	def get_pos(self):
		ret = self.dio.ctrl.in_byte('FBIDIO_IN1_8')
		if ret == 0x09:
			self.position = 'IN'
		elif ret == 0x05:
			self.position = 'OUT'
		else:
			self.position = 'MOVE'
		return

	def move(self, dist):
		self.get_pos()
		if dist == 'IN':
			self.buff = 0x00
		elif dist == 'OUT':
			self.buff = 0x01
		while dist != self.position:
			self.dio.ctrl.out_byte('FBIDIO_OUT1_8', self.buff)
			self.get_pos()
		return
	
	def read_pos(self):
		return self.position
	
	def start_thread(self, dist):
		if dist == 'IN':
			self.thread = threading.Thread(target = self.move, args = ('IN', ))
		else: # dist == 'OUT'
			self.thread = threading.Thread(target = self.move, args = ('OUT', ))
		self.thread.start()
		return

def abs_client(host, port):
	client = pyinterface.server_client_wrapper.control_client_wrapper(abs_controller, host, port)
	return client

def abs_monitor_client(host, port):
	client = pyinterface.server_client_wrapper.monitor_client_wrapper(abs_controller, host, port)
	return client

def start_abs_server(port1 = 5921, port2 = 5922):
	abs = abs_controller()
	server = pyinterface.server_client_wrapper.server_wrapper(abs,'', port1, port2)
	server.start()
	return server

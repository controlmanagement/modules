import time
import math
import pyinterface
import threading



class m2_controller(object):
	
	error = []
	position = ''
	count = 0
	
	
	
	def __init__(self):
		pass
	
	def open(self, ndev = 1)
		self.dio = pyinterface.create_gpg2000(ndev)
		pass
		
	def print_msg(self, msg):   
		print(msg)
		return
		
	def print_error(self, msg):
		self.error.append(msg)
		self.print_msg('!!!! ERROR !!!! ' + msg)
		return
	
	def get_count(self):
		
		
		
		
		
		
		
		
		return
	
	
	
	
	
	def move(self, dist, lock=True):
		
		
		
		
		
		
		
		
		
		
		return
	
	def start_thread(self, ):
		self.stop_thread = threading.Event()
		self.thread = threading.Thread(target = self.move, args = ())
		self.thread.start()
		return





def m2_client(host, port):
	client = pyinterface.server_client_wrapper.control_client_wrapper(m2_controller, host, port)
	return client

def m2_monitor_client(host, port):
	client = pyinterface.server_client_wrapper.monitor_client_wrapper(m2controller, host, port)
	return client

def start_m2_server(port1 = ????, port2 = ????):
	m2 = m2_controller()
	server = pyinterface.server_client_wrapper.server_wrapper(m2,'', port1, port2)
	server.start()
	return server




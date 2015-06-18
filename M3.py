import time
import threading
import pyinterface

class M3_controller(object):
	pos_on =
	pos_off =
	speed = 
	low_speed = 
	acc = 
	dec = 
	
	error = []
	
	position = ''
	count = 0
    
	def __init__(self, move_org=True):
		self.dio = pyinterface.create_gpg2724(1)
		if move_org: self.move_org()
		pass
        
	def print_msg(self, msg):
		print(msg)
		return
        
	def print_error(self, msg):
		self.error.append(msg)
		self.print_msg('!!!! ERROR !!!! ' + msg)
		return
    
		def get_count(self):
		self.count = self.dio.di_input()
		return
    
		def move_org(self):
		self.dio.do_output()
		self.dio.do_output()
		self.position = 'org'
		self.get_count
		return

		def move(self, dist, lock=True):
		pos = self.dio.di.input()
		if pos == dist: return
		diff = dist - pos
		if lock: self.dio.do_output()
		else: self.dio.do_output()
        
		self.get_count()
		return
    
	def move_on(self, lock=True):
		self.move(self.pos_on, lock)
		self.position = 'ON'
		return
    
	def move_off(self, lock=True):
		self.move(self.pos_off, lock)
		self.position = 'OFF'
		return
    
	def unlock_brake(self):
		self.dio.do_output(2, 0)
		msg = '!! Electromagnetic brake is now UNLOCKED !!'
		print('*'*len(msg))
		print(msg)
		print('*'*len(msg))
		return
    
	def lock_brake(self):
		self.dio.do_output(0)
		self.get_count()
		print('')
		print('')
		print('!! CAUTION !!')
		print('-------------')
		print('You must execute s.move_org() method, before executing any "move_**" method.')
		print('')
		return
    
	def clear_alarm(self):

		self.dio.do_output(1)
		return
        
	def clear_interlock(self):
      
		self.dio.do_output()
		return

	def read_position(self):
		return self.position
        
	def read_count(self):
		return self.count
    
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


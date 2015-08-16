
import time
import threading
import pyinterface

class mirror_controller(object):
	pos_nagoya = 0
	pos_smart = 180
	speed = 12000
	low_speed = 100
	acc = 12000
	dec = 12000
	
	error = []
	
	position = ''
	count = 0
	
	
	def __init__(self, move_org=True):
		self.mtr = pyinterface.create_gpg7204(1)
		pass
		
	def print_msg(self, msg):
		print(msg)
		return
		
	def print_error(self, msg):
		self.error.append(msg)
		self.print_msg('!!!! ERROR !!!! ' + msg)
		return
	
	def get_count(self):
		self.count = self.mtr.get_position()
		return

	def move(self, dist, lock=True):
		if dist == 'nagoya':
			nstep = -60500
		else:
			nstep = 60500
		status = self.mtr.get_status()
		if status:
			if status == 0x0004:
				pos = 'smart'
				if dist == pos:
					self.print_msg('m4 is already out')
					self.position = 'smart'
					return
			elif status == 0x0008:
				pos = 'nagoya'
				if dist == pos:
					self.print_msg('m4 is already in')
					self.position = 'nagoya'
					return
			else:
				self.print_error('limit error')
				return
		else:
			self.speed = 1000
			self.low_speed = 100
			self.acc = 1000
			self.dec = 1000
		if lock: self.mtr.move_with_lock(self.speed, nstep, self.low_speed,
										 self.acc, self.dec)
		else: self.mtr.move(self.speed, nstep, self.low_speed, self.acc,
							self.dec)
		self.get_count()
		if dist == 'nagoya':
			self.position = 'nagoya'
		else:
			self.position = 'smart'
		return
	
	def unlock_brake(self):
		"""
		Unlock the electromagnetic brake of the slider.
		
		Args
		====
		Nothing.
		
		Returns
		=======
		Nothing.
		
		Examples
		========
		>>> s.unlock_brake()
		"""
		self.mtr.do_output()
		msg = '!! Electromagnetic brake is now UNLOCKED !!'
		print('*'*len(msg))
		print(msg)
		print('*'*len(msg))
		return
	
	def lock_brake(self):
		"""
		Lock the electromagnetic brake of the slider.
		
		Args
		====
		Nothing.
		
		Returns
		=======
		Nothing.
		
		Examples
		========
		>>> s.lock_brake()
		"""
		self.mtr.do_output()
		self.get_count()
		print('')
		print('')
		print('!! CAUTION !!')
		print('-------------')
		print('You must execute s.move_org() method, before executing any "move_**" method.')
		print('')
		return
	
	def clear_alarm(self):
		"""
		Clear the alarm.
		
		Args
		====
		Nothing.
		
		Returns
		=======
		Nothing.
		
		Examples
		========
		>>> s.clear_alarm()
		"""
		self.mtr.do_output()
		return
		
	def clear_interlock(self):
		"""
		Clear the interlock.
		
		Args
		====
		Nothing.
		
		Returns
		=======
		Nothing.
		
		Examples
		========
		>>> s.clear_interlock()
		"""
		self.mtr.ctrl.off_inter_lock()
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


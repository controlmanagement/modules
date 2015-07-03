
import time
import threading
import pyinterface

class membrane_controller(object):
	pos_open = 

	pos_close = 
	buffer = [0, 0]

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
		self.dio.di_output()     #get_count
		return

	def move_org(self):
		 """
		 Move to ORG position.
		 
		 NOTE: This method will be excuted in instantiation.
		 
		 Args
		 ====
		 Nothing.
		 
		 Returns
		 =======
		 Nothing.
		 
		 Examples
		 ========
		 >>> s.move_org()
		 """
		get_memb()
		if pos == ??:
			buffer = [0, 1]
			self.dio.do_output(???, buffer, 6, 2)
			while pos == ??:
				get_memb()
			buffer = [0, 0]
			self.dio.do_output(???, buffer, 6, 2)     #set_org
			self.position = 'ORG'
			self.get_count()
			return

	def move_open(self, lock=True):
		"""
		Move to OPEN position.
		
		NOTE: If the membrane is already at open position, it doesn't move.
		
		Args
		====
		< lock : bool :  > (optional)
		    If <lock> is False, the method returns immediately.
		    Otherwise, it returns after the membrane stopped.
		
		Returns
		=======
		Nothing.
		
		Examples
		========
		>>> s.move_open()
		"""
		get_memb()
		if pos == ??:
			buffer = [1, 1]
			self.dio.do_output(???, buffer, 6, 2)
			while pos == ??:
				get_memb()
			buffer = [0, 0]
			self.dio.do_output(???, buffer, 6, 2)
			return
		self.position = 'OPEN'
		return

	def move_close(self, lock=True):
		"""
		Move to CLOSE position.
		
		NOTE: If the membrane is already at CLOSE position, it doesn't move.
		
		Args
		====
		< lock : bool :  > (optional)
		    If <lock> is False, the method returns immediately.
		    Otherwise, it returns after the membrane stopped.
		
		Returns
		=======
		Nothing.
		
		Examples
		========
		>>> s.move_close()
		
		"""
		get_memb()
		if pos == ??:
			buffer = [0, 1]
			self.dio.do_output(???, buffer, 6, 2)
			while pos == ??:
				get_memb()
			buffer = [0, 0]
			self.dio.do_output(???, buffer, 6, 2)
			return
		self.position = 'CLOSE'
		return
























	def unlock_brake(self):
		"""
		Unlock the electromagnetic brake of the membrane.
		
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
		self.dio.do_output()     #unlock_brake
		msg = '!! Electromagnetic brake is now UNLOCKED !!'
		print('*'*len(msg))
		print(msg)
		print('*'*len(msg))
		return

	def lock_brake(self):
		"""
		Lock the electromagnetic brake of the membrane.
		
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
		self.dio.do_output()     #lock_brake
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
		self.dio.do_output()     #clear_alarm
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
		self.dio.ctrl.off_inter_lock()     #※clear_interlock
		return




	def read_position(self):
		return self.position

	def read_count(self):
		return self.count






	def slider():
		client = pyinterface.server_client_wrapper.control_client_wrapper(slider_controller
			, '192.168.40.13', 4004)
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
















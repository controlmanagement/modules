import time
import threading
import pyinterface
import memb_enc



class membrane_controller(object):
	buffer = [0, 0]
	error = []
	position = ''
	count = 0







	def __init__(self):
		self.dio = pyinterface.create_gpg2724(1)
		self.memb = memb_enc.get_pos()
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
		move_open()
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
		self.memb.get_pos()
		if pos == 'CLOSE':
			global buffer
			membrane_controller.buffer = [1, 1]
			self.dio.do_output(self, membrane_controller.buffer, 6, 2)
			while pos != 'OPEN':
				self.memb.get_memb()
			membrane_controller.buffer = [0, 0]
			self.dio.do_output(self, membrane_controller.buffer, 6, 2)
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
		self.memb.get_pos()
		if pos == 'OPEN':
			global buffer
			membrane_controller.buffer = [0, 1]
			self.dio.do_output(self, membrane_controller.buffer, 6, 2)
			while pos != 'CLOSE':
				get_memb()
			buffer = [0, 0]
			self.dio.do_output(self, membrane_controller.buffer, 6, 2)
			return
		self.position = 'CLOSE'
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





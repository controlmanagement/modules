import time
import threading
import pyinterface
import dome_status



class membrane_controller(object):
	buffer = [0, 0]
	error = []
	position = ''
	act = ''


	def __init__(self):
		self.dio = pyinterface.create_gpg2000(1)
		self.status = dome_status.dome_get_status()
		pass

	def print_msg(self, msg):
		print(msg)
		return

	def print_error(self, msg):
		self.error.append(msg)
		self.print_msg('!!!! ERROR !!!! ' + msg)
		return

	def get_status(self):
		ret = self.status.get_memb_status()
		self.act = ret[0]
		self.position = ret[1]
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
		self.move_close()
		self.get_status()
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
		self.get_status()
		if self.position == 'CLOSE':
			global buffer
			membrane_controller.buffer = [1, 1]
			self.dio.do_output(membrane_controller.buffer, 6, 2)
			while self.position != 'OPEN':
				self.get_status()
			membrane_controller.buffer = [0, 0]
			self.dio.do_output(membrane_controller.buffer, 6, 2)
			return
		self.get_status()
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
		self.get_status()
		if self.position == 'OPEN':
			global buffer
			membrane_controller.buffer = [0, 1]
			self.dio.do_output(membrane_controller.buffer, 6, 2)
			while self.position != 'CLOSE':
				self.get_status()
			membrane_controller.buffer = [0, 0]
			self.dio.do_output(membrane_controller.buffer, 6, 2)
			return
		self.get_status()
		return




	def read_position(self):
		return self.position

	def read_act(self):
		return self.act

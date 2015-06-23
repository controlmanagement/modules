import time
import threading
import pyinterface



class dome_controller(object):
	speed = 
	low_speed = 
	acc = 
	dec = 
	





	def _init_(self, ):
    	self.dio = pyinterface.create_gpg2724(1)
    	if move_org: self.move_org()
    	pass

	def print_msg(self,msg):
		print(msg)
		return

	def print_error(self,msg):
		self.error.append(msg)
		self.print_msg('!!!!ERROR!!!!')
		return

	def get_count(self):
		self.dio.di_output()
		return

	def do_output(self, count):		
		self.dio.do_output()	
		self.get_count()
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
		self.do_output()	#lock_brake
		self.get_count()
		
		return








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
		
		self.dio.do_output()	#move_org
		self.position = 'ORG'
		self.get_count()
		return

	def move(self, dist, speed, lock=True):
		pos = self.dio.di_input()	#get_position
		if pos == dist: return
		diff = dist - pos
		if lock: self.dio.do_output()
		else: speed = 
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








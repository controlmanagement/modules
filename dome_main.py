import time
import math
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
		if lock: self.lock_brake()
		else: speed = 
		self.do_output()
		self.get_count()
		return

	def adjust_speed(self, diff, dist):
		if fabs(diff) >= ???:
			speed = ???
			acc = ???
			move(self,dist,speed,lock=True)
		pass








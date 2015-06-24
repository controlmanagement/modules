import time
import math
import threading
import pyinterface



class dome_controller_main(object):
	speed = 3600 #[arcsec/sec]
	low_speed = 






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
		
		if lock: self.lock_brake()
		self.dio.do_output(self, )	#move_org
		self.position = 'ORG'
		self.get_count()
		return

	def move(self, dist, speed, lock=True):
		pos = self.dio.di_input()	#get_position
		if pos == dist: return
		diff = dist - pos
		dir = (360.0 + dis) % 360.0
		if dir - 180.0 <= pos:
			turn = "right"
		else:
			turn = "left"
		if lock: self.lock_brake()
		else: speed = 
		self.do_output()
		self.get_count()
		return

	def adjust_speed(self, diff, dist):
		if fabs(diff) >= ??? and fabs(diff) < ???:
			speed = ???
			move(self,dist,speed,lock=True)
		elif fabs(diff) >= ???:
			speed = ???
		else:
			speed = ???











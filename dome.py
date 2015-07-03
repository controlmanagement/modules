import time
import math
import threading
import pyinterface



class dome_controller(object):
	speed = 3600 #[arcsec/sec]
	low_speed = 
	buffer = [0,0,0,0,0,0]






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
		dist = ???
		pos = get_pos()
		diff = dist - pos
		if diff != 0:
			move(self, dist, speed, lock=True)	#move_org
		self.position = 'ORG'
		self.get_count()
		return


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


	def memb_move(self, dist):
		m_pos = get_memb()
		if dist = 'open':
			buffer[4:6] = [1,1]
			while m_pos == ???:
				self.dio.do_output(???, buffer, 0, 6)
				m_pos = get_memb()
			buffer[5] = 0
			self.dio.do_output(???, buffer, 0, 6)
		else:
			buffer[4:6] = [0,1]
			while m_pos == ???????????:
				self.dio.so_output(???, buffer, 0, 6)
				m_pos = get_memb()
			buffer[5] = 0
			self.dio.do_output(???, buffer, 0, 6)


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


	def move(self, dist, speed, lock=True):
		pos = self.dio.di_input()	#get_position
		if pos == dist: return
		diff = dist - pos
		dir = (360.0 + dis) % 360.0
		if dir - 180.0 <= pos:
			turn = 'right'
		else:
			turn = 'left'
		if lock: self.lock_brake()
		if fabs(diff) >= ??? and fabs(diff) < ???:
			speed = ???
		elif fabs(diff) >= ???:
			speed = ???
		else:
			speed = ???
		self.do_output(???, turn, speed, buffer)
		self.get_count()
		return

	def emergency_stop():
		stop = [1]
		self.dio.do_output(self, stop, 10, 1)
		self.print_msg('!!EMERGENCY STOP!!')
		return

	def dome_fan(self, fan):
		if fan == 'on':
			fan_bit = [1, 1]
			self.dio.do_output(????, fan_bit, 8, 2)
		else:
			fan_bit = [0, 0]
			self.dio.do_output(????, fan_bit, 8, 2)
		return


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



;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


	def read_position(self):
		return self.position

	def read_count(self):
		return self.count

	def get_count(self):
		self.dio.di_output()
		return

	def get_memb(self):
		self.
		return

	def do_output(self, turn, speed, buffer):
		if turn = 'right': buffer[0] = 0
		else: buffer[0] = 1
		if speed <= ???:
			buffer[2:4] = [0, 0]
		elif speed <= ??? and speed > ???:
			buffer[2:4] = [1, 0]
		else:
			buffer[2:4] = [0, 1]
		if stop = 1:
			buffer[1] = 0
		else: buffer[1] = 1
		self.dio.do_output(?, buffer, 0, 6)
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



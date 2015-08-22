import time
import math
import threading
import pyinterface
import dome_status



class dome_controller(object):
	speed = 3600 #[arcsec/sec]
	buffer = [0,0,0,0,0,0]
	stop = [0]







	def __init__(self):
		self.dio = pyinterface.create_gpg2000(1)
		self.dio.initialize()
		self.status = dome_status.dome_get_status()
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
		
		

		dist = 90
		pos_arcsec = self.status.dome_encoder_acq()
		pos = pos_arcsec/3600
		diff = dist - pos
		if diff != 0:
			self.move(dist, speed, lock=True)	#move_org
		self.position = 'ORG'
		self.get_count()
		return



	def move(self, dist, speed, lock=True):
		pos = self.dio.di_input()	#get_position
		if pos == dist: return
		diff = dist - pos
		dir = (360.0 + dist) % 360.0
		if dir - 180.0 <= pos:
			turn = 'right'
		else:
			turn = 'left'
		if math.fabs(diff) >= 90 and math.fabs(diff) < 150:
			speed = 'mid'
		elif math.fabs(diff) >= 150:
			speed = 'high'
		else:
			speed = 'low'
		if diff != 0:
			global buffer
			dome_controller.buffer[1] = [1]
			self.do_output(turn, speed)
			while diff == 0:
				pos_arcsec = self.status.dome_encoder_acq()
				pos = pos_arcsec/3600
				diff = dist - pos
				if math.fabs(diff) <= 0.2:
					diff = 0
				else:
					self.do_output(self, turn, speed)
		dome_controller.buffer[1] = [0]
		self.do_output(self, turn, speed)
		self.get_count()
		return



	def emergency_stop(self):
		global stop
		dome_controller.stop = [1]
		self.dio.do_output(dome_controller.stop, 10, 1)
		self.print_msg('!!EMERGENCY STOP!!')
		return

	def dome_fan(self, fan):
		if fan == 'on':
			fan_bit = [1, 1]
			self.dio.do_output(self, fan_bit, 8, 2)
		else:
			fan_bit = [0, 0]
			self.dio.do_output(self, fan_bit, 8, 2)
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




	def read_count(self):
		return self.count

	def get_count(self):
		self.count = self.status.dome_encoder_acq()
		return

	def do_output(self, turn, speed):
		global buffer
		global stop
		if turn == 'right': dome_controller.buffer[0] = 0
		else: dome_controller.buffer[0] = 1
		if speed == 'low':
			dome_controller.buffer[2:4] = [0, 0]
		elif speed == 'mid':
			dome_controller.buffer[2:4] = [1, 0]
		else:
			dome_controller.buffer[2:4] = [0, 1]
		if dome_controller.stop == 1:
			dome_controller.buffer[1] = 0
		else: dome_controller.buffer[1] = 1
		self.dio.do_output(dome_controller.buffer, 0, 6)
		self.get_count()
		return



import time
import math
import threading
import pyinterface
import dome_status
import sys
import antenna_enc
import threading



class dome_controller(object):
	#speed = 3600 #[arcsec/sec]
	buffer = [0,0,0,0,0,0]
	stop = [0]
	error = []


	def __init__(self):
		pass

	def start_server(self):
		ret = self.start_dome_server()
		return

	def open(self, ndev=1):
		self.dio = pyinterface.create_gpg2000(ndev)
		self.status = dome_status.dome_get_status()
		return


	def start_thread(self):
		self.end_track_flag = threading.Event()
		self.thread = threading.Thread(target = self.move_track)
		self.thread.start()
		return

	def end_thread(self):
		self.end_tracking.set()
		self.thread.join()
		return

	def move_track(self):
		while not self.end_track_flag.is_set():
			ret = self.enc.read_azel() # ret[0] = antenna_az
			dome_az = self.get_count()
			self.status.dome_limit()
			if math.fabs(ret[0]-dome_az) >= 2.0:
				self.move(ret[0])

	def print_msg(self,msg):
		print(msg)
		return

	def print_error(self,msg):
		self.error.append(msg)
		self.print_msg('!!!!ERROR!!!!'+msg)
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
		self.move(dist)	#move_org
		self.position = 'ORG'
		self.get_count()
		return



	def move(self, dist):
		pos_arcsec = self.status.dome_encoder_acq()
		pos = pos_arcsec/3600
		pos = pos % 360.0
		dist = dist % 360.0
		diff = dist - pos
		dir = diff % 360.0
		if pos == dist: return
		if dir <= 180:
			turn = 'right'
		else:
			turn = 'left'
		if dir < 90 and dir > 270 :
			speed = 'low'
		elif dir > 150 and dir < 210:
			speed = 'high'
		else:
			speed = 'mid'
		if dir != 0:
			global buffer
			self.buffer[1] = 1
			self.do_output(turn, speed)
			while dir != 0:
				pos_arcsec = self.status.dome_encoder_acq()
				pos = pos_arcsec/3600
				pos = pos % 360.0
				dist = dist % 360.0
				diff = dist - pos
				dir = diff % 360.0
				#print(pos,dist,diff,dir)
				if dir <= 0.5:
					dir = 0
				else:
					if dir < 90 and dir > 270 :
						speed = 'low'
					elif dir > 150 and dir < 210:
						speed = 'high'
					else:
						speed = 'mid'
					self.do_output(turn, speed)
		self.buffer[1] = 0
		self.do_output(turn, speed)
		self.get_count()
		return



	def emergency_stop(self):
		global stop
		dome_controller.stop = [1]
		self.status.dio_2.do_output(self.stop, 11, 1)
		self.print_msg('!!EMERGENCY STOP!!')
		return

	def dome_fan(self, fan):
		if fan == 'on':
			fan_bit = [1, 1]
			self.status.dio_2.do_output(fan_bit, 9, 2)
		else:
			fan_bit = [0, 0]
			self.status.dio_2.do_output(fan_bit, 9, 2)
		return


	def read_count(self):
		return self.count

	def get_count(self):
		self.count = self.status.dome_encoder_acq()
		return self.count

	def do_output(self, turn, speed):
		global buffer
		global stop
		if turn == 'right': self.buffer[0] = 0
		else: self.buffer[0] = 1
		if speed == 'low':
			self.buffer[2:4] = [0, 0]
		elif speed == 'mid':
			self.buffer[2:4] = [1, 0]
		else:
			self.buffer[2:4] = [0, 1]
		if dome_controller.stop[0] == 1:
			self.buffer[1] = 0
		else: self.buffer[1] = 1
		self.status.dio_2.do_output(self.buffer, 1, 6)
		self.get_count()
		return


def dome_client(host, port):
	client = pyinterface.server_client_wrapper.control_client_wrapper(dome_controller, host, port)
	return client

def dome_monitor_client(host, port):
	client = pyinterface.server_client_wrapper.monitor_client_wrapper(dome_controller, host, port)
	return client

def start_dome_server(port1 = ????, port2 = ????):
	dome = dome_controller()
	server = pyinterface.server_client_wrapper.server_wrapper(dome,'', port1, port2)
	server.start()
	return server

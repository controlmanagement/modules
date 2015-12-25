import time
import math
import threading
import pyinterface
import dome_status
import sys
import antenna_enc
import threading
import antenna_enc



class dome_controller(object):
	#speed = 3600 #[arcsec/sec]
	buffer = [0,0,0,0,0,0]
	stop = [0]
	error = []
	count = 0


	def __init__(self):
		pass
	
	def start_server(self):
		ret = self.start_dome_server()
		return
	
	def open(self):
		self.status = dome_status.dome_get_status()
		self.status.open()
		self.dio = pyinterface.create_gpg2000(5)
		self.enc = antenna_enc.enc_controller()
		return
	
	def start_thread(self):
		self.end_track_flag = threading.Event()
		self.thread = threading.Thread(target = self.move_track)
		self.thread.start()
		return

	def end_thread(self):
		self.end_track_flag.set()
		self.thread.join()
		buff = [0]
		self.dio.do_output(buff, 2, 1)
		return

	def move_track(self):
		ret = self.status.dome_encoder_acq()
		while not self.end_track_flag.is_set():
			ret = self.enc.get_azel()
			ret[0] = ret[0]/3600. # ret[0] = antenna_az
			dome_az = self.get_count()
			dome_az = dome_az/3600.
			self.status.dome_limit()
			if math.fabs(ret[0]-dome_az) >= 2.0:
				self.move(ret[0])
	
	def test(self, num): #for track_test
		self.start_thread()
		time.sleep(num)
		self.end_thread()
		return

	def print_msg(self,msg):
		print(msg)
		return

	def print_error(self,msg):
		self.error.append(msg)
		self.print_msg('!!!!ERROR!!!!'+msg)
		return

	def move_org(self):
		dist = 90
		self.move(dist)	#move_org
		self.get_count()
		return
	
	def move(self, dist):
		pos_arcsec = self.status.dome_encoder_acq()
		pos = pos_arcsec/3600.
		pos = pos % 360.0
		dist = dist % 360.0
		diff = dist - pos
		dir = diff % 360.0
		if pos == dist: return
		if dir < 0:
			if abs(dir) >= 180:
				turn = 'right'
			else:
				turn = 'left'
		else:
			if abs(dir) >= 180:
				turn = 'left'
			else:
				turn = 'right'
		if abs(dir) < 5.0 or abs(dir) > 355.0 :
			speed = 'low'
		elif abs(dir) > 15.0 or abs(dir) < 345.0:
			speed = 'high'
		else:
			speed = 'mid'
		if dir != 0:
			global buffer
			self.buffer[1] = 1
			self.do_output(turn, speed)
			while dir != 0:
				pos_arcsec = self.status.dome_encoder_acq()
				pos = pos_arcsec/3600.
				pos = pos % 360.0
				dist = dist % 360.0
				diff = dist - pos
				dir = diff % 360.0
				#print(pos,dist,diff,dir)
				if dir <= 0.5:
					dir = 0
				else:
					if abs(dir) < 5.0 or dir > 355.0:
						speed = 'low'
					elif abs(dir) > 20.0 or abs(dir) < 340.0:
						speed = 'high'
					else:
						speed = 'mid'
					self.do_output(turn, speed)
		buff = [0]
		self.dio.do_output(buff, 2, 1)
		self.get_count()
		return
	
	def dome_open(self):
		ret = self.get_door_status()
		if ret[1] != 'OPEN' and ret[3] != 'OPEN':
			buff = [1, 1]
			self.dio.do_output(buff, 5, 2)
			d_door = self.get_door_status()
			while ret[1] != 'OPEN':
				time.sleep(5)
				ret = self.get_door_status()
		buff = [0, 0]
		self.dio.do_output(buff, 5, 2)
		return
	
	def dome_close(self):
		ret = self.get_door_status()
		if ret[1] != 'CLOSE' and ret[3] != 'CLOSE':
			buff = [0, 1]
			self.dio.do_output(buff, 5, 2)
			while ret[1] != 'CLOSE':
				time.sleep(5)
				ret = self.get_door_status()
		buff = [0, 0]
		self.dio.do_output(buff, 5, 2)
		return
	
	def memb_open(self):
		ret = self.get_memb_status()
		if ret[1] != 'OPEN':
			buff = [1, 1]
			self.dio.do_output(buff, 7, 2)
			while ret[1] != 'OPEN':
				time.sleep(5)
				ret = self.get_memb_status()
		buff = [0, 0]
		self.dio.do_output(buff, 7, 2)
		return
	
	def memb_close(self):
		ret = self.get_memb_status()
		if ret[1] != 'CLOSE':
			buff = [0, 1]
			self.dio.do_output(buff, 7, 2)
			while ret[1] != 'CLOSE':
				time.sleep(5)
				ret = self.get_memb_status()
		buff = [0, 0]
		self.dio.do_output(buff, 7, 2)
		return
	
	def emergency_stop(self):
		global stop
		dome_controller.stop = [1]
		self.status.dio.do_output(self.stop, 11, 1)
		self.print_msg('!!EMERGENCY STOP!!')
		return
	
	def dome_fan(self, fan):
		if fan == 'on':
			fan_bit = [1, 1]
			self.dio.do_output(fan_bit, 9, 2)
		else:
			fan_bit = [0, 0]
			self.dio.do_output(fan_bit, 9, 2)
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
		self.dio.do_output(self.buffer, 1, 6)
		self.status.dome_limit()
		self.get_count()
		return
	
	def get_action(self):
		ret = self.dio.di_check(1, 1)
		if ret == 0:
			move_status = 'OFF'
		else:
			move_status = 'DRIVE'
		return move_status

	def get_door_status(self):
		ret = self.dio.di_check(2, 6)
		if ret[0] == 0:
			right_act = 'OFF'
		else:
			right_act = 'DRIVE'
		
		if ret[1] == 0:
			if ret[2] == 0:
				right_pos = 'MOVE'
			else:
				right_pos = 'CLOSE'
		else:
			right_pos = 'OPEN'
		
		if ret[3] == 0:
			left_act = 'OFF'
		else:
			left_act = 'DRIVE'
		
		if ret[4] == 0:
			if ret[5] == 0:
				left_pos = 'MOVE'
			else:
				left_pos = 'CLOSE'
		else:
			left_pos = 'OPEN'
		return [right_act, right_pos, left_act, left_pos]
		
	def get_memb_status(self):
		ret = self.dio.di_check(8, 3)
		if ret[0] == 0:
			memb_act = 'OFF'
		else:
			memb_act = 'DRIVE'
		
		if ret[1] == 0:
			if ret[2] == 0:
				memb_pos = 'MOVE'
			else:
				memb_pos = 'CLOSE'
		else:
			memb_pos = 'OPEN'
		return [memb_act, memb_pos]

	def get_remote_status(self):
		ret = self.dio.di_check(11, 1)
		if ret[0] == 0:
			status = 'REMOTE'
		else:
			status = 'LOCAL'
		return status

	def error_check(self):
		ret = self.dio.di_check(16, 6)
		if ret[0] == 1:
			self.print_error('controll board sequencer error')
		if ret[1] == 1:
			self.print_error('controll board inverter error')
		if ret[2] == 1:
			self.print_error('controll board thermal error')
		if ret[3] == 1:
			self.print_error('controll board communication error')
		if ret[4] == 1:
			self.print_error('controll board sequencer(of dome_door or membrane) error')
		if ret[5] == 1:
			self.print_error('controll board inverter(of dome_door or membrane) error')
		return
	
		def limit_check(self):
		limit = self.dio.di_check(12, 4)
		ret = 0
		if limit[0:4] == [0,0,0,0]:
			ret = 0
		elif limit[0:4] == [1,0,0,0]:
			ret = 1
		elif limit[0:4] == [0,1,0,0]:
			ret = 2
		elif limit[0:4] == [1,1,0,0]:
			ret = 3
		elif limit[0:4] == [0,0,1,0]:
			ret = 4
		elif limit[0:4] == [1,0,1,0]:
			ret = 5
		elif limit[0:4] == [0,1,1,0]:
			ret = 6
		elif limit[0:4] == [1,1,1,0]:
			ret = 7
		elif limit[0:4] == [0,0,0,1]:
			ret = 8
		elif limit[0:4] == [1,0,0,1]:
			ret = 9
		elif limit[0:4] == [0,1,0,1]:
			ret = 10
		elif limit[0:4] == [1,1,0,1]:
			ret = 11
		elif limit[0:4] == [0,0,1,1]:
			ret = 12
		return ret
	
	def dome_limit(self):
		limit = self.limit_check()
		if limit != 0:
			self.status.dio.ctrl.set_counter(self.touchsensor_pos[limit-1]+self.dome_encoffset)
		return limit
	


def dome_client(host, port):
	client = pyinterface.server_client_wrapper.control_client_wrapper(dome_controller, host, port)
	return client

def dome_monitor_client(host, port):
	client = pyinterface.server_client_wrapper.monitor_client_wrapper(dome_controller, host, port)
	return client

def start_dome_server(port1 = 9999, port2 = 9999):
	dome = dome_controller()
	server = pyinterface.server_client_wrapper.server_wrapper(dome,'', port1, port2)
	server.start()
	return server


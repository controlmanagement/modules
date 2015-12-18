import time
import threading
import pyinterface
import threading

class m4_controller(object):
	pos_nagoya = 0
	pos_smart = 180
	speed = 12000
	low_speed = 100
	acc = 12000
	dec = 12000
	
	error = []
	
	position = ''
	count = 0
	
	
	def __init__(self):
		pass
	
	def start_server(self):
		ret = self.start_m4_server()
		return

	def open(self, ndev=1):
		self.mtr = pyinterface.create_gpg7204(ndev)
		self.mtr.ctrl.off_inter_lock()
		return

	def print_msg(self, msg):
		print(msg)
		return
		
	def print_error(self, msg):
		self.error.append(msg)
		self.print_msg('!!!! ERROR !!!! ' + msg)
		return
	
	def get_position(self):
		status = self.mtr.ctrl.get_status('MTR_LIMIT_STATUS')
		if status == 0x0008:
			self.position = 'SMART'
		elif status == 0x004:
			self.position = 'NAGOYA'
		else:
			self.print_error('limit_error')
			return
		return self.position

	def move(self, dist):
		if dist == 'NAGOYA':
			nstep = -60500
		else:
			nstep = 60500
		status = self.mtr.ctrl.get_status('MTR_LIMIT_STATUS')
		self.print_msg(status)
		if status:
			if status == 0x0008:
				pos = 'SMART'
				if dist == pos:
					self.print_msg('m4 is already out')
					self.position = 'SMART'
					return
			elif status == 0x0004:
				pos = 'NAGOYA'
				if dist == pos:
					self.print_msg('m4 is already in')
					self.position = 'NAGOYA'
					return
			else:
				self.print_error('limit error')
				return
		
		self.speed = 1000
		self.low_speed = 100
		self.acc = 1000
		self.dec = 1000
		
		self.mtr.move(self.speed, nstep, self.low_speed, self.acc,self.dec)
		self.get_count()
		if dist == 'NAGOYA':
			self.position = 'NAGOYA'
		else:
			self.position = 'SMART'
		return
	
	def unlock_brake(self):
		"""
		Unlock the electromagnetic brake of the slider.
		
		Args
		====
		Nothing.
		
		Returns
		=======
		Nothing.
		
		Examples
		========
		>>> s.unlock_brake()
		"""
		self.mtr.do_output()
		msg = '!! Electromagnetic brake is now UNLOCKED !!'
		print('*'*len(msg))
		print(msg)
		print('*'*len(msg))
		return
	
	def lock_brake(self):
		"""
		Lock the electromagnetic brake of the slider.
		
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
		self.mtr.do_output()
		self.get_count()
		print('')
		print('')
		print('!! CAUTION !!')
		print('-------------')
		print('You must execute s.move_org() method, before executing any "move_**" method.')
		print('')
		return
	
	def clear_alarm(self):
		"""
		Clear the alarm.
		
		Args
		====
		Nothing.
		
		Returns
		=======
		Nothing.
		
		Examples
		========
		>>> s.clear_alarm()
		"""
		self.mtr.do_output()
		return
		
	def clear_interlock(self):
		"""
		Clear the interlock.
		
		Args
		====
		Nothing.
		
		Returns
		=======
		Nothing.
		
		Examples
		========
		>>> s.clear_interlock()
		"""
		self.mtr.ctrl.off_inter_lock()
		return
		
	def read_pos(self):
		return self.position
		
	def read_count(self):
		return self.count
	
	def start_thread(self, status):
		if status == 'NAGOYA':
			self.thread = threading.Thread(target = self.move, args = ('NAGOYA', ))
		else: # status == 'SMART'
			self.thread = threading.Thread(target = self.move, args = ('SMART', ))
		self.thread.start()
		return

def m4_client(host, port):
	client = pyinterface.server_client_wrapper.control_client_wrapper(m4_controller, host, port)
	return client

def m4_monitor_client(host, port):
	client = pyinterface.server_client_wrapper.monitor_client_wrapper(m4_controller, host, port)
	return client

def start_m4_server(port1 = 5923, port2 = 5924):
	m4 = m4_controller()
	server = pyinterface.server_client_wrapper.server_wrapper(m4,'', port1, port2)
	server.start()
	return server



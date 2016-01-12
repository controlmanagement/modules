import math
import time
import sys
import numpy as np

import pyinterface
import antenna_enc

class nanten_main_controller(object):

	#memo
	MOTOR_SAMPLING = 10 
	dt = MOTOR_SAMPLING/1000.

	# define parameter
	m_stop_rate_az = 0
	m_stop_rate_el = 0
	MOTOR_MAXSTEP = 1000
	MOTOR_AZ_MAXRATE = 16000
	MOTOR_EL_MAXRATE = 12000
	
	DEG2ARCSEC = 3600.

	# initialize
	count = 0
	target_az_array = []
	target_el_array = []
	
	az_rate = 0
	el_rate = 0
	az_rate_d = 0
	el_rate_d = 0
	t1 = 0.0
	t2 = 0.0
	t_az = 0.0
	t_el = 0.0
	pre_hensa_az = 0
	pre_hensa_el = 0
	pre_az_arcsec = 0
	pre_el_arcsec = 0
	az_enc_before = 0
	el_enc_before = 0
	ihensa_az = 0
	ihensa_el = 0
	ihensa_azt = 0
	ihensa_elt = 0
	
	# for monitor
	az_encmoni = 0
	el_encmoni = 0
	az_targetmoni = 0
	el_targetmoni = 0
	az_hensamoni = 0
	el_hensa_moni = 0
	az_rate_dmoni = 0
	el_rate_dmoni = 0
	az_targetspeedmoni = 0
	el_targetspeedmoni = 0
	az_currentspeedmoni = 0
	el_currentspeendmoni = 0
	az_ihensamoni = 0
	el_ihensamoni = 0
	limit_check_box = ["FALSE","FALSE","FALSE","FALSE","FALSE","FALSE","FALSE","FALSE","FALSE","FALSE","FALSE","FALSE"]

	def __init__(self):
		self.dio = pyinterface.create_gpg2000(3)
		self.enc = antenna_enc.enc_monitor_client('172.20.0.11',8002)
		pass

	def azel_move(self, az_arcsec, el_arcsec, az_max_rate, el_max_rate):
		test_flag = 1
		while test_flag:
			hensa_flag = 1
			ret = self.enc.read_azel()
			if abs(az_arcsec-ret[0]) >= 1 or abs(el_arcsec-ret[1]) > 1:
				while hensa_flag:
					b_time = time.time()
					self.move_azel(az_arcsec, el_arcsec, az_max_rate, el_max_rate)
					ret = self.enc.read_azel()
					if abs(az_arcsec-ret[0]) <= 1 and abs(el_arcsec-ret[1]) <= 1:
						hensa_flag = 0
						self.dio.ctrl.out_word("FBIDIO_OUT1_16", 0)
						self.dio.ctrl.out_word("FBIDIO_OUT17_32", 0)
						time.sleep(0.02)
					else:
						interval = time.time()-b_time
						if interval <= 0.01:
							time.sleep(0.01-interval)
			else:
				test_flag = 0
		return

	def move_azel(self, az_arcsec, el_arcsec, az_max_rate = 16000, el_max_rate = 12000, m_bStop = 'FALSE'):
		ret = self.calc_pid(az_arcsec, el_arcsec, az_max_rate, el_max_rate)
		az_rate_ref = ret[0]
		el_rate_ref = ret[1]
		Az_track_flag = ret[2]
		El_track_flag = ret[3]

		# command value to target value
		daz_rate = az_rate_ref - self.az_rate_d
		del_rate = el_rate_ref - self.el_rate_d
		
		#limit of acc
		if abs(daz_rate) < self.MOTOR_MAXSTEP:
			az_rate_ref = az_rate_ref
		else:
			if daz_rate < 0:
				a = -1
			else:
				a = 1
			az_rate_ref = self.az_rate_d + a*self.MOTOR_MAXSTEP
		if abs(del_rate) < self.MOTOR_MAXSTEP:
			el_rate_ref = el_rate_ref
		else:
			if del_rate < 0:
				a = -1
			else:
				a = 1
			el_rate_ref = self.az_rate_d + a*self.MOTOR_MAXSTEP
		
		#limit of max v
		if az_rate_ref > self.MOTOR_AZ_MAXRATE:
			az_rate_ref = self.MOTOR_AZ_MAXRATE
		if az_rate_ref < -self.MOTOR_AZ_MAXRATE:
			az_rate_ref = -self.MOTOR_AZ_MAXRATE
		if el_rate_ref > self.MOTOR_EL_MAXRATE:
			el_rate_ref = self.MOTOR_EL_MAXRATE
		if el_rate_ref < -self.MOTOR_EL_MAXRATE:
			el_rate_ref = -self.MOTOR_EL_MAXRATE

		# output to port
		if m_bStop == 'TRUE':
			dummy = self.m_stop_rate_az
		else:
			dummy = int(az_rate_ref)
		self.dio.ctrl.out_word("FBIDIO_OUT1_16", dummy)
		self.az_rate_d = dummy

		if m_bStop == 'TRUE':
			dummy = self.m_stop_rate_el
		else:
			dummy = int(el_rate_ref)
		self.dio.ctrl.out_word("FBIDIO_OUT17_32", dummy)
		self.el_rate_d = dummy

		#for monitor
		self.az_encmoni = self.az_enc_before
		self.el_encmoni = self.el_enc_before
		self.az_targetmoni = self.pre_az_arcsec
		self.el_targetmoni = self.pre_el_arcsec
		self.az_hensamoni = self.pre_hensa_az
		self.el_hensamoni = self.pre_hensa_el
		self.az_rate_dmoni = self.az_rate_d
		self.el_rate_dmoni = self.el_rate_d
		self.az_targetspeedmoni = self.target_speed_az
		self.el_targetspeedmoni = self.target_speed_el
		self.az_currentspeedmoni = self.current_speed_az
		self.el_currentspeedmoni = self.current_speed_el
		self.az_ihensamoni = self.ihensa_azt
		self.el_ihensamoni = self.ihensa_elt

		return [Az_track_flag, El_track_flag]

	def calc_pid(self, az_arcsec, el_arcsec, az_max_rate, el_max_rate):
		# Default
		"""
		Paz = 3.8
		Iaz = 8
		Daz = 0.11
		Pel = 3.73
		Iel = 8
		Del = 0.07
		"""
		# New parameter
		p_az_coeff = 3.3
		i_az_coeff = 2.0
		d_az_coeff = 0.
		s_az_coeff = 0.
		p_el_coeff = 3.3
		i_el_coeff = 3.0
		d_el_coeff = 0.
		s_el_coeff = 0.

		m_bAzTrack = "FALSE"
		m_bElTrack = "FALSE"

		if self.t2 == 0.0:
			self.t2 = time.time()
		
		ret = self.enc.read_azel()
		az_enc = ret[0]
		el_enc = ret[1]

		if az_enc > 40*3600 and az_arcsec+360*3600 < 220*3600:
			az_arcsec += 360*3600
		elif az_enc < -40*3600 and az_arcsec-360*3600 > -220*3600:
			az_arcsec -= 360*3600
		
		if 10000 < math.fabs(self.az_rate):
			m_bAzTrack = "TRUE" #def Paz=2?
		else:
			# az_err_integral += (self.az_err_before+az_err)*self.dt/2.+azv_acc*0.0
			m_bAzTrack = 'FALSE'
			pass
		if 10000 < math.fabs(self.el_rate):
			m_bElTrack = "TRUE" #def Pel=2?
		else:
			#el_err_integral += (self.el_err_before+el_err)*self.dt/2.+elv_acc*0.0
			m_bElTrack = 'FALSE'
			pass

		#calculate ichi_hensa
		hensa_az = az_arcsec-az_enc
		hensa_el = el_arcsec-el_enc

		dhensa_az = hensa_az - self.pre_hensa_az
		dhensa_el = hensa_el - self.pre_hensa_el
		if math.fabs(dhensa_az) > 1:
			dhensa_az = 0
		if math.fabs(dhensa_el) > 1:
			dhensa_el = 0
		
		self.t1 = time.time()
		if self.t_az == 0.0 and self.t_el == 0.0:
			self.t_az = self.t_el = self.t1
		else:
			if (az_enc - self.az_enc_before) != 0.0:
				self.current_speed_az = (az_enc - self.az_enc_before) / (self.t1-self.t_az)
				self.t_az = self.t1
			if (el_enc - self.el_enc_before) != 0.0:
				self.current_speed_el = (el_enc - self.el_enc_before) / (self.t1-self.t_el)
				self.t_el = self.t1
		
		# for first move
		if self.pre_az_arcsec == 0:
			self.target_speed_az = 0
		else:
			self.target_speed_az = (az_arcsec-self.pre_az_arcsec)/(self.t1-self.t2)
		if self.pre_el_arcsec == 0: 
			self.target_speed_el = 0
		else:
			self.target_speed_el = (el_arcsec-self.pre_el_arcsec)/(self.t1-self.t2)
		ret = self.medi_calc(self.target_speed_az, self.target_speed_el)
		self.target_speed_az = ret[0]
		self.target_speed_el = ret[1]
		
		self.ihensa_az += (hensa_az+self.pre_hensa_az)/2 
		self.ihensa_el += (hensa_el+self.pre_hensa_el)/2
		
		#if math.fabs(hensa_az) > math.fabs(self.current_speed_az)/10.+10.:
			#self.ihensa_az = 0
		#if math.fabs(hensa_el) > math.fabs(self.current_speed_el)/10.+10.:
			#self.ihensa_el = 0
		if math.fabs(hensa_az) > 150:
			self.ihensa_az = 0
		if math.fabs(hensa_el) > 150:
			self.ihensa_el = 0
		
		self.ihensa_azt = self.ihensa_az*(self.t1-self.t2)
		self.ihensa_elt = self.ihensa_el*(self.t1-self.t2)

		#self.az_rate = target_speed_az * 20.9 + (current_speed_az*20.9 - self.az_rate) * s_az_coeff + p_az_coeff*hensa_az + i_az_coeff*ihensa_az*(self.t1-self.t2) + d_az_coeff*dhensa_az/(self.t1-self.t2)
		#self.el_rate = target_speed_el * 20.9 + p_el_coeff*hensa_el + i_el_coeff*ihensa_el*(self.t1-self.t2) + d_el_coeff*dhensa_el/(self.t1-self.t2)
		self.az_rate = self.target_speed_az + (self.current_speed_az - self.az_rate) * s_az_coeff + p_az_coeff*hensa_az + i_az_coeff*self.ihensa_azt + d_az_coeff*dhensa_az/(self.t1-self.t2)
		self.el_rate = self.target_speed_el + (self.current_speed_el - self.el_rate) * s_el_coeff + p_el_coeff*hensa_el + i_el_coeff*self.ihensa_elt + d_el_coeff*dhensa_el/(self.t1-self.t2)
		
		if math.fabs(hensa_az) < 8000 and self.az_rate > 10000:
			self.az_rate = 10000
		
		if math.fabs(hensa_az) < 8000 and self.az_rate < -10000:
			self.az_rate = -10000
		
		if math.fabs(hensa_el) < 9000 and self.el_rate > 10000:
			self.el_rate = 10000
		
		if math.fabs(hensa_el) < 7000 and self.el_rate < -8000:
			self.el_rate = -8000
		
		#update
		self.az_enc_before = az_enc
		self.el_enc_before = el_enc
		self.pre_hensa_az = hensa_az
		self.pre_hensa_el = hensa_el
		
		self.pre_az_arcsec = az_arcsec
		self.pre_el_arcsec = el_arcsec
		
		if az_max_rate > 16000:
			az_max_rate = 16000
		if el_max_rate > 12000:
			el_max_rate = 12000
		
		if (el_enc < 30.*self.DEG2ARCSEC and self.el_rate < 0 ) or (el_enc > 70.*self.DEG2ARCSEC and self.el_rate > 0):
			el_max_rate = min(0, el_max_rate)
		if (az_enc < -270.*self.DEG2ARCSEC and self.az_rate < 0) or (az_enc > 270.*self.DEG2ARCSEC and self.az_rate > 0): 
			az_max_rate = min(1600, az_max_rate); #bug?
		
		#lmit of speed
		if self.az_rate > az_max_rate:
			self.az_rate = az_max_rate
		if self.az_rate < -az_max_rate:
			self.az_rate = -az_max_rate
		if self.el_rate > el_max_rate:
			self.el_rate = el_max_rate
		if self.el_rate < -el_max_rate:
			self.el_rate = -el_max_rate
		
		if az_enc <= -270*self.DEG2ARCSEC and self.az_rate < 0:
			self.az_rate = 0
		if az_enc >= 380*self.DEG2ARCSEC and self.az_rate > 0:
			self.az_rate = 0
		
		if el_enc <= 0*self.DEG2ARCSEC and self.el_rate < 0:
			self.el_rate = 0 
		if el_enc >= 90*self.DEG2ARCSEC and self.el_rate > 0:
			self.el_rate = 0
		self.t2 = self.t1
		
		az_rate_ref = int(self.az_rate) #??
		el_rate_ref = int(self.el_rate) #??
		return [az_rate_ref, el_rate_ref, m_bAzTrack, m_bElTrack]
	
	def medi_calc(self, target_az, target_el):
		target_num = 13 # number of median array
		if self.count < target_num:
			self.target_az_array.insert(0, target_az)
			self.target_el_array.insert(0, target_el)
			self.count += 1
		else:
			self.target_az_array.insert(0, target_az)
			self.target_el_array.insert(0, target_el)
			self.target_az_array.pop(13)
			self.target_el_array.pop(13)
		
		median_az = np.median(self.target_az_array)
		median_el = np.median(self.target_el_array)
		return [median_az, median_el]
	
	def antenna_limit_check(self):
		stop_flag = 0
		ret = [0]*3
		ret[0] = self.dio.ctrl.in_byte('FBIDIO_IN1_8')
		ret[1] = self.dio.ctrl.in_byte('FBIDIO_IN9_16')
		ret[2] = self.dio.ctrl.in_byte('FBIDIO_IN17_24')
		
		if (ret[0]>>4 & 0x01) == 0:
			print('!!!soft limit CW!!!')
			self.limit_check_box[0] = "TRUE"
			stop_flag = 1
		if (ret[0]>>5 & 0x01) == 0:
			print('!!!soft limit CCW!!!')
			self.limit_check_box[1] = "TRUE"
			stop_flag = 1
		if (ret[0]>>6 & 0x01) == 0:
			print('!!!soft limit UP!!!')
			self.limit_check_box[2] = "TRUE"
			stop_flag = 1
		if (ret[0]>>7 & 0x01) == 0:
			print('!!!soft limit DOWN!!!')
			self.limit_check_box[3] = "TRUE"
			stop_flag = 1
		if (ret[1]>>0 & 0x01) == 0:
			print('!!!1st limit CW!!!')
			self.limit_check_box[4] = "TRUE"
			stop_flag = 1
		if (ret[1]>>1 & 0x01) == 0:
			print('!!!1st limit CCW!!!')
			self.limit_check_box[5] = "TRUE"
			stop_flag = 1
		if (ret[1]>>2 & 0x01) == 0:
			print('!!!1st limit UP!!!')
			self.limit_check_box[6] = "TRUE"
			stop_flag = 1
		if (ret[1]>>3 & 0x01) == 0:
			print('!!!1st limit DOWN!!!')
			self.limit_check_box[7] = "TRUE"
			stop_flag = 1
		if (ret[1]>>4 & 0x01) == 0:
			print('!!!2nd limit CW!!!')
			self.limit_check_box[8] = "TRUE"
			stop_flag = 1
		if (ret[1]>>5 & 0x01) == 0:
			print('!!!2nd limit CCW!!!')
			self.limit_check_box[9] = "TRUE"
			stop_flag = 1
		if (ret[1]>>6 & 0x01) == 0:
			print('!!!2nd limit UP!!!')
			self.limit_check_box[10] = "TRUE"
			stop_flag = 1
		if (ret[1]>>7 & 0x01) == 0:
			print('!!!2nd limit DOWN!!!')
			self.limit_check_box[11] = "TRUE"
			stop_flag = 1
		return stop_flag
	
	def read_azel(self):
		return [self.az_encmoni, self.el_encmoni, self.az_targetmoni, self.el_targetmoni, self.az_hensamoni, self.el_hensamoni, self.az_rate_dmoni, self.el_rate_dmoni,
		self.az_targetspeedmoni, self.el_targetspeedmoni, self.az_currentspeedmoni, self.el_currentspeedmoni, self.az_ihensamoni ,self.el_ihensamoni]
	
	def read_limit(self):
		# [0]=soft_cw,[1]=soft_ccw,[2]=soft_up,[3]=soft_down,[4]=1st_cw,[5]=1st_ccw,[6]=1st_up,[7]=1st_down,[8]=2nd_cw,[9]=2nd_ccw,[10]=2nd_up,[11]=2nd_down
		return self.limit_check_box

def nanten_main_client(host, port):
	client = pyinterface.server_client_wrapper.control_client_wrapper(nanten_main_controller, host, port)
	return client

def nanten_main_monitor_client(host, port):
	client = pyinterface.server_client_wrapper.monitor_client_wrapper(nanten_main_controller, host, port)
	return client

def start_nanten_main_server(port1 = 7003, port2 = 7004):
	nanten_main = nanten_main_controller()
	server = pyinterface.server_client_wrapper.server_wrapper(nanten_main, '', port1, port2)
	server.start()
	return server

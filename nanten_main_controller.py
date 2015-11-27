import math
import time
import sys
sys.path.append('/home/amigos/python/')
import pyinterface
import antenna_enc





class nanten_main_controller(object):
	
	MOTOR_SAMPLING = 10 #memo
	dt = MOTOR_SAMPLING/1000.
	
	count = 0
	az_array = [0]*13
	AZV_ERR_AVG_NUM = 13
	el_array = [0]*13
	ELV_ERR_AVG_NUM = 13 #AZV_ERR_AVG_NUM = ELV_ERR_AVG_NUM
	#azv_before = elv_before = 0
	az_enc_before = el_enc_before = 0
	az_rate = el_rate = 0
	az_rate_d = el_rate_d = 0
	m_stop_rate_az = m_stop_rate_el = 0
	t1 = t2 = 0.0
	pre_hensa_az = pre_hensa_el = 0
	pre_az_arcsec = pre_el_arcsec = 0
	
	
	def __init__(self):
		self.dio = pyinterface.create_gpg2000(1)
		self.enc = antenna_enc.enc_controller()
		pass

	def move_azel(self, az_arcsec, el_arcsec, az_max_rate = 16000, el_max_rate = 12000, m_bStop = 'FALSE'):
		MOTOR_MAXSTEP = 10000
		MOTOR_AZ_MAXRATE = 16000
		MOTOR_EL_MAXRATE = 12000
		
		ret = self.calc_pid(az_arcsec, el_arcsec, az_max_rate, el_max_rate)
		az_rate_ref = ret[0]
		el_rate_ref = ret[1]
		Az_track_flag = ret[2]
		El_track_flag = ret[3]
		
		# command value to target value
		daz_rate = az_rate_ref - self.az_rate_d
		del_rate = el_rate_ref - self.el_rate_d
		
		#limit of acc
		if abs(daz_rate) < MOTOR_MAXSTEP:
			self.az_rate_d = az_rate_ref
		else:
			if daz_rate < 0:
				a = -1
			else:
				a = 1
			self.az_rate_d += a*MOTOR_MAXSTEP
		if abs(del_rate) < MOTOR_MAXSTEP:
			self.el_rate_d = el_rate_ref
		else:
			if del_rate < 0:
				a = -1
			else:
				a = 1
			self.el_rate_d += a*MOTOR_MAXSTEP
		
		#limit of max v
		if self.az_rate_d > MOTOR_AZ_MAXRATE:
			self.az_rate_d = MOTOR_AZ_MAXRATE
		if self.az_rate_d < -MOTOR_AZ_MAXRATE:
			self.az_rate_d = -MOTOR_AZ_MAXRATE
		if self.el_rate_d > MOTOR_EL_MAXRATE:
			self.el_rate_d = MOTOR_EL_MAXRATE
		if self.el_rate_d < -MOTOR_EL_MAXRATE:
			self.el_rate_d = -MOTOR_EL_MAXRATE
		
		# confirm limit of controll rack => forced outage
		#if(0< motordrv_nanten2_cw_limit()+motordrv_nanten2_ccw_limit()+motordrv_nanten2_up_limit()+motordrv_nanten2_down_limit())
		#	 motordrv_nanten2_drive_on(FALSE,FALSE);
		
		# output to port
		if m_bStop == 'TRUE':
			dummy = self.m_stop_rate_az
		else:
			dummy = int(self.az_rate_d)
		#dummy=m_bStop==TRUE?m_stop_rate_az:motor_param.az_rate_ref;
		self.dio.ctrl.out_word("FBIDIO_OUT1_16", dummy)
		#dioOutputWord(CONTROLER_BASE2,0x00,dummy)  output port is unreliable
		self.az_rate_d = dummy
		
		if m_bStop == 'TRUE':
			dummy = self.m_stop_rate_el
		else:
			dummy = int(self.el_rate_d)
		#dummy=m_bStop==TRUE?m_stop_rate_el:motor_param.el_rate_ref;
		self.dio.ctrl.out_word("FBIDIO_OUT17_32", dummy)
		#dioOutputWord(CONTROLER_BASE2,0x02,dummy);
		self.el_rate_d = dummy
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
		p_az_coeff = 26.2
		i_az_coeff = 1.7
		d_az_coeff = 0.
		s_az_coeff = 0.
		p_el_coeff = 26.2
		i_el_coeff = 0.8
		d_el_coeff = 0.
		
		
		DEG2ARCSEC = 3600
		m_bAzTrack = "FALSE"
		m_bElTrack = "FALSE"
		if self.t2 == 0.0:
			self.t2 = time.time()
		else:
			pass
		
		ret = self.enc.get_azel()
		az_enc = ret[0]
		el_enc = ret[1]
		
		#calculate ichi_hensa
		az_err = az_arcsec-az_enc
		el_err = el_arcsec-el_enc
		
		"""
		#old ver(Unknown)
		az_err_integral_integral = el_err_integral_integral = 0
		
		#integrate error
		az_err_integral_integral+=az_err_integral*dt;
		el_err_integral_integral+=el_err_integral*dt;
		
		#deivative
		azv_err = azv-(az_enc-self.az_enc_before)/self.dt
		elv_err = elv-(el_enc-self.el_enc_before)/self.dt
		"""
		
		"""
		azv_acc = (azv-self.azv_before)
		elv_acc = (elv-self.elv_before)
		self.azv_before = azv
		self.elv_before = elv
		
		if azv_acc > 50:
			azv_acc = 50
		elif azv_acc < -50:
			azv_acc = -50
		
		if elv_acc > 50:
			elv_acc = 50
		elif elv_acc < -50:
			elv_acc = -50
		"""
		
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
		
		target_az = az_arcsec
		target_el = el_arcsec
		hensa_az = target_az - az_enc
		hensa_el = target_el - el_enc
		dhensa_az = hensa_az - self.pre_hensa_az
		dhensa_el = hensa_el - self.pre_hensa_el
		if math.fabs(dhensa_az) > 1:
			dhensa_az = 0
		if math.fabs(dhensa_el) > 1:
			dhensa_el = 0
		
		self.t1 = time.time()
		current_speed_az = (az_enc - self.az_enc_before) / (self.t1-self.t2)
		current_speed_el = (el_enc - self.el_enc_before) / (self.t1-self.t2)
		
		if self.pre_az_arcsec == 0: # for first move
			target_speed_az = 0
		else:
			target_speed_az = (az_arcsec-self.pre_az_arcsec)/(self.t1-self.t2)
		if self.pre_el_arcsec == 0: # for first move
			target_speed_el = 0
		else:
			target_speed_el = (el_arcsec-self.pre_el_arcsec)/(self.t1-self.t2)
		
		if math.fabs(hensa_az) >= 0.00: # don't use ihensa?
			ihensa_az = 0
			#hensa_flag_az = 0;
		else:
			#if(hensa_flag_az == 0 && hensa_az * pre_hensa_az <= 0)
			#  hensa_flag_az = 1;
			#if(hensa_flag_az == 1)
			ihensa_az += hensa_az
		if math.fabs(hensa_el) >= 0.000:
			ihensa_el = 0
			#hensa_flag_el = 0;
		else:
			#if(hensa_flag_el == 0 && hensa_el * pre_hensa_el <= 0)
			#  hensa_flag_el = 1;
			#if(hensa_flag_el == 1)
			ihensa_el += hensa_el
		
		""" Original
		self.az_rate = Paz*az_err + Iaz*az_err_integral + Daz*azv_err_avg +azv*1.57
		self.el_rate = Pel*el_err + Iel*el_err_integral + Del*elv_err_avg +elv*1.57
		"""
		
		self.az_rate = target_speed_az * 20.9 + (current_speed_az*20.9 - self.az_rate) * s_az_coeff + p_az_coeff*hensa_az + i_az_coeff*ihensa_az*(self.t1-self.t2) + d_az_coeff*dhensa_az/(self.t1-self.t2)
		self.el_rate = target_speed_el * 20.9 + p_el_coeff*hensa_el + i_el_coeff*ihensa_el*(self.t1-self.t2) + d_el_coeff*dhensa_el/(self.t1-self.t2)
		
		
		if math.fabs(az_err) < 8000 and self.az_rate > 10000:
			self.az_rate = 10000
		
		if math.fabs(az_err) < 8000 and self.az_rate < -10000:
			self.az_rate = -10000
		
		if math.fabs(el_err) < 9000 and self.el_rate > 10000:
			self.el_rate = 10000
		
		if math.fabs(el_err) < 7000 and self.el_rate < -8000:
			self.el_rate = -8000
		
		
		#update
		self.az_enc_before = az_enc
		self.el_enc_before = el_enc
		self.az_err_before = az_err
		self.el_err_before = el_err
		
		self.pre_hensa_az = hensa_az
		self.pre_hensa_el = hensa_el
		
		self.pre_az_arcsec = az_arcsec
		self.pre_el_arcsec = el_arcsec
		
		if az_max_rate > 16000:
			az_max_rate = 16000
		if el_max_rate > 12000:
			el_max_rate = 12000
		
		#if(az_enc<5*DEG2ARCSEC) rate=min(1000, rate);
		
		#limit of dangerous zone
		if (el_enc < 5.*DEG2ARCSEC and self.el_rate < 0 ) or (el_enc > 85.*DEG2ARCSEC and self.el_rate > 0):
			el_max_rate = min(1600, az_max_rate)
		if (az_enc < -270.*DEG2ARCSEC and self.az_rate < 0) or (az_enc > 270.*DEG2ARCSEC and self.az_rate > 0): 
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
		
		# arienai ryouiki deno gyakuunndou kinnsi //bug?
		if az_enc <= -270*DEG2ARCSEC and self.az_rate < 0:
			self.az_rate = 0
		if az_enc >= 270*DEG2ARCSEC and self.az_rate > 0:
			self.az_rate = 0
		
		if el_enc <= 0*DEG2ARCSEC and self.el_rate < 0:
			self.el_rate = 0 
		if el_enc >= 90*DEG2ARCSEC and self.el_rate > 0:
			self.el_rate = 0
		self.t2 = self.t1
		
		az_rate_ref = int(self.az_rate) #??
		el_rate_ref = int(self.el_rate) #??
		return [az_rate_ref, el_rate_ref, m_bAzTrack, m_bElTrack]

	"""
	def err_avg_func(self, az_value, el_value):
		AZV_ERR_AVG_NUM = ELV_ERR_AVG_NUM = 13
		if self.count < AZV_ERR_AVG_NUM:
		 	 self.az_array[count] = az_value
		 	 self.el_array[count] = el_value
		 	 self.count += 1
		else:
			for i in range(AZV_ERR_AVG_NUM-1):
				self.az_array[i] = self.az_array[i+1]
				self.el_array[i] = self.el_array[i+1]
			self.az_array[AZV_ERR_AVG_NUM-1] = az_value
			self.el_array[ELV_ERR_AVG_NUM-1] = el_value
		
		sum_az = sum_el = 0
		for i in range(self.count):
			sum_az += self.az_array[i]
			sum_el += self.el_array[i]
		
		azv_err_avg = sum_az/self.count
		elv_err_avg = sum_el/self.count
		return [azv_err_avg, elv_err_avg]
	"""

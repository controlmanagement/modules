import math
import time
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
	az_enc_before = el_enc_before = azv_before = elv_before = 0
	az_rate = el_rate = 0
	az_rate_d = el_rate_d = 0
	m_stop_rate_az = m_stop_rate_el = 0
	
	
	def __init__(self):
		self.dio = pyinterface.create_gpg2000(1)
		self.enc = antenna_enc.enc_controller()
		pass

	def move_azel(self, az_arcsec, el_arcsec, azv, elv, m_bStop, az_max_rate = 16000, el_max_rate = 12000):
		MOTOR_MAXSTEP = 10000
		MOTOR_AZ_MAXRATE = 16000
		MOTOR_EL_MAXRATE = 12000
		
		ret = self.calc_pid(az_arcsec, el_arcsec, azv, elv, az_max_rate, el_max_rate)
		az_rate_ref = ret[0]
		el_rate_ref = ret[1]
		
		#指令値を目標値に向ける
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
			self.el_rate += a*MOTOR_MAXSTEP
		
		#limit of max v
		if self.az_rate_d > MOTOR_AZ_MAXRATE:
			self.az_rate_d = MOTOR_AZ_MAXRATE
		if self.az_rate_d < -MOTOR_AZ_MAXRATE:
			self.az_rate_d = -MOTOR_AZ_MAXRATE
		if self.el_rate_d > MOTOR_EL_MAXRATE:
			self.el_rate_d = MOTOR_EL_MAXRATE
		if self.el_rate_d < -MOTOR_EL_MAXRATE:
			self.el_rate_d = -MOTOR_EL_MAXRATE
		
		# confirm limit of controll rack → forced outage
		#if(0< motordrv_nanten2_cw_limit()+motordrv_nanten2_ccw_limit()+motordrv_nanten2_up_limit()+motordrv_nanten2_down_limit())
		#	 motordrv_nanten2_drive_on(FALSE,FALSE);
		
		# output to port
		if m_bStop == TRUE:
			dummy = self.m_stop_rate_az
		else:
			dummy = int(self.az_rate_d)
		#dummy=m_bStop==TRUE?m_stop_rate_az:motor_param.az_rate_ref;
		self.dio.ctrl.out_word("FBIDIO_OUT1_16", dummy)
		#dioOutputWord(CONTROLER_BASE2,0x00,dummy)  output port is unreliable
		seld.az_rate_d = dummy
		
		if m_bStop == TRUE:
			dummy = self.m_stop_rate_el
		else:
			dummy = int(self.el_rate_d)
		#dummy=m_bStop==TRUE?m_stop_rate_el:motor_param.el_rate_ref;
		self.dio.ctrl.out_word("FBIDIO_OUT33_48", dummy)
		#dioOutputWord(CONTROLER_BASE2,0x02,dummy);
		self.el_rate_d = dummy

	def calc_pid(self, az_arcsec, el_arcsec, azv, elv, az_max_rate, el_max_rate):
		# Default
		Paz = 3.8
		Iaz = 8
		Daz = 0.11
		Pel = 3.73
		Iel = 8
		Del = 0.07
		
		DEG2ARCSEC = 3600
		m_bAzTrack = "FALSE"
		m_bElTrack = "FALSE"
		
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
		"""
		
		#deivative
		azv_err = azv-(az_enc-self.az_enc_before)/self.dt
		elv_err = elv-(el_enc-self.el_enc_before)/self.dt
		
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
		
		
		if　10000 < math.fabs(self.az_rate):
			m_bAzTrack = "TRUE" #def Paz=2?
		else:
			az_err_integral += (self.az_err_before+az_err)*self.dt/2.+azv_acc*0.0
		if 10000 < math.fabs(self.el_rate):
			m_bElTrack = "TRUE" #def Pel=2?
		else:
			el_err_integral += (self.el_err_before+el_err)*self.dt/2.+elv_acc*0.0;
		
		ret = self.err_avg_func(azv_err, elv_err)
		azv_err_avg = ret[0]
		elv_err_avg = ret[1]
		
		if math.fabs(azv_err_avg) > math.fabs(azv)/10.+10.):
			az_err_integral = 0.
		
		if math.fabs(az_err) > 150:
			az_err_integral = 0
		
		if math.fabs(elv_err_avg) > math.fabs(elv)/10.+10.):
			el_err_integral = 0.
		
		if math.fabs(el_err) > 150:
			el_err_integral = 0.
		
		self.az_rate = Paz*az_err + Iaz*az_err_integral + Daz*azv_err_avg +azv*1.57
		self.el_rate = Pel*el_err + Iel*el_err_integral + Del*elv_err_avg +elv*1.57
		
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
		if self.el_rate > el_max_rate
			self.el_rate = el_max_rate
		if self.el_rate < -el_max_rate:
			self.el_rate = -el_max_rate
		
		#ありえない領域での逆運動禁止 //bug?
		if az_enc <= -270*DEG2ARCSEC and self.az_rate < 0:
			self.az_rate = 0
		if az_enc >= 270*DEG2ARCSEC and self.az_rate > 0:
			self.az_rate = 0
		
		if el_enc <= 0*DEG2ARCSEC and self.el_rate < 0:
			self.el_rate = 0 
		if el_enc >= 90*DEG2ARCSEC and self.el_rate > 0:
			self.el_rate = 0
		
	    az_rate_ref = int(self.az_rate) #??
	    el_rate_ref = int(self.el_rate) #??
		return [az_rate_ref, el_rate_ref]

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

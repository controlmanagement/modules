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
	
	def __init__(self):
		self.dio = pyinterface.create_gpg2000(1)
		self.enc = antenna_enc.enc_controller()
		pass
	
	
	
	
	
	
	def move_azel(self, ):
		
		
		
		az_rate=  self.Paz*az_err + self.Iaz*az_err_integral + self.Daz*azv_err_avg	+azv*1.57;
		el_rate=  self.Pel*el_err + self.Iel*el_err_integral + self.Del*elv_err_avg	+elv*1.57;
		
		
		
	def calc_pid(self, az_arcsec, el_arcsec, azv, elv, az_mate_rate = 16000, el_max_rate = 12000):
		# Default
		Paz = 3.8
		Iaz = 8
		Daz = 0.11
		Pel = 3.73
		Iel = 8
		Del = 0.07
		
		m_bAzTrack = "FALSE"
		m_bElTrack = "FALSE"
		
		az_enc = self.enc.???
		el_enc = self.enc.???
		
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
		
		
		
		
		if　10000 < math.fabs(az_rate):
			m_bAzTrack = "TRUE" #def Paz=2?
		else:
			az_err_integral += (self.az_err_before+az_err)*self.dt/2.+azv_acc*0.0
		if 10000 < math.fabs(el_rate):
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
		
		az_rate = Paz*az_err + Iaz*az_err_integral + Daz*azv_err_avg +azv*1.57
		el_rate = Pel*el_err + Iel*el_err_integral + Del*elv_err_avg +elv*1.57
		
		if math.fabs(az_err) < 8000 and az_rate > 10000:
			az_rate = 10000
		
		if math.fabs(az_err) < 8000 and az_rate < -10000:
			az_rate = -10000
		
		if math.fabs(el_err) < 9000 and el_rate > 10000:
			el_rate = 10000
		
		if math.fabs(el_err) < 7000 and el_rate < -8000:
			el_rate = -8000
		
		
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
		if (el_enc < 5.*DEG2ARCSEC and el_rate < 0 ) or (el_enc > 85.*DEG2ARCSEC and el_rate > 0):
			el_max_rate = min(1600, az_max_rate)
		if (az_enc < -270.*DEG2ARCSEC and el_rate < 0) or (az_enc > 270.*DEG2ARCSEC and az_rate > 0): 
			az_max_rate = min(1600, az_max_rate); #bug?
		
		#lmit of speed
		if az_rate > az_max_rate:
			az_rate = az_max_rate
		if az_rate < -az_max_rate:
			az_rate = -az_max_rate
		if el_rate > el_max_rate
			el_rate = el_max_rate
		if el_rate < -el_max_rate:
			el_rate = -el_max_rate
		
		#ありえない領域での逆運動禁止 //bug?
		if az_enc <= -270*DEG2ARCSEC and az_rate < 0:
			az_rate = 0
		if az_enc >= 270*DEG2ARCSEC and az_rate > 0:
			az_rate = 0
		
		if el_enc <= 0*DEG2ARCSEC and el_rate < 0:
			el_rate = 0 
		if el_enc >= 90*DEG2ARCSEC and el_rate > 0:
			el_rate = 0
		
	    motordrv_nanten2_set_rate_ref((int)az_rate,(int)el_rate);
	motordrv_nanten2_output();
	
	return TRUE;
#else
	motordrv_dummy_moveto(az_arcsec,el_arcsec);
	return TRUE;
#endif
}
		
		
		
		
		
		
	def err_avg_func(self, az_value, el_value):
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

		
		
		
		
		
		
		
		
		
		
		
		
		
		

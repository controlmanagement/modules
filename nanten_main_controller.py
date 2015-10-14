import math
import time
import pyinterface





class nanten_main_controller(object):
	
	# Default
	Paz = 3.8
	Iaz = 8
	Daz = 0.11
	Pel = 3.73
	Iel = 8
	Del = 0.07
	MOTOR_SAMPLING = 10 #memo
	dt = MOTOR_SAMPLING/1000.
	
	count = 0
	az_array = [0]*13
	AZV_ERR_AVG_NUM = 13
	el_array = [0]*13
	ELV_ERR_AVG_NUM = 13 #AZV_ERR_AVG_NUM = ELV_ERR_AVG_NUM
	
	def __init__(self):
		self.dio = pyinterface.create_gpg2000(1)
		pass
	
	
	
	
	
	
	def move_azel(self, ):
		
		
		
		az_rate=  self.Paz*az_err + self.Iaz*az_err_integral + self.Daz*azv_err_avg	+azv*1.57;
		el_rate=  self.Pel*el_err + self.Iel*el_err_integral + self.Del*elv_err_avg	+elv*1.57;
		
		
		
	def calc_pid(self, ):
		
		
		
		
		
		
		
		
		
		
		
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

		
		
		
		
		
		
		
		
		
		
		
		
		
		

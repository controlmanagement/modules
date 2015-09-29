import math
import numpy
import pyinterface


class enc_controller(object):
	
	Az = ''
	El = ''
	
	
	
	
	def __init__(self):
		self.dio = pyinterface.create_gpg6204(1)
		pass
	
	def print_msg(self, msg):
		print(msg)
		return
	
	def print_error(self, msg):
		self.error.append(msg)
		self.print_msg('!!!! ERROR !!!! ' + msg)
		return
	
	def get_azel(self, ):
		
		
		
		
		
		
		cnt_Az = self.dio.
		cnt_El = self.dio.
		
		if cnt_El > 0:
			enc_El = (324*cnt_El+295)/590
		else:
			enc_El = (324*cnt_El-295)/590
		self.El = enc_El+45*3600
		
		
		

	def read_azel(self):
		return [self.Az, self.El]

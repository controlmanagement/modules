import math
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
	
	def get_azel(self):
		cntAz = self.dio.get_position(2)
		cntEl = self.dio.get_position(1)
		
		if cntAz > 0:
			encAz = (324*cntAz+295)/590
		else:
			encAz = (324*cntAz-295)/590
		self.Az = encAz      #arcsecond
		
		if cntEl > 0:
			encEl = (324*cntEl+295)/590
		else:
			encEl = (324*cntEl-295)/590
		self.El = encEl+45*3600      #arcsecond
		return [self.Az, self.El]

	def read_azel(self):
		return [self.Az, self.El]

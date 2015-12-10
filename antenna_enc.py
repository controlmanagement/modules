import math
import time
import pyinterface
import portio


class enc_controller(object):
	
	Az = ''
	El = ''
	
	def __init__(self):
		portio.iopl(3)
		pass
	
	def start_server(self):
		ret = self.start_enc_server()
		return
	
	def print_msg(self, msg):
		print(msg)
		return
	
	def print_error(self, msg):
		self.error.append(msg)
		self.print_msg('!!!! ERROR !!!! ' + msg)
		return
	
	
	"""
	# for renishaw (Az,El)
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
	"""
	
	
	def get_azel(self):
		# for renishaw(El), for nikon(Az)
		byte_az = [0]*3
		
		#dioOutputByte(CONTROLER_BASE0,0x03,0x04);
		#CONRROLER_BASE0 = 0xc000
		portio.outb(0x04, (0x2050+0x03)) # Az
		
		time.sleep(3./1000) # need waiting
		#dioOutputByte(CONTROLER_BASE0,0x03,0x00);
		portio.outb(0x00, (0x2050+0x03))
		
		# get data from board
		for i in range(3):
			# byte_az[i] = dioInputByte(CONTROLER_BASE0,i);
			byte_az[i] = portio.inb((0x2050+i))
			
			# reverse byte
			# byte_az[i]=~byte_az[i];byte[2] is hugou 1keta+7keta suuji
			byte_az[i] = ~byte_az[i] & 0b11111111
			
		self.Az = self.bin2dec_2s_complement(byte_az, 3)
		
		portio.outb(2, 0x2006)
		cntEl = portio.inl(0x2000)
		b_num = bin(cntEl)
		b_num = b_num.lstrip("0b")
		if len(b_num) == 32:
			if int(b_num[0]) == 1:
				b_num = int(b_num, 2)
				cntEl = -(~b_num & 0b01111111111111111111111111111111)
		if cntEl > 0:
			encEl = int((324*cntEl+295)/590)
		else:
			encEl = int((324*cntEl-295)/590)
		self.El = encEl+45*3600      #arcsecond
		print(self.Az/3600.)
		print(self.El/3600.)
		return [self.Az, self.El]
	
	
	
	def bin2dec_2s_complement(self, byte, nSize):
		i = sign = ord = 1
		abs = 0
		if nSize == 0:
			return 0
		
		#sign = byte[nSize-1]>>7 ?-1:1;
		if byte[nSize-1]>>7 == True:
			sign = -1
		else:
			sign = 1
		"""
		num = bin(byte[nSize-1])
		if len(num) == 11:
			num = num[3:10]
			byte[nSize-1] = int(num, 2)
		"""
		if sign == 1:
			for i in range(nSize):
				abs += ord*byte[i]
				ord *= 256
			abs += ord*byte[nSize-1] & (~0x80 & 0b01111111)
			
		else:
			for i in range(nSize):
				abs += ord*(~byte[i] & 0b11111111)
				ord *= 256
			abs += 1
		
		return abs*sign
	
	
	
	def read_azel(self):
		return [self.Az, self.El]


def enc_client(host, port):
	client = pyinterface.server_client_wrapper.control_client_wrapper(enc_controller, host, port)
	return client

def enc_monitor_client(host, port):
	client = pyinterface.server_client_wrapper.monitor_client_wrapper(enc_controller, host, port)
	return client

def start_enc_server(port1 = 9999, port2 = 9999):
	enc = enc_controller()
	server = pyinterface.server_client_wrapper.server_wrapper(enc, '', port1, port2)
	server.start()
	return server

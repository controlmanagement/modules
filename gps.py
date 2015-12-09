import pyinterface

class gps_controller(object):

	error = []

	def __init__(self):
		self.dio = pyinterface.create_gpg2000(2)
		print("__init__:on")
		return

	def print_msg(self,msg):
		print(msg)
		return

	def print_error(self,msg):
		self.error.append(msg)
		self.print_msg('!!!!ERROR!!!!' + msg)
		return

	def gpsJuliusDayUTC(self):

	
		cnt = self.dio.di_check(1,50)	
	
		year = 2000 + (cnt[0] & 1) + (cnt[1] & 1)*4 + (cnt[25] & 1)*2 +(cnt[26] & 1)*8 + (cnt[2] & 1)*10 + (cnt[3] & 1)*40 + (cnt[27] & 1)*20 + (cnt[28] & 1)*80
		month = (cnt[4] &1) + (cnt[5] &1)*4+ (cnt[29] &1)*2 + (cnt[30]&1)*8  +(cnt[6] &1)*10

		day=(cnt[7]&1)*2 + (cnt[8] &1)*8+ (cnt[9] &1)*20 + (cnt[31] &1) +(cnt[32] &1)*4 + (cnt[33] &1)*10

		hour=(cnt[10] &1)*1 + (cnt[11] &1)*4+ (cnt[12] &1)*10 + (cnt[35] &1)*2 +(cnt[36] &1)*8 + (cnt[37] &1)*20

		min=(cnt[13] &1)*1 + (cnt[14] &1)*4+ (cnt[15] &1)*10 + (cnt[16] &1)*40 +(cnt[38] &1)*2 + (cnt[39] &1)*8+ (cnt[40] &1)*20

		sec=(cnt[17] &1)*2 + (cnt[18] &1)*8+ (cnt[19] &1)*20 + (cnt[41] &1) +(cnt[42] &1)*4 + (cnt[43] &1)*10+ (cnt[44] &1)*40

		subsec=(cnt[20] &1)*1 + (cnt[21] &1)*4+(cnt[45] &1)*2 + (cnt[46] &1)*8
	
		d=day+hour/24.0+min/(24.0*60.0)+(sec+subsec/10.0)/(24.0*60.0*60.0)
		m=-int((14-month)/12.0)
		p=int((1461*(year+4800+m)/4.0))+int((367*(month-2-12*m)/12.0))
		jd=p-(3*int((int((year+4900+m)/100.0/4.0))))      -32075.5+d
		 
		mjd=int((365.25*year))+int((year/400))-int((year/100))+int((30.59*(month-2)))+day-678912
	
		#print year,month,day,hour,min,sec,subsec
  		#print d,m,p,mjd,jd
	
		return jd


from datetime import datetime as dt
import time
import sys

#import controller
import antenna_nanten_controller

argvs = sys.argv 
argc = len(argvs) 
print argvs
print argc
if (argc != 2):
	print 'Usage: # python %s filename' % argvs[0]
	quit()

f = open(argvs[1],"a")
#status = controller.read_status()
status = antenna_nanten_controller.antenna_monitor_client('172.20.0.11',8004)




while(1):
	# Calculate current MJD
	tv = time.time()
	mjd = tv/24./3600. + 40587.0 # 40587.0 = MJD0
	mid = int(mjd)
	ntime = dt.now()
	secofday = ntime.hour*60*60 + ntime.minute*60 + ntime.second + ntime.microsecond*0.000001
	#data = status.read_status()
	data = status.read_azel()
	ntime2 = dt.now()
	secofday2 = ntime2.hour*60*60 + ntime2.minute*60 + ntime2.second + ntime2.microsecond*0.000001
	
	#mjd,secofday,self.az_encmoni, self.el_encmoni, self.az_targetmoni, self.el_targetmoni, self.az_hensamoni, self.el_hensamoni, self.az_rate, self.el_rate, self.az_targetspeed, self.el_targetspeed, self.current_speed_az, self.current_speed_el
	#mjd,secofday,self.az_encmoni, self.el_encmoni, self.az_targetmoni, self.el_targetmoni, self.az_hensamoni, self.el_hensamoni, self.az_rate, self.el_rate, self.az_targetspeed, self.el_targetspeed, self.current_speed_az, self.current_speed_el ,self.t1_moni ,self.t2_moni ,self.az_pidihensamoni ,self.el_pidihensamoni
	
	#log = str(mjd) + ' ' + str(secofday) + ' ' + str(data["command_az"])+ ' ' + str(data["command_el"])+ ' ' + str(data["current_az"]) + ' ' + str(data["current_el"])
	log = str(mjd) + ' ' + str(secofday) + ' ' + str(secofday2) + str(data[2])+ ' ' + str(data[3])+ ' ' + str(data[0]) + ' ' + str(data[1]) + ' ' + str(data[4]) + ' ' + str(data[5]) + ' ' + str(data[6]) + ' ' + str(data[7])+ ' ' + str(data[8]) + ' ' + str(data[9]) + ' ' + str(data[10]) + ' ' + str(data[11]) + ' ' + str(data[12]) + ' ' + str(data[13]) + ' ' + str(data[14]) + ' ' + str(data[15]) + ' ' + str(data[16]) + ' ' + str(data[17])

	f.write(log + "\n")
	print log

	time.sleep(0.01)

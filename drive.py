
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
	tv_sec = int(tv)
	tv_usec = tv - tv_sec
	mjd = (tv_sec + tv_usec/1000000.)/24./3600. + 40587.0 # 40587.0 = MJD0
	mid = int(mjd)
	ntime = dt.now()
	secofday = ntime.hour*60*60 + ntime.minute*60 + ntime.second + ntime.microsecond*0.000001
	#data = status.read_status()
	data = status.read_azel()
	# mjd,secofday,command[az],command[el],current[az],currennt[el]
	#log = str(mjd) + ' ' + str(secofday) + ' ' + str(data["command_az"])+ ' ' + str(data["command_el"])+ ' ' + str(data["current_az"]) + ' ' + str(data["current_el"])
	log = str(mjd) + ' ' + str(secofday) + ' ' + str(data[2])+ ' ' + str(data[3])+ ' ' + str(data[0]) + ' ' + str(data[1])

	f.write(log + "\n")
	print log

	time.sleep(0.01)

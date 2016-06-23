from datetime import datetime as dt
import time
import sys

#import controller
import geomech

argvs = sys.argv 
argc = len(argvs) 
print argvs
print argc
if (argc != 2):
	print 'Usage: # python %s filename' % argvs[0]
	quit()

f = open(argvs[1],"a")
#status = controller.read_status()
status = geomech.geomech_monitor_client('172.20.0.12',8101)




while(1):
  # Calculate current MJD
  tv = time.time()
  mjd = tv/24./3600. + 40587.0 # 40587.0 = MJD0
  mid = int(mjd)
  ntime = dt.now()
  secofday = ntime.hour*60*60 + ntime.minute*60 + ntime.second + ntime.microsecond*0.000001
  #data = [geo_x, geo_y]
  data = status.read_geomech_col()
  ntime2 = dt.now()
  secofday2 = ntime2.hour*60*60 + ntime2.minute*60 + ntime2.second + ntime2.microsecond*0.000001

  log = str(mjd) + ' ' + str(secofday) + ' ' + str(data[0])+ ' ' + str(data[1])
  f.write(log + "\n")
  print log
	
time.sleep(0.1)

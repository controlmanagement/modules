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
  #data1 = [x1, ,y1, x2, y2]
  data1 = status.read_geomech()
  #data2 = [geo_x, geo_y]
  data2 = status.read_geomech_col()
  #data3 = [t1, t2]
  data3 = status.read_geomech_temp()
  ntime2 = dt.now()
  secofday2 = ntime2.hour*60*60 + ntime2.minute*60 + ntime2.second + ntime2.microsecond*0.000001

  log = str(mjd) + ' ' + str(secofday) + ' ' + str(data1[0])+ ' ' + str(data1[1] + ' ' + str(data2[0])+ ' ' + str(data2[1] + ' ' + str(data3[0])+ ' ' + str(data3[1])
  f.write(log + "\n")
  print log
	
time.sleep(0.1)

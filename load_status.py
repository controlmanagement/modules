
import m4
import abs

import time
from datetime import datetime as dt

dtime = dt.now()

if dtime.month < 10:
    month = '0' + str(dtime.month)
else:
    month = str(dtime.month)

if dtime.day < 10:
    day = '0' + str(dtime.day)
else:
    day = str(dtime.day)

file = str(dtime.year) + month + day + '.txt'


#f = open(file,"a")




m4 = m4.m4_monitor_client('172.20.0.12',6004)
hot = abs.abs_monitor_client('172.20.0.12',6002)

while(1):
	tv = time.time()
	mjd = tv/24./3600. + 40587.0 # 40587.0 = MJD0

	ntime = dt.now()
	secofday = ntime.hour*60*60 + ntime.minute*60 + ntime.second + ntime.microsecond*0.000001
    
	lst_g = 0.67239+1.00273781*(mjd-40000.0)
	l_plb = -67.7222222222/360.0
	lst_plb = lst_g + l_plb
	lst_plb_i = int(lst_plb)
	lst_plb -= lst_plb_i
	lst_plb = 24.0*lst_plb
	lst_hh = int(lst_plb)
	lst_plb = 60.0*(lst_plb - lst_hh)
	lst_mm = int(lst_plb)
	lst_plb = 60.0*(lst_plb -lst_mm)
	lst_ss = int(lst_plb)

	m4pos = m4.read_pos()
	hotpos = hot.read_pos()
	
	log = "%5.0f %6.1f %2d:%2d:%2d m4: %s  hot: %s" %(mjd, secofday, lst_hh, lst_mm, lst_ss, m4pos, hotpos)	
	print log
	time.sleep(1)

	#f.write(log + "\n")
    

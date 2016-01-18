#import controller
import antenna_nanten_controller
import antenna_enc
import dome
import dome_pos

import time
from datetime import datetime as dt


tel = antenna_nanten_controller.antenna_monitor_client('172.20.0.11',8004)
enc = antenna_enc.enc_monitor_client('172.20.0.11',8002)
dome = dome.dome_monitor_client('172.20.0.11',8008)
dome_pos = dome_pos.dome_pos_monitor_client('172.20.0.11',8006)

while(1):
    telstatus = tel.read_limit()
    encstatus = enc.read_azel()
    domestatus = dome.read_status()
    domeposstatus = dome_pos.read_dome_enc()

    tv = time.time()
    mjd = tv/24./3600. + 40587.0 # 40587.0 = MJD0
    mjd = int(mjd)
    ntime = dt.now()
    secofday = ntime.hour*60*60 + ntime.minute*60 + ntime.second + ntime.microsecond*0.000001
    
    #print "TIME : %s  AZ_r: %3.2f  EL_r: %3.2f  AZ_i : %3.2f  EL_i: %3.2f" %(now,data[0]/3600.,data[1]/3600.,data[2]/3600.,data[3]/3600.,)
    #print domestatus
    #print domeposstatus
    log = 'telescope:' + str(telstatus[0]) + ' ' + str(telstatus[1]) + ' ' + str(telstatus[2])+ ' ' + str(telstatus[3])+ ' ' + str(mjd) + ' ' + str(secofday) + ' ' + str(encstatus[0]/3600.) + ' ' + str(encstatus[1]/3600.) + ' dome:door:' + str(domestatus[1][1]) + ' :membrane:' + str(domestatus[2][1])+ ' ' + str(domestatus[3]) + ' ' + str(domeposstatus/3600.)
    print log

    time.sleep(1.)


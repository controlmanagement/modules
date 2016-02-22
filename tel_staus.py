#import controller
import antenna_nanten_controller
import antenna_enc
import dome
#import dome_pos

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


f = open(file,"a")



tel = antenna_nanten_controller.antenna_monitor_client('172.20.0.11',8004)
enc = antenna_enc.enc_monitor_client('172.20.0.11',8002)
dome = dome.dome_monitor_client('172.20.0.11',8008)
#dome_pos = dome_pos.dome_pos_monitor_client('172.20.0.11',8006)

while(1):
    telstatus = tel.read_error()
    telstatus2 = tel.read_status()
    encstatus = enc.read_azel()
    domestatus = dome.read_status()
    domeposstatus = dome.read_domepos()

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

    # limit check
    if telstatus[4] == 0:
        print 'soft limit cw\n'
    if telstatus[5] == 0:
        print 'soft limit ccw\n'
    if telstatus[6] == 0:
        print 'soft limit up\n'
    if telstatus[7] == 0:
        print 'soft limit down\n'
    if telstatus[8] == 0:
        print '1st limit cw\n'
    if telstatus[9] == 0:
        print '1st limit ccw\n'
    if telstatus[10] == 0:
        print '1st limit up\n'
    if telstatus[11] == 0:
        print '1st limit down\n'
    if telstatus[12] == 0:
        print '2nd limit cw\n'
    if telstatus[13] == 0:
        print '2nd limit ccw\n'
    if telstatus[14] == 0:
        print '2nd limit up\n'
    if telstatus[15] == 0:
        print '2nd limit down\n'
    if telstatus[18] == 1:
        print 'deviation error az\n'
    if telstatus[19] == 1:
        print 'deviation error el\n'
    if telstatus[20] == 1:
        print 'controller error az\n'
    if telstatus[21] == 1:
        print 'controller error el\n'
    #if telstatus[22] == 1:
        #print 'servo pack error az\n'
    #if telstatus[23] == 1:
        #print 'servo pack error el\n'
    if telstatus[24] == 0:
        print 'emergency switch\n'


    log = "telescope: %s %s %s %s %s %5.0f %6.1f %2d:%2d:%2d %5.2f %5.2f  dome: door %s  membrane: %s %s %5.2f" %(telstatus[0], telstatus[1], telstatus[2], telstatus[3], telstatus2, mjd, secofday, lst_hh, lst_mm, lst_ss, encstatus[0]/3600., encstatus[1]/3600., domestatus[1][1], domestatus[2][1], domestatus[3], domeposstatus/3600.,)

    f.write(log + "\n")
    print log

    time.sleep(1.)


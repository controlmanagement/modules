import time
import math
import coord
from pyslalib import slalib
import nanten_main_controller
import pyinterface
import threading




class antenna_nanten_controller(object):
    
    longitude = -67.70308139*math.pi/180
    latitude = -22.96995611*math.pi/180
    height = 4863.85
    #temporary dut1
    dut1 = -0.20489  #delta UT:  UT1-UTC (UTC seconds)
    
    # for socket
    instruction = ''
    dx = dy = dt = n = rampt = delay = 0
    
    target_az = 0
    target_el = 0
    drive_az = drive_el = "OFF"
    az_track = el_track = "FALSE"
    error_az = error_el = servo_error_az = servo_error_el = emergency_switch = "FALSE"
    antenna_status = ""
    az_v = el_v = 0
    off_list = {"off_az":0, "off_el":0, "off_ra":0, "off_dec":0, "off_l":0, "off_b":0}
    
    def __init__(self):
        self.coord = coord.coord_calc() # for test <= MUST REMOVE [#]
        self.nanten = nanten_main_controller.nanten_main_controller()
        self.dio = pyinterface.create_gpg2000(4)
        pass
    
    def drive_on(self): # this fanction => clear_error and drive_on
        # void motordrv_nanten2_drive_on(BOOL az_drive,BOOL el_drive) by [motordrv_nanten2.c]
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 3)
        self.nanten.init_speed()
        return
    
    def drive_off(self):
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0)
        return
    
    def contactor_on(self):
        self.dio.ctrl.out_byte("FBIDIO_OUT9_16", 15)
        return
    
    def contactor_off(self):
        self.dio.ctrl.out_byte("FBIDIO_OUT9_16", 0)
        return
    
    def drive_check(self):
        ret = self.nanten.dio.ctrl.in_byte("FBIDIO_IN1_8")
        if (ret>>2 & 0x01) == 1:
            self.drive_az = "ON"
        else:
            self.drive_az = "OFF"
        if (ret>>3 & 0x01) == 1:
            self.drive_el = "ON"
        else:
            self.drive_el = "OFF"
        return [self.drive_az, self.drive_el]
    
    def error_check(self):
        ret = self.nanten.dio.ctrl.in_byte("FBIDIO_IN17_24")
        if (ret>>0 & 0x01) == 1:
            cable_cw = "TRUE"
        else:
            cable_cw = "FALSE"
        if (ret>>1 & 0x01) == 1:
            cable_ccw = "TRUE"
        else:
            cable_ccw = "FALSE"
        if (ret>>4 & 0x01) == 1:
            self.error_az = "TRUE"
        else:
            self.error_az = "FALSE"
        if (ret>>5 & 0x01) == 1:
            self.error_el = "TRUE"
        else:
            self.error_el = "FALSE"
        if (ret>>6 & 0x01) == 1:
            self.servo_error_az = "TRUE"
        else:
            self.servo_error_az = "FALSE"
        if (ret>>7 & 0x01) == 1:
            self.servo_error_el = "TRUE"
        else:
            self.servo_errr_el = "TRUE"
        
        ret = self.nanten.dio.ctrl.in_byte("FBIDIO_IN25_32")
        if (ret>>0 & 0x01) == 1:
            self.emergency_switch = "TRUE"
        else:
            self.emergency_switch = "FALSE"
        if (ret>>2 & 0x01) == 1:
            self.antenna_status = "LOCAL"
        else:
            self.antenna_status = "REMOTE"
        return [self.error_az, self.error_el, self.servo_error_az, self.servo_error_el, cable_cw, cable_ccw, self.emergency_switch, self.antenna_status]
    
    def clear_error(self):
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 8)
        return
    
    def set_offset(self, coord, off_x, off_y):
        self.off_list["off_az"] = self.off_list["off_el"] = self.off_list["off_ra"] = self.off_list["off_dec"] = self.off_list["off_l"] = self.off_list["off_b"] = 0
        if coord == "HORIZONTAL":
            self.off_list["off_az"] = off_x
            self.off_list["off_el"] = off_y
        elif coord == "EQUATRIAL":
            self.off_list["off_ra"] = off_x
            self.off_list["off_dec"] = off_y
        else: #GALACTIC
            self.off_list["off_l"] = off_x
            self.off_list["off_b"] = off_y
        return
    
    def test_move(self,az_speed,el_speed,dist_arcsec = 5 * 3600):
        try:
            self.stop_thread.set()
        except: pass
        try:
            self.otf_stop_thread.set()
        except: pass
        
        self.nanten.test_move(az_speed,el_speed,dist_arcsec)
        return
    
    
    def azel_move_start(self, az_arcsec, el_arcsec, az_max_rate = 10000, el_max_rate = 10000):
        self.azel_stop_thread = threading.Event()
        self.azel_thread = threading.Thread(target = self.azel_move, args = (az_arcsec, el_arcsec, az_max_rate, el_max_rate))
        self.azel_thread.start()
        return
    
    def azel_move(self, az_arcsec, el_arcsec, az_max_rate = 10000, el_max_rate = 10000):
        try:
            self.stop_thread.set()
        except: pass
        try:
            self.otf_stop_thread.set()
        except: pass
        hensa_flag = 1
        
        #for drive off
        ret = self.drive_check()
        if ret[0] == "OFF" or ret[1] == "OFF":
            return
        
        while hensa_flag:
            self.target_az = az_arcsec
            self.target_el = el_arcsec
            hensa_flag = self.nanten.azel_move(az_arcsec, el_arcsec, az_max_rate, el_max_rate)
            if self.azel_stop_thread.is_set():
                self.nanten.dio.ctrl.out_word("FBIDIO_OUT1_16", 0)
                self.nanten.dio.ctrl.out_word("FBIDIO_OUT17_32", 0)
                return
        return
    
    def azel_stop(self):
        self.azel_stop_thread.set()
        self.azel_thread.join()
        print("STOP MOVING")
        return
    
    def move_azel(self, real_az, real_el, dcos, hosei = 'hosei_230.txt', off_az = 0, off_el = 0, az_max_rate=16000, el_max_rate=12000):
        #for drive off
        ret = self.drive_check()
        if ret[0] == "OFF" or ret[1] == "OFF":
            return
        #if off_az != 0 or off_el != 0: #for test
        self.set_offset("HORIZONTAL", off_az, off_el)
        if dcos == 0:
            #print(real_az, real_el, type(real_az), type(real_el))
            #print(self.off_list)
            real_el += self.off_list["off_el"]
            real_az += self.off_list["off_az"]
        else:
            real_el += self.off_list["off_el"]
            real_az = real_az+self.off_list["off_az"]/math.cos(real_el/3600.*math.pi/180.) # because of projection
        """
        if set_coord == "HORIZONTAL":
            ret = self.coord.apply_kisa(real_az, real_el, hosei)
            target_az = real_az+ret[0]
            target_el = real_el+ret[1]
        else:
            target_az = real_az
            target_el = real_el
        """
        
        real_az_n = real_az/3600.*math.pi/180.
        real_el_n = real_el/3600.*math.pi/180.

        ret = self.coord.apply_kisa(real_az_n, real_el_n, hosei) # until define the set_coord
        target_az = real_az+ret[0]
        target_el = real_el+ret[1]
        
        self.target_az = target_az
        self.target_el = target_el

        #az_max_rate =3000
        #el_max_rate =3000
        
        print("az:"+str(target_az)+" el:"+str(target_el))
        track = self.nanten.move_azel(target_az, target_el, az_max_rate, el_max_rate) #until define the set_coord
        self.az_track = track[0]
        self.el_track = track[1]
        #self.az_v = ret[2]
        #self.el_v = ret[3]
        return track
    
    def move_radec(self, gx, gy, gpx, gpy, code_mode, temp, pressure, humid, lamda, dcos, hosei = 'hosei_230.txt', off_coord = "HORIZONTAL", off_x = 0, off_y = 0, az_max_rate=16000, el_max_rate=12000):
        ##debug
        #print('moving!!!, {gx}, {gy}, {code_mode}'.format(**locals()))
        ##debug-end
        #if off_x != 0 or off_y != 0: #for test
        self.set_offset(off_coord, off_x, off_y)
        #lamda not equals lambda
        # Calculate current MJD
        tv = time.time()
        mjd = tv/24./3600. + 40587.0 # 40587.0 = MJD0
        #tv = time.time()
        #tv_sec = int(tv)
        #tv_usec = tv - tv_sec
        #mjd = (tv_sec + tv_usec/1000000.)/24./3600. + 40587.0 # 40587.0 = MJD0
        
        
        tai_utc = 36.0 # tai_utc=TAI-UTC  2015 July from ftp://maia.usno.navy.mil/ser7/tai-utc.dat
        
        # lamda is wavelength(not lambda)
        if code_mode == "B1950":
            ret = slalib.sla_fk425(gx, gy, gpx, gpy, 0, 0)
            gaJ2000 = ret[0]
            gdJ2000 = ret[1]
            gpaJ2000 = ret[2]
            gpdJ2000 = ret[3]
        else: # code mode == "J2000"
            gaJ2000 = gx # for check
            gdJ2000 = gy # for check
            gpaJ2000 = gpx # for check
            gpdJ2000 = gpy # for check
        
        ret = slalib.sla_map(gaJ2000, gdJ2000, gpaJ2000, gpdJ2000, 0, 0, 2000, mjd + (tai_utc + 32.184)/(24.*3600.))
        ret = list(ret)
        """
        ret[0] = apparent_ra
        ret[1] = apparent_dec
        """
        if dcos == 0:
            #print(type(ret), ret[1], self.off_list['off_dec'])
            ret[1] = ret[1] + float(self.off_list["off_dec"])/3600.*math.pi/180
            ret[0] = ret[0] + float(self.off_list["off_ra"])/3600.*math.pi/180
        else:
            ret[1] = ret[1] + float(self.off_list["off_dec"])/3600.*math.pi/180
            ret[0] = ret[0] + (float(self.off_list["off_ra"])/3600.*math.pi/180)/math.cos(ret[1])
        ret = slalib.sla_aop(ret[0], ret[1], mjd, self.dut1, self.longitude, self.latitude, self.height, 0, 0, temp, pressure, humid, lamda, tlr=0.0065)
        """
        ret[0] = azimath(radian, N=0, E=90)
        ret[1] = zenith(radian)
        """
        #From zenith angle to elevation 
        real_az = ret[0]
        real_el = math.pi/2. - ret[1]
        real_az = real_az*180./math.pi*3600.
        real_el = real_el*180./math.pi*3600.
        track = self.move_azel(real_az, real_el, dcos, hosei, off_az=off_x,off_el=off_y,az_max_rate=az_max_rate, el_max_rate=el_max_rate)
        return track
    
    def move_lb(self, gx, gy, temp, pressure, humid, lamda, dcos, hosei = 'hosei_230.txt', off_coord = "HORIZONTAL", off_x = 0, off_y = 0, az_max_rate=16000, el_max_rate=12000):
        if off_x != 0 or off_y != 0: # for test
            self.set_offset(off_coord, off_x, off_y)
        if dcos == 0:
            gy += self.off_list["off_b"]/3600.*math.pi/180
            gx += self.off_list["off_l"]/3600.*math.pi/180
        else:
            gy += self.off_list["off_b"]/3600.*math.pi/180
            gx = gx+(self.off_list["off_l"]/3600.*math.pi/180)/math.cos(gy)
        
        ret = slalib.sla_galeq(gx, gy)
        """
        gaJ2000 = ret[0]
        gdj2000 = ret[1]
        gpaJ2000 = gpdJ2000 = 0
        """
        
        track = self.move_radec(ret[0], ret[1], 0, 0, "J2000", temp, pressure, humid, lamda, dcos, hosei, az_max_rate=az_max_rate, el_max_rate=el_max_rate)
        return track
    
    def move_planet(self, ntarg, code_mode, temp, pressure, humid, lamda, dcos, hosei = 'hosei_230.txt', off_coord = "HORIZONTAL", off_x = 0, off_y = 0, az_max_rate=16000, el_max_rate=12000):
        ret = self.coord.calc_planet_coordJ2000(ntarg)
        if len(ret) == 1:
            print(ret) #error
            return
            
        ret = self.coord.planet_J2000_geo_to_topo(ret[0], ret[1], ret[2], ret[3], self.dut1, self.longitude, self.latitude, self.height)
        
        #ret[2] = ra, ret[3] = dec
        self.move_radec(ret[2], ret[3], 0, 0, code_mode, temp, pressure, humid, lamda, dcos, hosei, off_coord, off_x, off_y, az_max_rate=az_max_rate, el_max_rate=el_max_rate)
        return
    
    """
    def calc_otf(self, x, y, dcos, coord_sys, dx, dy, dt, n, rampt, delay, temp, pressure, humid, lamda, hosei, code_mode):
        start_x = x-float(dx)/2.-float(dx)/float(dt)*rampt
        start_y = y-float(dy)/2.-float(dy)/float(dt)*rampt
        total_t = rampt + dt * n
        end_x = x + dx * (n - 0.5)
        end_y = y + dy * (n - 0.5)
        
        Az_track_flag = El_track_flag = 'TRUE'
        while Az_track_flag == 'TRUE' or El_track_flag == 'TRUE':
            if coord_sys == 'HORIZONTAL':
                ret = self.move_azel(start_x, start_y,dcos)
                Az_track_flag = ret[0]
                El_track_flag = ret[1]
            elif coord_sys == 'EQUATORIAL':                
                # ret = self.move_radec(start_x, start_y, gpx, gpy, code_mode, temp, pressure, humid, lamda, dcos, hosei)
                # gpx,gpy => 0 for radio observation or planet observation
                # change this when you do optical observation
                ret = self.move_radec(start_x, start_y, 0, 0, code_mode, temp, pressure, humid, lamda, dcos, hosei)
                Az_track_flag = ret[0]
                El_track_flag = ret[1]
            else:
                ret = self.move_lb(start_x, start_y, temp, pressure, humid, lamda, dcos, hosei)
                Az_track_flag = ret[0]
                El_track_flag = ret[1]
        mjd = 40587 + time.time()/(24.*3600.)
        self.otf(mjd+delay/24./3600., start_x, start_y, mjd+(delay+total_t)/24./3600., end_x, end_y, dcos, coord_sys, hosei, temp, pressure, humid, lamda, code_mode)
        return
    """
    
    def otf_thread_start(self, mjd_start, start_x, start_y, mjd_end, end_x, end_y, dcos, coord_sys, hosei, temp, pressure, humid, lamda, code_mode, ntarg=0, off_coord = "HORIZONTAL", off_x=0, off_y=0):
        self.otf_stop_thread = threading.Event()
        self.otf_tracking = threading.Thread(target = self.otf, args = (mjd_start, start_x, start_y, mjd_end, end_x, end_y, dcos, coord_sys, hosei,temp, pressure, humid, lamda, code_mode, ntarg, off_coord, off_x, off_y))
        self.otf_tracking.start()
        return
    
    def otf(self, mjd_start, start_x, start_y, mjd_end, end_x, end_y, dcos, coord_sys, hosei,temp, pressure, humid, lamda, code_mode, ntarg, off_coord, off_x, off_y):
        otf_end_flag = 0
        geomech_flag = 0
        loop_count = 0
        interval = 0


        while otf_end_flag == 0:
            loop_count += 1
            if loop_count%10 == 1 or interval > 0.1:
                geomech_flag = 1
                loop_count = 1
                #f.write(str(loop_count)+ 'if' +'\n')
                #f.write(str(mjd_start) + ' ' + str(mjd_end) + '\n')
            else:
                geomech_flag = 0
                #f.write(str(loop_count)+ 'else' +'\n')
                #f.write(str(mjd) + ' ' + str(mjd_start) + ' ' + str(mjd_end) + '\n')
            mjd = 40587 + time.time()/(24.*3600.)
            if mjd >= mjd_start and mjd <= mjd_end:
                off_x = (end_x - start_x) / (mjd_end - mjd_start) * (mjd - mjd_start) + start_x
                off_y = (end_y - start_y) / (mjd_end - mjd_start) * (mjd - mjd_start) + start_y
                
                if coord_sys == 'HORIZONTAL':
                    self.move_azel(off_x, off_y, dcos)
                    #self.move_azel(off_x,off_y, dcos, geomech_flag)
                elif coord_sys == 'EQUATORIAL':
                    #f.write(str('first') + ' ' + str(mjd) + ' ' + str(mjd_start) + ' ' + str(mjd_end) + ' ' + str(off_x) + ' ' + str(off_y) + '\n')
                    self.move_radec(off_x*math.pi/180., off_y*math.pi/180., 0, 0, code_mode, temp, pressure, humid, lamda, dcos, hosei, off_coord, off_x, off_y)
                    #for i in range(1000):
                    #f.write(str('second') + ' ' + str(mjd) + ' ' + str(mjd_start) + ' ' + str(mjd_end) + ' ' + str(off_x) + ' ' + str(off_y) + '\n')
                        #time.sleep(0.01)
                    #self.move_radec(off_x, off_y, 0, 0, code_mode, temp, pressure, humid, lamda, hosei, geomech_flag)
                elif coord_sys == 'GALACTIC':
                    self.move_lb(off_x*math.pi/180., off_y*math.pi/180., temp, pressure, humid, lamda, dcos, hosei, off_coord, off_x, off_y)
                    #self.move_lb(off_x, off_y, temp, pressure, humid, lamda, dcos, geomech_flag)
                else:#planet
                    self.move_planet(ntarg, code_mode, temp, pressure, humid, lamda, dcos, hosei, off_coord, off_x, off_y)#coord_mode = 0 → j2000 

            if mjd > mjd_end:
                otf_end_flag = 1

                #f.write('finish_program' + ' ' + str(mjd) + ' ' + str(mjd_start) + ' ' + str(mjd_end) + '\n')
            loop_time = 40587 + time.time()/(24.*3600.)
            interval = (loop_time-mjd)*24*3600.
            if interval < 0.01:
                time.sleep(0.01-interval)
        #f.close()
        return
    
    def thread_start(self, coord_sys, ntarg, gx, gy, gpx, gpy, code_mode, temp, pressure, humid, lamda, dcos, hosei = 'hosei_230.txt', off_coord = "HORIZONTAL", off_x = 0, off_y = 0, az_max_rate=16000, el_max_rate=12000):
        self.stop_thread = threading.Event()
        self.tracking = threading.Thread(target = self.tracking_start, args = (coord_sys, ntarg, gx, gy, gpx, gpy, code_mode, temp, pressure, humid, lamda, dcos, hosei, off_coord, off_x, off_y, az_max_rate, el_max_rate))
        self.tracking.start()
        return
    
    def tracking_start(self, coord_sys, ntarg, gx, gy, gpx, gpy, code_mode, temp, pressure, humid, lamda, dcos, hosei, off_coord, off_x, off_y, az_max_rate, el_max_rate):
        if coord_sys == 'EQUATRIAL':
            while not self.stop_thread.is_set():
                ret = self.nanten.enc.read_azel()
                if ret[0] >= 240.*3600. or ret[0] <= -240.*3600. or ret[1] >= 88.*3600. or ret[1] <= 2.*3600.:
                    self.nanten.dio.ctrl.out_word("FBIDIO_OUT1_16", 0)
                    self.nanten.dio.ctrl.out_word("FBIDIO_OUT17_32", 0)
                    return
                b_time = time.time()
                self.move_radec(gx, gy, gpx, gpy, code_mode, temp, pressure, humid, lamda, dcos, hosei, off_coord, off_x, off_y, az_max_rate, el_max_rate)
                a_time = time.time()
                if (a_time-b_time) < 0.01:
                    time.sleep(0.01-(a_time-b_time))
        elif coord_sys == 'GALACTIC':
            while not self.stop_thread.is_set():
                ret = self.nanten.enc.read_azel()
                if ret[0] >= 240.*3600. or ret[0] <= -240.*3600. or ret[1] >= 88.*3600. or ret[1] <= 2.*3600.:
                    self.nanten.dio.ctrl.out_word("FBIDIO_OUT1_16", 0)
                    self.nanten.dio.ctrl.out_word("FBIDIO_OUT17_32", 0)
                    return
                b_time = time.time()
                self.move_lb(gx, gy, temp, pressure, humid, lamda, dcos, hosei, off_coord, off_x, off_y, az_max_rate, el_max_rate)
                a_time = time.time()
                if (a_time-b_time) < 0.01:
                    time.sleep(0.01-(a_time-b_time))
        else: # planet
            while not self.stop_thread.is_set():
                ret = self.nanten.enc.read_azel()
                if ret[0] >= 240.*3600. or ret[0] <= -240.*3600. or ret[1] >= 88.*3600. or ret[1] <= 2.*3600.:
                    self.nanten.dio.ctrl.out_word("FBIDIO_OUT1_16", 0)
                    self.nanten.dio.ctrl.out_word("FBIDIO_OUT17_32", 0)
                    return
                b_time = time.time()
                self.move_planet(ntarg, code_mode, temp, pressure, humid, lamda, dcos, hosei, off_coord, off_x, off_y, az_max_rate, el_max_rate)
                a_time = time.time()
                if (a_time-b_time) < 0.01:
                    time.sleep(0.01-(a_time-b_time))
        return
        
    def tracking_end(self):
        print('DEBUG : tracking_end start')
        MOTOR_MAXSTEP = 1000
        print('DEBUG : tracking_end stop_thread.set()')
        self.stop_thread.set()
        print('DEBUG : tracking_end tracking.join()')
        self.tracking.join()
        print('DEBUG : start while')
        
        while abs(self.nanten.az_rate_d) > MOTOR_MAXSTEP or abs(self.nanten.el_rate_d) > MOTOR_MAXSTEP:
            print('==========================================')
            print('az_rate_d : %.1f, el_rate_d : %.1f, MOTOR_MAXSTEP : %.1f'%(self.nanten.az_rate_d, self.nanten.el_rate_d, MOTOR_MAXSTEP))
            print('==========================================')
            if abs(self.nanten.az_rate_d) > MOTOR_MAXSTEP:
                if self.nanten.az_rate_d < 0:
                    a = 1
                else:
                    a = -1
                self.nanten.az_rate_d += a*MOTOR_MAXSTEP
            else:
                self.nanten.az_rate_d = 0
            dummy = int(self.nanten.az_rate_d)
            self.nanten.dio.ctrl.out_word("FBIDIO_OUT1_16", dummy)
            
            if abs(self.nanten.el_rate_d) > MOTOR_MAXSTEP:
                if self.nanten.el_rate_d < 0:
                    a = 1
                else:
                    a = -1
                self.nanten.el_rate_d += a*MOTOR_MAXSTEP
            dummy = int(self.nanten.el_rate_d)
            self.nanten.dio.ctrl.out_word("FBIDIO_OUT17_32", dummy)
            time.sleep(0.01)
        print('==========================================')
        print('az_rate_d : %.1f, el_rate_d : %.1f, MOTOR_MAXSTEP : %.1f'%(self.nanten.az_rate_d, self.nanten.el_rate_d, MOTOR_MAXSTEP))
        print('------------------------------------------')
        self.nanten.dio.ctrl.out_word("FBIDIO_OUT1_16", 0)
        self.nanten.dio.ctrl.out_word("FBIDIO_OUT17_32", 0)
        return
    
    def otf_tracking_end(self):
        self.stop_thread.set()
        self.tracking.join()
        return
    
    """
    def otf_start(self, x, y, dcos, coord_sys, dx, dy, dt, n, rampt, delay, lamda, temp = 0, pressure = 0, humid = 0, hosei = 'hosei_230.txt', code_mode = 'J2000'):
        self.otf_stop_thread = threading.Event()
        self.otf_thread = threading.Thread(target = self.calc_otf, args = (x, y, dcos, coord_sys, dx, dy, dt, n, rampt, delay, temp, pressure, humid, lamda, hosei, code_mode, ))
        self.otf_thread.start()
        return
    """
    
    def otf_stop(self):
        MOTOR_MAXSTEP = 1000
        while abs(self.nanten.az_rate_d) > MOTOR_MAXSTEP or abs(self.nanten.el_rate_d) > MOTOR_MAXSTEP:
            if abs(self.nanten.az_rate_d) > MOTOR_MAXSTEP:
                if self.nanten.az_rate_d < 0:
                    a = 1
                else:
                    a = -1
                self.nanten.az_rate_d += a*MOTOR_MAXSTEP
            else:
                self.nanten.az_rate_d = 0
            dummy = int(self.nanten.az_rate_d)
            self.nanten.dio.ctrl.out_word("FBIDIO_OUT1_16", dummy)
            
            if abs(self.nanten.el_rate_d) > MOTOR_MAXSTEP:
                if self.nanten.el_rate_d < 0:
                    a = 1
                else:
                    a = -1
                self.nanten.el_rate_d += a*MOTOR_MAXSTEP
            dummy = int(self.nanten.el_rate_d)
            self.nanten.dio.ctrl.out_word("FBIDIO_OUT17_32", dummy)
            time.sleep(0.01)
        self.nanten.dio.ctrl.out_word("FBIDIO_OUT1_16", 0)
        self.nanten.dio.ctrl.out_word("FBIDIO_OUT17_32", 0)
        return
    
    def start_limit_check(self):
        self.stop_limit_flag = threading.Event()
        self.limit_thread = threading.Thread(target = self.limit_check)
        self.limit_thread.start()
        return
    
    def limit_check(self):
        while not self.stop_limit_flag.is_set():
            ret = self.nanten.antenna_limit_check()
            ret2 = self.error_check()
            if ret:
                self.stop_limit_flag.set()
            else:
                time.sleep(3)
        try:
            self.stop_thread.set()
        except: pass
        try:
            self.otf_stop_thread.set()
        except: pass
        return
    
    def stop_limit_check(self):
        self.stop_limit_check.set()
        self.limit_thread.join()
        return

    #def read_targetazel(self):
        #return [self.target_az, self.target_el]

    def read_azel(self):
        ret = self.nanten.read_azel()
        return ret

    def read_track(self):
        return [self.az_track, self.el_track]
    
    def read_error(self):
        ret = self.nanten.read_error()
        return ret

    def read_limit(self):
        ret = self.nanten.read_error()
        return ret
        
    def read_v(self): # [arcsec/s]
        return [self.az_v, self.el_v]
    
    def read_status(self):
        return self.antenna_status


def antenna_client(host, port):
    client = pyinterface.server_client_wrapper.control_client_wrapper(antenna_nanten_controller, host, port)
    return client

def antenna_monitor_client(host, port):
    client = pyinterface.server_client_wrapper.monitor_client_wrapper(antenna_nanten_controller, host, port)
    return client

def start_antenna_server(port1 = 8003, port2 = 8004):
    antenna = antenna_nanten_controller()
    server = pyinterface.server_client_wrapper.server_wrapper(antenna, '', port1, port2)
    server.start()
    return server

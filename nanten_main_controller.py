import math
import time
import sys
sys.path.append('/home/amigos/python/')
import numpy as np
import pyinterface
import antenna_enc
import threading


class nanten_main_controller(object):
    
    MOTOR_SAMPLING = 10 #memo
    dt = MOTOR_SAMPLING/1000.
    
    count = 0
    az_array = []
    el_array = []
    target_az_array = []
    target_el_array = []

    error_box = [0]*32
    #azv_before = elv_before = 0
    az_enc_before = el_enc_before = 0
    az_rate = el_rate = 0
    az_rate_d = el_rate_d = 0
    m_stop_rate_az = m_stop_rate_el = 0
    t1 = t2 = 0.0
    t_az = t_el = 0.0
    current_speed_az = current_speed_el = 0.0
    pre_hensa_az = pre_hensa_el = 0
    ihensa_az = ihensa_el = 0.0
    pre_az_arcsec = pre_el_arcsec = 0
    
    indaz = 0
    indel = 0
    
    az_encmoni = 0
    el_encmoni = 0
    az_targetmoni = 0
    el_targetmoni = 0
    az_targetspeedmoni = 0
    el_targetspeedmoni = 0
    az_hensamoni = 0
    el_hensamoni = 0
    az_ihensamoni = 0
    el_ihensamoni = 0
    
    #for drive.py
    t1_moni = 0
    t2_moni = 0
    az_pidihensamoni = 0
    el_pidihensamoni = 0
    
    
    
    th_az = 0
    th_el = 0
    server_flag = []
    end_flag = 0
    
    
    
    def __init__(self):
        self.dio = pyinterface.create_gpg2000(3)
        self.enc = antenna_enc.enc_monitor_client('172.20.0.11',8002)
        #self.enc = antenna_enc.enc_controller()
        ret = self.enc.read_azel()
        self.az_encmoni = ret[0]
        self.el_encmoni = ret[1]
        pass
    
    
    
    
    
    
    def read_enc(self):
        ret = self.enc.read_azel()
        self.th_az = ret[0]
        self.th_el = ret[1]
        return
    
    def count_time(self):
        flag_list = self.server_flag[:]
        time.sleep(1)
        if self.server_flag == flag_list:
            self.dio.ctrl.out_word("FBIDIO_OUT1_16", 0)
            self.dio.ctrl.out_word("FBIDIO_OUT17_32", 0)
            self.end_flag = 1
            for i in range(1000):
                print(flag_list)
        return
    
    
    
    
    
    
    
    
    def init_speed(self):
        self.dio.ctrl.out_word("FBIDIO_OUT1_16", 0)
        self.dio.ctrl.out_word("FBIDIO_OUT17_32", 0)
        return
    
    def azel_move(self, az_arcsec, el_arcsec, az_max_rate, el_max_rate):
        test_flag = 1
        self.indaz = az_arcsec
        self.indel = el_arcsec
        ret = self.enc.read_azel()
        if abs(az_arcsec-ret[0]) >= 1 or abs(el_arcsec-ret[1]) > 1:
            b_time = time.time()
            self.move_azel(az_arcsec, el_arcsec, az_max_rate, el_max_rate)
            ret = self.enc.read_azel()
            interval = time.time()-b_time
            if interval <= 0.01:
                time.sleep(0.01-interval)
        else:
            self.dio.ctrl.out_word("FBIDIO_OUT1_16", 0)
            self.dio.ctrl.out_word("FBIDIO_OUT17_32", 0)
            time.sleep(0.02)
            return 0
        return 1
        
    def move_azel(self, az_arcsec, el_arcsec, az_max_rate = 16000, el_max_rate = 12000, m_bStop = 'FALSE'):
        MOTOR_MAXSTEP = 1000
        #MOTOR_AZ_MAXRATE = 16000
        MOTOR_AZ_MAXRATE = 10000
        MOTOR_EL_MAXRATE = 12000
        stop_flag = 0
        
        ret = self.calc_pid(az_arcsec, el_arcsec, az_max_rate, el_max_rate)
        az_rate_ref = ret[0]
        el_rate_ref = ret[1]
        Az_track_flag = ret[2]
        El_track_flag = ret[3]
        
        # command value to target value
        daz_rate = az_rate_ref - self.az_rate_d
        del_rate = el_rate_ref - self.el_rate_d
        
        #limit of acc
        if abs(daz_rate) < MOTOR_MAXSTEP:
            self.az_rate_d = az_rate_ref
        else:
            if daz_rate < 0:
                a = -1
            else:
                a = 1
            self.az_rate_d += a*MOTOR_MAXSTEP
        if abs(del_rate) < MOTOR_MAXSTEP:
            self.el_rate_d = el_rate_ref
        else:
            if del_rate < 0:
                a = -1
            else:
                a = 1
            self.el_rate_d += a*MOTOR_MAXSTEP
        
        #limit of max v
        if self.az_rate_d > MOTOR_AZ_MAXRATE:
            self.az_rate_d = MOTOR_AZ_MAXRATE
        if self.az_rate_d < -MOTOR_AZ_MAXRATE:
            self.az_rate_d = -MOTOR_AZ_MAXRATE
        if self.el_rate_d > MOTOR_EL_MAXRATE:
            self.el_rate_d = MOTOR_EL_MAXRATE
        if self.el_rate_d < -MOTOR_EL_MAXRATE:
            self.el_rate_d = -MOTOR_EL_MAXRATE
        
        # confirm limit of controll rack => forced outage
        #if(0< motordrv_nanten2_cw_limit()+motordrv_nanten2_ccw_limit()+motordrv_nanten2_up_limit()+motordrv_nanten2_down_limit())
        #     motordrv_nanten2_drive_on(FALSE,FALSE);
        
        
        # output to port
        if m_bStop == 'TRUE':
            dummy = self.m_stop_rate_az
        else:
            dummy = int(self.az_rate_d)
        
        
        #for 1st limit
        ret = self.dio.ctrl.in_byte("FBIDIO_IN1_8")
        if (ret>>2 & 0x01) == 1:
            pass
        else:
            dummy = 0
            stop_flag = 1
        
        
        #dummy=m_bStop==TRUE?m_stop_rate_az:motor_param.az_rate_ref;
        self.dio.ctrl.out_word("FBIDIO_OUT1_16", dummy)
        #dioOutputWord(CONTROLER_BASE2,0x00,dummy)  output port is unreliable
        self.az_rate_d = dummy
        
        if m_bStop == 'TRUE':
            dummy = self.m_stop_rate_el
        else:
            dummy = int(self.el_rate_d)
        
        if (ret>>3 & 0x01) == 1:
            pass
        else:
            dummy = 0
            stop_flag = 1
        
        #dummy=m_bStop==TRUE?m_stop_rate_el:motor_param.el_rate_ref;
        self.dio.ctrl.out_word("FBIDIO_OUT17_32", dummy)
        #dioOutputWord(CONTROLER_BASE2,0x02,dummy);
        self.el_rate_d = dummy
        if stop_flag:
            sys.exit()
        return [Az_track_flag, El_track_flag]
    
    def test_move(self,az_speed,el_speed,dist_arcsec = 5 * 3600):
        # type check
        if isinstance(az_speed,int) and isinstance(el_speed,int) and isinstance(dist_arcsec,int):
            type_flag = 1
            # get current position
            pos = self.enc.read_azel()
            # max speed limit
            if az_speed > 10000:
                az_speed = 10000
            if el_speed > 10000:
                el_speed = 10000
            # speed set
            self.dio.ctrl.out_word("FBIDIO_OUT1_16", az_speed)
            self.dio.ctrl.out_word("FBIDIO_OUT17_32", el_speed)
        else:
            type_flag = 0
            print("Please input Int.")
        if (az_speed == 0 and el_speed == 0) or type_flag == 0:
            dist_flag = 0
        else:
            dist_flag = 1
        while dist_flag:
            b_time = time.time()
            ret = self.enc.read_azel()
            if ret[0] < -265 * 3600 or ret[0] > 265 * 3600 or ret[1] < -0.1 * 3600 or ret[1] > 90.1 *3600:
                dist_flag = 0
                self.dio.ctrl.out_word("FBIDIO_OUT1_16", 0)
                self.dio.ctrl.out_word("FBIDIO_OUT17_32", 0)
                time.sleep(0.02)
            else:
                if abs(ret[0] - pos[0]) + abs(ret[1] - pos[1]) >= dist_arcsec:
                    dist_flag = 0
                    self.dio.ctrl.out_word("FBIDIO_OUT1_16", 0)
                    self.dio.ctrl.out_word("FBIDIO_OUT17_32", 0)
                    time.sleep(0.02)
                else:
                    ret = self.enc.read_azel()
                    az_enc = ret[0]
                    el_enc = ret[1]
                    #for az >= 180*3600 and az <= -180*3600
                    if az_enc > 40*3600 and az_arcsec+360*3600 < 220*3600:
                        az_arcsec += 360*3600
                    elif az_enc < -40*3600 and az_arcsec-360*3600 > -220*3600:
                        az_arcsec -= 360*3600
                    self.az_encmoni = ret[0]
                    self.el_encmoni = ret[1]
                    #for drive.py
                    self.t1_moni = self.t1
                    self.t2_moni = self.t2
                    interval = time.time()-b_time
                    if interval <= 0.01:
                        time.sleep(0.01-interval)
        
        return

    def calc_pid(self, az_arcsec, el_arcsec, az_max_rate, el_max_rate):
        # Default
        """
        Paz = 3.8
        Iaz = 8
        Daz = 0.11
        Pel = 3.73
        Iel = 8
        Del = 0.07
        """
        # New parameter
        """
        p_az_coeff = 3.0
        i_az_coeff = 2.0
        d_az_coeff = 0.
        s_az_coeff = 0.
        p_el_coeff = 3.0
        i_el_coeff = 3.0
        d_el_coeff = 0.
        s_el_coeff = 0.
        """
        
        f = open('/home/amigos/NECST/soft/obs/telescope_nanten/PID_param.txt')
        param = f.read()
        f.close()
        line1=param.split('\n')
        
        p_az_coeff = float(line1[0])
        i_az_coeff = float(line1[1])
        d_az_coeff = float(line1[2])
        s_az_coeff = float(line1[3])
        p_el_coeff = float(line1[4])
        i_el_coeff = float(line1[5])
        d_el_coeff = float(line1[6])
        s_el_coeff = float(line1[7])
        
        
        DEG2ARCSEC = 3600.
        m_bAzTrack = "FALSE"
        m_bElTrack = "FALSE"
        if self.t2 == 0.0:
         self.t2 = time.time()
        else:
            pass
        
        
        
        tv = time.time()
        self.server_flag.append(tv)
        if len(self.server_flag) == 4:
            self.server_flag.pop(0)
        self.end_flag = 0
        enc_thread = threading.Thread(target = self.read_enc)
        enc_thread.start()
        count_thread = threading.Thread(target = self.count_time)
        count_thread.start()
        enc_thread.join()
        
        
        if self.end_flag:
            for i in range(2000):
                print("!!!end!!!")
            sys.exit()
        
        #ret = self.enc.read_azel()
        #az_enc = ret[0]
        #el_enc = ret[1]
        az_enc = self.th_az
        el_enc = self.th_el
        
        
        
        
        #for az >= 180*3600 and az <= -180*3600
        if az_enc > 40*3600 and az_arcsec+360*3600 < 220*3600:
            az_arcsec += 360*3600
        elif az_enc < -40*3600 and az_arcsec-360*3600 > -220*3600:
            az_arcsec -= 360*3600
        
        #self.az_encmoni = ret[0]
        #self.el_encmoni = ret[1]
        self.az_encmoni = self.th_az
        self.el_encmoni = self.th_el
        self.az_targetmoni = az_arcsec
        self.el_targetmoni = el_arcsec
        
        #calculate ichi_hensa
        az_err = az_arcsec-az_enc
        el_err = el_arcsec-el_enc
        
        """
        #old ver(Unknown)
        #integrate error
        az_err_integral_integral+=az_err_integral*dt;
        el_err_integral_integral+=el_err_integral*dt;
        
        #derivative
        azv_err = azv-(az_enc-self.az_enc_before)/self.dt
        elv_err = elv-(el_enc-self.el_enc_before)/self.dt
        """
        
        """
        azv_acc = (azv-self.azv_before)
        elv_acc = (elv-self.elv_before)
        self.azv_before = azv
        self.elv_before = elv
        
        if azv_acc > 50:
            azv_acc = 50
        elif azv_acc < -50:
            azv_acc = -50
        
        if elv_acc > 50:
            elv_acc = 50
        elif elv_acc < -50:
            elv_acc = -50
        """
        
        target_az = az_arcsec
        target_el = el_arcsec
        hensa_az = target_az - az_enc
        hensa_el = target_el - el_enc
        ret = self.ave_calc(hensa_az, hensa_el) #average of hensa_az(ret[0]) and hensa_el(ret[1])
        
        if 3 > math.fabs(ret[0]):
            m_bAzTrack = "TRUE" #def Paz=2?
        else:
            # az_err_integral += (self.az_err_before+az_err)*self.dt/2.+azv_acc*0.0
            m_bAzTrack = 'FALSE'
            pass
        if 3 > math.fabs(ret[1]):
            m_bElTrack = "TRUE" #def Pel=2?
        else:
            #el_err_integral += (self.el_err_before+el_err)*self.dt/2.+elv_acc*0.0
            m_bElTrack = 'FALSE'
            pass
        
        
        
        self.az_hensamoni = hensa_az
        self.el_hensamoni = hensa_el
        
        dhensa_az = hensa_az - self.pre_hensa_az
        dhensa_el = hensa_el - self.pre_hensa_el
        if math.fabs(dhensa_az) > 1:
            dhensa_az = 0
        if math.fabs(dhensa_el) > 1:
            dhensa_el = 0
        
        self.t1 = time.time()
        if self.t_az == 0.0 and self.t_el == 0.0:
            self.t_az = self.t_el = self.t1
        else:
            if (az_enc - self.az_enc_before) != 0.0:
                self.current_speed_az = (az_enc - self.az_enc_before) / (self.t1-self.t_az)
                self.t_az = self.t1
            if (el_enc - self.el_enc_before) != 0.0:
                self.current_speed_el = (el_enc - self.el_enc_before) / (self.t1-self.t_el)
                self.t_el = self.t1
        
        if self.pre_az_arcsec == 0: # for first move
            target_speed_az = 0
        else:
            target_speed_az = (az_arcsec-self.pre_az_arcsec)/(self.t1-self.t2)
        if self.pre_el_arcsec == 0: # for first move
            target_speed_el = 0
        else:
            target_speed_el = (el_arcsec-self.pre_el_arcsec)/(self.t1-self.t2)
        ret = self.medi_calc(target_speed_az, target_speed_el)
        target_speed_az = ret[0]
        target_speed_el = ret[1]
        
        self.ihensa_az += (hensa_az+self.pre_hensa_az)/2
        self.ihensa_el += (hensa_el+self.pre_hensa_el)/2
        #if math.fabs(hensa_az) > math.fabs(self.current_speed_az)/10.+10.:
        #self.ihensa_az = 0
        #if math.fabs(hensa_el) > math.fabs(self.current_speed_el)/10.+10.:
            #self.ihensa_el = 0
        """
        if math.fabs(hensa_az) > 150:
            self.ihensa_az = 0
        if math.fabs(hensa_el) > 150:
            self.ihensa_el = 0
        
        if math.fabs(hensa_az) > 100:
            self.ihensa_az = 0
        if math.fabs(hensa_el) > 100:
            self.ihensa_el = 0
        """
        if math.fabs(hensa_az) > 50:
            self.ihensa_az = 0
        if math.fabs(hensa_el) > 50:
            self.ihensa_el = 0
        
        """Previous
        if math.fabs(hensa_az) >= 0.00: # don't use ihensa?
            ihensa_az = 0
            #hensa_flag_az = 0;
        else:
            #if(hensa_flag_az == 0 && hensa_az * pre_hensa_az <= 0)
            #  hensa_flag_az = 1;
            #if(hensa_flag_az == 1)
            ihensa_az += hensa_az
        if math.fabs(hensa_el) >= 0.000:
            ihensa_el = 0
            #hensa_flag_el = 0;
        else:
            #if(hensa_flag_el == 0 && hensa_el * pre_hensa_el <= 0)
                hensa_flag_el = 1;
            #if(hensa_flag_el == 1)
                ihensa_el += hensa_el
        """
        
        """ Original
        self.az_rate = Paz*az_err + Iaz*az_err_integral + Daz*azv_err_avg +azv*1.57
        self.el_rate = Pel*el_err + Iel*el_err_integral + Del*elv_err_avg +elv*1.57
        """
        
        #self.az_rate = target_speed_az * 20.9 + (current_speed_az*20.9 - self.az_rate) * s_az_coeff + p_az_coeff*hensa_az + i_az_coeff*ihensa_az*(self.t1-self.t2) + d_az_coeff*dhensa_az/(self.t1-self.t2)
        #self.el_rate = target_speed_el * 20.9 + p_el_coeff*hensa_el + i_el_coeff*ihensa_el*(self.t1-self.t2) + d_el_coeff*dhensa_el/(self.t1-self.t2)
        self.az_rate = target_speed_az + (self.current_speed_az - self.az_rate) * s_az_coeff + p_az_coeff*hensa_az + i_az_coeff*self.ihensa_az*(self.t1-self.t2) + d_az_coeff*dhensa_az/(self.t1-self.t2)
        self.el_rate = target_speed_el + (self.current_speed_el - self.el_rate) * s_el_coeff + p_el_coeff*hensa_el + i_el_coeff*self.ihensa_el*(self.t1-self.t2) + d_el_coeff*dhensa_el/(self.t1-self.t2)
        
        self.az_targetspeedmoni = target_speed_az
        self.el_targetspeedmoni = target_speed_el
        self.az_ihensamoni = self.ihensa_az*(self.t1-self.t2)
        self.el_ihensamoni = self.ihensa_el*(self.t1-self.t2)
        
        #for drive.py
        self.t1_moni = self.t1
        self.t2_moni = self.t2
        self.az_pidihensamoni = self.ihensa_az
        self.el_pidihensamoni = self.ihensa_el
        
        
        if math.fabs(az_err) < 8000 and self.az_rate > 10000:
            self.az_rate = 10000
        
        if math.fabs(az_err) < 8000 and self.az_rate < -10000:
            self.az_rate = -10000
        
        if math.fabs(el_err) < 9000 and self.el_rate > 10000:
            self.el_rate = 10000
        
        if math.fabs(el_err) < 7000 and self.el_rate < -8000:
            self.el_rate = -8000
        
        
        #update
        self.az_enc_before = az_enc
        self.el_enc_before = el_enc
        self.az_err_before = az_err
        self.el_err_before = el_err
        
        self.pre_hensa_az = hensa_az
        self.pre_hensa_el = hensa_el
        
        self.pre_az_arcsec = az_arcsec
        self.pre_el_arcsec = el_arcsec
        
        #for negative value of az|el_max_rate
        az_max_rate = math.fabs(az_max_rate)
        el_max_rate = math.fabs(el_max_rate)
        
        if az_max_rate > 16000:
            az_max_rate = 16000
        if el_max_rate > 12000:
            el_max_rate = 12000
        
        #if(az_enc<5*DEG2ARCSEC) rate=min(1000, rate);
        
        softlimit_az_plus = 265.0
        softlimit_az_minus = -265.0
        softlimit_el_plus = 90.1
        softlimit_el_minus = -0.1
        
        
        #limit of dangerous zone
        if (el_enc < softlimit_el_minus * DEG2ARCSEC and self.el_rate < 0 ) or (el_enc > softlimit_el_plus*DEG2ARCSEC and self.el_rate > 0):
            el_max_rate = min(0, el_max_rate)
        if (az_enc < softlimit_az_minus*DEG2ARCSEC and self.az_rate < 0) or (az_enc > softlimit_az_plus*DEG2ARCSEC and self.az_rate > 0):
            az_max_rate = min(1600, az_max_rate); #bug?
        
        #lmit of speed
        if self.az_rate > az_max_rate:
            self.az_rate = az_max_rate
        if self.az_rate < -az_max_rate:
            self.az_rate = -az_max_rate
        if self.el_rate > el_max_rate:
            self.el_rate = el_max_rate
        if self.el_rate < -el_max_rate:
            self.el_rate = -el_max_rate
        
        # arienai ryouiki deno gyakuunndou kinnsi //bug?
        #if az_enc <= -90*DEG2ARCSEC and self.az_rate < 0:
            #self.az_rate = 0
        #if az_enc >= 380*DEG2ARCSEC and self.az_rate > 0:
            #self.az_rate = 0
        
        if az_enc <= softlimit_az_minus*DEG2ARCSEC and self.az_rate < 0:
            self.az_rate = 0
        if az_enc >= softlimit_az_plus*DEG2ARCSEC and self.az_rate > 0:
            self.az_rate = 0
        
        if el_enc <= softlimit_el_minus*DEG2ARCSEC and self.el_rate < 0:
            self.el_rate = 0
        if el_enc >= softlimit_el_plus*DEG2ARCSEC and self.el_rate > 0:
            self.el_rate = 0
        self.t2 = self.t1
        
        az_rate_ref = int(self.az_rate) #??
        el_rate_ref = int(self.el_rate) #??
        return [az_rate_ref, el_rate_ref, m_bAzTrack, m_bElTrack]
    
    def ave_calc(self, az, el):
        array_num = 3
        length = len(self.az_array)
        if length < 3:
            self.az_array.insert(0, az)
            self.el_array.insert(0, el)
        else:
            self.az_array.insert(0, az)
            self.el_array.insert(0, el)
            self.az_array.pop(3)
            self.el_array.pop(3)
        
        ave_az = np.average(self.az_array)
        ave_el = np.average(self.el_array)
        return [ave_az, ave_el]
    
    def medi_calc(self, target_az, target_el):
        target_num = 13 # number of median array
        if self.count < target_num:
            self.target_az_array.insert(0, target_az)
            self.target_el_array.insert(0, target_el)
            self.count += 1
        else:
            self.target_az_array.insert(0, target_az)
            self.target_el_array.insert(0, target_el)
            self.target_az_array.pop(13)
            self.target_el_array.pop(13)
        
        median_az = np.median(self.target_az_array)
        median_el = np.median(self.target_el_array)
        return [median_az, median_el]
    
    def antenna_limit_check(self):
        stop_flag = 0
        ret = [0]*4
        ret[0] = self.dio.ctrl.in_byte('FBIDIO_IN1_8')
        ret[1] = self.dio.ctrl.in_byte('FBIDIO_IN9_16')
        ret[2] = self.dio.ctrl.in_byte('FBIDIO_IN17_24')
        ret[3] = self.dio.ctrl.in_byte('FBIDIO_IN25_32')

        for i in range(8):
            self.error_box[i] = ret[0] >> i & 0x01
        for i in range(8):
            self.error_box[i+8] = ret[1] >> i & 0x01
        for i in range(8):
            self.error_box[i+16] = ret[2] >> i & 0x01
        for i in range(8):
            self.error_box[i+24] = ret[3] >> i & 0x01
        

        if (ret[0]>>4 & 0x01) == 0:
            print('!!!soft limit CW!!!')
            stop_flag = 1
        if (ret[0]>>5 & 0x01) == 0:
            print('!!!soft limit CCW!!!')
            stop_flag = 1
        if (ret[0]>>6 & 0x01) == 0:
            print('!!!soft limit UP!!!')
            stop_flag = 1
        if (ret[0]>>7 & 0x01) == 0:
            print('!!!soft limit DOWN!!!')
            stop_flag = 1
        if (ret[1]>>0 & 0x01) == 0:
            print('!!!1st limit CW!!!')
            stop_flag = 1
        if (ret[1]>>1 & 0x01) == 0:
            print('!!!1st limit CCW!!!')
            stop_flag = 1
        if (ret[1]>>2 & 0x01) == 0:
            print('!!!1st limit UP!!!')
            stop_flag = 1
        if (ret[1]>>3 & 0x01) == 0:
            print('!!!1st limit DOWN!!!')
            stop_flag = 1
        if (ret[1]>>4 & 0x01) == 0:
            print('!!!2nd limit CW!!!')
            stop_flag = 1
        if (ret[1]>>5 & 0x01) == 0:
            print('!!!2nd limit CCW!!!')
            stop_flag = 1
        if (ret[1]>>6 & 0x01) == 0:
            print('!!!2nd limit UP!!!')
            stop_flag = 1
        if (ret[1]>>7 & 0x01) == 0:
            print('!!!2nd limit DOWN!!!')
            stop_flag = 1
        return stop_flag
    
    def read_azel(self):
        #return [self.az_encmoni, self.el_encmoni, self.az_targetmoni, self.el_targetmoni, self.az_hensamoni, self.el_hensamoni, self.az_rate_d, self.el_rate_d, self.az_targetspeedmoni, self.el_targetspeedmoni, self.current_speed_az, self.current_speed_el, self.az_ihensamoni ,self.el_ihensamoni]
        #for drive.py
        return [self.az_encmoni, self.el_encmoni, self.az_targetmoni, self.el_targetmoni, self.az_hensamoni, self.el_hensamoni, self.az_rate_d, self.el_rate_d, self.az_targetspeedmoni, self.el_targetspeedmoni, self.current_speed_az, self.current_speed_el, self.az_ihensamoni ,self.el_ihensamoni ,self.t1_moni ,self.t2_moni ,self.az_pidihensamoni ,self.el_pidihensamoni]

    def read_error(self):
        return self.error_box

def nanten_main_client(host, port):
    client = pyinterface.server_client_wrapper.control_client_wrapper(nanten_main_controller, host, port)
    return client

def nanten_main_monitor_client(host, port):
    client = pyinterface.server_client_wrapper.monitor_client_wrapper(nanten_main_controller, host, port)
    return client

def start_nanten_main_server(port1 = 7003, port2 = 7004):
    nanten_main = nanten_main_controller()
    server = pyinterface.server_client_wrapper.server_wrapper(nanten_main, '', port1, port2)
    server.start()
    return server


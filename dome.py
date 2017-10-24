import time
import math
import threading
import pyinterface
import sys

import dome_pos
import antenna_enc



class dome_controller(object):
    #speed = 3600 #[arcsec/sec]
    touchsensor_pos = [-391,-586,-780,-974,-1168,-1363,-1561,-1755,-1948,-2143, 0, -197]
    dome_encoffset = 10000
    buffer = [0,0,0,0,0,0]
    stop = [0]
    error = []
    count = 0
    status_box = []
    dome_enc = 0
    limit = 0
    
    def __init__(self):
        self.enc = antenna_enc.enc_monitor_client('172.20.0.11',8002)
        #self.enc = antenna_enc.enc_controller()
        #self.dome_pos = dome_pos.dome_pos_client('172.20.0.11',8006)
        self.dome_pos = dome_pos.dome_pos_controller()
        self.dio = pyinterface.create_gpg2000(5)
        self.start_status_check()
        pass
    
    def start_thread(self):
        tlist = threading.enumerate()
        for i in tlist:
            n = i.getName()
            if n == "d_track":
                return
        self.end_track_flag = threading.Event()
        self.thread = threading.Thread(target = self.move_track, name = "d_track")
        self.thread.start()
        return
    
    def end_thread(self):
        try:
            self.end_track_flag.set()
            self.thread.join()
            buff = [0]
            self.dio.do_output(buff, 2, 1)
            return
        except:
            pass
    
    def move_track(self):
        #ret = self.dome_pos.read_dome_enc()
        #ret = self.dome_pos.dome_encoder_acq()
        ret = self.read_domepos()
        while not self.end_track_flag.is_set():
            ret = self.enc.read_azel()
            ret[0] = ret[0]/3600. # ret[0] = antenna_az
            #dome_az = self.dome_pos.read_dome_enc()
            #dome_az = self.dome_pos.dome_encoder_acq()
            dome_az = self.read_domepos()
            dome_az = dome_az/3600.
            self.dome_limit()
            if math.fabs(ret[0]-dome_az) >= 2.0:
                self.move(ret[0])
            time.sleep(0.01)
    
    def test(self, num): #for track_test
        self.start_thread()
        time.sleep(num)
        self.end_thread()
        return
    
    def print_msg(self,msg):
        print(msg)
        return
    
    def print_error(self,msg):
        self.error.append(msg)
        self.print_msg('!!!!ERROR!!!!'+msg)
        return
    
    def move_org(self):
        dist = 90
        self.move(dist)    #move_org
        #self.dome_pos.read_dome_enc()
        return
    
    def move(self, dist):
        #pos_arcsec = self.dome_pos.dome_encoder_acq()
        #pos_arcsec = self.dome_pos.read_dome_enc()
        pos_arcsec = self.read_domepos()
        pos = pos_arcsec/3600.
        pos = pos % 360.0
        dist = dist % 360.0
        diff = dist - pos
        dir = diff % 360.0
        
        if pos == dist: return
        if dir < 0:
            if abs(dir) >= 180:
                turn = 'right'
            else:
                turn = 'left'
        else:
            if abs(dir) >= 180:
                turn = 'left'
            else:
                turn = 'right'
        if abs(dir) < 5.0 or abs(dir) > 355.0 :
            speed = 'low'
        elif abs(dir) > 20.0 and abs(dir) < 340.0:#or => and
            speed = 'high'
        else:
            speed = 'mid'
        if dir <= 1:
            dir = 0
        if dir != 0:
            global buffer
            self.buffer[1] = 1
            self.do_output(turn, speed)
            while dir != 0:
                #pos_arcsec = self.dome_pos.dome_encoder_acq()
                #pos_arcsec = self.dome_pos.read_dome_enc()
                pos_arcsec = self.read_domepos()
                pos = pos_arcsec/3600.
                pos = pos % 360.0
                dist = dist % 360.0
                diff = dist - pos
                dir = diff % 360.0
                #print(pos,dist,diff,dir)
                if dir <= 0.5:
                    dir = 0
                else:
                    if abs(dir) < 5.0 or dir > 355.0:
                        speed = 'low'
                    elif abs(dir) > 20.0 and abs(dir) < 340.0:
                        speed = 'high'
                    else:
                        speed = 'mid'
                    self.do_output(turn, speed)
        
        self.dome_stop()
        #self.get_count()
        return
    
    def dome_stop(self):
        buff = [0]
        self.dio.do_output(buff, 2, 1)
        return
    
    def dome_open(self):
        ret = self.get_door_status()
        if ret[1] != 'OPEN' and ret[3] != 'OPEN':
            buff = [1, 1]
            self.dio.do_output(buff, 5, 2)
            d_door = self.get_door_status()
            while ret[1] != 'OPEN':
                time.sleep(5)
                ret = self.get_door_status()
        buff = [0, 0]
        self.dio.do_output(buff, 5, 2)
        return
    
    def dome_close(self):
        ret = self.get_door_status()
        if ret[1] != 'CLOSE' and ret[3] != 'CLOSE':
            buff = [0, 1]
            self.dio.do_output(buff, 5, 2)
            while ret[1] != 'CLOSE':
                time.sleep(5)
                ret = self.get_door_status()
        buff = [0, 0]
        self.dio.do_output(buff, 5, 2)
        return
    
    def memb_open(self):
        ret = self.get_memb_status()
        if ret[1] != 'OPEN':
            buff = [1, 1]
            self.dio.do_output(buff, 7, 2)
            while ret[1] != 'OPEN':
                time.sleep(5)
                ret = self.get_memb_status()
        buff = [0, 0]
        self.dio.do_output(buff, 7, 2)
        return
    
    def memb_close(self):
        ret = self.get_memb_status()
        if ret[1] != 'CLOSE':
            buff = [0, 1]
            self.dio.do_output(buff, 7, 2)
            while ret[1] != 'CLOSE':
                time.sleep(5)
                ret = self.get_memb_status()
        buff = [0, 0]
        self.dio.do_output(buff, 7, 2)
        return
    
    def emergency_stop(self):
        global stop
        dome_controller.stop = [1]
        self.pos.dio.do_output(self.stop, 11, 1)
        self.print_msg('!!EMERGENCY STOP!!')
        return
    
    def dome_fan(self, fan):
        if fan == 'on':
            fan_bit = [1, 1]
            self.dio.do_output(fan_bit, 9, 2)
        else:
            fan_bit = [0, 0]
            self.dio.do_output(fan_bit, 9, 2)
        return
    
    def get_count(self):
        self.count = self.dome_pos.dome_encoder_acq()
        return self.count
    
    def do_output(self, turn, speed):
        global buffer
        global stop
        if turn == 'right': self.buffer[0] = 0
        else: self.buffer[0] = 1
        if speed == 'low':
            self.buffer[2:4] = [0, 0]
        elif speed == 'mid':
            self.buffer[2:4] = [1, 0]
        else:
            self.buffer[2:4] = [0, 1]
        if dome_controller.stop[0] == 1:
            self.buffer[1] = 0
        else: self.buffer[1] = 1
        self.dio.do_output(self.buffer, 1, 6)
        #self.dome_limit()
        #pos_arcsec = self.dome_pos.dome_encoder_acq()
        #pos_arcsec = self.dome_pos.read_dome_enc()
        return
    
    def get_action(self):
        ret = self.dio.di_check(1, 1)
        if ret == 0:
            move_status = 'OFF'
        else:
            move_status = 'DRIVE'
        return move_status
    
    def get_door_status(self):
        ret = self.dio.di_check(2, 6)
        if ret[0] == 0:
            right_act = 'OFF'
        else:
            right_act = 'DRIVE'
        
        if ret[1] == 0:
            if ret[2] == 0:
                right_pos = 'MOVE'
            else:
                right_pos = 'CLOSE'
        else:
            right_pos = 'OPEN'
        
        if ret[3] == 0:
            left_act = 'OFF'
        else:
            left_act = 'DRIVE'
        
        if ret[4] == 0:
            if ret[5] == 0:
                left_pos = 'MOVE'
            else:
                left_pos = 'CLOSE'
        else:
            left_pos = 'OPEN'
        return [right_act, right_pos, left_act, left_pos]
        
    def get_memb_status(self):
        ret = self.dio.di_check(8, 3)
        if ret[0] == 0:
            memb_act = 'OFF'
        else:
            memb_act = 'DRIVE'
        
        if ret[1] == 0:
            if ret[2] == 0:
                memb_pos = 'MOVE'
            else:
                memb_pos = 'CLOSE'
        else:
            memb_pos = 'OPEN'
        return [memb_act, memb_pos]
    
    def get_remote_status(self):
        ret = self.dio.di_check(11, 1)
        if ret[0] == 0:
            status = 'REMOTE'
        else:
            status = 'LOCAL'
        return status
    
    def error_check(self):
        ret = self.dio.di_check(16, 6)
        if ret[0] == 1:
            self.print_error('controll board sequencer error')
        if ret[1] == 1:
            self.print_error('controll board inverter error')
        if ret[2] == 1:
            self.print_error('controll board thermal error')
        if ret[3] == 1:
            self.print_error('controll board communication error')
        if ret[4] == 1:
            self.print_error('controll board sequencer(of dome_door or membrane) error')
        if ret[5] == 1:
            self.print_error('controll board inverter(of dome_door or membrane) error')
        return
    
    def limit_check(self):
        while True:
            limit1 = self._limit_check()
            time.sleep(0.002)
            limit2 = self._limit_check()
            if limit1 == limit2:
                return limit1
            continue
        pass
        
    def _limit_check(self):
        limit = self.dio.di_check(12, 4)
        ret = 0
        if limit[0:4] == [0,0,0,0]:
            ret = 0
        elif limit[0:4] == [1,0,0,0]:
            ret = 1
        elif limit[0:4] == [0,1,0,0]:
            ret = 2
        elif limit[0:4] == [1,1,0,0]:
            ret = 3
        elif limit[0:4] == [0,0,1,0]:
            ret = 4
        elif limit[0:4] == [1,0,1,0]:
            ret = 5
        elif limit[0:4] == [0,1,1,0]:
            ret = 6
        elif limit[0:4] == [1,1,1,0]:
            ret = 7
        elif limit[0:4] == [0,0,0,1]:
            ret = 8
        elif limit[0:4] == [1,0,0,1]:
            ret = 9
        elif limit[0:4] == [0,1,0,1]:
            ret = 10
        elif limit[0:4] == [1,1,0,1]:
            ret = 11
        elif limit[0:4] == [0,0,1,1]:
            ret = 12
        return ret
    
    def dome_limit(self):
        limit = self.limit_check()
        if limit != 0:
            #self.dome_pos.dio.ctrl.set_counter(self.touchsensor_pos[limit-1]+self.dome_encoffset)
            self.dome_pos.dome_set_counter(self.touchsensor_pos[limit-1]+self.dome_encoffset)
        #print (limit)
        self.get_count()
        #print (self.count)
        return limit
    
    def get_domepos(self):
        self.limit = self.dome_limit()
        self.dome_enc = self.dome_pos.dome_encoder_acq()
        return self.dome_enc
    
    def read_limit(self):
        return self.limit
    
    def start_status_check(self):
        self.stop_status_flag = threading.Event()
        self.status_thread = threading.Thread(target = self.status_check)
        self.status_thread.start()
        return
    
    def status_check(self):
        while not self.stop_status_flag.is_set():
            ret1 = self.get_action()
            ret2 = self.get_door_status()
            ret3 = self.get_memb_status()
            ret4 = self.get_remote_status()
            ret5 = self.get_domepos()
            self.status_box = [ret1, ret2, ret3, ret4]
            time.sleep(0.1)
        return
    
    def stop_status_check(self):
        self.stop_staus_flag.set()
        self.status_thread.join()
        return
    
    def read_count(self):
        return self.count
    
    def read_status(self):
        return self.status_box
    
    def read_domepos(self):
        return self.dome_enc


def dome_client(host, port):
    client = pyinterface.server_client_wrapper.control_client_wrapper(dome_controller, host, port)
    return client

def dome_monitor_client(host, port):
    client = pyinterface.server_client_wrapper.monitor_client_wrapper(dome_controller, host, port)
    return client

def start_dome_server(port1 = 8007, port2 = 8008):
    dome = dome_controller()
    server = pyinterface.server_client_wrapper.server_wrapper(dome,'', port1, port2)
    server.start()
    return server

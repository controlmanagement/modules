
import time
import threading
import pyinterface

class m4_controller(object):
    speed = 3000
    low_speed = 100
    acc = 500
    dec = 500
    
    error = []
    
    position = ''
    count = 0
    
    shutdown_flag = False
    
    def __init__(self, ndev=1):
        self.mtr = pyinterface.create_gpg7204(ndev)
        self.mtr.ctrl.set_limit_config('MTR_LOGIC',0x000c)
        self.mtr.ctrl.off_inter_lock()
        self.get_pos()
        pass
    
    def print_msg(self, msg):
        print(msg)
        return
        
    def print_error(self, msg):
        self.error.append(msg)
        self.print_msg('!!!! ERROR !!!! ' + msg)
        return
    
    def get_count(self):
        self.count = self.mtr.get_position()
        return self.count
    
    def get_pos(self):
        status = self.mtr.ctrl.get_status('MTR_LIMIT_STATUS')
        """
        if status == 0x0008:
            #SMART
            self.position = 'OUT'
        elif status == 0x0004:
            #NAGOYA
            self.position = 'IN'
        elif status == 0x000c:
            self.position = 'MOVE'
        else:
            self.print_error('limit error')
        """
        if status == 0x0004:
            #SMART
            self.position = 'OUT'
        elif status == 0x0008:
            #NAGOYA
            self.position = 'IN'
        elif status == 0x0000:
            self.position = 'MOVE'
        else:
            self.print_error('limit error')
            return
        
        return self.position

    def move(self, dist):
        pos = self.get_pos()
        if dist == pos:
            if dist == 'OUT':
                self.print_msg('m4 is already out')
                return
            elif dist == 'IN':
                self.print_msg('m4 is already in')
                return
            else:
                self.print_msg('m4 is already move')
                return
        #elif pos == 'MOVE':
                #self.print_msg('m4 is already move')
                #return

        else:
            if dist == 'OUT':
                nstep = 60500
                self.print_msg('m4 move out')
            elif dist == 'IN':
                nstep = -60500
                self.print_msg('m4 move in')
            else:
                self.print_error('parameter error')
                return
            self.mtr.move(self.speed, nstep, self.low_speed, self.acc,self.dec)
            time.sleep(12.)
            count = self.get_count()
            pos= self.get_pos()
            return
    
    def m4_out(self):
        self.move('OUT')
        return
    
    def m4_in(self):
        self.move('IN')
        return
    
    def stop(self):
        self.mtr.stop()
        return
    
    def read_pos(self):
        return self.position
    
    def read_count(self):
        return self.count

def m4_client(host,port):
    client = pyinterface.server_client_wrapper.control_client_wrapper(m4_controller, host, port)
    return client

def m4_monitor_client(host,port):
    client = pyinterface.server_client_wrapper.monitor_client_wrapper(m4_controller, host, port)
    return client

def start_m4_server(port1=6003, port2=6004):
    m4 = m4_controller()
    server = pyinterface.server_client_wrapper.server_wrapper(m4,'', port1, port2)
    server.start()
    return server

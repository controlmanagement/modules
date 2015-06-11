import time
import threading
import pyinterface

class slider_controller(object):
    pos_sky = -400
    pos_sig = 25000
    pos_r = 25000
    
    speed = 50000
    low_speed = 5
    acc = 1000
    dec = 1000
    
    error = []
    
    position = ''
    count = 0
    
    cosmos_flag = False
    cosmos_recv = ''
    cosmos_interval = 0.3
    
    shutdown_flag = False
    
    def __init__(self, move_org=True):
        self.mtr = pyinterface.create_gpg7204(1)
        if move_org: self.move_org()
        self.start_cosmos_server()
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
        return
    
    def move_org(self):
        """
        Move to ORG position.
        
        NOTE: This method will be excuted in instantiation.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> s.move_org()
        """
        self.mtr.do_output(3)
        self.mtr.set_org()
        self.position = 'ORG'
        self.get_count()
        return

    def move(self, dist, lock=True):
        pos = self.mtr.get_position()
        if pos == dist: return
        diff = dist - pos
        if lock: self.mtr.move_with_lock(self.speed, diff, self.low_speed,
                                         self.acc, self.dec)
        else: self.mtr.move(self.speed, diff, self.low_speed, self.acc,
                            self.dec)
        
        self.get_count()
        return
    
    def move_r(self, lock=True):
        """
        Move to R position.
        
        NOTE: If the slider is already at R position, it doesn't move.
        
        Args
        ====
        < lock : bool :  > (optional)
            If <lock> is False, the method returns immediately.
            Otherwise, it returns after the slider stopped.
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> s.move_r()
        """
        self.move(self.pos_r, lock)
        self.position = 'R'
        return
    
    def move_sky(self, lock=True):
        """
        Move to SKY position.
        
        NOTE: If the slider is already at SKY position, it doesn't move.
        
        Args
        ====
        < lock : bool :  > (optional)
            If <lock> is False, the method returns immediately.
            Otherwise, it returns after the slider stopped.
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> s.move_sky()
        """
        self.move(self.pos_sky, lock)
        self.position = 'SKY'
        return
    
    def move_sig(self, lock=True):
        """
        Move to SIG position.
        
        NOTE: If the slider is already at SIG position, it doesn't move.
        
        Args
        ====
        < lock : bool :  > (optional)
            If <lock> is False, the method returns immediately.
            Otherwise, it returns after the slider stopped.
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> s.move_sig()
        """
        self.move(self.pos_sig, lock)
        self.position = 'SIG'
        return
    
    def unlock_brake(self):
        """
        Unlock the electromagnetic brake of the slider.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> s.unlock_brake()
        """
        self.mtr.do_output(2, 0)
        msg = '!! Electromagnetic brake is now UNLOCKED !!'
        print('*'*len(msg))
        print(msg)
        print('*'*len(msg))
        return
    
    def lock_brake(self):
        """
        Lock the electromagnetic brake of the slider.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> s.lock_brake()
        """
        self.mtr.do_output(0)
        self.get_count()
        print('')
        print('')
        print('!! CAUTION !!')
        print('-------------')
        print('You must execute s.move_org() method, before executing any "move_**" method.')
        print('')
        return
    
    def clear_alarm(self):
        """
        Clear the alarm.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> s.clear_alarm()
        """
        self.mtr.do_output(1)
        return
        
    def clear_interlock(self):
        """
        Clear the interlock.
        
        Args
        ====
        Nothing.
        
        Returns
        =======
        Nothing.
        
        Examples
        ========
        >>> s.clear_interlock()
        """
        self.mtr.ctrl.off_inter_lock()
        return
    
    def start_cosmos_server(self):
        cs = threading.Thread(target=self._start_cosmos_server)
        cs.start()
        return
    
    def read_position(self):
        return self.position
        
    def read_count(self):
        return self.count
        
    def _start_cosmos_server(self):
        self.print_msg('INFO: start cosmos server')
        
        while True:
            try:
                self._cosmos_server()
            except Exception as e:
                self.print_msg('**********************************************')
                self.print_error('cosmos server except error: %s'%(e))
                self.print_msg('**********************************************')
                self.print_msg('INFO: restart cosmos_server')
                continue
            break
        self.print_msg('INFO: stop cosmos server')
        return

    def _cosmos_server(self):
        while True:
            if self.shutdown_flag:
                self.print_msg('INFO: cosmos: detect shutdown signal')
                self.print_msg('INFO: cosmos: break')
                break
            
            f = open('/mnt/45msmb/mult/mmc.dat', 'r')
            cmd = f.readline()
            f.close()
            
            if cmd[0] == '1':
                pass
            
            elif cmd[0] == '3':
                pass
                
            elif cmd[0] == '2':
                self.cosmos_recv = cmd
                self.print_msg('INFO: cosmos: recv: %s'%(repr(cmd)))
                
                if cmd.find('LDM1') != -1:
                    self.move_r()
                    f = open('/mnt/45msmb/mult/mmc.dat', 'w')
                    f.write('1        \n')
                    f.close()
                
                elif cmd.find('SKYM1') != -1:
                    self.move_sky()
                    f = open('/mnt/45msmb/mult/mmc.dat', 'w')
                    f.write('1        \n')
                    f.close()
                    
                else:
                    pass
                
            else:
                pass
                
            time.sleep(self.cosmos_interval)
            continue
        
    def shutdown(self):
        self.shutdown_flag = True
        return
    
    """
    def _cosmos_server(self):
        server = socket.socket()
        server.settimeout(1)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.print_msg('INFO: cosmos: (bind) %s:%s'%('', cosmos_server_port))
        server.bind(('', cosmos_server_port))
        server.listen(1)
        
        while True:
            self.cosmos_flag = False
            
            try:
                client, client_address = server.accept()
                self.print_msg('INFO: cosmos: Accept from %s'%(str(client_address)))
                client.settimeout(1)
            
            except socket.timeout:
                if self.shutdown_flag:
                    self.print_msg('INFO: cosmos: detect shutdown signal')
                    self.print_msg('INFO: cosmos: break')
                    break
                continue
            
            self.cosmos_flag = True

            while True:
                if self.shutdown_flag: 
                    self.print_msg('INFO: cosmos: detect shutdown signal')
                    self.print_msg('INFO: cosmos: break')
                    break
                
                try:
                    ret = client.recv(24)
                except socket.timeout:
                    continue
                except socket.error, e:
                    self.print_error('cosmos: %s'%str((e.errno, e.message, e.strerror)))
                    self.print_msg('INFO: cosmos: connection break')
                    break
                
                #print('RECV: %s'%(repr(ret)))
                self.cosmos_recv = ret
                if ret == '': 
                    self.print_msg('INFO: cosmos: connection break')
                    break
                
                ret = ret.strip('\0').split('\t')
                operate = int(ret[0])
                return_flag = int(ret[1])
                timestamp = ret[2]
                target = float(ret[3])
                self.cosmos_angle = target
                
                if self.tracking_count > 4: is_tracking = 1
                else: is_tracking = 0
                
                msg = '[%s] op=%s ret=%s t=%s prog=%s '%(time.strftime('%Y/%m/%d %H:%M:%S'),
                                                         ret[0], ret[1], ret[2], ret[3])
                msg += 'real=%+06.1f diff=%.1f vel=%+06.1f track=%d'%(self.real_angle,
                                                                      self.residual,
                                                                      self.real_vel,
                                                                      self.tracking_count)
                self.print_msg(msg)
                
                if operate == 1: 
                    self.move(target)
                    pass
                
                if return_flag == 1:
                    err_no = 0
                    err_msg = ''
                    msg = '%d\t%s\t%+06.1f\t%02d\t%50s\0'%(is_tracking, self.real_timestamp,
                                                           self.real_angle, err_no, err_msg)
                    #print('SEND: %s'%(repr(msg)))
                    self.cosmos_send = msg
                    client.send(msg)
                    pass
                continue
            continue
        return
    """

def slider():
    client = pyinterface.server_client_wrapper.control_client_wrapper(
        slider_controller, '192.168.40.13', 4004)
    return client

def slider_monitor():
    client = pyinterface.server_client_wrapper.monitor_client_wrapper(
        slider_controller, '192.168.40.13', 4104)
    return client

def start_slider_server():
    slider = slider_controller()
    server = pyinterface.server_client_wrapper.server_wrapper(slider,
                                                              '', 4004, 4104)
    server.start()
    return server


Enter file contents here

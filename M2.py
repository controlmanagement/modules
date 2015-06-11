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


import time
import threading
import pyinterface

class mirror_controller(object):
    pos_nagoya = 
    
    pos_smart = 
        
    speed = 
    low_speed = 
    acc = 
    dec = 
    
    error = []
    
    position = ''
    count = 0
    
    
    def __init__(self, move_org=True):
        self.mtr = pyinterface.create_gpg7204(1)
        if move_org: self.move_org()
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
        self.mtr.do_output()
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
    
    def move_nagoya(self, lock=True):
        """
        Move to NAGOYA position.
        
        NOTE: If the slider is already at NAGOYA position, it doesn't move.
        
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
        >>> s.move_n()
        """
        self.move(self.pos_nagoya, lock)
        self.position = 'NAGOYA'
        return
    
    def move_smart(self, lock=True):
        """
        Move to SMART position.
        
        NOTE: If the slider is already at SMART position, it doesn't move.
        
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
        >>> s.move_smart()
        """
        self.move(self.pos_smart, lock)
        self.position = 'SMART'
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
        self.mtr.do_output( , )
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
        self.mtr.do_output()
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
        self.mtr.do_output()
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
        
    def read_position(self):
        return self.position
        
    def read_count(self):
        return self.count
    
    
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


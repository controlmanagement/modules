import time
import pyinterface
import threading



class m2_controller(object):
    #reference  /src/obs/modules/hal/subref.cpp
    #micron is controlled by time
    
    error = []
    m_pos = 0.0
    CW = 0x10
    CCW = 0x11
    LIMIT_CW = 1000
    LIMIT_CCW = -1000
    PULSRATE = 80 #1puls = 0.1micron
    MOTOR_SPEED = 200 # * 10pulses/sec
    m_limit_up = 1
    m_limit_down = 1
    
    
    
    
    def __init__(self):
        pass
    
    def open(self, ndev = 1)
        self.dio = pyinterface.create_gpg2000(ndev)
        self.InitIndexFF()
        self.get_pos()
        pass
    
    def print_msg(self, msg):
        print(msg)
        return
    
    def print_error(self, msg):
        self.error.append(msg)
        self.print_msg('!!!! ERROR !!!! ' + msg)
        return
    
    def get_pos(self):
        buff = []
        buff2 = []
        
        bin  = self.dio.ctrl.in_byte("FBIDIO_IN1_8")
        bin2 = self.dio.ctrl.in_byte("FBIDIO_IN9_16")
        
        if bin2 & 0x40:
            self.m_limit_up = 1
        else:
            self.m_limit_up = 0
        if bin2 & 0x80:
            self.m_limit_down = 1
        else:
            self.m_limit_down = 0
        
        for i in range(8):
            if i != 0 and bin == 0:
                buff.append(0)
            if bin % 2 == 0:
                buff.append(0)
            else:
                buff.append(1)
            bin = int(bin/2)
        
        for i in range(8):
            if i != 0 and bin2 == 0:
                buff2.append(0)
            if bin2 % 2 == 0:
                buff2.append(0)
            else:
                buff2.append(1)
            bin2 = int(bin2/2)
        
        #calculate each digit
        total = (buff[0]*1+buff[1]*2+buff[2]*pow(2.,2.)+buff[3]*pow(2.,3.))/100.0
        total = total + (buff[4]*1+buff[5]*2+buff[6]*pow(2.,2.)+buff[7]*pow2.,3.)/10.0
        total2 = buff2[0]*1+buff2[1]*2+buff2[2]*pow(2.,2.)+buff2[3]*pow(2.,3.)
        total2 = total2 + (buff2[4]*1)*10
        
        self.m_pos = (total+total2)*pow(-1.,(buff2[5]+1))
        
        return self.m_pos
    
    def read_pos(self):
        return self.m_pos
    
    def Strobe(self):
        time.sleep(0.001)
        self.dio.ctrl.out_byte("FBIDIO_OUT9_16", 0x01)
        time.sleep(0.001)
        self.dio.ctrl.out_byte("FBIDIO_OUT9_16", 0x00)
        time.sleep(0.001)
        return
    
    def Strobe_HOFF(self):
        time.sleep(0.001)
        self.dio.ctrl.out_byte("FBIDIO_OUT9_16", 0x05)
        time.sleep(0.001)
        self.dio.ctrl.out_byte("FBIDIO_OUT9_16", 0x04)
        time.sleep(0.001)
        return
    
    def move(self, dist):
        #move subref
        puls = int(dist) * PULSLRTE
        
        if self.m_limit_up == 0 and puls < 0:
            self.print_error("can't move up direction")
            return
        if self.m_limit_down == 0 and puls > 0:
            self.print_error("can't move down direction")
            return
        
        self.MoveIndexFF(puls)
        return
    
    
    
    def InitIndexFF(void):
        #initialization?
        
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0x08)
        self.StrobeHOff()
        #step no.
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0xff)
        self.StrobeHOff()
        #vs set
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0x48)
        self.StrobeHOff()
        #5(*10=50)
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0x00)
        self.StrobeHOff()
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0x05)
        self.StrobeHOff()
        #vr set
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0x40)
        self.StrobeHOff()
        
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0x00)
        self.StrobeHOff()
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", self.MOTOR_SPEED)
        self.StrobeHOff()
        #su-sd set
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0x50)
        self.StrobeHOff()
        #100(/10=10)
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0x00)
        self.StrobeHOff()
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 100)
        self.StrobeHOff()
        #position set
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0xc0)
        self.StrobeHOff()
        #cw
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", self.CW)
        self.StrobeHOff()
        #0
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0x00)
        self.StrobeHOff()
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0x00)
        self.StrobeHOff()
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0x00)
        self.StrobeHOff()
        #start
        self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0x18)
        self.StrobeHOff()
        return
    
    def MoveIndexFF(self, puls):
        if puls >= -65535 and puls <= 65535):
            #index mode
            self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0x08)
            self.Strobe()
            #step no.
            self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0xff)
            self.Strobe()
            #position set
            self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0xc0)
            self.Strobe()
            #direction
            if puls >= 0:
                self.dio.ctrl.out_byte("FBIDIO_OUT1_8", self.CW)
                self.Strobe()
            else:
                self.dio.ctrl.out_byte("FBIDIO_OUT1_8", self.CCW)
                self.Strobe()
            #displacement
            self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0x00)
            self.Strobe()
            self.dio.ctrl.out_byte("FBIDIO_OUT1_8", (abs(puls) / 256))
            self.Strobe()
            self.dio.ctrl.out_byte("FBIDIO_OUT1_8", (abs(puls) % 256))
            self.Strobe()
            #start
            self.dio.ctrl.out_byte("FBIDIO_OUT1_8", 0x18)
            self.Strobe()
            sleep((abs(puls) / self.MOTOR_SPEED / 10.) + 1.)
            self.print_msg("Motor stopped")
        else:
            self.print_msg("Puls number is over.")
            return false
        return true






def m2_client(host, port):
    client = pyinterface.server_client_wrapper.control_client_wrapper(m2_controller, host, port)
    return client

def m2_monitor_client(host, port):
    client = pyinterface.server_client_wrapper.monitor_client_wrapper(m2controller, host, port)
    return client

def start_m2_server(port1 = ctrl?, port2 = ctrl?):
    m2 = m2_controller()
    server = pyinterface.server_client_wrapper.server_wrapper(m2,'', port1, port2)
    server.start()
    return server

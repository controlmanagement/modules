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
        InitIndexFF()
        get_pos()
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
        
        bin  = dio.???.inb()
        bin2 = dio.???.inb(+1)
        
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
        
        m_pos = (total+total2)*pow(-1.,(buff2[5]+1))
        
        return m_pos
    
    def read_pos(self):
        return m_pos
    
    def Strobe(self):
        time.sleep(0.001)
        dio.???.outb(0x01, PCI2724_PORT + 1)
        time.sleep(0.001)
        dio.???.outb(0x00, PCI2724_PORT + 1)
        time.sleep(0.001)
        return
    
    def Strobe_HOFF(self):
        time.sleep(0.001)
        dio.???.outb(0x05, PCI2724_PORT + 1)
        time.sleep(0.001)
        dio.???.outb(0x04, PCI2724_PORT + 1)
        time.sleep(0.001)
        return
    
    def move(self, dist):
        #move subref
        puls = int(dist) * PULSLRTE
        
        if self.m_limit_up == 0 and puls < 0:
            print_error("can't move up direction")
            return
        if self.m_limit_down == 0 and puls > 0:
            print_error("can't move down direction")
            return
        
        MoveIndexFF(puls)
        return
    
    
    
    def InitIndexFF(void):
        #initialization?
        
        dio.???.outb(0x08, PCI2724_PORT)
        StrobeHOff()
        #step no.
        dio.???.outb(0xff, PCI2724_PORT)
        StrobeHOff()
        #vs set
        dio.???.outb(0x48, PCI2724_PORT)
        StrobeHOff()
        #5(*10=50)
        dio.???.outb(0, PCI2724_PORT)
        StrobeHOff()
        dio.???.outb(5, PCI2724_PORT)
        StrobeHOff()
        #vr set
        dio.???.outb(0x40, PCI2724_PORT)
        StrobeHOff()
        
        dio.???.outb(0, PCI2724_PORT)
        StrobeHOff()
        dio.???.outb(MOTOR_SPEED, PCI2724_PORT)
        StrobeHOff()
        #su-sd set
        dio.???.outb(0x50, PCI2724_PORT)
        StrobeHOff()
        #100(/10=10)
        dio.???.outb(0, PCI2724_PORT)
        StrobeHOff()
        dio.???.outb(100, PCI2724_PORT)
        StrobeHOff()
        #position set
        dio.???.outb(0xc0, PCI2724_PORT)
        StrobeHOff()
        #cw
        dio.???.outb(CW, PCI2724_PORT)
        StrobeHOff()
        #0
        dio.???.outb(0, PCI2724_PORT)
        StrobeHOff()
        dio.???.outb(0, PCI2724_PORT)
        StrobeHOff()
        dio.???.outb(0, PCI2724_PORT)
        StrobeHOff()
        #start
        dio.???.outb(0x18, PCI2724_PORT)
        StrobeHOff()
        return
    
    def MoveIndexFF(self, puls):
        if puls >= -65535 and puls <= 65535):
            #index mode
            dio.???.outb(0x08, PCI2724_PORT)
            Strobe()
            #step no.
            dio.???.outb(0xff, PCI2724_PORT)
            Strobe()
            #position set
            dio.???.outb(0xc0, PCI2724_PORT)
            Strobe()
            #direction
            if puls >= 0:
                dio.???.outb(CW, PCI2724_PORT)
                Strobe()
            else:
                dio.???.outb(CCW, PCI2724_PORT)
                Strobe()
            #displacement
            dio.???.outb(0, PCI2724_PORT)
            Strobe()
            dio.???.outb((abs(puls) / 256), PCI2724_PORT)
            Strobe()
            dio.???.outb((abs(puls) % 256), PCI2724_PORT)
            Strobe()
            #start
            dio.???.outb(0x18, PCI2724_PORT)
            Strobe()
            sleep((abs(puls) / MOTOR_SPEED / 10.) + 1.)
            print_msg("Motor stopped")
        else:
            print_msg("Puls number is over.")
            return false
        return true






def m2_client(host, port):
    client = pyinterface.server_client_wrapper.control_client_wrapper(m2_controller, host, port)
    return client

def m2_monitor_client(host, port):
    client = pyinterface.server_client_wrapper.monitor_client_wrapper(m2controller, host, port)
    return client

def start_m2_server(port1 = ????, port2 = ????):
    m2 = m2_controller()
    server = pyinterface.server_client_wrapper.server_wrapper(m2,'', port1, port2)
    server.start()
    return server

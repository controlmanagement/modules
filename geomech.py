import ctypes
import pyinterface
import numpy as np



class geomech_controller(object):
    GAIN_X1 = 0.4556
    GAIN_Y1 = 0.4875
    GAIN_X2 = 0.4556
    GAIN_Y2 = 0.4875
    GAIN_T_X1 = 0.5
    GAIN_T_Y1 = 2
    GAIN_T_X2 = -0.5
    GAIN_T_Y2 = 0.5
    URAD2ARCSEC = 0.206264
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    t1 = 0
    t2 = 0
    geo_x = 0
    geo_y = 0
    x1_arr = []
    y1_arr = []
    x2_arr = []
    y2_arr = []
    
    def __init__(self):
        self.open()
        pass
    
    def open(self, ndev = 1):
        self.dio = pyinterface.create_gpg3100(ndev)
    
    def start_server(self):
        ret = self.start_geomech_server()
        return
    
    def get_geomech(self):
        chs = []
        for i in range(10):
            chs.append(i)
        ranges = ["AD_10V"]*10
        AdVoltage = [0]*10
        
        # int ret=AdInputAD(m_dnum,10,AD_INPUT_SINGLE,&m_Conf[0],AdData);
        # m_dum = 1(device_number), 10(ulCh),   m_conf[0]
        
        AdData = self.dio.ctrl.input_ad(chs, ranges)
        for i in range(10):
            AdVoltage[i] = (AdData[i]-32768.)/3276.8
        
        x1 = (AdVoltage[0]-AdVoltage[1])*1000*self.GAIN_X1*self.URAD2ARCSEC
        y1 = (AdVoltage[2]-AdVoltage[3])*1000*self.GAIN_Y1*self.URAD2ARCSEC
        t1 = (AdVoltage[4]*100)
        x2 = (AdVoltage[5]-AdVoltage[6])*1000*self.GAIN_X2*self.URAD2ARCSEC
        y2 = (AdVoltage[7]-AdVoltage[8])*1000*self.GAIN_Y2*self.URAD2ARCSEC
        t2 = (AdVoltage[9]*100)
        
        self.t1 = t1
        self.t2 = t2
        
        # thermal correction
        t_x1 = x1-self.GAIN_T_X1*t1
        t_y1 = y1-self.GAIN_T_Y1*t1
        t_x2 = x2-self.GAIN_T_X2*t2
        t_y2 = y2-self.GAIN_T_Y2*t2
        
        if abs(self.x1 - t_x1) > 150.:
            pass
        else:
            self.x1 = t_x1
        if abs(self.x2 - t_x2) > 150.:
            pass
        else:
            self.x2 = t_x2
        if abs(self.y1 - t_y1) > 150.:
            pass
        else:
            self.y1 = t_y1
        if abs(self.y2 - t_y2) > 150.:
            pass
        else:
            self.y2 = t_y2
        
        self.x1_arr.append(self.x1)
        if len(self.x1_arr) > 3:
            self.x1_arr.pop(0)
        self.x1 = np.median(self.x1_arr)
        
        self.x2_arr.append(self.x2)
        if len(self.x2_arr) > 3:
            self.x2_arr.pop(0)
        self.x2 = np.median(self.x2_arr)
        
        self.y1_arr.append(self.y1)
        if len(self.y1_arr) > 3:
            self.y1_arr.pop(0)
        self.y1 = np.median(self.y1_arr)
        
        self.y2_arr.append(self.y2)
        if len(self.y2_arr) > 3:
            self.y2_arr.pop(0)
        self.y2 = np.median(self.y2_arr)
        return [self.x1, self.x2, self.y1, self.y2]
    
    def get_geomech_col(self):
        X = Y = X2 = Y2 = [0]*10
        X_ave = Y_ave = X_ave2 = Y_ave2 = 0
        """
        x1 = ret[0]
        x2 = ret[1]
        y1 = ret[2]
        y2 = ret[3]
        """
        
        for i in range(10):
            ret = self.get_geomech()
            X[i] = (ret[0]-ret[1])/2.0
            Y[i] = (ret[2]-ret[3])/2.0
            X_ave += X[i]
            Y_ave += Y[i]
        
        for i in range(10):
            X2[i] = X[i]-(X[i]-Y[i])+(X_ave-Y_ave)
            Y2[i] = Y[i]-(X[i]-Y[i])+(X_ave-Y_ave)
            X_ave2 += X2[i]
            Y_ave2 += Y2[i]
        
        self.geo_x = X_ave2/10
        self.geo_y = Y_ave2/10
        return [self.geo_x, self.geo_y]
        
    def read_geomech(self):
        return [self.x1, self.y1, self.x2, self.y2]

    def read_geomech_col(self):
        return [self.geo_x, self.geo_y]

    def read_geomech_temp(self):
        return [self.t1, self.t2]



def geomech_client(host, port):
    client = pyinterface.server_client_wrapper.control_client_wrapper(geomech_controller, host, port)
    return client

def geomech_monitor_client(host, port):
    client = pyinterface.server_client_wrapper.monitor_client_wrapper(geomech_controller, host, port)
    return client

def start_geomech_server(port1 = 8100, port2 = 8101):
    geomech = geomech_controller()
    server = pyinterface.server_client_wrapper.server_wrapper(geomech, '', port1, port2)
    server.start()
    return server


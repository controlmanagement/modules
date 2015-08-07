
""" -- comment --
:: 1p85_server python client ::

motor.py

[original-comment]
2010/11/02 2010ver created nishimura

This client source is written by Takenaka.
latest_ver:December 26th 2009.

"""

# ------ settings ------

COORD_J2000      = 1
COORD_B1950      = 2
COORD_LB         = 3
COORD_APP        = 10
COORD_HORIZONTAL = 100
COORD_SAME       = 0


REPLY_FLOAT  = 'motor:REPLY_DATA_FLOAT'
REPLY_STR    = 'motor:REPLY_DATA_STR'


# ------ start source code ------

import math, time
import client

HOST = '192.168.100.11'
PORT = 12122


class motor_client(client.Client):
    """motor Client module (1p85server python client)"""
    J2000      = COORD_J2000
    B1950      = COORD_B1950
    LB         = COORD_LB
    APP        = COORD_APP
    HORIZONTAL = COORD_HORIZONTAL
    SAME       = COORD_SAME
    
    def __init__(self, host=HOST, port=PORT, print_socket=True):
        """initialize"""
        # Common Settings
        client.Client.__init__(self, print_socket=print_socket)
        self._set_reply_handler(self.__reply_handler)
        self._init_socket(host, port)
        
        # motor Settings
        self.J2000=1
        self.B1950=2
        self.LB=3
        self.APP=10
        self.SAME=0
        self.__float_data = 0.0
        self.__str_data = ""
        return

    def help(self):
        self._print_common_help()
        print(HELP_STR)
        return
    
    def __reply_handler(self, reply):
        if   reply==REPLY_FLOAT:  self.__reply_float(reply)
        elif reply==REPLY_STR:    self.__reply_str(reply)
        else: self.__reply_else(reply)
        return
    
    def __reply_else(self, reply):
        if self.print_socket==True: print(reply)
        return
    
    def __reply_float(self, reply):
        self.__float_data = map(float, self._socket.read_reply_line().split())
        return
    
    def __reply_str(self, reply):
        self.__str_data = self._socket.read_reply_line()
        return

    def __get_server_params(self, mode):
        self._send_command('1.85m:get_'+mode)
        self._read_reply_loop()
        return self.__float_data
 
    def __get_server_mode(self, mode):
        self._send_command('1.85m:get_'+mode)
        self._read_reply_loop()
        return self.__str_data
   
    def get_target_azel(self):
        """  """
        return self.__get_server_params('target_azel')
    
    def get_hensa(self):
        """ """
        return self.__get_server_params('hensa')
    
    def get_angle(self):
        """ """
        return self.__get_server_params('angle_azel')
    
    def get_speed(self):
        """ """
        return self.__get_server_params('speed')
    
    def get_inst_speed(self):
        """  """
        return self.__get_server_params('inst_speed')
    
    def get_target_speed(self):
        """ """
        return self.__get_server_params('target_speed')
    
    def get_current_vobs(self):
        """ """
        return self.__get_server_params('currend_vobs')[0]

    def get_vobs(self, mjd, x, y, coord, offx, offy, dcos, offmode):
        """
        """
        r = math.radians
        self._send_command('1.85m:get_vobs',
                           '%.7f %.7f %.7f %d %.7f %.7f %d %d'
                           %(mjd, r(x), r(y), coord, r(offx), r(offy), dcos, offmode))
        self._read_reply_loop()
        return self.__float_data[0] # + 30 ### debug ###
    
    def get_max_rpm(self):
        """ """
        return self.__get_server_params('max_motor_rpm')
    
    def get_azel(self):
        """ """
        return self.__get_server_params('azel')
    
    def get_obs_mode(self):
        """ """
        return self.__get_server_mode('obs_mode')
    
    def get_coord_mode(self):
        """ """
        return self.__get_server_mode('coord_mode')

    def get_offset_mode(self):
        """ """
        return self.__get_server_mode('offset_mode')

    def get_is_planet(self):
        """ """
        return self.__get_server_mode('is_planet')

    def get_planet_number(self):
        num = int(self.__get_server_mode('planet_number'))
        if   num==1:  return 'mercury'
        elif num==2:  return 'venus'
        elif num==3:  return 'earth'
        elif num==4:  return 'mars'
        elif num==5:  return 'jupiter'
        elif num==6:  return 'saturn'
        elif num==7:  return 'uranus'
        elif num==8:  return 'neptune'
        elif num==9:  return 'pluto'
        elif num==10: return 'moon'
        elif num==11: return 'sun'
        else:         return 'unknown'

    def get_coord_planet(self):
        """ """
        return self.__get_server_params('get_coord_planet')

    def get_is_opt(self):
        """ """
        return self.__get_server_mode('is_opt')

    def get_mjd(self):
        """ """
        return 40587 + time.time()/(24.*3600.)

    def get_lst(self):
        """
        """
        pi = math.pi
        sin = math.sin
        cos = math.cos
        
        mjd = self.get_mjd()
        jd = mjd+2400000.5
        tu = (jd - 2451545.) / 36525.
        
        am = 18.*3600.+41.*60.+50.54841+8640184.812866*tu +0.093104*tu*tu-0.0000062*tu*tu*tu
        gmst = (jd - 0.5 - long(jd - 0.5)) * 24. * 3600. + am - 12.*3600.

        l = 280.4664*3600. + 129602771.36*tu  - 1.093*tu*tu
        l = l * (pi/(180.*3600.))
        p = (282.937+1.720*tu)*3600.
        p = p * (pi/(180.*3600.))

        w = (125.045 - 1934.136*tu + 0.002*tu*tu)*3600.
        w = w * (pi/(180.*3600.))
        ll = (218.317+481267.881*tu-0.001*tu*tu)*3600.
        ll = ll*(pi/(180.*3600.))
        pp = (83.353+4069.014*tu-0.010*tu*tu)*3600.
        pp = pp*(pi/(180.*3600.))

        dpsi = (-17.1996-0.01742*tu)*sin(w) + (-1.3187)*sin(2*l)+0.2062*sin(2*w) +0.1426*sin(l-p)-0.0517*sin(3*l-p)+0.0217*sin(l+p)+0.0129*sin(2*l-w)-0.2274*sin(2*ll)+0.0712*sin(ll-pp)-0.0386*sin(2*ll-w)-0.0301*sin(3*ll-pp)-0.0158*sin(-ll+3*l-pp)+0.0123*sin(ll+pp)

        e = (23.439291 - 0.013004*tu)*3600.
        e = e  * (pi/(180.*60.*60.))
        dpsicose = dpsi * cos(e)
        lst = gmst + (dpsicose + ((138.472153)*3600.)) / 15.
        
        return lst

    def kisa(self):
        """
        """
        self._send_command('1.85m:kisa')
        self._read_reply_loop()
        return
    
    def wait_track(self, acc=10):
        """
        """
        while True:
            time.sleep(0.1)
            hx, hy = self.get_hensa()
            if abs(hx) <= acc/3600. and abs(hy) <= acc/3600.: break
            continue
        return

    def wait_stop(self, acc=1):
        """
        """
        while True:
            time.sleep(0.1)
            hx, hy = self.get_hensa()
            sx, sy = self.get_speed()
            if abs(hx) <= acc/3600. and abs(hy) <= acc/3600. and abs(sx) <= 1/3600. and abs(sy) <= 1/3600.: break
            continue
        return
    
    def go_azel(self, az, el):
        """
        """
        self._send_command('1.85m:horizontal', '%lf %lf'%(math.radians(az), math.radians(el)))
        self._read_reply_loop()
        return
    
    def move_azel(self, az, el, acc=1):
        """
        """
        self.go_azel(az, el)
        time.sleep(0.1)
        try:
            self.wait_stop(acc)
        except KeyboardInterrupt:
            self.stop_tracking()
        return
    
    def start_tracking(self):
        """
        """
        self._send_command('1.85m:coord_tracking')
        self._read_reply_loop()
        return
    
    def set_coord_planet(self, no):
        """
        mercury=1,venus=2,mars=4,jupiter=5,saturn=6
        uranus=7,neptune=8,pluto=9,moon=10,sun=11
        """
        self._send_command('1.85m:coord_planet', '%d'%(no))
        self._read_reply_loop()
        return
     
    def set_coord_planet_c(self, no):
        """
        mercury=1,venus=2,mars=4,jupiter=5,saturn=6
        uranus=7,neptune=8,pluto=9,moon=10,sun=11
        """
        self._send_command('1.85m:coord_planet_c', '%d'%(no))
        self._read_reply_loop()
        return
   
    def calc_coord_planet(self, no):
        """
        """
        self._send_command('1.85m:calc_coord_planet')
        self._read_reply_loop()
        return
    
    def go_planet(self, planet_number):
        """
        mercury=1,venus=2,mars=4,jupiter=5,saturn=6
        uranus=7,neptune=8,pluto=9,moon=10,sun=11
        """
        self.set_coord_planet(planet_number)
        self.start_tracking()
        return
    
    def move_planet(self, planet_number, acc=10):
        """
        mercury=1,venus=2,mars=4,jupiter=5,saturn=6
        uranus=7,neptune=8,pluto=9,moon=10,sun=11
        """
        self.go_planet(planet_number)
        self.wait_track(acc)
        return

    def set_coord_source(self, x, y, coord_sys=1):
        """
        (x, y) in degrees
        coord_sys: 1:J2000, 2:B1950, 3:LB, 10:Apparent
        """
        self._send_command('1.85m:coord','%d %.7f %.7f'%(coord_sys, math.radians(x), math.radians(y)))
        self._read_reply_loop()
        return

    def set_propermotion(self, px, py):
        """
        (px, py) in degrees (per Julian year)
        px is in RA/dt not in cos(Dec)*dRA/dt
       """
        self._send_command('1.85m:propermotion','%.7f %.7f'%(math.radians(px), math.radians(py)))
        self._read_reply_loop()
        return

    def set_radio(self):
        """
        """
        self._send_command('1.85m:coord_radio')
        self._read_reply_loop()
        return

    def set_opt(self):
        """
        """
        self._send_command('1.85m:coord_opt')
        self._read_reply_loop()
        return

    def set_offset(self, x, y, dcos=1, coord_sys=1):
        """
        (x, y) in degrees
        coord_sys: 1:J2000, 2:B1950, 3:LB, 0: Same as source 10:Apparent
        """
        self._send_command('1.85m:offset','%d %.7f %.7f %d'%(coord_sys, math.radians(x), math.radians(y), dcos))
        self._read_reply_loop()
        return

    def set_offset_horizontal(self, x, y, dcos=1):
        """
        (x, y) in degrees
        """
        self._send_command('1.85m:offset_horizontal','%.7f %.7f %d'%(math.radians(x), math.radians(y), dcos))
        self._read_reply_loop()
        return
    
    def go_radio(self, x, y, coord_sys=1):
        """
        """
        self.set_radio()
        self.set_coord_source(x, y, coord_sys)
        self.start_tracking()
        return
    
    def go_opt(self, x, y, px, py, coord_sys=1):
        """
        """
        self.set_opt()
        self.set_coord_source(x, y, coord_sys)
        self.set_propermotion(px/math.cos(math.radians(y)), py)
        self.start_tracking()
        return

    def move_radio(self, x, y, coord_sys=1, acc=10):
        """
        """
        print(x,y,coord_sys)
        self.go_radio(x, y, coord_sys)
        try:
            self.wait_track(acc)
        except:
            self.stop_tracking()
            pass
        return
    
    def move_opt(self, x, y, px, py, coord_sys=1, acc=10):
        """
        """
        self.go_opt(x, y, px, py, coord_sys)
        try:
            self.wait_track(acc)
        except:
            self.stop_tracking()
            pass
        return
    
    def set_max_rpm(self, x, y):
        """
        """
        self._send_command('1.85m:max_motor_rpm', '%.f %.f'%(x, y))
        self._read_reply_loop()
        return

    def set_humidity(self, v):
        """
        """
        if v>0.99: v = 0.99
        self._send_command('1.85m:humidity', '%.f'%(v))
        self._read_reply_loop()
        return

    def set_pressure(self, v):
        """
        """
        self._send_command('1.85m:pressure', '%.f'%(v))
        self._read_reply_loop()
        return

    def set_temperature(self, v):
        """
        """
        self._send_command('1.85m:temperature', '%.f'%(v))
        self._read_reply_loop()
        return

    def set_lambda(self, v):
        """
        """
        self._send_command('1.85m:lambda', '%.f'%(v))
        self._read_reply_loop()
        return

    def otf(self, start_time, sx, sy, end_time, ex, ey, dcos, coord_sys):
        """
        """
        r = math.radians
        self._send_command('1.85m:coord_otf',
                           '%f %f %f %f %f %f %d %d'
                           %(start_time, r(sx), r(sy), end_time, r(ex), r(ey), dcos, coord_sys))
        self._read_reply_loop()
        return
    
    def otf_horizontal(self, start_time, sx, sy, end_time, ex, ey, dcos=1):
        """
        """
        r = math.radians
        self._send_command('1.85m:coord_otf_horizontal',
                           '%f %f %f %f %f %f %d'
                           %(start_time, r(sx), r(sy), end_time, r(ex), r(ey), dcos))
        self._read_reply_loop()
        return

    def otf_ramp(self, sx, sy, dcos, coord_sys, dx, dy, dt, n, rampt, delay):
        """
        """
        ssx = sx - float(dx)/2. - float(dx)/float(dt) * rampt
        ssy = sy - float(dy)/2. - float(dy)/float(dt) * rampt
        total_t = rampt + dt * n
        eex = sx + dx * (n - 0.5)
        eey = sy + dy * (n - 0.5)
        self.set_offset(ssx, ssy, dcos, coord_sys)
        self.wait_track()
        mjd = self.get_mjd()
        self.otf(mjd+delay/24./3600., ssx, ssy, mjd+(delay+total_t)/24./3600., eex, eey, dcos, coord_sys)
        print mjd+delay/24./3600.
        return mjd + (delay+rampt) /24. /3600.
      
    def otf_horizontal_ramp(self, sx, sy, dcos, dx, dy, dt, n, rampt, delay):
        """
        """
        ssx = sx - float(dx)/2. - float(dx)/float(dt) * rampt
        ssy = sy - float(dy)/2. - float(dy)/float(dt) * rampt
        total_t = rampt + dt * n
        eex = sx + dx * (n - 0.5)
        eey = sy + dy * (n - 0.5)
        self.set_offset_horizontal(ssx, ssy, dcos)
        self.wait_track()
        mjd = self.get_mjd()
        self.otf_horizontal(mjd+delay/24./3600., ssx, ssy, mjd+(delay+total_t)/24./3600., eex, eey, dcos)
        return mjd+(delay+rampt)/24./3600.

    def stop_tracking(self):
        """
        """
        self._send_command('1.85m:stop_tracking')
        self._read_reply_loop()
        return
   


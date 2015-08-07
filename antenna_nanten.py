#! /usr/bin/env python2.6
#-*- coding: utf-8 -*-

"""
モーターの制御を行う

================================================
Radio Telescope Observing System
------------------------------------------------
[Abstract]

file-name: antenna_1p85.py

role: モーターの制御を行う

main-author: Akihito Minami

path: /home/1.85m/soft/obs/telescope_1p85/antenna_1p85.py

------------------------------------------------
[Detail Description]

・構成

　公開しているクラス
　（１）antenna_1p85：モーターの制御を行う

------------------------------------------------
[History]

2011/11/16 minami ver.1

------------------------------------------------
"""

import telescope_1p85.motor
import core.file_manager
import core.controller

class antenna_1p85(core.controller.antenna):
    """モーターの制御を行う"""
    coord_dict = {"J2000"     : telescope_1p85.motor.COORD_J2000,
                  "B1950"     : telescope_1p85.motor.COORD_B1950,
                  "LB"        : telescope_1p85.motor.COORD_LB,
                  "GALACTIC"  : telescope_1p85.motor.COORD_LB,
                  "APPARENT"  : telescope_1p85.motor.COORD_APP,
                  "HORIZONTAL": telescope_1p85.motor.COORD_HORIZONTAL,
                  "SAME"      : telescope_1p85.motor.COORD_SAME}

    def __init__(self):
 
        self.m = telescope_1p85.motor.motor_client(print_socket=False)
        self.m.open()
        self.dev = core.file_manager.dev_manager()
        return

    def use_radio(self):
        """機差の補正、観測する周波数のセッティング(電波観測)"""
        self.m.kisa()
        self.m.set_radio()
        self.m.set_lambda(float(self.dev["LIGHT_SPEED"]) / float(self.dev['1stLO1'])*1000.)
        return


    def use_opt(self):
        """機差の補正、観測する周波数のセッティング(可視光観測)"""
        self.m.kisa()
        self.m.set_opt()
        return
    

    def set_condition(self, pressure, humidity, temperature_C):
        """気圧、気温、湿度による大気屈折率の補正"""
        self.m.set_pressure(pressure)
        self.m.set_humidity(humidity)
        self.m.set_temperature(temperature_C)
        return


    def move(self, x, y, coord, offset_x, offset_y, offset_dcos, offset_coord, planet):
        """offset値をセッティングし、指定したターゲットにアンテナを向ける(電波観測)"""
        if offset_coord == "HORIZONTAL":
            self.m.set_offset(0, 0, 1, self.coord_dict["SAME"])
            self.m.set_offset_horizontal(offset_x, offset_y,  offset_dcos)
        else:
            self.m.set_offset_horizontal(0, 0, 1)
            self.m.set_offset(offset_x, offset_y, offset_dcos, self.coord_dict[offset_coord.upper()])
            pass
        if planet == None:
            if coord.upper()=='HORIZONTAL':
                self.m.move_azel(x, y)
            else:
                self.m.move_radio(x, y, self.coord_dict[coord.upper()])
                pass
            pass
        else:
            self.m.move_planet(planet)
            pass
        return
    
    
    def move_opt(self, x, y, px, py, coord, acc):
        """指定したターゲットにアンテナを向ける(可視光観測)"""
        self.m.move_opt(x, y, px, py, self.coord_dict[coord.upper()], acc)
        return


    def scan(self, sx, sy, coord, scan_dcos, dx, dy, dt, n, ramp, delay):
        """スキャン開始時刻を計算する"""
        if coord == "HORIZONTAL":
            stime = self.m.otf_horizontal_ramp(sx, sy, scan_dcos, dx, dy, dt, n, ramp, delay)
        else:
            stime = self.m.otf_ramp(sx, sy, scan_dcos, self.coord_dict[coord.upper()], dx, dy, dt, n, ramp, delay)
        return stime


    def get_status(self):
        """現在の(az,el)を取得する"""
        az, el = self.m.get_azel()
        return az, el
        
        
    def finalize(self):
        """トラッキングを終了する"""
        self.m.stop_tracking()
        return

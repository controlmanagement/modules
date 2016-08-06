#-*- coding: utf-8 -*-

#import csv
from pyslalib import slalib
#import SG
import math
import time
"""
class doppler(object):

    def set_track(self, stime, x, y, coord, offset_x, offset_y, offset_dcos, offset_coord, vlsrs):
        pass

    def callibrate_doppler(self, x, y, coord, offset_x=0, offset_y=0,
                           offset_dcos=1, offset_coord="SAME",
                           vlsrs=0., stime=0):
        #ドップラーシフトの補正

        vobs = self.doppler.set_track(x, y, coord, vlsrs, offset_x, offset_y,
                                      offset_dcos, offset_coord, stime)
        return vobs[0], vobs[1], vobs[2]
"""
class doppler_nanten (object):


    #PATH_DEVICE_TABLE = "/home/amigos/NECST/soft/obs/params/device_table.prm"
    #doppler_1p85.py,motor_command.c,motor_server.c,nanten_astro.h,calc_doppler.cpp,
    dic1 = {"bandnum":2,
            #set frequency [GHz]
            "restFreq":230.5380,
            #12CO Rest frequency [GHz] from Koln Univ.
            "REST_FREQ_12COJ1_0":115.2712018,
            "REST_FREQ_12COJ2_1":230.5380000,
            "REST_FREQ_12COJ3_2":345.7959899,
            "REST_FREQ_12COJ4_3":461.0407682,
            "REST_FREQ_12COJ7_6":806.6518060,
            #13CO Rest frequency [GHz] from Koln Univ.
            "REST_FREQ_13COJ1_0":110.2013541,
            "REST_FREQ_13COJ2_1":220.3986190,
            "REST_FREQ_13COJ3_2":330.5878655,
            "REST_FREQ_13COJ4_3":440.7650398,
            "REST_FREQ_13COJ7_6":771.1838856,
            #C18O Rest frequency [GHz] from Koln Univ.
            "REST_FREQ_C18OJ1_0":109.7821734,
            "REST_FREQ_C18OJ2_1":219.5603541,
            "REST_FREQ_C18OJ3_2":329.3305525,
            "REST_FREQ_C18OJ4_3":439.0887658,
            "REST_FREQ_C18OJ7_6":768.2515933,
            #CI Rest frequency [GHz] from Koln Univ.
            "REST_FREQ_CI3P1_0":492.1606510,
            "REST_FREQ_CI3P2_1":809.3419700,
            #set speed [km/sec]
            "vlsr":0,
            #Upper ***sb*:1 , Lower ***sb*:-1
            "1stsb1":1,
            "1stsb2":1,
            #set frequency [GHz]
            "2ndLO1":8.038000000000,
            "2ndLO2":9.301318999999,
            #set sg_power [dBm]
            "power_sg21":13.0,
            "power_sg22":13.0,
            #light speed [km/sec]
            "LIGHT_SPEED":299792.458 }

    coord_dict = {"J2000"     : 1,
                  "B1950"     : 2,
                  "LB"        : 3,
                  "GALACTIC"  : 3,
                  "APPARENT"  : 10,
                  #"HORIZONTAL": "COORD_HORIZONTAL",
                  "SAME"      : 0}





    def __init__(self):

        #self.sg2if1 = SG.secondsg01()
        #self.sg2if2 = SG.secondsg02()

        #for device_table
        """
        for record in csv.reader(open(PATH_DEVICE_TABLE,"r")):
            r_dict[record[0]] =record[1]
            continue
        """

        pass

    def set_track(self, x, y, coord, offset_x, offset_y, offset_dcos, offset_coord, stime):
        """
        setting 2ndLO
        """
        coord = self.coord_dict[coord]
        offset_coord = self.coord_dict[offset_coord]
        mjd = 40587.0 + time.time()/(24.*3600.)
        vobs_mjd = mjd + stime/24./3600.
        vobs = self.get_vobs(vobs_mjd,math.radians(x),math.radians(y),coord,
                             offset_x, offset_y, offset_dcos, offset_coord)
        c = self.dic1["LIGHT_SPEED"]
        for band in range(1, self.dic1["bandnum"]+1):
            rf = self.dic1["restFreq"]
            vdiff = vobs - self.dic1["vlsr"]
            fdiff = vdiff / c * rf
            if self.dic1["1stsb%d"%(band)] == 1:
                sb = 1
            if self.dic1["1stsb%d"%(band)] == -1:
                sb = -1
            set_freq = self.dic1["2ndLO%d"%(band)] + sb * fdiff
            if band == 1:
                #self.sg2if1.set_sg(dic1["set_freq"],dic1["power_sg21"])
                vdiff_21 = vdiff
                fdiff_21 = fdiff
            elif band == 2:
                #self.sg2if2.set_sg(dic1["set_freq"],dic1["power_sg22"])
                vdiff_22 = vdiff
                fdiff_22 = fdiff

        Vdiff = {"sg21":vdiff_21, "sg22":vdiff_22}
        Fdiff = {"sg21":fdiff_21, "sg22":fdiff_22}
        print("vobs=",vobs,"Vdiff=",Vdiff,"Fdiff=",Fdiff)
        return vobs,Vdiff,Fdiff

    def set_track_old(self, x, y, coord, offset_x, offset_y, offset_dcos, offset_coord, stime, mjd, secofday):
        """
        setting 2ndLO
        """
        coord = self.coord_dict[coord]
        offset_coord = self.coord_dict[offset_coord]
        mjd = mjd + secofday / (24.* 3600.)
        vobs_mjd = mjd + stime / (24. * 3600.)
        vobs = self.get_vobs(vobs_mjd,math.radians(x),math.radians(y),coord,
                             offset_x, offset_y, offset_dcos, offset_coord)
        c = self.dic1["LIGHT_SPEED"]
        for band in range(1, self.dic1["bandnum"]+1):
            rf = self.dic1["restFreq"]
            vdiff = vobs - self.dic1["vlsr"]
            fdiff = vdiff / c * rf
            if self.dic1["1stsb%d"%(band)] == 1:
                sb = 1
            if self.dic1["1stsb%d"%(band)] == -1:
                sb = -1
            set_freq = self.dic1["2ndLO%d"%(band)] + sb * fdiff
            if band == 1:
                #self.sg2if1.set_sg(dic1["set_freq"],dic1["power_sg21"])
                vdiff_21 = vdiff
                fdiff_21 = fdiff
            elif band == 2:
                #self.sg2if2.set_sg(dic1["set_freq"],dic1["power_sg22"])
                vdiff_22 = vdiff
                fdiff_22 = fdiff

        Vdiff = {"sg21":vdiff_21, "sg22":vdiff_22}
        Fdiff = {"sg21":fdiff_21, "sg22":fdiff_22}
        print("vobs=",vobs,"Vdiff=",Vdiff,"Fdiff=",Fdiff)
        return vobs,Vdiff,Fdiff
    """
    def get_status(self):
        freq_sg = self.sg.freq_check()

        pow_sg =

        freq = {"sg":freq_sg, }
        power = {"sg":pow_sg,}
        return {"freq":freq, "power":power}
    """
    def get_vobs(self, mjdtmp, xtmp, ytmp, mode, offx, offy, dcos, offmode):
        if offmode == self.coord_dict["SAME"] | offmode == mode :
            ytmp += offy
            if dcos == 0 :
                xtmp += offx
            else :
                xtmp += offx/math.cos(ytmp)
        else :
            print("error coord != off_coord")
            pass
        if mode == self.coord_dict["J2000"] :
            xxtmp = xtmp
            yytmp = ytmp
        elif mode == self.coord_dict["B1950"] :
            ret = slalib.sla_fk45z(xtmp, ytmp, 1950)
            xxtmp = ret[0]
            yytmp = ret[1]
        elif mode == self.coord_dict["LB"] :
            ret = slalib.sla_galeq(xtmp, ytmp)
            xxtmp = ret[0]
            yytmp = ret[1]
        else :
            xxtmp = xtmp
            yytmp = ytmp

        vobs = self.calc_vobs(mjdtmp+2400000.5, xxtmp, yytmp)
        return vobs

    def calc_vobs(self, jd, ra_2000, dec_2000):

        x_2000 = [0.,0.,0.]
        x = [0.,0.,0.]
        x1 = [0.,0.,0.]
        v = [0.,0.,0.]
        v_rev = [0.,0.,0.]
        v_rot = [0.,0.,0.]
        v2 = [0.,0.,0.]
        solx = [0.,0.,0.]
        solx1 = [0.,0.,0.]
        solv = [0.,0.,0.]
        DEG2RAD = math.pi/180.
        SEC2RAD = (2*math.pi)/(24.*60.*60.)
        ARCSEC2RAD = math.pi/(180.*60.*60.)
        RAD2DEG = 180./math.pi
        #1.85m at nobeyama
        #glongitude = 138.472153 * math.pi/180.
        #nanten2 at atacama (nanten2wiki)
        glongitude = -67.70308139 * DEG2RAD
        #1.85m at nobeyama
        #glatitude = 35.940874 * math.pi/180.
        #nanten2 at atacama (nanten2wiki)
        glatitude = -22.96995611 * DEG2RAD
        #1.85m at nobeyama
        #gheight = 1386
        #nanten2 at atacama
        gheight = 4863.85

        #gdut1 = -0.14
        #gstop_flag = 1
        #gkisa = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        #gtemperature = 273.0
        #gpressure = 860
        #ghumidity = 0.2
        #gtlr = 0.0065
        #tai_utc = 34.0
        #instruction = 0
        #target_changed = 1




        #ra_2000=ra_2000*DEG2RAD
        #dec_2000=dec_2000*DEG2RAD
        a = math.cos(dec_2000)
        x_2000[0] = a*math.cos(ra_2000)
        x_2000[1] = a*math.sin(ra_2000)
        x_2000[2] = math.sin(dec_2000)

        tu= (jd - 2451545.) / 36525.

        ranow=ra_2000
        delnow=dec_2000
        ret =slalib.sla_preces("FK5", 2000.,2000.+tu*100.,ranow,delnow)
        ranow = ret[0]
        delnow = ret[1]

        a = math.cos(delnow)
        x[0]=a*math.cos(ranow)
        x[1]=a*math.sin(ranow)
        x[2]=math.sin(delnow)

        ret = slalib.sla_nutc(jd-2400000.5)#radian
        nut_long = ret[0]
        nut_obliq = ret[1]
        eps0 = ret[2]


        #x1[0]=x[0]-(x[1]*math.cos(eps0)+x[2]*math.sin(eps0))*nut_long
        #x1[1]=x[1]+x[0]*math.cos(eps0)*nut_long - x[2]*nut_obliq
        #x1[2]=x[2]+x[0]*math.sin(eps0)*nut_long + x[1]*nut_obliq


        x1[0]=x[0]-(x[1]*math.cos(nut_obliq)+x[2]*math.sin(nut_obliq))*nut_long
        x1[1]=x[1]+x[0]*math.cos(nut_obliq)*nut_long - x[2]*nut_obliq
        x1[2]=x[2]+x[0]*math.sin(nut_obliq)*nut_long + x[1]*nut_obliq

        x[0]=x1[0]
        x[1]=x1[1]
        x[2]=x1[2]

        v0= 47.404704e-3

        ramda=35999.3729*tu+100.4664+(1.9146-0.0048*tu)*math.cos((35999.05*tu+267.53)*DEG2RAD)+0.0200*math.cos((71998.1*tu+265.1)*DEG2RAD)

        r=1.000141+(0.016707-0.000042*tu)*math.cos((35999.05*tu+177.53)*DEG2RAD)+0.000140*math.cos((71998.*tu+175.)*DEG2RAD)

        ramda1=628.308+(20.995-0.053*tu)*math.cos((35999.5*tu+357.52)*DEG2RAD)+0.439*math.cos((71998.1*tu+355.1)*DEG2RAD)+0.243*math.cos((445267.*tu+298.)*DEG2RAD)

        beta=0.024*math.cos((483202.*tu+273.)*DEG2RAD)

        r1 = (10.497-0.026*tu) * math.cos((35999.05*tu+267.53)*DEG2RAD)+ 0.243 * math.cos((445267.*tu+28.)*DEG2RAD)+ 0.176 * math.cos((71998.*tu+265.)*DEG2RAD)

        ramda = ramda *DEG2RAD

        v[0] = -r*ramda1*math.sin(ramda) + r1*math.cos(ramda)
        v[1] = r*ramda1*math.cos(ramda) + r1*math.sin(ramda)
        v[2] = r * beta

        v[0]    = v[0] - (0.263 * math.cos((3034.9*tu+124.4)*DEG2RAD) +0.058 * math.cos((1222. *tu+140.)*DEG2RAD) +0.013 * math.cos((6069. *tu+144.)*DEG2RAD))
    	v[1]    = v[1] - (0.263 * math.cos((3034.9*tu+34.4)*DEG2RAD) +0.058 * math.cos((1222. *tu+50.)*DEG2RAD) +0.013 * math.cos((6069. *tu+54.)*DEG2RAD))

    	v[0] = v[0] * v0
    	v[1] = v[1] * v0
    	v[2] = v[2] * v0

    	e = (23.439291 - 0.013004*tu)*3600.

    	v_rev[0] = v[0]
    	v_rev[1] = v[1] * math.cos(e * ARCSEC2RAD) - v[2] * math.sin(e * ARCSEC2RAD)
    	v_rev[2] = v[1] * math.sin(e * ARCSEC2RAD) + v[2] * math.cos(e * ARCSEC2RAD)

    	v_e = (465.1e-3) * (1.+0.0001568*gheight/1000.) * math.cos(glatitude)/math.sqrt(1.+0.0066945*math.pow(math.sin(glatitude),2.0))

    	am = 18.*3600.+41.*60.+50.54841+8640184.812866*tu +0.093104*tu*tu-0.0000062*tu*tu*tu

    	gmst = (jd - 0.5 - long(jd - 0.5)) * 24. * 3600. + am - 12.*3600.

    	l = 280.4664*3600. + 129602771.36*tu - 1.093*tu*tu
    	l = l * ARCSEC2RAD
    	p = (282.937+1.720*tu)*3600.
    	p = p * ARCSEC2RAD

    	w = (125.045 - 1934.136*tu + 0.002*tu*tu)*3600.
    	w = w * ARCSEC2RAD
    	ll = (218.317+481267.881*tu-0.001*tu*tu)*3600.
    	ll = ll*ARCSEC2RAD
    	pp = (83.353+4069.014*tu-0.010*tu*tu)*3600.
    	pp = pp*ARCSEC2RAD
    	dpsi = (-17.1996-0.01742*tu)*math.sin(w) + (-1.3187)*math.sin(2*l)+0.2062*math.sin(2*w) +0.1426*math.sin(l-p)-0.0517*math.sin(3*l-p)+0.0217*math.sin(l+p) +0.0129*math.sin(2*l-w)-0.2274*math.sin(2*ll)+0.0712*math.sin(ll-pp) -0.0386*math.sin(2*ll-w)-0.0301*math.sin(3*ll-pp) -0.0158*math.sin(-ll+3*l-pp)+0.0123*math.sin(ll+pp)
    	e = e  * ARCSEC2RAD

    	dpsicose = dpsi * math.cos(e)

    	lst = gmst + (dpsicose + glongitude*RAD2DEG*3600.) / 15.

    	v_rot[0] = -v_e * math.sin(lst * SEC2RAD)
    	v_rot[1] = v_e * math.cos(lst * SEC2RAD)
    	v_rot[2] = 0.

    	v2[0] = v_rev[0] + v_rot[0]
    	v2[1] = v_rev[1] + v_rot[1]
    	v2[2] = v_rev[2] + v_rot[2]

    	vobs = -(v2[0] * x_2000[0] + v2[1] * x_2000[1] + v2[2] * x_2000[2])
    	rasol=18.*15. *DEG2RAD
    	delsol=30.*DEG2RAD

    	#ret = slalib.sla_preces( "FK4", 1900.,2000.+tu*100., rasol, delsol)

    	ret = slalib.sla_preces( "FK4", 1950.,2000.+tu*100., rasol, delsol)

        rasol = ret[0]
        delsol = ret[1]

    	a = math.cos(delsol)
    	solx[0] = a*math.cos(rasol)
    	solx[1] = a*math.sin(rasol)
    	solx[2] = math.sin(delsol)


    	#solx1[0] = solx[0] - (solx[1] * math.cos(eps0) + solx[2] *	\
    	#		      math.sin(eps0)) * nut_long
    	#solx1[1] = solx[1] + (solx[0] * math.cos(eps0) * nut_long\
    	#		      - solx[2] * nut_obliq)
    	#solx1[2] = solx[2] + (solx[0] * math.sin(eps0) * nut_long \
    	#		      + solx[1] * nut_obliq)


    	solx1[0] = solx[0] - (solx[1] * math.cos(nut_obliq) + solx[2] * math.sin(nut_obliq)) * nut_long
    	solx1[1] = solx[1] + (solx[0] * math.cos(nut_obliq) * nut_long - solx[2] * nut_obliq)
    	solx1[2] = solx[2] + (solx[0] * math.sin(nut_obliq) * nut_long + solx[1] * nut_obliq)

    	solv[0]=solx1[0]*20.
    	solv[1]=solx1[1]*20.
    	solv[2]=solx1[2]*20.

    	vobs = vobs - (solv[0] * x[0] + solv[1] * x[1] + solv[2] * x[2])
    	vobs = -vobs

    	print("vobs=%f\n" % vobs)
        """
        if gcalc_flag == 1 :
    		return vobs

    	else gcalc_flag == 2:
    		return lst
        """
    	return vobs

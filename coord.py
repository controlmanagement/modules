import math
import ctypes
import numpy
import lib_sla as sla
import lib_jpl as jpl




class coord_calc(object):
	
	_P = ctypes.POINTER
	_char_p = ctypes.c_char_p
	_uchar = ctypes.c_ubyte
	_uchar_p = _P(ctypes.c_ubyte)
	_ushort = ctypes.c_ushort
	_ushort_p = _P(ctypes.c_ushort)
	_int = ctypes.c_int
	_int_p = _P(ctypes.c_int)
	_uint = ctypes.c_uint
	_long = ctypes.c_long
	_long_p = _P(ctypes.c_long)
	_ulong = ctypes.c_ulong
	_ulong_p = _P(ctypes.c_ulong)
	_float = ctypes.c_float
	_float_p = _P(ctypes.c_float)
	_double = ctypes.c_double
	_double_p = _P(ctypes.c_double)
	_void_p = ctypes.c_void_p
	
	def calc_planet_coordJ2000(self, ephem, jd_utc, tai_utc, ntarg, ra, dec, dist, radi):
		err_code = i = nctr = 3
		tau = 499.004782       # Light time for unit distance (sec) 
		aukm = 1.49597870e8    # AU in km 
		r = r1 = r2 = rr = []
		
		
		jd = jd_utc + (tai_utc + 32.184) / (24. * 3600.)  # Convert UTC to Dynamical Time 
		err_code = jpl.jpl_pleph(ephem, jd, ntarg, nctr, r, 1)
		
		if err_code == False:
			*dist = sqrt(r[0] * r[0] + r[1] * r[1] + r[2] * r[2])
			jpl_pleph(ephem, jd, nctr, 12, r1, 1)                                #Earth position at jd
			jpl_pleph(ephem, jd - *dist * tau / (24. * 3600.), ntarg, 12, r2, 1)  # Target position when the light left 
			for(i = 0; i <= 5; i++) rr[i] = r2[i] - r1[i]
			*dist = sqrt(rr[0] * rr[0] + rr[1] * rr[1] + rr[2] * rr[2])
			slaDcc2s(rr, ra, dec)
			
			*ra = slaDranrm(*ra)
			*radi = asin(eqrau[ntarg] / (*dist * aukm))
		else
		
		
		
		



	def 






	def apply_kisa(self, ):
		
		
		
		
		
		
		
		
		
		
		
		
		
		

	def calc_vobs_fk5(self, jd, ra_2000, dec_2000):
		x_2000 = x = x1 = [0,0,0]
		double v0,ramda,r,ramda1,beta,r1;
		double v[3],v_rev[3],v_rot[3],v2[3];
		double e,v_e,am,gmst,l,p,w,ll,pp,dpsi,dpsicose;
		double solx[3],solv[3],solx1[3];
		double rasol,delsol;
		double vobs, lst;
		
		#ra_2000=DEG2RAD
		#dec_2000=DEG2RAD
		a = math.cos(dec_2000)
		x_2000[0] = a*math.cos(ra_2000)
		x_2000[1] = a*math.sin(ra_2000)
		x_2000[2]= math.sin(dec_2000)
		
		tu= (jd - 2451545.)/36525.
		
		ranow = self._double(ra_2000)
		delow = self._double(dec_2000)
		sla.slaPreces( "FK5", 2000., 2000.+tu*100., ranow, delnow)
		
		a = math.cos(delnow);
		x[0] = a*math.cos(ranow);
		x[1] = a*math.sin(ranow);
		x[2] = math.sin(delnow);
		
		nut_long = self._double(0)
		nut_obliq = self._double(0)
		eps0 = self._double(0)
		sla.slaNutc(jd-2400000.5, nut_long, nut_obliq, eps0)
		
		x1[0]=x[0]-(x[1]*cos(eps0)+x[2]*sin(eps0))*nut_long;
		x1[1]=x[1]+x[0]*cos(eps0)*nut_long - x[2]*nut_obliq;
		x1[2]=x[2]+x[0]*sin(eps0)*nut_long + x[1]*nut_obliq;
		
		x[0]=x1[0];
		x[1]=x1[1];
		x[2]=x1[2];
		
		v0= 47.404704e-3;
		
		ramda=35999.3729*tu+100.4664+(1.9146-0.0048*tu)*cos((35999.05*tu+267.53)*DEG2RAD)+0.0200*cos((71998.1*tu+265.1)*DEG2RAD);
		
		r=1.000141+(0.016707-0.000042*tu)*cos((35999.05*tu+177.53)*DEG2RAD)+0.000140*cos((71998.*tu+175.)*DEG2RAD);
		
		ramda1=628.308\
			+(20.995-0.053*tu)*cos((35999.5*tu+357.52)*DEG2RAD)\
			+0.439*cos((71998.1*tu+355.1)*DEG2RAD)\
			+0.243*cos((445267.*tu+298.)*DEG2RAD);
		
		beta=0.024*cos((483202.*tu+273.)*DEG2RAD);
		
		r1      = (10.497-0.026*tu) * cos((35999.05*tu+267.53)*DEG2RAD) \
   	           + 0.243 * cos((445267.*tu+28.)*DEG2RAD) \
   	           + 0.176 * cos((71998.*tu+265.)*DEG2RAD);
		
		ramda   = ramda *DEG2RAD;
		
		v[0]    = -r*ramda1*sin(ramda) + r1*cos(ramda);
		v[1]    =  r*ramda1*cos(ramda) + r1*sin(ramda);
		v[2]    =  r * beta;
		
		v[0]    = v[0] - (      0.263 * cos((3034.9*tu+124.4)*DEG2RAD) \
   	             +       0.058 * cos((1222. *tu+140.)*DEG2RAD) \
   	             +       0.013 * cos((6069. *tu+144.)*DEG2RAD));
		v[1]    = v[1] - (     0.263 * cos((3034.9*tu+34.4)*DEG2RAD) \
   	             +       0.058 * cos((1222. *tu+50.)*DEG2RAD) \
   	             +       0.013 * cos((6069. *tu+54.)*DEG2RAD));
			
		v[0] = v[0] * v0;
		v[1] = v[1] * v0;
		v[2] = v[2] * v0;
		
		e = (23.439291 - 0.013004*tu)*3600.;
		
		v_rev[0] = v[0];
		v_rev[1] = v[1] * cos(e * ARCSEC2RAD) - v[2] * sin(e * ARCSEC2RAD);
		v_rev[2] = v[1] * sin(e * ARCSEC2RAD) + v[2] * cos(e * ARCSEC2RAD);
		
		v_e = (465.1e-3) * (1.+0.0001568*gheight/1000.) \
		  * cos(glatitude)/sqrt(1.+0.0066945*pow(sin(glatitude),2.0));
		
		am = 18.*3600.+41.*60.+50.54841+8640184.812866*tu \
		               +0.093104*tu*tu-0.0000062*tu*tu*tu;
		
		gmst = (jd - 0.5 - (long)(jd - 0.5)) * 24. * 3600. + am - 12.*3600.;
		
		l = 280.4664*3600. + 129602771.36*tu \
    	              - 1.093*tu*tu;
		l = l * ARCSEC2RAD;
		p = (282.937+1.720*tu)*3600.;
		p = p * ARCSEC2RAD;
		
		w = (125.045 - 1934.136*tu + 0.002*tu*tu)*3600.;
		w = w * ARCSEC2RAD;
		ll = (218.317+481267.881*tu-0.001*tu*tu)*3600.;
		ll = ll*ARCSEC2RAD;
		pp = (83.353+4069.014*tu-0.010*tu*tu)*3600.;
		pp = pp*ARCSEC2RAD;
		dpsi = (-17.1996-0.01742*tu)*sin(w) + \
   	          (-1.3187)*sin(2*l)+0.2062*sin(2*w) \
   	          +0.1426*sin(l-p)-0.0517*sin(3*l-p)+0.0217*sin(l+p) \
    	         +0.0129*sin(2*l-w)-0.2274*sin(2*ll)+0.0712*sin(ll-pp) \
   	          -0.0386*sin(2*ll-w)-0.0301*sin(3*ll-pp) \
   	          -0.0158*sin(-ll+3*l-pp)+0.0123*sin(ll+pp);
		e = e  * ARCSEC2RAD;
		
		dpsicose = dpsi * cos(e);
		
		lst = gmst + (dpsicose + glongitude*RAD2DEG*3600.) / 15.;
		
		v_rot[0] = -v_e * sin(lst * SEC2RAD);
		v_rot[1] = v_e * cos(lst * SEC2RAD);
		v_rot[2] = 0.;
		
		v2[0] = v_rev[0] + v_rot[0];
		v2[1] = v_rev[1] + v_rot[1];
		v2[2] = v_rev[2] + v_rot[2];
		
		vobs = -(v2[0] * x_2000[0] + v2[1] * x_2000[1] + v2[2] * x_2000[2]);
		rasol=18.*15. *DEG2RAD;
		delsol=30.*DEG2RAD;
			
		//slaPreces( "FK4", 1950.,2000.+tu*100.,&rasol,&delsol);
		slaPreces( "FK4", 1900.,2000.+tu*100.,&rasol,&delsol);
		
		a = cos(delsol);
		solx[0] = a*cos(rasol);
		solx[1] = a*sin(rasol);
		solx[2] = sin(delsol);
		
		/*
		solx1[0] = solx[0] - (solx[1] * cos(nut_obliq) + solx[2] * \
			sin(nut_obliq)) * nut_long;
		solx1[1] = solx[1] + (solx[0] * cos(nut_obliq) * nut_long\
			- solx[2] * nut_obliq);
		solx1[2] = solx[2] + (solx[0] * sin(nut_obliq) * nut_long \
			+ solx[1] * nut_obliq);
		*/
		solx1[0] = solx[0] - (solx[1] * cos(eps0) + solx[2] *	\
				      sin(eps0)) * nut_long;
		solx1[1] = solx[1] + (solx[0] * cos(eps0) * nut_long\
				      - solx[2] * nut_obliq);
		solx1[2] = solx[2] + (solx[0] * sin(eps0) * nut_long \
				      + solx[1] * nut_obliq);
		
		solv[0]=solx1[0]*20.;
		solv[1]=solx1[1]*20.;
		solv[2]=solx1[2]*20.;
		
		vobs = vobs - (solv[0] * x[0] + solv[1] * x[1] + solv[2] * x[2]);
		vobs = -vobs;
		
		//printf("vobs=%f\n",vobs);
		if (gcalc_flag == 1){
			return vobs;
   	 }
		else if (gcalc_flag == 2){
			return lst;
   	 }
		//return vobs;


import math
import ctypes
import slalib as sla
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
	
	eqrau = [0.0,
		2440.0,            # Mercury
		6051.8,            # Venus
		0.0,
		3389.9,            # Mars
		69134.1,           # Jupiter
		57239.9,           # Saturn
		25264.3,           # Uranus
		24553.1,           # Neptune
		1151.0,            # Pluto
		1737.53,           # Moon
		696000.0           """ Sun """]
	
	
	def calc_planet_coordJ2000(self, ephem, jd_utc, tai_utc, ntarg):
		err_code = i = nctr = 3
		tau = 499.004782       # Light time for unit distance (sec) 
		aukm = 1.49597870e8    # AU in km 
		r = r1 = r2 = rr = [0,0,0,0,0,0]
		
		ephem = self._void_p(ephem)
		jd = jd_utc + (tai_utc + 32.184) / (24. * 3600.)  # Convert UTC to Dynamical Time 
		err_code = jpl.jpl_pleph(ephem, jd, ntarg, nctr, r, 1)
		
		if err_code == False:
			dist = math.sqrt(r[0] * r[0] + r[1] * r[1] + r[2] * r[2])
			jpl.jpl_pleph(ephem, jd, nctr, 12, r1, 1)                                #Earth position at jd
			jpl.jpl_pleph(ephem, jd - dist * tau / (24. * 3600.), ntarg, 12, r2, 1)  # Target position when the light left 
			for i in range(6):
				rr[i] = r2[i] - r1[i]
			dist = math.sqrt(rr[0] * rr[0] + rr[1] * rr[1] + rr[2] * rr[2])
			ret = sla.slaDcc2s(rr)
			ra = ret[0]
			dec = ret[1]
			ra = sla.slaDranrm(ra)
			radi = math.asin(self.eqrau[ntarg] / (dist.value * aukm))
			return [ra, dec, dist, radi]
		else
			return err_code

	def planet_J2000_geo_to_topo(gra, gdec, dist, radi, jd_utc, dut1, tai_utc, longitude, latitude, height):
		date = jd_utc - 2400000.5 + dut1 / (24. * 3600.)
		jd = jd_utc - 2400000.5 + (tai_utc + 32.184) / (24. * 3600.)
		
		# Spherical to x,y,z 
		v = sla.slaDcs2c(gra, gdec)
		for i in range[3]:
			v[i] *= dist
  		
		# Precession to date. 
		rmat = sla.slaPrec(2000.0, sla.slaEpj(jd))
		vgp = sla.slaDmxv(rmat, v)
		
		# Geocenter to observer (date). 
		stl = sla.slaGmst(date) + longitude
		vgo = sla.slaPvobs(latitude, height, stl)
		
		# Observer to planet (date). 
		for i in range (6):
			v[i] = vgp[i] - vgo[i]
		
		disttmp = *dist
		dist = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
		radi *= disttmp / dist
		
		# Precession to J2000 
		rmat = sla.slaPrec(sla.slaEpj(jd), 2000.)
		vgp = sla.slaDmxv(rmat, v)
		
		# To RA,Dec. 
		ret = sla.slaDcc2s(vgp)
		tra = sla.slaDranrm(ret[0])
		tdec = ret[1]
		return [dist, radi, tra, tdec]

	def apply_kisa(self, double az1, double el1, double *az2, double *el2):
  double cos_az,sin_az,cos_el,sin_el,
    d_az,	/* offset of Az origin */
    d_el;	/* offest of El origin */
  		
		# calculate the values of correction
		cos_az = math.cos(az1)
		sin_az = math.sin(az1)
		cos_el = math.cos(el1)
		sin_el = math.sin(el1)
		
		# basic correction for AzEl mount
		d_az = gkisa.a1*sin_el + gkisa.a2 + gkisa.a3*cos_el +gkisa.b1*sin_az*sin_el - gkisa.b2*cos_az*sin_el;
  d_el =  gkisa.b1*cos_az + gkisa.b2*sin_az + gkisa.b3 + gkisa.g1 * el1 * 180. / M_PI;

  /* For radio observations */
  if(gopt_flag == 0) {
    d_az=d_az
      + gkisa.c1*sin(az1-el1) + gkisa.c2*cos(az1-el1)
      + gkisa.d1
      + gkisa.e1*cos_el - gkisa.e2*sin_el;
    d_el=d_el
      + gkisa.c1*cos(az1-el1) - gkisa.c2*sin(az1-el1)
      + gkisa.d2
      + gkisa.e1*sin_el + gkisa.e2*cos_el;
  }
  /* convert to encoder offset on the horizon */
  d_az =  d_az / cos_el;

  /* apply the correction values ->  radians*/
  *az2 = az1 +(d_az /60.0) * M_PI / 180.;
  *el2 = el1 +(d_el /60.0)* M_PI / 180.;
}
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

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
		
		nut_long = self._double_p(0)
		nut_obliq = self._double_p(0)
		eps0 = self._double_p(0)
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















	def tracking_proc()
{
  double dum1, dum2, dum3;
  double gxx, gyy, lambda;
  double planet_ra, planet_dec;
  struct timeval tv;
  static double pre_az=0, pre_el=0;
  static double pre_target_speed_az = 0, pre_target_speed_el = 0, pre_mjd = 0;

  // Calculate current MJD 
  gettimeofday(&tv, NULL);
  gmjd = (tv.tv_sec + tv.tv_usec/1000000.)/24./3600. + MJD0;
  
  // If radio source or planet, the proper motion sets to zero 
  if(gopt_flag == 0 || gplanet_flag == 1){
    gpx = 0.0; gpy = 0.0;
  }

  if(gplanet_flag == 1){
    gcoord_mode_flag = COORD_J2000;
    // Calculate geocentric J2000 coordinate 
    if(0 != calc_planet_coordJ2000_geocent(ephem, gmjd+2400000.5, tai_utc, gplanet_number, &planet_ra, &planet_dec, &gplanet_dist, &gplanet_radi)){
    fprintf(stderr, "Cannot calculate the position!\n");
      exit(1);
    }
    planet_J2000_geo_to_topo(planet_ra, planet_dec, &gplanet_dist, &gplanet_radi, &gx, &gy, gmjd+2400000.5, gdut1, tai_utc, glongitude, glatitude, gheight);
  }

  // Apply offset when the offset coordinate system is the same as that of the source 
  // gx -> gxx, gy -> gyy 
  if(goffset_mode_flag == COORD_SAME || goffset_mode_flag == gcoord_mode_flag){
    gyy = gy + goffy;
    gxx = (goffdcos == 0)? (gx + goffx): (gx + goffx / cos(gyy));
        //printf("%f %f %f %f\n", gx, gy, gxx, gyy);
  }else if(goffset_mode_flag != COORD_J2000){
    // THIS PART IS NOT IMPLIMENTED YET 
    gxx = gx; gyy = gy;
  }
  // =================== added by nishimura 2011/11/23
  else
    {
     gxx = gx; gyy = gy;
   }
  // ------------------- END

  // Convert to J2000
  if(gcoord_mode_flag == COORD_J2000){
    gaJ2000 = gxx; gdJ2000 = gyy;
    gpaJ2000 = gpx; gpdJ2000 = gpy;
  }else if(gcoord_mode_flag == COORD_B1950){
    slaFk425(gxx, gyy, gpx, gpy, 0, 0, &gaJ2000, &gdJ2000, &gpaJ2000, &gpdJ2000, &dum1, &dum2);
    //printf("%f %f %f %f\n", gxx, gyy,gaJ2000, gdJ2000);
  }else if(gcoord_mode_flag == COORD_LB){
    // Ignore proper motion in this case 
    slaGaleq(gxx, gyy, &gaJ2000, &gdJ2000);
    gpaJ2000 = 0; gpdJ2000 = 0;
  }

  // Apply offset when the offset coordinate system is not the same as that of the source, 
  // and the offset coordinate system is J2000 
  if(!(goffset_mode_flag == COORD_SAME || goffset_mode_flag == gcoord_mode_flag) && goffset_mode_flag == COORD_J2000){
    gdJ2000 += goffy;
    gaJ2000 = (goffdcos == 0)? (gaJ2000 + goffx): (gaJ2000 + goffx / cos(gdJ2000));
  }


  // From J2000 to Apparent 
  if(gcoord_mode_flag != COORD_APP){
    slaMap(gaJ2000, gdJ2000, gpaJ2000, gpdJ2000, 0.0, 0.0, 2000.0, gmjd + (tai_utc + 32.184)/(24.*3600.), &gaApparent, &gdApparent);
  }else{
    // In this case, the proper motion is ignored 
    gaApparent = gx;
    gdApparent = gy;
  }
  
  // Apply offset when the offset coordinate system is apparent. 
  if(goffset_mode_flag == COORD_APP){
    gpdJ2000 += goffy;
    gpaJ2000 = (goffdcos == 0)? (gpaJ2000 + goffx): (gpaJ2000 + goffx / cos(gpdJ2000));
  }

  if(gopt_flag == 1)
    lambda = glambda_opt;
  else
    lambda = glambda_radio;

  // From apparent to Horizontal 
  slaAop(gaApparent, gdApparent, gmjd, gdut1, glongitude, glatitude, gheight, 0, 0, gtemperature, gpressure, ghumidity, lambda, gtlr, &greal_az, &greal_el, &dum1, &dum2, &dum3);
  
  // From zenith angle to elevation 
  greal_el = M_PI / 2. - greal_el;
  //greal_az = greal_az + M_PI;

  // Apply horizontal offset. 
  greal_el += goffel;
  greal_az = (goffazeldcos == 0)? (greal_az + goffaz): (greal_az + goffaz / cos(greal_el));

  if(instruction == SET_COORD_HORIZONTAL){
    gtarget_az = greal_az; gtarget_el = greal_el;
  }else{
    apply_kisa(greal_az, greal_el, &gtarget_az, &gtarget_el);
  }

  if(gtarget_az*180./M_PI - angle_az > 180. && gtarget_az*180./M_PI - 360. > AZ_LIMIT_MIN)
    gtarget_az -= 2*M_PI;
  else if(gtarget_az*180./M_PI - angle_az < -180. && gtarget_az*180./M_PI + 360. < AZ_LIMIT_MAX)
    gtarget_az += 2*M_PI;

  if(target_changed == 1){
    pre_az = gtarget_az; pre_el = gtarget_el; pre_mjd = gmjd;
    target_changed = 0;
  }else{
    gtarget_speed_az = (gtarget_az - pre_az) / (gmjd - pre_mjd) * 180. / M_PI / (24.*3600.);  // degree/sec 
    gtarget_speed_el = (gtarget_el - pre_el) / (gmjd - pre_mjd) * 180. / M_PI / (24.*3600.);  // degree/sec 
    pre_az = gtarget_az; pre_el = gtarget_el; pre_mjd = gmjd;
	//gtarget_az=gtarget_az*180./M_PI;
	//gtarget_el=gtarget_el*180./M_PI;
    
    //||||||||||||||||||||||||||||||||||||||||||||||||
    printf("(%lf,%lf)->(%lf,%lf)->J2000(%lf,%lf)->App(%lf,%lf)->real(%lf,%lf)\n",gx,gy,gxx,gyy,gaJ2000,gdJ2000,gaApparent,gdApparent,greal_az,greal_el);
    //||||||||||||||||||||||||||||||||||||||||||||||||


  }
}









	def read_kisa_file():
{
  FILE *fp;
  int i_prm;
  char buffer[BUFFERSIZE], *file_stat;

  if(NULL == (fp = fopen(KISA_FILE, "r"))){
    return -1;
  }
  
  i_prm=0;
  while(1) {
    file_stat=fgets(buffer,BUFFERSIZE,fp); /* 1st line for comment */
    if(file_stat==NULL) {
      fclose(fp);
      return(-2);
    }
    if(buffer[0]=='#' || strncmp(buffer,"/*",2)==0 || strncmp(buffer,"//",2)==0) {
      continue;
    } else {
      switch(i_prm) {
      case 0:
		gkisa.a1=atof(buffer);
		break;
      case 1:
		gkisa.a2=atof(buffer);
		break;
      case 2:
		gkisa.a3=atof(buffer);
		break;
      case 3:
		gkisa.b1=atof(buffer);
		break;
      case 4:
		gkisa.b2=atof(buffer);
		break;
      case 5:
		gkisa.b3=atof(buffer);
		break;
      case 6:
		gkisa.c1=atof(buffer);
		break;
      case 7:
		gkisa.c2=atof(buffer);
		break;
      case 8:
		gkisa.d1=atof(buffer);
		break;
      case 9:
		gkisa.d2=atof(buffer);
		break;
      case 10:
		gkisa.e1=atof(buffer);
		break;
      case 11:
		gkisa.e2=atof(buffer);
		break;
      case 12:
		gkisa.g1=atof(buffer);
		break;
      }
      i_prm++;
      if(i_prm>12){
		fprintf(stderr, "%f %f %f %f %f %f %f %f %f %f %f %f %f\n", gkisa.a1, gkisa.a2, gkisa.a3, gkisa.b1, gkisa.b2, gkisa.b3, gkisa.c1, gkisa.c2, gkisa.d1, gkisa.d2, gkisa.e1, gkisa.e2, gkisa.g1);
		break;
      }
    }
  }
  fclose(fp);
 
  return 0;
}



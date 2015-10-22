import math
import ctypes
import lib_slalib as lib


class slalib_controller(object):
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
	
	def slaDcc2s(self, v):
		"""
		slaDcc2s
		"""
		ra = dec = self._double_p(self._int(0))
		vc= self._double*6
		v = vc(*v)
		lib.slaDcc2s(v, ra, dec)
		return [ra.value, dec.value]
	
	def slaDranrm(self, ra):
		"""
		slaDranrm
		"""
		ra = self._double(ra)
		ra = lib.slaDranrm(ra)
		return ra.value
	
	def slaDcs2c(self, ra, dec):
		"""
		slaDcs2c
		"""
		ra = self._double(ra)
		dec = self._double(dec)
		v = self._double_p*3
		data = [0]*3
		v = v(*data)
		lib.slaDcs2c(ra, dec, v)
		return v
	
	def slaPrec(self, begin_epoch, end_epoch):
		"""
		slaPrec
		"""
		begin_epoch = self._double(begin_epoch)
		end_epoch = self._double(end_epoch)
		rmat = [[0,0,0],[0,0,0],[0,0,0]]
		rmat = self._double(rmat)
		lib.slaPrc(begin_epoch, end_epoch, rmat)
		return rmat
	
	def slaEpj(self, jd):
		"""
		slaEpj
		"""
		jd = self._double(jd)
		je = lib.slaEpj(jd)
		return je.value
	
	def slaDmxv(self, dm, va):
		"""
		slaDmxv
		"""
		dum0 =dum1 = dum2 = c_va = vb = self._double*3
		data0 = data1 = data2 = []
		data0 = dm[0]
		data1 = dm[1]
		data2 = dm[2]
		dum0 = dum0(*data0)
		dum1 = dum1(*data1)
		dum2 = dum2(*data2)
		dum = [dum0,dum1,dum2] #doubtful??
		va = c_va(*va)
		data = [0]*3
		vb = vb(*data)
		lib.slaDmxv(dum, va, vb)
		return vb
	
	def slaGmst(self, ut1):
		"""
		slaGmst
		"""
		ut1 = self._double(ut1)
		st = lib.slaGmst(ut1)
		return st.value
	
	def slaPvobs(self, latitude, height, stl):
		"""
		slaPvobs
		"""
		latitude = self._double(latitude)
		height = self._double(height)
		stl = self._double(stl)
		pv6 = self._double*6
		data = [0]*6
		pv6 = pv6(*data)
		lib.slaPvobs(latitude, height, stl, pv6)
		return pv6
	
	def slaPreces(self, FK, ep0, ep1, ra, dec):
		"""
		slaPreces
		"""
		FK = self._uchar_p(FK)
		ep0 = self._double(ep0)
		ep1 = self._double(ep1)
		ra = self._double_p(self._float(ra))
		dec = self._double_p(self._float(dec))
		lib.slaPreces(FK, ep0, ep1, ra, dec)
		return [ra.value, dec.value]
	
	def slaNutc(self, date):
		"""
		slaNutc
		"""
		date = self._double(date)
		long = obliq = eps0 = self._double_p(self._int(0))
		lib.slaNutc(date, long, obliq, eps0)
		return [long.value, obliq.value, eps0.value]
	
	def slaFk425(self, r1950, d1950, dr1950, dd1950, p1950, v1950):
		"""
		slaFk425
		"""
		r1950 = self._double(r1950)
		d1950 = self._double(d1950)
		dr1950 = self._double(dr1950)
		dd1950 = self._double(dd1950)
		p1950 = self._double(p1950)
		v1950 = self._double(v1950)
		r2000 = d2000 = dr2000 = dd2000 = p2000 = v2000 = self._double_p(self._int(0))
		lib.slaFk425(r1950, d1950, dr1950, dd1950, p1950, v1950, r2000, d2000, dr2000, dd2000, p2000, v2000)
		return [r2000.value, d2000.value, dr2000.value, dd2000.value, p2000.value, v2000.value]
	
	def slaGaleq(self, long, lati):
		"""
		slaGaleq
		"""
		long = self._double(long)
		lati = self._double(lati)
		ra = dec = self._double_p(self._int(0))
		lib.slaGaleq(long, lati, ra, dec)
		return [ra.value, dec.value]
	
	def slaMap(self, m_ra, m_dec, p_ra, p_dec, px, rv, eq, date):
		"""
		slaMap
		"""
		m_ra = self._double(m_ra)
		m_dec = self._double(m_dec)
		p_ra = self._doube(p_dec)
		px = self._double(px)
		rv = self._double(rv)
		eq = self._double(eq)
		date = self._double(date)
		ap_ra = ap_dec = self._double_p(self._int(0))
		lib.slaMap(m_ra, m_dec, p_ra, p_dec, px, rv, eq, date, ap_ra, ap_dec)
		return [ap_ra.value, ap_dec.value]
	
	def slaAop(self, g_ra, g_dec, mjd, dut, m_long, m_lati, height, xp, yp, temp, pressure, humid, w_length, tlr):
		"""
		slaAop
		"""
		g_ra = self._double(g_ra)
		g_dec = self._double(g_dec)
		mjd = self._double(mjd)
		dut = self._double(dut)
		m_long = self._double(m_long)
		m_lati = self._double(m_lati)
		height = self._double(height)
		xp = self._double(xp)
		yp = self._double(yp)
		temp = self._double(temp)
		pressure = self._double(pressure)
		humid = self._double(humid)
		w_length = self._double(w_length)
		tlr = self._double(tlr)
		az = el = ha = dec = ra = self._double_p(self._int(0))
		lib.slaAop(g_ra, g_dec, mjd, dut, m_long, m_lati, height, xp, yp, temp, pressure, humid, w_length, tlr, az, el, ha, dec, ra)
		return [az.value, el.value, ha.value, ra.value, dec.value]
	
	def slaMappa(self, eq, tdb):
		"""
		slaMappa
		"""
		eq = self._double(eq)
		tdb = self._double(tdb)
		amprms = self._double*21
		date = [0]*21
		amprms = amprms(*date)
		lib.slaMappa(eq, mjd_tdb, amprms)
		return amprms
	
	def slaAoppa(self, mjd_utc, dut, long, lat, alt, xp, yp, tmp, p, hu, wl, tlr):
		"""
		slaAoppa
		"""
		mjd_utc = self._double(mjd_utc)
		dut = self._double(dut)
		long = self,_double(long)
		lat = self._doubel(lat)
		alt = self._double(alt)
		xp = sele._double(xp)
		yp = self._double(yp)
		tmp = self._double(tmp)
		p = self._double(p)
		hu = self._double(hu)
		wl = self._double(wl)
		tlr = self._double(tlr)
		aoprms = self._double_p*14
		date = [0]*14
		aoprms = aoprms(*date)
		lib.slaAoppa(mjd_utc, dut, long, lat, alt, xp, yp, tmp, p, hu, wl, tlr, aoprms)
		return aoprms
	
	def slaOapqk(self, type, ob1, ob2, aoprms):
		"""
		slaOapqk
		"""
		type = self._char_p(type)
		ob1 = self._double(ob1)
		ob2 = self._double(ob2)
		ra = dec = self._double_p(self._int(0))
		lib.slaOapqk(type, ob1, ob2, aoprms, ra, dec)
		return [ra.value, dec.value]
	
	def slaAmpqk(self, ra, dec, amprms):
		"""
		slaAmpqk
		"""
		ra = self._double(ra)
		dec = self._double(dec)
		m_ra = m_dec = self._double_p(self._int(0))
		lib.slaAmpqk(ra, dec, amprms, m_ra, m_dec)
		return [m_ra.value, m_dec.value]
	

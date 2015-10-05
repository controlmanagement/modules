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
		ra = dec = self._double_p(0)
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
		latitude = self._double(latitude)
		height = self._double(height)
		stl = self._double(stl)
		pv6 = self._double*6
		data = [0]*6
		pv6 = pv6(*data)
		lib.slaPvobs(latitude, height, stl, pv6)
		return pv6
	
	def slaPreces(self, )
	
	
	
	
	
	
	
	
	
	
	

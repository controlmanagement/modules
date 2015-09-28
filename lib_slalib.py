import os
import ctypes


SO_DIR = '/usr/lib'


try:
	Dcc2s = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaDCC2s'))
	Dranrm = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaDranrm'))
	Dcs2c = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaDcs2c'))
	Prec = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaPrec'))
	Epj = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaEpj'))
	Dmxv = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaDmxv'))
	Gmst = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaGmst'))
	Pvobs = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaPvobs'))
	Preces = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaPreces'))
	Nutc = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaNutc'))
	Fk425 = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaFk425'))
	Galeq = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaGaleq'))
	Map = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaMap'))
	Aop = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaAop'))
except OSError:
	pass
else:
	
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

	#slaDcc2s
	#--------------------------------
	slaDcc2s = Dcc2s.slaDcc2s
	slaDcc2s.restype = _uint
	slaDcc2s.argtypes = (_double, _double_p, _double_p)
	
	#slaDranrm
	#--------------------------------
	slaDranrm = Dranrm.slaDranrm
	slaDranrm.restype = _uint
	slaDranrm.argtypes = (_double)
	
	#slaDcs2c
	#--------------------------------
	slaDcs2c = Dcs2c.slaDcs2c
	slaDcs2c.restype = _uint
	slaDcs2c.argtypes = (_double, _double, _double)
	
	#slaPrec
	#--------------------------------
	slaPrec = Prec.slaPrec
	slaPrec.restype = _uint
	slaPrec.argtypes = (_double, _double, _double)
	
	#slaEpj
	#--------------------------------
	slaEpj = Epj.slaEpj
	slaEpj.restype = _uint
	slaEpj.argtypes = (_double)
	
	#slaDmxv
	#--------------------------------
	slaDmxv = Dmxv.slaDmxv
	slaDmxv.restype = _uint
	slaDmxv.argtypes = (_double, _double, _double)
	
	#slaGmst
	#--------------------------------
	slaGmst = Gmst.slaGmst
	slaGmst.restype = _uint
	slaGmst.argtypes = (_double)
	
	#slaPvobs
	#--------------------------------
	slaPvobs = Pvobs.slaPvobs
	slaPvobs.restype = _uint
	slaPvobs.argtypes = (_double, _double, _double, _double)
	
	#slaPreces
	#--------------------------------
	slaPreces = Preces.slaPreces
	slaPreces.restype = _uint
	slaPreces.argtypes = (_uchar, _double, _double, _double_p, _double_p)
	
	#slaNutc
	#--------------------------------
	slaNutc = Nutc.slaNutc
	slaNutc.restype = _uint
	slaNutc.argtypes = (_double, _double_p, _double_p, _double_p)
	
	#slaFk425
	#--------------------------------
	slaFk425 = Fk425.slaFk425
	slaFk425.restype = _uint
	slaFk425.argtypes = (_double, _double, _double, _double, _double, _double, _double_p, _double_p, _double_p, _double_p, _double_p, _double_p)
	
	#slaGaleq
	#--------------------------------
	slaGaleq = Galeq.slaGaleq
	slaGaleq.restype = _uint
	slaGaleq.argtypes = (_double, _double, _double_p, _double_p)
	
	#slaMap
	#--------------------------------
	slaMap = Map.slaMap
	slaMap.restype = _uint
	slaMap.argtypes = (_double, _double, _double, _double, _double, _double, _double, _double, _double_p, _double_p)
	
	#slaAop
	#--------------------------------
	slaAop = Aop.slaAop
	slaAop.restype = _uint
	slaAop.argtypes = (_double, _double, _double, _double, _double, _double, _double, _double, _double, _double, _double, _double, _double, _double,
						_double_p, _double_p, _double_p, _double_p, _double_p)



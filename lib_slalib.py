import os
import ctypes


SO_DIR = '/usr/lib/slalib'


try:
	Dcc2s = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaDCC2s.o'))
	Dranrm = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaDranrm.o'))
	Dcs2c = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaDcs2c.o'))
	Prec = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaPrec.o'))
	Epj = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaEpj.o'))
	Dmxv = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaDmxv.o'))
	Gmst = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaGmst.o'))
	Pvobs = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaPvobs.o'))
	Preces = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaPreces.o'))
	Nutc = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaNutc.o'))
	Fk425 = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaFk425.o'))
	Galeq = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaGaleq.o'))
	Map = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaMap.o'))
	Aop = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaAop.o'))
	
	Mappa = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaMappa.o'))
	Aoppa = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaAoppa.o'))
	Oapqk = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaOapqk.o'))
	Ampqk = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaAmpqk.o'))
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
	slaDranrm.restype = _double
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
	slaEpj.restype = _double
	slaEpj.argtypes = (_double)
	
	#slaDmxv
	#--------------------------------
	slaDmxv = Dmxv.slaDmxv
	slaDmxv.restype = _uint
	slaDmxv.argtypes = (_double, _double, _double)
	
	#slaGmst
	#--------------------------------
	slaGmst = Gmst.slaGmst
	slaGmst.restype = _double
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
	
	#slaMappa
	#--------------------------------
	slaMappa = Mappa.slaMappa
	slaMappa.restype = _uint
	slaMappa.argtypes = (_double, _double, _double)
	
	#slaAoppa
	#--------------------------------
	slaAoppa = Aoppa.slaAoppa
	slaAoppa.restype = _uint
	slaAoppa.argtypes = (_double, _double, _double, _double, _double, _double, _double, _double, _double, _double, _double, _double, _double)
	
	#slaOapqk
	#--------------------------------
	slaOapqk = Oapqk.slaOapqk
	slaOapqk.restype = _uint
	slaOapqk.argtypes = (_char_p, _double, _double, _double, _double_p, _double_p)
	
	#slaAmpqk
	#--------------------------------
	slaAmpqk = Ampqk.slaAmpqk
	slaAmpqk.restype = _uint
	slaAmpqk.argtypes = (_double, _double, _double, _double_p, _double_p)
	

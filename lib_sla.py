import os
import ctypes


SO_DIR = '/usr/lib'


try:
	Dcc2s = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaDCC2s'))
	Dranrm = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaDranrm'))
	Dcs2c = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaDcs2c'))
	Prec= ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaPrec'))
	Epj= ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaEpj'))
	Dmxv= ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaDmxv'))
	Gmst= ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaGmst'))
	Pvobs= ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaPvobs'))
	Preces= ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaPreces'))
	Nutc= ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaNutc'))
	Fk425= ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaFk425'))
	Galeq= ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaGaleq'))
	Map= ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaMap'))
	Aop= ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'slaAop'))
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
	
	#Dranrm
	#--------------------------------
	
	
	



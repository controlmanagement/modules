import os
import ctypes



#define
#-----------------------------------
JPL_EPHEM_START_JD = 0
JPL_EPHEM_END_JD = 8
JPL_EPHEM_STEP = 16
JPL_EPHEM_N_CONSTANTS = 24
JPL_EPHEM_AU_IN_KM = 28
JPL_EPHEM_EARTH_MOON_RATIO = 36
JPL_EPHEM_EPHEMERIS_VERSION = 200
JPL_EPHEM_KERNEL_SIZE = 204
JPL_EPHEM_KERNEL_RECORD_SIZE = 208
JPL_EPHEM_KERNEL_NCOEFF = 212
JPL_EPHEM_KERNEL_SWAP_BYTES = 216


SO_DIR = '/usr/lib/jpl_ephem'



try:
	jpl = ctypes.cdll.LoadLibrary(os.path.join(SO_DIR,'jpleph-c.o'))
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
	
	
	#jpl_init_ephemeris
	#--------------------------------
	jpl_init_ephemeris = jpl.jpl_init_ephemeris
	jpl_init_ephemeris.restype = None
	jpl_init_ephemeris.argtypes = (_char_p, _char, _double_p)
	
	#jpl_close_ephemeris
	#--------------------------------
	jpl_close_ephemeris = jpl.jpl_close_ephemeris
	jpl_close_ephemeris.restype = None
	jpl_close_ephemeris.argtypes = (_void_p)
	
	#jpl_state
	#--------------------------------
	jpl_state = jpl.jpl_state
	jpl_state.restype = _int
	jpl_state.argtypes = (_void_p, _double, _int, _double, _double, _int)
	
	#jpl_pleph
	#--------------------------------
	jpl_pleph = jpl.jpl_pleph
	jpl_pleph.restype = _int
	jpl_pleph.argtypes = (_void_p, _double, _int, _int, _double, _int)
	
	#jpl_get_double
	#--------------------------------
	jpl_get_double = jpl.jpl_get_double
	jpl_get_double.restype = _double
	jpl_get_double.argtypes = (_void_p, _int)
	
	#jpl_get_long
	#--------------------------------
	jpl_get_long = jpl.jpl_get_long
	jpl_get_long.restype = _double
	jpl_get_long.argtypes = (_void_p, _int)
	
	#make_sub_ephem
	#--------------------------------
	make_sub_ephem = jpl.make_sub_ephem
	make_sub_ephem.restype = _int
	make_sub_ephem.argtypes = (_void_p, _char_p, _double, _double)
	

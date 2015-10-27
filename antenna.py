import pyinterface
import antenna_nanten_controller





class antenna_controller(object):
	
	
	
	def __init__(self):
		self.antenna = antenna_nanten_controller.antenna_nanten_controller()
		pass
	
	def start_server(self):
		self.start_antenna_server()
		return
	
	def move_azel(self, az, el, hosei, off_az, off_el):
		self.antenna.move_azel(az, el, hosei, off_az, off_el)
		return
	
	def move_radec(self, ra, dec, p_ra, p_dec, code_mode, temp, pressure, humid, lamda, hosei):
		self.antenna.move_radec(ra, dec, p_ra, p_dec, code_mode, temp, pressure, humid, lamda, hosei)
		return
	
	def move_lb(self, g_long, g_lati, temp, pressure, humid, lamda, hosei):
		self.antenna.move_lb(g_long, g_lati, temp, pressure, humid, lamda, hosei)
		return
	
	def move_planet(self, ):
		self.antenna.move_planet()
		return
	



def antenna_client(host, port):
        client = pyinterface.server_client_wrapper.control_client_wrapper(antenna_controller, host, port)
        return client

def antenna_monitor_client(host, port):
        client = pyinterface.server_client_wrapper.monitor_client_wrapper(antenna_controller, host, port)
        return client

def start_antenna_server(port1 = 5921, port2 = 5922):
        antenna = antenna_controller()
        server = pyinterface.server_client_wrapper.server_wrapper(antenna,'', port1, port2)
        server.start()
        return server

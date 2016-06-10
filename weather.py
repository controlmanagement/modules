import subprocess
import datetime
import time

import pyinterface

class weather_controller(object):

	host = "weather@200.91.8.66"
	dir = "/home/weather/WeatherMonitor/Weather_Data/"
	data = [0]*20
		
	def __init__(self):
		pass
	
	def get_weather(self):
		now = time.time()
		d = datetime.datetime.utcfromtimestamp(now)

		if d.month < 10:
			month = '0'+str(d.month)
		else:
			month = str(d.month)

		if d.day < 10:
			day = '0'+str(d.day)
		else:
			day = str(d.day)

		data = str(d.year)+month+"/"+str(d.year)+month+day+".nwd"
		# Year | Month | Day | Hour | Min | Sec | InTemp | OutTemp | InHumi | OutHumi | WindDir | WindSp | Press | Rain | CabinTemp1 | CabinTemp2 | DomeTemp1 | DomeTemp2 | GenTemp1 | GenTemp2 |
		#     0|      1|    2|     3|    4|    5|       6|        7|       8|        9|       10|      11|     12|    13|          14|          15|         16|         17|        18|        19|
		
		ret = subprocess.check_output(["ssh", self.host, "tail", self.dir+data, "-n", "1"])
		res = ret.split()
		for i in range(20):
			self.data[i] = res[i].strip(',')
		return self.data

	def read_weather(self):
		return self.data

def weather_client(host, port):
	client = pyinterface.server_client_wrapper.control_client_wrapper(weather_controller, host, port)
	return client

def weather_monitor_client(host, port):
	client = pyinterface.server_client_wrapper.monitor_client_wrapper(weather_controller, host, port)
	return client

def start_weather_server(port1 = 3001, port2 = 3002):
	weather = weather_controller()
	server = pyinterface.server_client_wrapper.server_wrapper(weather,'', port1, port2)
	server.start()
	return server

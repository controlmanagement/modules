import subprocess
import datetime

class weather_controller(object):

	host = "weather@200.91.8.66"
	dir = "/home/weather/WeatherMonitor/Weather_Data/"

		
	def __init__(self):
		pass
	
	def get_weather(self):

		d = datetime.datetime.today()
		data = "/"+str(d.year)+str(d.month)+"/"+str(d.year)+str(d.month)+str(d.day)+".nwd"
		# Year | Month | Day | Hour | Min | Sec | InTemp | OutTemp | InHumi | OutHumi | WindDir | WindSp | Press | Rain | CabinTemp1 | CabinTemp2 | DomeTemp1 | DomeTemp2 | GenTemp1 | GenTemp2 |
		#     0|      1|    2|     3|    4|    5|       6|        7|       8|        9|       10|      11|     12|    13|          14|          15|         16|         17|        18|        19|
		
		ret = subprocess.check_output(["ssh", self.host, "tail", self.dir+data, "-n", "1"])
		#ret = subprocess.check_output(["tail", "/home/amigos/python/test_hyouka/test_space/20151019.nwd", "-n", "1"])
		ret = ret.split( )
		return ret

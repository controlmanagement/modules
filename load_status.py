
import controller

import time

status = controller.read_status()

while(1):
	ret = status.read_status()
	print ret
	time.sleep(5)


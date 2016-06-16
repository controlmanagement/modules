import pyinterface

class ccd_controller(object):

	error = []
	status = ''


	def __init__(self):
		#　open
		self.img = pyinterface.create_gpg5520(1)
		return

	def print_msg(self,msg):
		print(msg)
		return

	def print_error(self,msg):
		self.error.append(msg)
		self.print_msg('!!!!ERROR!!!!' + msg)
		return

	def oneshot(self, filename, frame_no = 1, size=640*480, Bufferformat='IFIMG_COLOR_RGB24', StartMode = 'IFIMG_DMACAPTURE_START', framenum = 1):
		# set buffer
		self.img.set_format(frame_no, size, Bufferformat)
		#start cap
		self.img.start_cap(frame_no, StartMode)
		# get status
		status = self.img.get_status()
		# get data
		self.img.get_data(frame_no, framenum, size, dwDataFormat = 'IFIMG_COLOR_RGB24', dwXcoodinates = 0, dwYcoodinates = 0, dwXLength = 640, dwYLength = 480)
		# save data
		self.img.save(fiename, size*3, Bufferformat)
		return status

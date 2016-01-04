import controller
#import dome_status

import time

status = controller.read_status()

"""
dome.open()
dome1 = dome.get_remote_status()
dome2 = dome.get_door_status()
dome3 = dome.get_memb_status()
"""

while(1):
    data = status.read_status()
    #dome1 = dome.get_remote_status()
    #dome2 = dome.get_door_status()
    #dome3 = dome.get_memb_status()
    #dome4 = dome.dome_encoder_acq()
    now = time.strftime('%H:%M:%S',time.gmtime())

    #print "TIME : %s  AZ : %3.2f  EL : %3.2f  DOME : %s  door : %s  membrane : %s  %3.2f" %(now,azel[0]/3600.,azel[1]/3600.,dome1,dome2[1],dome3[1],dome4/3600.)
    print "TIME : %s  AZ_r: %3.2f  EL_r: %3.2f  AZ_i : %3.2f  EL_i: %3.2f" %(now,data['current_az']/3600.,data['current_el']/3600.,data['command_az']/3600.,data['command_el']/3600.,)
    
    time.sleep(1.)


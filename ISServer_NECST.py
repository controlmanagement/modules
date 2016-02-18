#!/usr/bin/python
# *************************************************************
#
# Copyright (C) 2012-2015 Inside Systems Pty Ltd
#
# *************************************************************
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# *************************************************************
# Description
# *************************************************************
# This is the generic data server which serves data from any file in the data directory to
# the open-monica server.
# To retrieve the data in the file named "data", connect to this server and send any
# string terminated by "\n". This will trigger the read command and you will be served
# the contents of any file in the data directory which commences by the name "data_".
#
# *************************************************************
# Installation instructions
# *************************************************************
# 1. Adjust the port, datahome and logdir directories to suit your needs.
# 2. datahome is where your data gatherer saves the data. Refer to the Gather_Sample_Data.pl script for an example.
# 3. Run ISServer.pl manually and look at any output as well as the log file to make sure there are no error messages
# 4. Install it as a cronjob to start every minute. It'll only start one instance.
# *************************************************************
# This is a python rewrite of ISServer.pl


from socket import *
import glob
import thread
from os.path import *
import sys
import time
import os
import controller

#datahome = "/home/amigos/NOSU/data/"
#datahome = "./"

HOST, PORT = "172.20.0.11", 50007
#HOST, PORT = "192.168.100.187", 5927
#HOST, PORT = "172.20.0.31", 7111
##HOST, PORT = "127.0.0.1", 7111

def check_running():
  if os.access("/tmp/ISServer.lock", os.F_OK):
    # Lock file exists. Get the PID:
    pidfile = open("/tmp/ISServer.lock", "r")
    pidfile.seek(0)
    old_pid = pidfile.readline()
    pidfile.close()

    try:
      os.kill(int(old_pid), 0)
      print "Process exists, exiting"
      sys.exit(0)
    except OSError:
      print "Process does not exist, remove lock file"
      os.remove("/tmp/ISServer.lock")

  print "Setting lock file"
  pidfile = open("/tmp/ISServer.lock", "w")
  pidfile.write("%s" % os.getpid())
  pidfile.close()


def handler(clientsocket, clientaddr):
    # loop forever so we don't close the TCP connection. One of these handlers
    # is automatically instantiated for each TCP connection
    print "Accepted connection from: ", clientaddr

    while 1:
        data = clientsocket.recv(1024)
        data = data.strip()
        if data == "bye":
          # bye was sent, close the connection
          break
        ## now go read the directory
        #filelist = glob.glob(datahome + "data*")
        #newdata = ''
        #for file in filelist:
          # read the files
        #  with open(file, "r") as ins:
        #    for line in ins:
        #      newdata += basename(file)+'-'+line
        # send the data back to the client
        dic1 = con.read_status()
        newdata = "data_ut\t"+str(dic1["Time"])+"\tFloat"+" "\
                  "data_Current-position-Az\t"+str(dic1["Current_Az"])+"\tFloat"+" "\
                  "data_Current-position-El\t"+str(dic1["Current_El"])+"\tFloat"+" "\
                  "data_Command-position-Az\t"+str(dic1["Command_Az"])+"\tFloat"+" "\
                  "data_Command-position-El\t"+str(dic1["Command_El"])+"\tFloat"+" "\
                  "data_Deviation-Az\t"+str(dic1["Deviation_Az"])+"\tFloat"+" "\
                  "data_Deviation-El\t"+str(dic1["Deviation_El"])+"\tFloat"+" "\
                  "data_Drive-ready_Az\t"+str(dic1["Drive_ready_Az"])+"\tString"+" "\
                  "data_Drive-ready_El\t"+str(dic1["Drive_ready_El"])+"\tString"+" "\
                  "data_Authority\t"+str(dic1["Authority"])+"\tString"+" "\
                  "data_Emergency-switch\t"+str(dic1["Emergency"])+"\tString"+" "\
                  "data_Door-Current-position-Az\t"+str(dic1["None"])+"\tFloat"+" "\
                  "data_Door\t"+str(dic1["Door_Dome"])+"\tString"+" "\
                  "data_Membrane\t"+str(dic1["Door_Membrane"])+"\tString"+" "\
                  "data_Az-Speed\t"+str(dic1["None"])+"\tString"+" "\
                  "data_Door-Authority\t"+str(dic1["Door_Authority"])+"\tString"+" "\
                  "data_Synchronous-with-Antenna\t"+str(dic1["None"])+"\tString"+" "\
                  "data_Emergency-switch\t"+str(dic1["None"])+"\tString"+" "\
                  "data_Current-position-M4\t"+str(dic1["Current_M4"])+"\tString"+" "\
                  "data_Current-position-HOT\t"+str(dic1["Current_Hot"])+"\tString"+" "\
                  "data_Motion-status\t"+str(dic1["None"])+"\tString"+" "\
                  "data_Deviation-error\t"+str(dic1["None"])+"\tString"+" "\
                  "data_Limit-switch-ON\t"+str(dic1["None"])+"\tString"+" "\
                  "data_Emergency-switch-ON\t"+str(dic1["None"])+"\tString"+" "\
                  "data_Deviation-error\t"+str(dic1["None"])+"\tString"+" "\
                  "data_Emergency-switch-ON\t"+str(dic1["None"])+"\tString"+" "\
                  "data_Synchronous-error\t"+str(dic1["None"])+"\tString"+" "\
                  "data_Limit-switch-M4\t"+str(dic1["None"])+"\tString"+" "\
                  "data_Limit-switch-HOT\t"+str(dic1["None"])+"\tString"+" "\
                  "data_Cabin-temperature1\t"+str(dic1["CabinTemp1"])+"\tFloat"+" "\
                  "data_Cabin-temperature2\t"+str(dic1["CabinTemp2"])+"\tFloat"+" "\
                  "data_In-temperature\t"+str(dic1["InTemp"])+"\tFloat"+" "\
                  "data_Ambient-temperature\t"+str(dic1["OutTemp"])+"\tFloat"+" "\
                  "data_HOT-temperature\t"+str(dic1["None"])+"\tFloat"+" "\
                  "data_Dew-point\t"+str(dic1["None"])+"\tFloat"+" "\
                  "data_Wind-speed\t"+str(dic1["WindSp"])+"\tFloat"+" "\
                  "data_Wind-direction\t"+str(dic1["WindDir"])+"\tFloat"+" "\
                  "data_Pressure\t"+str(dic1["Press"])+"\tFloat"+" "\
                  "data_In-Humidity\t"+str(dic1["InHumi"])+"\tFloat"+" "\
                  "data_Ambient-Humidity\t"+str(dic1["OutHumi"])+"\tFloat"+" "\
                  "data_PWV\t"+str(dic1["None"])+"\tFloat"+" "\
                  "data_Rainfall\t"+str(dic1["Rain"])+"\tFloat"+" "\
                    """
                  #Nagoya Receiver

                  #Assistance for observations

                  #Quick Look
                  #Arran variance
                  #Linearity measurement

                  #Others
                    """


        clientsocket.send(newdata)
        time.sleep(1)

    # close the socket
    print "Closing connection to: ", clientaddr
    clientsocket.close()

if __name__ == "__main__":

    #check_running()

    addr = (HOST, PORT)
    serversocket = socket(AF_INET, SOCK_STREAM)
    serversocket.bind(addr)
    serversocket.listen(2)
    con = controller.read_status()

    while 1:
      print "Server listening for connections"
      clientsocket, clientaddr = serversocket.accept()
      thread.start_new_thread(handler, (clientsocket, clientaddr))
      print "start_new_thread"
    serversocket.close()

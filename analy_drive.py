#! /usr/bin/env python
# coding:utf-8


import sys
import re
import numpy as np
import pylab as pl

fig = pl.figure()
#xr = [0,6800]

argvs = sys.argv 
argc = len(argvs) 
print argvs
print argc
print
if (argc != 2):   
    print 'Usage: # python %s filename' % argvs[0]
    quit()

print 'The content of %s ...n' % argvs[1]
hoge = open(argvs[1],'r')
file = re.split(r'[ ,\n]+',hoge.read())

size = len(file)
new = np.zeros((20,size/20))
#new = np.zeros((16,size/16))
#new = np.zeros((11,size/11))

for i in range(0,20):
    for j in range(0,size/20):
        new[i,j] = file[i+j*20];

"""
for i in range(0,16):
    for j in range(0,size/16):
        new[i,j] = file[i+j*16];
"""
#for i in range(0,11):
    #for j in range(0,size/11):
        #new[i,j] = file[i+j*11];


#----------------------
# plot
#----------------------

#pl.ylim(,)

ax1 = fig.add_subplot(2,2,1)
#pl.plot(new[1,],new[2,]-new[4,],linestyle='None',marker='o')
pl.plot(new[1,],new[2,]-new[4,])
#pl.xlim(xr[0],xr[1])
pl.ylim(-7.0,7.0)
#pl.xlabel("secofday")
pl.ylabel("Az-refAz[arcsec]")

ax2 = fig.add_subplot(2,2,2)
pl.plot(new[1,],new[3,]-new[5,])
#pl.xlim(xr[0],xr[1])
pl.ylim(-7.0,7.0)
#pl.xlabel("secofday")
pl.ylabel("El-refEl[arcsec]")

ax3 = fig.add_subplot(2,2,3)
pl.plot(new[1,],(new[2,]))
pl.plot(new[1,],(new[4,]))
#pl.xlim(xr[0],xr[1])
#pl.ylim(-164.0,-163.0)
pl.xlabel("secofday")
pl.ylabel("Az[arcsec]")

ax4 = fig.add_subplot(2,2,4)
pl.plot(new[1,],new[3,])
pl.plot(new[1,],new[5,])
#pl.xlim(xr[0],xr[1])
#pl.ylim(42.0,43.0)
pl.xlabel("secofday")
pl.ylabel("El[arcsec]")

pl.show()

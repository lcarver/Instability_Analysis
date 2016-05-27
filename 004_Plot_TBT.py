from __future__ import division
import os
import numpy as np
import scipy as sci
from scipy.optimize import leastsq
import h5py
import matplotlib.pyplot as plt
import glob as glob
import re
import mystyle as ms
import config

cf = config.cf()


beam = 'B1'
plane = 'H'


fig = plt.figure(figsize=(8,6))
rect = fig.patch
rect.set_facecolor('white')
ax1 = fig.add_subplot(111)

tbt_filename = '{:s}/TBT_{:s}.h5'.format(cf.output_path,beam)

f = h5py.File(tbt_filename,'r')
tbt_h = f['horizontal'][:]
tbt_v = f['vertical'][:]
time = f.attrs['Start_Time']
f.close()

if plane=='H':
  dat = tbt_h
else:
  dat = tbt_v

turns = np.arange(0,len(dat),1)/(11245*60)
ax1.plot(turns,dat,color='r',linestyle='-',alpha=0.2,label=r'$\mathrm{{Sussix\ Mode\ }}$')
plt.show()

#ax1.plot(turndat,dat,'ro')
#plt.show()

#timelow = 15.5
#timehigh = 16.9

'''

####MAKE FUNCTION THAT CALCULATES THE ENVELOPE
def envelope(dat):
  steps = 50000
  num_of_steps = np.floor(len(dat)/steps)
  max_vals = np.zeros((num_of_steps))
  turn_vals = np.zeros((num_of_steps))

  for i in np.arange(0,num_of_steps-1):
    max_val = np.amax(np.abs(dat)[i*steps:(i+1)*steps])
    max_vals[i] = max_val

    turn_val = steps*i + steps/2
    turn_vals[i] = turn_val

    turn_vals = turn_vals
    mask = turn_vals > 0
  

  return turn_vals[mask], max_vals[mask]

turn_vals, max_vals = envelope(dat)
turn_vals = turn_vals/(11000.*60.)
max_vals = max_vals/np.amax(max_vals)

ax1.plot(turn_vals,max_vals,'go')

#ax1.plot(turndat, coef[0]*turndat + coef[1],'b--',label=r'$\mathrm{{Numerical\ Fit}}\ \tau={:g},\ C={:g}$'.format(coef[0],coef[1]))
ax1.set_xlabel('Time [minutes]')
ax1.set_ylabel('Amplitude')
ax1.legend(loc=2)
plt.show()

'''










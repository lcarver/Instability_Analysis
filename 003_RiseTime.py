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

beam = 'B2'
plane = 'H'
mode_to_fit = 0


fig = plt.figure(figsize=(8,6))
rect = fig.patch
rect.set_facecolor('white')
ax1 = fig.add_subplot(111)

sus_filename = '{:s}/{:s}_Modes_Sussix.h5'.format(cf.output_path, beam)

f = h5py.File(sus_filename,'r')
sus_h = f['Horizontal'][:]
sus_v = f['Vertical'][:]
time = f.attrs['Start_Time']
turn_step = f.attrs['Turn_Step']
modes = f.attrs['Modes']
f.close()

turns = np.arange(0,len(sus_h)*turn_step,turn_step)
if plane=='H':
  dat = sus_h[:,mode_to_fit + 2]
elif plane=='V':
  dat = sus_v[:,mode_to_fit + 2]

dat = dat/np.amax(dat)
datmask = dat > 0.05

dat=dat[datmask]
turndat = turns[datmask]/(11000*60.)

ax1.plot(turndat,dat,color='r',linestyle='',marker='o',alpha=0.2,label=r'$\mathrm{{Sussix\ Mode\ }} {:d}$'.format(mode_to_fit))

timelow=3.2
timehigh=3.44

turnmask = ((turndat > timelow) & (turndat < timehigh))

dat=dat[turnmask]
turndat=turndat[turnmask]


fit_param = np.polyfit(turndat,np.log(dat),1)

ax1.plot(turndat,np.exp(turndat*fit_param[0]+fit_param[1]),'b--',linewidth=2.,label=r'$\mathrm{{Numerical\ Fit}}\ \tau={:g}\mathrm{{\ s}}$'.format(60/fit_param[0]))
ax1.set_xlabel('Time [minutes]')
ax1.set_ylabel('Amplitude')
ax1.legend(loc=2)
ax1.set_ylim(0,1.1)
fig.suptitle('{:s}{:s} Sussix Mode Growth \n Start Time: {:s}'.format(beam, plane, time),fontsize=14)
plt.show()












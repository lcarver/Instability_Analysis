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
import PySUSSIX



filln = 4769
beam = 'B2'
plane = 'H'
mode_to_fit = -2
output_path = '/afs/cern.ch/work/l/lcarver/public/Instability_Data/{:d}'.format(filln)




fig = plt.figure(figsize=(8,6))
rect = fig.patch
rect.set_facecolor('white')
ax1 = fig.add_subplot(111)

tbt_filename = '{:s}/TBT_{:s}.h5'.format(output_path,beam)

f = h5py.File(tbt_filename,'r')
tbt_h = f['horizontal'][:]
tbt_v = f['vertical'][:]
time = f.attrs['Start_Time']
f.close()

if plane=='H':
  dat = tbt_h
else:
  dat = tbt_v

turns = np.arange(0,len(dat),1)
turndat = turns/(11000*60.)

ax1.plot(turndat,dat,color='r',linestyle='',marker='o',alpha=0.2,label=r'$\mathrm{{Sussix\ Mode\ }}$')


#ax1.plot(turndat,dat,'ro')
#plt.show()

#timelow = 15.5
#timehigh = 16.9

timelow=0
timehigh=1
turn_step = 1000

####MAKE FUNCTION THAT CALCULATES THE ENVELOPE


turnmask = ((turndat > timelow) & (turndat < timehigh))

dat=dat[turnmask]
turndat=turndat[turnmask]




def fit_exp(tfit,afit):
  guess_tau=0.25
  guess_off=0.2
  guess_amp = 0.05
  guess_phase = -0.

  data_first_guess = guess_off + guess_amp*np.exp(guess_tau * tfit - guess_phase)

  optimise_func = lambda x: x[0] + x[1]*np.exp(x[2]*tfit - x[3]) - afit

  est_off, est_amp, est_tau, est_phase = leastsq(optimise_func,[guess_off, guess_amp, guess_tau, guess_phase])[0]
  return [est_off, est_amp, est_tau, est_phase]

[est_off,est_amp,est_tau, est_phase] = fit_exp(turndat,dat)
#[est_off,est_amp,est_tau] = [1,15/60,1]


ax1.plot(turndat,est_off + est_amp*np.exp(est_tau*turndat - est_phase),'b--',linewidth=2.,label=r'$\mathrm{{Numerical\ Fit}}\ \tau={:g}\mathrm{{\ s}}$'.format(60/est_tau))

#ax1.plot(turndat, coef[0]*turndat + coef[1],'b--',label=r'$\mathrm{{Numerical\ Fit}}\ \tau={:g},\ C={:g}$'.format(coef[0],coef[1]))
ax1.set_xlabel('Time [minutes]')
ax1.set_ylabel('Amplitude')
ax1.legend(loc=2)
fig.suptitle('{:s}{:s} Sussix Mode Growth'.format(beam,plane),fontsize=18)
#plot_fit()
plt.show()












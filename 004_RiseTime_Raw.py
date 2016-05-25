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




filln = 4914
beam = 'B1'
plane = 'H'
output_path = '/afs/cern.ch/work/l/lcarver/public/Instability_Data/{:d}_Squeeze'.format(filln)



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
turndat = turns

#ax1.plot(turndat[::2],dat[::2],color='r',linestyle='',marker='o',alpha=0.2,label=r'$\mathrm{{Sussix\ Mode\ }}$')


#ax1.plot(turndat,dat,'ro')
#plt.show()

#timelow = 15.5
#timehigh = 16.9



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

timelow=4.4
timehigh=5.

print('lll')

turnmask = ((turn_vals > timelow) & (turn_vals < timehigh))

fit_dat = max_vals[turnmask]
fit_turn = turn_vals[turnmask]




def fit_exp(tfit,afit):
  guess_tau=0.1
  guess_off=0.05
  guess_amp = 0.0002
  guess_phase = timelow

  data_first_guess = guess_off + guess_amp*np.exp( (tfit-guess_phase)/guess_tau)

  optimise_func = lambda x: x[0] + x[1]*np.exp(x[2]*tfit - x[3]) - afit

  est_off, est_amp, est_tau, est_phase = leastsq(optimise_func,[guess_off, guess_amp, guess_tau, guess_phase])[0]
  return [est_off, est_amp, est_tau, est_phase]

[est_off,est_amp,est_tau, est_phase] = fit_exp(turndat,dat)
#[est_off,est_amp,est_tau] = [1,15/60,1]
print est_off, est_amp, est_tau, est_phase

time_plot = np.arange(timelow,timehigh,0.1)
ax1.plot(time_plot,est_off + est_amp*np.exp((time_plot-est_phase)/est_tau),'r',linewidth=3.,label=r'$\mathrm{{Numerical\ Fit}}\ \tau={:g}\mathrm{{\ s}}$'.format(est_tau*60))

#ax1.plot(turndat, coef[0]*turndat + coef[1],'b--',label=r'$\mathrm{{Numerical\ Fit}}\ \tau={:g},\ C={:g}$'.format(coef[0],coef[1]))
ax1.set_xlabel('Time [minutes]')
ax1.set_ylabel('Amplitude')
ax1.legend(loc=2)
fig.suptitle('{:s}{:s} Sussix Mode Growth'.format(beam,plane),fontsize=18)
#plot_fit()
plt.show()
plt.semilogy(max_vals)
plt.show()

#plt.semilogy(turn_vals,max_vals)
#plt.show()












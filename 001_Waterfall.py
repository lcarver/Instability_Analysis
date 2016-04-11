#!/afs/cern.ch/user/p/pyhdtl/public/anaconda/bin/python
from __future__ import division
import os
import numpy as np
import scipy as sci
import h5py
import matplotlib.pyplot as plt
import glob as glob
import re
import mystyle as ms

def plot_waterfall(axes,data_set,turn_split,title):
  data_set_new = np.split(data_set,len(data_set)/turn_split)

  tune_dat = np.fft.rfftfreq(len(data_set_new[0]))

  fft_spectra = np.asarray([np.fft.rfft(data) for data in data_set_new])
  fft_spectra = np.abs(fft_spectra) - np.abs(fft_spectra[0])
  x = tune_dat
  y = np.arange(0,len(data_set),turn_split)

  xx,yy = np.meshgrid(x,y)
  zz = np.abs(fft_spectra)

  axes.pcolormesh(xx,yy,zz)
  #axes.suptitle(title)

fig = plt.figure(figsize=(15,8))
rect = fig.patch
rect.set_facecolor('white')

ax1 = fig.add_subplot(121)
ms.sciy()
ax2 = fig.add_subplot(122,sharex=ax1,sharey=ax1)
ms.sciy()


filln = 4774
beam = 'B1'

output_path = '{:d}/ACQ_HS'.format(filln)

filename = '{:s}/TBT_{:s}.h5'.format(output_path,beam)

f = h5py.File(filename,'r')
tbt_h = f['horizontal'][:]
tbt_v = f['vertical'][:]
time = f.attrs['Start_Time']
f.close()

plot_waterfall(ax1,tbt_h/1e6,2048*4,'Horizontal')
plot_waterfall(ax2,tbt_v/1e6,2048*4,'Vertical')

ax1.set_ylabel('Turns')

ax1.set_xlabel('Tune')
ax1.set_title('Horizontal Spectrum')
ax2.set_title('Vertical Spectrum')
ax2.set_xlabel('Tune')
ax1.set_xlim([0.26,0.33])
ax2.set_xlim([0.26,0.33])
ax1.set_ylim([0,len(tbt_h)])

fig.suptitle('{:s} spectrum on {:s}'.format(beam,time),fontsize=18)

plt.show()



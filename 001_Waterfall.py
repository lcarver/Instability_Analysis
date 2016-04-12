from __future__ import division
import os
import numpy as np
import h5py
import matplotlib.pyplot as plt
import mystyle as ms

def plot_waterfall(axes,data_set,turn_split):
  data_set_new = np.split(data_set,len(data_set)/turn_split)

  tune_dat = np.fft.rfftfreq(len(data_set_new[0]))

  fft_spectra = np.asarray([np.fft.rfft(data) for data in data_set_new])
  fft_spectra = np.abs(np.abs(fft_spectra) - np.abs(fft_spectra[0]))
  x = tune_dat
  y = np.arange(0,len(data_set),turn_split)

  xx,yy = np.meshgrid(x,y)
  zz = fft_spectra
  axes.pcolormesh(xx,yy,zz)




filln = 4769
output_path = '/afs/cern.ch/work/l/lcarver/public/Instability_Data/{:d}/'.format(filln)


for beam in ['B1','B2']:
  fig = plt.figure(figsize=(15,8))
  rect = fig.patch
  rect.set_facecolor('white')

  ax1 = fig.add_subplot(121)
  ms.sciy()
  ax2 = fig.add_subplot(122)
  ms.sciy()

  filename = '{:s}/TBT_{:s}.h5'.format(output_path,beam)


  f = h5py.File(filename,'r')
  tbt_h = f['horizontal'][:]
  tbt_v = f['vertical'][:]
  time = f.attrs['Start_Time']
  f.close()

  plot_waterfall(ax1,tbt_h/1e6,2048*4)
  plot_waterfall(ax2,tbt_v/1e6,2048*4)

  ax1.set_ylabel('Turns')

  ax1.set_xlabel('Tune')
  ax1.set_title('Horizontal Spectrum')
  ax2.set_title('Vertical Spectrum')
  ax2.set_xlabel('Tune')
  ax1.set_xlim([0.26,0.3])
  ax2.set_xlim([0.3,0.33])
  ax1.set_ylim([0,len(tbt_h)])
  ax2.set_ylim([0,len(tbt_h)])

  fig.suptitle('{:s} spectrum on {:s}'.format(beam,time),fontsize=18)
  fig.savefig('{:s}{:s}_{:s}.png'.format(output_path,'Waterfall',beam))

plt.show()



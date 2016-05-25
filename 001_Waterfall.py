from __future__ import division
import os
import numpy as np
import h5py
import matplotlib.pyplot as plt
import mystyle as ms
import config

def plot_waterfall(axes,data_set,turn_split):

  n_array = int(np.floor(len(data_set)/turn_split))
  data_set_2 = data_set[:n_array*turn_split]
  data_set_new = np.split(data_set_2, n_array)

  tune_dat = np.fft.rfftfreq(len(data_set_new[0]))

  fft_spectra = np.asarray([np.abs(np.fft.rfft(data)) for data in data_set_new])
  x = tune_dat
  y = np.arange(0,len(data_set_2),turn_split)

  xx,yy = np.meshgrid(x,y)
  zz = np.log(fft_spectra)

  axes.pcolormesh(xx,yy,zz)


cf = config.cf()

for beam in ['B1','B2']:
  fig = plt.figure(figsize=(15,8))
  rect = fig.patch
  rect.set_facecolor('white')

  ax1 = fig.add_subplot(121)
  ms.sciy()
  ax2 = fig.add_subplot(122)
  ms.sciy()

  filename = '{:s}/TBT_{:s}.h5'.format(cf.output_path, beam)


  f = h5py.File(filename,'r')
  tbt_h = f['horizontal'][:]
  tbt_v = f['vertical'][:]
  time = f.attrs['Start_Time']
  f.close()

  plot_waterfall(ax1, tbt_h/1e6, 2048*8)
  plot_waterfall(ax2, tbt_v/1e6, 2048*8)

  ax1.set_ylabel('Turns')

  ax1.set_xlabel('Tune')
  ax1.set_title('Horizontal Spectrum')
  ax2.set_title('Vertical Spectrum')
  ax2.set_xlabel('Tune')
  ax1.set_xlim([0.26,0.33])
  ax2.set_xlim([0.26,0.33])
  ax1.set_ylim([0,len(tbt_h)])
  ax2.set_ylim([0,len(tbt_h)])

  fig.suptitle('{:s} spectrum from {:s}'.format(beam,time),fontsize=18)
  fig.savefig('{:s}{:s}_{:s}.png'.format(cf.output_path,beam, 'Waterfall'))


plt.show()



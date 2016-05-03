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
import PySUSSIX

def calc_sussix_spectra(x, y, window_width, q_x, q_y, n_lines=2):

    SX = PySUSSIX.Sussix()
    SX.sussix_inp(nt1=1, nt2=window_width, idam=2, ir=0, tunex=q_x, tuney=q_y)

    SX.sussix(x, np.zeros(len(x)),
              y, np.zeros(len(y)),
              x, x) # this line is not used by sussix!

    return SX

def filter_SX(SX):
  mask_x = ((0.275 < SX.ox) & (SX.ox < 0.295))
  mask_y = ((0.295 < SX.oy) & (SX.oy < 0.32))

  SX.ox = SX.ox[mask_x]
  SX.ax = SX.ax[mask_x]


  SX.oy = SX.oy[mask_y]
  SX.ay = SX.ay[mask_y]



filln = 4805
tag = 'QDecrease'
beam = 'B2'
n_lines = 20

output_path = '/afs/cern.ch/work/l/lcarver/public/Instability_Data/{:d}_{:s}'.format(filln,tag)

tbt_filename = '{:s}/TBT_{:s}.h5'.format(output_path,beam)

f = h5py.File(tbt_filename,'r')
tbt_h = f['horizontal'][:]
tbt_v = f['vertical'][:]
time = f.attrs['Start_Time']
f.close()

turn_split = 512*2
num_arr = int(np.floor(len(tbt_h)/turn_split))
turn_num = num_arr*turn_split

data_h = np.split(tbt_h[:turn_num],num_arr)
data_v = np.split(tbt_v[:turn_num],num_arr)



turns = turn_split*np.arange(0,len(data_h),1)+turn_split/2
peaks_h = np.zeros((len(data_h),2,n_lines))
peaks_v = np.zeros((len(data_v),2,n_lines))

i=0
for dat_h, dat_v in zip(data_h, data_v):
  SX = calc_sussix_spectra(dat_h,dat_v,turn_split,0.28,0.31)  
  #filter_SX(SX)
  peaks_h[i,:,:] = np.array([SX.ox[:n_lines],SX.ax[:n_lines]])
  peaks_v[i,:,:] = np.array([SX.oy[:n_lines],SX.ay[:n_lines]])
  
  i=i+1

f = h5py.File('{:s}/{:s}_Sussix_Tunes.h5'.format(output_path,beam),'w')
hor = f.create_group('Horizontal')
ver = f.create_group('Vertical')

for j in np.arange(n_lines):
  hor.create_dataset('Peak_{:g}'.format(j), data=peaks_h[:,:,j])
  ver.create_dataset('Peak_{:g}'.format(j), data=peaks_v[:,:,j])
f.attrs['Turn_Split'] = turn_split
f.attrs['Start_Time'] = time
f.close()







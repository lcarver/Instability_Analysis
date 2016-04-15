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

def calc_sussix_spectra(x, y, window_width, q_x, q_y, n_lines=50):

    SX = PySUSSIX.Sussix()
    SX.sussix_inp(nt1=1, nt2=window_width, idam=2, ir=0, tunex=q_x, tuney=q_y)

    SX.sussix(x, np.zeros(len(x)),
              y, np.zeros(len(y)),
              x, x) # this line is not used by sussix!

    return SX

def filter_SX(SX):
  mask_x = SX.ox > 0
  SX.ox = SX.ox[mask_x]
  SX.ax = SX.ax[mask_x]

  mask_y = SX.oy > 0
  SX.oy = SX.oy[mask_y]
  SX.ay = SX.ay[mask_y]

def sort_SX(SX,plane):
  Qs = 2e-3
  if plane=='x':
    q_ = SX.tunex
    peaks = SX.ox
    amps = SX.ax
  if plane=='y':
    q_ = SX.tuney
    peaks = SX.oy
    amps = SX.ay
      
  modes = {'Mode_0':[],'Mode_1':[],'Mode_-1':[],
           'Mode_2':[],'Mode_-2':[]}

  for peak,amp in zip(peaks,amps):
    i=-2
    while i<2:
     if q_ + i*Qs -Qs/2 < peak < q_ + i*Qs + Qs/2:
       arr = modes['Mode_{:s}'.format(str(i))]
       arr.append([peak,amp])
       break 
     else:
       i+=1
  all_modes = {}
  for key in modes.keys():

    if len(modes[key])==0:
      all_modes[key] = np.array([0,0])

    if len(modes[key])>=1:
      all_modes[key] = np.array(max(modes[key]))

  return all_modes
 



filln = 4769
beam = 'B1'

output_path = '/afs/cern.ch/work/l/lcarver/public/Instability_Data/{:d}'.format(filln)

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

full_dict_x = {'Mode_0':[],'Mode_1':[],'Mode_-1':[],
           'Mode_2':[],'Mode_-2':[]}
full_dict_y = {'Mode_0':[],'Mode_1':[],'Mode_-1':[],
           'Mode_2':[],'Mode_-2':[]}

for dat_h, dat_v in zip(data_h, data_v):
  SX = calc_sussix_spectra(dat_h,dat_v,turn_split,0.28,0.31)
  filter_SX(SX)
  modes_x = sort_SX(SX,'x')
  modes_y = sort_SX(SX,'y')

  for key_x in modes_x.keys():
    full_dict_x[key_x].append(modes_x[key_x])

  for key_y in modes_y.keys():
    full_dict_y[key_y].append(modes_y[key_y])

hor_sus = np.zeros((num_arr,5))
ver_sus = np.zeros((num_arr,5))

for key in full_dict_x.keys():
  mode = int(key.split('_')[1])
  for it1, arr in enumerate(full_dict_x[key]):
    hor_sus[it1][mode+2] = arr[1]
  for it2, arr in enumerate(full_dict_y[key]):
    ver_sus[it2][mode+2] = arr[1]



f = h5py.File('{:s}/{:s}_Modes_Sussix.h5'.format(output_path,beam),'w')
f.create_dataset('Horizontal',data=hor_sus)
f.create_dataset('Vertical',data=ver_sus)
f.attrs['Modes']=[-2,-1,0,1,2]  
f.attrs['Start_Time'] = time
f.attrs['Turn_Step'] = turn_split
f.close()







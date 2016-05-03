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


filln = 4805
tag = 'QDecrease'
beam = 'B2'

output_path = '/afs/cern.ch/work/l/lcarver/public/Instability_Data/{:d}_{:s}'.format(filln,tag)

sus_filename = '{:s}/{:s}_Sussix_Tunes.h5'.format(output_path,beam)

f = h5py.File(sus_filename,'r')
turn_split = f.attrs['Turn_Split']
sus_h = f['Horizontal']
sus_v = f['Vertical']
time = f.attrs['Start_Time']
tune_h = sus_h['Peak_0']
tune_v = sus_v['Peak_0']

tune_h2 = np.zeros((len(tune_h),2))
tune_v2 = np.zeros((len(tune_v),2))

turns = turn_split*np.arange(0,len(tune_h)) + turn_split/2


#crossing_turn = 125000
#crossing_turn = 150000

#for j in np.arange(0,len(tune_h),1):
#  for i in np.arange(1,18,1):
#    peak = 'Peak_{:d}'.format(i)
#    if ((sus_h[peak][j][0] > 0.275) & (sus_h[peak][j][0] < 0.295)):
#        tune_h2[j] = sus_h[peak][j]
#    if ((sus_v[peak][j][0] > 0.29) & (sus_v[peak][j][0] < 0.5)):
#        tune_v2[j] = sus_v[peak][j]

#    else:
#        print 'No tune in window'


#f1001 = 0.5*np.arctan(np.sqrt((tune_h2[:,1]*tune_v2[:,1])/(tune_h[:,1]*tune_v[:,1])))
#Cminus = 4*np.abs(f1001)*np.abs(tune_v[:,0]-tune_h[:,0])


fig = plt.figure(figsize=(8,6))
rect = fig.patch
rect.set_facecolor('white')
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

#ax1.plot(0.28,'g-',label=r'$C^{{-}}$')
ax1.plot(turns,tune_h[:,0],'ro',label=r'$Q_{{h}}$')
ax1.plot(turns,tune_v[:,0],'bo',label=r'$Q_{{v}}$')

def calc_cminus(tune_h,tune_v,mid_point):
  arr_1 = tune_h > mid_point
  arr_2 = tune_v > mid_point
  pk_1 = np.amin(np.concatenate((tune_h[arr_1],tune_v[arr_2])))

  arr_1 = tune_h < mid_point
  arr_2 = tune_v < mid_point
  pk_2 = np.amax(np.concatenate((tune_h[arr_1],tune_v[arr_2])))

  return [pk_1,pk_2,np.abs(pk_2 - pk_1)]

#[pk_1, pk_2, cminus] = calc_cminus(tune_h[:,0], tune_v[:,0], 0.295)
#ax1.axhline(y=pk_1,color='g',linestyle='dashed',label=r'$|C^{{-}}|={:g}$'.format(cminus))
#ax1.axhline(y=pk_2,color='g',linestyle='dashed')


#ax1.set_title(r'$C^{{-}}={:g}$'.format(cminus),fontsize=18)
ax1.set_title('Tunes for {:s} from {:s}'.format(beam, time),fontsize=14)

ax1.set_xlabel('Turns')
ax1.set_ylabel('Fractional Tune')
ax1.legend(loc=1)
#turns_mask = turns > crossing_turn
#ax2.plot(turns[turns_mask],Cminus[turns_mask],'g-',label=r'$C^{{-}}$')
plt.savefig('{:s}/Crossing.png'.format(output_path))

plt.show()

f.close()







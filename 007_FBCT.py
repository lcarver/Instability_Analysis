import numpy as np
import h5py as h5
import matplotlib.pyplot as plt

filln = 4927
beam = 'B2'

output_dir = '/afs/cern.ch/work/l/lcarver/public/Instability_Data/{:d}/'.format(filln)

f = h5.File('{:s}/FBCT_{:s}.h5'.format(output_dir, beam),'r')
start_time_str = f.attrs['Start_Time_Str']
start_time = f.attrs['Start_Time']
time_step = f.attrs['Time_Step']

is_filled = f[beam][-100,:] > 8e9
filled_index = np.arange(0,3564)[is_filled]


fig = plt.figure(figsize=(8,6))
rect = fig.patch
rect.set_facecolor('white')
ax1 = fig.add_subplot(111)



for bucket in filled_index:
  int_dat = f[beam][:,bucket]
  bucket_int = np.max(int_dat)

  int_dat /= bucket_int
  time_dat = np.arange(0,len(int_dat),1)*time_step

  ax1.plot(time_dat, int_dat*100, label=r'$\mathrm{{Bucket\ {:g}}}: N_{{b}}={:g}\mathrm{{e11}}$'.format(bucket,bucket_int/1e11))


ax1.legend(loc=3)
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Norm. Intensity [%]')
fig.suptitle('FBCT {:s} \n Time Since: {:s}'.format(beam, start_time_str),fontsize=14)

plt.show()

f.close()
  



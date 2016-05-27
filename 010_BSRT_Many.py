import numpy as np
import h5py
import config
import matplotlib.pyplot as plt

cf = config.cf()

f = h5py.File('{:s}/BSRT_B1.h5'.format(cf.output_path),'r')

time_start = f.attrs['Start_Time']
filled_buckets = f.attrs['Buckets']

batch = 4
if batch==1:
  bucket_start = 218
  bucket_end = 289
elif batch==2:
  bucket_start = 327
  bucket_end = 398
elif batch==3:
  bucket_start = 436
  bucket_end = 507
elif batch==4:
  bucket_start = 545
  bucket_end = 616
  

mask = filled_buckets == bucket_start
index_start = np.arange(0,len(filled_buckets),1)[mask][0]

mask = filled_buckets == bucket_end
index_end = np.arange(0,len(filled_buckets),1)[mask][0]

fig = plt.figure(figsize=(12,8))
rect = fig.patch
rect.set_facecolor('white')


ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

data_h = f['sigma_h']
data_v = f['sigma_v']
dat_t =  f['Time_Stamps']


for kk, i in enumerate(np.arange(index_start,index_end,1)):
  t_dat = dat_t[:,i]
  t_mask = t_dat > 0
  t_dat = t_dat[t_mask]

  h_dat = data_h[:,i][t_mask]
  v_dat = data_v[:,i][t_mask]

  if h_dat[-1] > 1.2*h_dat[0]:
    ax1.plot((t_dat-time_start)/60, h_dat,label='Bunch {:d}'.format(kk))
  if v_dat[-1] > 1.2*v_dat[0]:
    ax2.plot((t_dat-time_start)/60, v_dat,label='Bunch {:d}'.format(kk))

ax1.set_title('Horizontal',fontsize=12)
ax2.set_title('Vertical',fontsize=12)
ax1.set_xlabel('Time [minutes]',fontsize=14)
ax2.set_xlabel('Time [minutes]',fontsize=14)
ax1.set_ylabel(r'$\sigma_{{H}}$',fontsize=14)
ax2.set_ylabel(r'$\sigma_{{V}}$',fontsize=14)

ax1.legend(loc=2)
ax2.legend(loc=2)
fig.suptitle('BSRT for B1. Batch from bucket {:g} to {:g}\nTime since: {:s}'.format(bucket_start, bucket_end, f.attrs['Time_Start_STR']),fontsize=16)
plt.savefig('{:s}/Batch_{:d}_BSRT.png'.format(cf.output_path,batch))
plt.show()

f.close()

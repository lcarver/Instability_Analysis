import time
import numpy as np
import matplotlib.pyplot as plt
import pytimber
import h5py

filln = 4927
beam = 'B1'

output_path = '/afs/cern.ch/work/l/lcarver/public/Instability_Data/{:g}/'.format(filln)

bsrt_f = h5py.File(output_path + 'BSRT_{:s}.h5'.format(beam),'r')
time_start = bsrt_f['Time_Stamps'][0]
time_end = bsrt_f['Time_Stamps'][-1]

mdb = pytimber.LoggingDB(source='mdb')
b1h_bbq = mdb.get('LHC.BQBBQ.CONTINUOUS_HS.B1:EIGEN_AMPL_1',time_start, time_end)['LHC.BQBBQ.CONTINUOUS_HS.B1:EIGEN_AMPL_1']
b1v_bbq = mdb.get('LHC.BQBBQ.CONTINUOUS_HS.B1:EIGEN_AMPL_2',time_start, time_end)['LHC.BQBBQ.CONTINUOUS_HS.B1:EIGEN_AMPL_2']
b2h_bbq = mdb.get('LHC.BQBBQ.CONTINUOUS_HS.B2:EIGEN_AMPL_1',time_start, time_end)['LHC.BQBBQ.CONTINUOUS_HS.B2:EIGEN_AMPL_1']
b2v_bbq = mdb.get('LHC.BQBBQ.CONTINUOUS_HS.B2:EIGEN_AMPL_2',time_start, time_end)['LHC.BQBBQ.CONTINUOUS_HS.B2:EIGEN_AMPL_2']

fig = plt.figure(figsize=(8,6))
rect = fig.patch
rect.set_facecolor('white')
ax1 = fig.add_subplot(111)

if beam == 'B1':
  ax1.plot(b1h_bbq[0]-time_start,b1h_bbq[1],'b',label='BBQ B1H')
  ax1.plot(b1v_bbq[0]-time_start,b1v_bbq[1],'r',label='BBQ B1V')
elif beam == 'B2':
  ax1.plot(b2h_bbq[0]-time_start,b2h_bbq[1],'b',label='BBQ B2H')
  ax1.plot(b2v_bbq[0]-time_start,b2v_bbq[1],'r',label='BBQ B2V')


ax2 = ax1.twinx()
col = ['k','b','g','p']
for i, bucket in enumerate(bsrt_f.attrs['Buckets']): 
  ax2.plot(bsrt_f['Time_Stamps'] - time_start, bsrt_f['sigma_h'][:,i],color=col[i],linestyle='-',label=r'$\sigma_{{h}},\mathrm{{Bucket\ }}{:g}$'.format(bucket))
  ax2.plot(bsrt_f['Time_Stamps'] - time_start, bsrt_f['sigma_v'][:,i],color=col[i],linestyle='--',label=r'$\sigma_{{v}},\mathrm{{Bucket\ }}{:g}$'.format(bucket))


ax1.legend(loc=3,frameon=False)
ax2.legend(loc=2,frameon=False)
ax2.set_ylim([0,0.9])

ax1.set_xlabel('Time [s]')
ax1.set_ylabel('BBQ Amp [A.U.]')
ax2.set_ylabel('BSRT_Sigma [mm]')
fig.suptitle('BSRT and BBQ: {:s}, Fill = {:g} \nTime Since: {:s}'.format(beam,filln,bsrt_f.attrs['Time_Start_STR']),fontsize=14)
plt.savefig(output_path + 'BSRT_BBQ_{:s}.png'.format(beam))
plt.show()



bsrt_f.close()

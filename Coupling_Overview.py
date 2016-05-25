import pytimber
import numpy as np
import datetime
import seaborn
import matplotlib.pyplot as plt
plt.rc('xtick', labelsize=14)
plt.rc('ytick', labelsize=14)

db = pytimber.LoggingDB(source='mdb')


t1 = '2016-05-11 14:05:01'
t2 = '2016-05-12 12:00:01'

fillns = db.get('HX:FILLN', t1,t2)['HX:FILLN']  

def unix_to_local(time):
  return datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')

index = 1

for index in range(len(fillns[0])-1):
  time_start = unix_to_local(fillns[0][index])
  time_end = unix_to_local(fillns[0][index+1])
  filln = fillns[1][index]



  b1_int = db.get('LHC.BCTDC.A6R4.B1:BEAM_INTENSITY', time_start, time_end)['LHC.BCTDC.A6R4.B1:BEAM_INTENSITY']
  #b2_int = db.get('LHC.BCTDC.A6R4.B2:BEAM_INTENSITY', time_start, time_end)['LHC.BCTDC.A6R4.B2:BEAM_INTENSITY']
  energy = db.get('LHC.BOFSU:OFC_ENERGY', time_start, time_end)['LHC.BOFSU:OFC_ENERGY']

  bbq_b1h = db.get('LHC.BQBBQ.CONTINUOUS_HS.B1:EIGEN_AMPL_1', time_start, time_end)['LHC.BQBBQ.CONTINUOUS_HS.B1:EIGEN_AMPL_1']
  bbq_b1v = db.get('LHC.BQBBQ.CONTINUOUS_HS.B1:EIGEN_AMPL_2', time_start, time_end)['LHC.BQBBQ.CONTINUOUS_HS.B1:EIGEN_AMPL_2']
  bbq_coup = db.get('LHC.BQBBQ.CONTINUOUS_HS.B1:COUPLING_ABS', time_start, time_end)['LHC.BQBBQ.CONTINUOUS_HS.B1:COUPLING_ABS']

  #bbq_b2h = db.get('LHC.BQBBQ.CONTINUOUS_HS.B2:EIGEN_AMPL_1', time_start, time_end)['LHC.BQBBQ.CONTINUOUS_HS.B2:EIGEN_AMPL_1']
  #bbq_b2v = db.get('LHC.BQBBQ.CONTINUOUS_HS.B2:EIGEN_AMPL_2', time_start, time_end)['LHC.BQBBQ.CONTINUOUS_HS.B2:EIGEN_AMPL_2']

  beta_ip1 = db.get('HX:BETASTAR_IP1', time_start, time_end)['HX:BETASTAR_IP1']
  beta_ip5 = db.get('HX:BETASTAR_IP5', time_start, time_end)['HX:BETASTAR_IP5']

  fig = plt.figure(figsize=((15,8)))
  ax1 = fig.add_subplot(111)


  ax1.set_title('Fill {:d}, Time Start: {:s}'.format(int(filln), time_start),fontsize=16)
  ax1.plot(b1_int[0]-fillns[0][index], b1_int[1],'r-')
  #ax1.plot(b2_int[0]-fillns[0][index], b2_int[1],'b-')

  ax2 = ax1.twinx()
  ax2.plot(bbq_b1h[0]-fillns[0][index],bbq_b1h[1], label='B1H')
  ax2.plot(bbq_b1v[0]-fillns[0][index],bbq_b1v[1], label='B1V')
  ax2.plot(bbq_coup[0]-fillns[0][index], bbq_coup[1], label='|C-|')
  #ax2.plot(bbq_b2h[0]-fillns[0][index],bbq_b2h[1], label='B2H')
  #ax2.plot(bbq_b2v[0]-fillns[0][index],bbq_b2v[1], label='B2V')
  ax2.plot(0,0,'b--',label='IP1')
  ax2.plot(0,0,'r--',label='IP5')
  


  ax3 = ax1.twinx()
  ax3.plot(energy[0]-fillns[0][index],energy[1],'k-')
  ax3.set_ylim([400,6700])
  ax3.spines['right'].set_position(('axes', 1.1))


  ax4 = ax1.twinx()
  ax4.plot(beta_ip1[0]-fillns[0][index],beta_ip1[1]/100, 'b--')
  ax4.plot(beta_ip5[0]-fillns[0][index], beta_ip5[1]/100, 'r--')
  ax4.spines['right'].set_position(('axes',1.2))


  ax2.legend(loc=2,fontsize=16)
  ax2.grid(False)
  ax3.grid(False)
  ax4.grid(False)
  ax1.set_ylim([-1e9,np.average(b1_int[1])*3])
  ax1.set_xlim([0,np.max(b1_int[0]-fillns[0][index])])
  ax4.set_ylim([0,12])
  ax1.set_xlabel('Time [s]',fontsize=16)
  ax1.set_ylabel('Bunch Intensity [ppb]',fontsize=16)
  ax2.set_ylabel('BBQ Amp',fontsize=16)
  ax3.set_ylabel('Energy [GeV]',fontsize=16)
  ax4.set_ylabel('BetaStar [m]',fontsize=16)
  
  plt.subplots_adjust(right=0.8)
  plt.show()
  #plt.savefig('/afs/cern.ch/work/l/lcarver/private/FillbyFill_Analysis/Plots/{:d}.png'.format(int(filln)))















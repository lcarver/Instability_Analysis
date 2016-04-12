import pytimber
import numpy as np
import os
import h5py


mdb = pytimber.LoggingDB(source='mdb')
t1 = '2016-04-07 07:59:00.000'
t2 = '2016-04-07 08:00:20.000'

#fills = mdb.get('HX:FILLN',t1,t2)
#filln = int(fills['HX:FILLN'][1][-1])
filln=4769
print 'Fill number = {:d}'.format(filln)

output_path = os.path.join('/afs/cern.ch/work/l/lcarver/public/Instability_Data','{:d}'.format(filln))

if not os.path.exists(output_path):
  os.mkdir(output_path)


for beam in ['B1','B2']: 
  var = 'LHC.BQBBQ.CONTINUOUS_HS.{:s}:ACQ_DATA_{:s}'.format(beam,'H')
  d=mdb.get(var,t1,t2)
  f = h5py.File(output_path + '/TBT_{:s}.h5'.format(beam),'w')
  f.create_dataset('horizontal', data=np.concatenate(d[var][1]))

  var = 'LHC.BQBBQ.CONTINUOUS_HS.{:s}:ACQ_DATA_{:s}'.format(beam,'V')
  d=mdb.get(var,t1,t2)
  f.create_dataset('vertical', data=np.concatenate(d[var][1]))
  f.attrs['Start_Time'] = t1
  f.attrs['Fill'] = filln

  f.close()
    
    









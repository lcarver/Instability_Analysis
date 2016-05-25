import pytimber
import numpy as np
import os
import h5py
import config


cf = config.cf()

mdb = pytimber.LoggingDB(source='mdb')

print 'Fill number = {:d}'.format(cf.filln)
if cf.tag=='':
  print('No tag')
else:
  print(cf.tag)

if not os.path.exists(cf.output_path):
  os.mkdir(cf.output_path)


for beam in ['B1','B2']: 

  var = 'LHC.BQBBQ.CONTINUOUS_HS.{:s}:ACQ_DATA_{:s}'.format(beam,'H')
  d=mdb.get(var, cf.t1, cf.t2)
  f = h5py.File('{:s}/TBT_{:s}.h5'.format(cf.output_path, beam),'w')
  f.create_dataset('horizontal', data=np.concatenate(d[var][1]))

  var = 'LHC.BQBBQ.CONTINUOUS_HS.{:s}:ACQ_DATA_{:s}'.format(beam,'V')
  d=mdb.get(var, cf.t1, cf.t2)
  f.create_dataset('vertical', data=np.concatenate(d[var][1]))
  f.attrs['Start_Time'] = cf.t1
  f.attrs['Fill'] = cf.filln

  f.close()


  f = h5py.File('{:s}/FBCT_{:s}.h5'.format(cf.output_path, beam),'w')
  var = 'LHC.BCTFR.A6R4.{:s}:BUNCH_INTENSITY'.format(beam)
  d=mdb.get(var, cf.t1, cf.t2)
  f.create_dataset('{:s}'.format(beam), data=d[var][1])
  f.attrs['Time_Step'] = d[var][0][1] - d[var][0][0]
  f.attrs['Start_Time'] = d[var][0][0]
  f.attrs['Start_Time_Str'] = cf.t1
  f.attrs['Fill'] = cf.filln
  f.close()

  if beam=='B1':
    bsrt_var = ['LHC.BSRT.5R4.B1:GATE_DELAY',
                'LHC.BSRT.5R4.B1:FIT_SIGMA_H',
                'LHC.BSRT.5R4.B1:FIT_SIGMA_V']
  elif beam=='B2':
    bsrt_var = ['LHC.BSRT.5L4.B2:GATE_DELAY',
                'LHC.BSRT.5L4.B2:FIT_SIGMA_H',
                'LHC.BSRT.5L4.B2:FIT_SIGMA_V']

  gate_delay_var = bsrt_var[0]
  gate_delay_dat = mdb.get(gate_delay_var, cf.t1, cf.t2)[gate_delay_var]
  filled_buckets = np.array(list(set([item for sublist in gate_delay_dat[1] for item in sublist]
)))
  filled_buckets = [int(i) for i in filled_buckets]
  sigma_h_var = bsrt_var[1]
  sigma_h_dat = mdb.get(sigma_h_var, cf.t1, cf.t2)[sigma_h_var]

  sigma_v_var = bsrt_var[2]
  sigma_v_dat = mdb.get(sigma_v_var, cf.t1, cf.t2)[sigma_v_var]

  bsrt_data = {}
  for bucket in filled_buckets:

    bucket_dict = {}
    time_dat = sigma_h_dat[0]
    sigma_h = []
    sigma_v = []
    std_h = []
    std_v = []

    for i, gate in enumerate(gate_delay_dat[1]):
      mask = gate == bucket  
      dat_h = sigma_h_dat[1][i][mask]
      dat_v = sigma_v_dat[1][i][mask]
      std_h.extend([np.std(dat_h)])
      std_v.extend([np.std(dat_v)])
      sigma_h.extend([np.mean(dat_h)])
      sigma_v.extend([np.mean(dat_v)])

    bucket_dict['time_stamps'] = time_dat
    bucket_dict['std_h'] = std_h
    bucket_dict['std_v'] = std_v
    bucket_dict['sigma_h'] = sigma_h
    bucket_dict['sigma_v'] = sigma_v
    bsrt_data['Bucket_{:g}'.format(bucket)] = bucket_dict


  f = h5py.File('{:s}/BSRT_{:s}.h5'.format(cf.output_path, beam),'w')
  f.attrs['Buckets'] = filled_buckets
  f.attrs['Time_Start_STR'] = cf.t1
  f.create_dataset('Time_Stamps', data=bsrt_data[bsrt_data.keys()[0]]['time_stamps'])

  tup_h = []
  tup_v = []
  tup_sh = []
  tup_sv = []
  for key in bsrt_data.keys():
    tup_h.append(bsrt_data[key]['sigma_h'])
    tup_v.append(bsrt_data[key]['sigma_v'])
    tup_sh.append(bsrt_data[key]['std_h'])
    tup_sv.append(bsrt_data[key]['std_v'])

  f.attrs['Start_Time_Str'] = cf.t1
  f.attrs['Fill'] = cf.filln
  f.create_dataset('sigma_h', data=np.vstack(tuple(tup_h)).T)
  f.create_dataset('sigma_v', data=np.vstack(tuple(tup_v)).T)
  f.create_dataset('std_h', data=np.vstack(tuple(tup_sh)).T)
  f.create_dataset('std_v', data=np.vstack(tuple(tup_sv)).T)
  f.close()
  print('{:s} is finished!'.format(beam))
  
  
 









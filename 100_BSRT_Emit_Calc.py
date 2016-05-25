#!/afs/cern.ch/user/p/pyhdtl/public/anaconda/bin/python
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import os
from Tools.TimberManager import local2seconds as lt


filln = 4574
beam = 2
plane = 'H'
plot_emittance = True
beam_energy_for_emittance = 6500

path_to_bsrt = '/afs/cern.ch/work/l/lcarver/public/LHC_DATA/{:d}/BSRT/'.format(filln)

def l_or_r(beam):
  if beam==1:
    return 'R'
  else:
    return 'L'

def read_timber(filename):
  with open(filename) as fid:
    lines = fid.readlines()
    times = []
    data = []

    for i,line in enumerate(lines):
      if line[:8]=='VARIABLE':
        print 'FOUND: {:s}'.format(line[10:])
      elif line=='\n':
        pass    
      elif line[:9]=='Timestamp':
        pass
      else:
        line_time = line[:23]
        data_string = line[24:-1]
        if data_string[0]==',':
          data_string = data_string[1:]
        data.append(np.float_(data_string.split(',')))
        times.append(line_time)
  file_dict = {}
  file_dict['Timestamps']=times
  file_dict['Values']=data
  return file_dict

def emittance_dictionary():
  e_dict = {'betaf_h':{}, 'betaf_v':{}, 'gamma':{},
              'sigma_corr_h':{}, 'sigma_corr_v':{}}
  e_dict['betaf_h'][450] = {1:203.47, 2:200.73}
  e_dict['betaf_v'][450] = {1:317.45, 2:327.75}
  e_dict['betaf_h'][6500] = {1:204.1, 2:191.5}
  e_dict['betaf_v'][6500] = {1:322.7, 2:395}
  e_dict['gamma'][450] = 479.6
  e_dict['gamma'][6500] = 6927.6
  e_dict['sigma_corr_h'][450] = 0.85
  e_dict['sigma_corr_v'][450] = 0.87
#  e_dict['sigma_corr_h'][6500] = {1:0.37, 2:0.336}
#  e_dict['sigma_corr_v'][6500] = {1:0.3, 2:0.36} 
  e_dict['sigma_corr_h'][6500] = {1:0.2, 2:0.2}
  e_dict['sigma_corr_v'][6500] = {1:0.2, 2:0.2} 

  return e_dict

#filename_data = path_to_bsrt + 'LHC.BSRT.5{:s}4.B{:d}:FIT_SIGMA_{:s}.csv'.format(l_or_r(beam),beam,plane)
#filename_gate = path_to_bsrt + 'LHC.BSRT.5{:s}4.B{:d}:GATE_DELAY.csv'.format(l_or_r(beam),beam)
filename_data = path_to_bsrt + 'LHC.BSRT.5{:s}4.B{:d}:FIT_SIGMA_{:s}.csv'.format(l_or_r(beam),beam,plane)
filename_gate = path_to_bsrt + 'LHC.BSRT.5{:s}4.B{:d}:GATE_DELAY.csv'.format(l_or_r(beam),beam)
#filename_data = path_to_bsrt + 'LHC.BSRT.5{:s}4.B{:d}_FIT_SIGMA_{:s}.csv'.format(l_or_r(beam),beam,plane)
#filename_gate = path_to_bsrt + 'LHC.BSRT.5{:s}4.B{:d}_GATE_DELAY.csv'.format(l_or_r(beam),beam)

e_dict = emittance_dictionary()

gate_dict = read_timber(filename_gate)
data_dict = read_timber(filename_data)
gate_start_time = gate_dict['Timestamps'][0]

def parse_bsrt(gate_dict,data_dict):
  all_dict = {}
  for i,array in enumerate(gate_dict['Values']):
    single_stamp = lt(gate_dict['Timestamps'][i])
    acq_dict = {}
    for j,item in enumerate(array):
      item = int(item)
      if not (item in acq_dict.keys()):
        acq_dict[item]=[]
      acq_dict[item].append(data_dict['Values'][i][j])

    for key in acq_dict.keys():
      if not (key in all_dict.keys()):
        all_dict[key]=[]
      all_dict[key].append([single_stamp,acq_dict[key]])
  return all_dict

all_dict = parse_bsrt(gate_dict,data_dict)

def process_dict(all_dict,num_of_acq):
  processed_dict = {}
  for bunch in all_dict.keys():
    bunch_dict = {}
    plot_time = np.asarray([i[0] for i in all_dict[bunch]])
    plot_time = plot_time
    bunch_dict['Timestamps'] = plot_time

    beta_f = e_dict['betaf_{:s}'.format(plane.lower())][beam_energy_for_emittance][beam]
    gamma = e_dict['gamma'][beam_energy_for_emittance]
    corr_factor = e_dict['sigma_corr_{:s}'.format(plane.lower())][beam_energy_for_emittance][beam]

    mean_emit_array = []
    std_emit_array = []

    emit_array = []

    for i in all_dict[bunch]:
      fit_for_acq = np.asarray(i[1])

      sigma_corr_squared = fit_for_acq**2 - corr_factor**2
      phys_emit = sigma_corr_squared / beta_f
      norm_emit  = phys_emit*gamma

      emit_array.append(norm_emit)

      mean_emit = np.mean(norm_emit)
      std_emit = np.std(norm_emit)

      mean_emit_array.append(mean_emit)
      std_emit_array.append(std_emit)

    bunch_dict['Emit_Array'] = np.asarray(emit_array)
    bunch_dict['Mean_Emit'] = np.asarray(mean_emit_array)
    bunch_dict['Std.Dev_Emit'] = np.asarray(std_emit_array) 
      
  
    processed_dict[bunch] = bunch_dict

  return processed_dict

final_dict = process_dict(all_dict,1)

def multiple_acq(all_dict,num_of_acq = 50):
  moving_average_dict = {}
  for bunch_num in all_dict.keys():
    bunch_dict = {}
    times = []
    emits = []
    stds = []
    for i in np.arange(0,len(all_dict[bunch_num]['Timestamps'])-num_of_acq,1):
      all_time_array = all_dict[bunch_num]['Timestamps'][i:i+num_of_acq]
      all_emit_array = np.concatenate(all_dict[bunch_num]['Emit_Array'][i:i+num_of_acq],axis=0)

      mean_time = np.mean(all_time_array)
      mean_emit = np.mean(all_emit_array)
      std_emit = np.std(all_emit_array)

      times.append(mean_time)
      emits.append(mean_emit)
      stds.append(std_emit)
    

    times = np.asarray(times)
    emits = np.asarray(emits)
    stds = np.asarray(stds)
    bunch_dict['Timestamps']=(times- lt(gate_start_time))/60.
    bunch_dict['Mean_Emit']=emits
    bunch_dict['Std.Dev_Emit']=stds
    moving_average_dict[bunch_num]=bunch_dict
  return moving_average_dict

moving_avg_dict = multiple_acq(final_dict)


for bunch_to_plot in moving_avg_dict.keys()[10:30]:
#for bunch_to_plot in [1621,1622,1623,1624]:

  fig = plt.figure()
  plt.title('Fill {:d}, Bunch {:d}, Time since: {:s}'.format(filln,bunch_to_plot,gate_start_time))
  plt.xlabel('Time [minutes]')
  plt.ylabel('Emit_{:s}'.format(plane))
  plt.plot(moving_avg_dict[bunch_to_plot]['Timestamps'],moving_avg_dict[bunch_to_plot]['Mean_Emit'] + moving_avg_dict[bunch_to_plot]['Std.Dev_Emit'],'g',label='Std. Deviation')
  plt.plot(moving_avg_dict[bunch_to_plot]['Timestamps'],moving_avg_dict[bunch_to_plot]['Mean_Emit'] - moving_avg_dict[bunch_to_plot]['Std.Dev_Emit'],'g')
  plt.plot(moving_avg_dict[bunch_to_plot]['Timestamps'],moving_avg_dict[bunch_to_plot]['Mean_Emit'],'b',label='Mean')
  plt.legend(frameon=False)

plt.show()

  
'''
Fill 4038, 4284, 4290, 4291
def emittance_dictionary():
  e_dict = {'betaf_h':{}, 'betaf_v':{}, 'gamma':{},
              'sigma_corr_h':{}, 'sigma_corr_v':{}}
  e_dict['betaf_h'][450] = {1:203.47, 2:200.73}
  e_dict['betaf_v'][450] = {1:317.45, 2:327.75}
  e_dict['betaf_h'][6500] = {1:204.1, 2:191.5}
  e_dict['betaf_v'][6500] = {1:322.7, 2:395}
  e_dict['gamma'][450] = 479.6
  e_dict['gamma'][6500] = 6927.6
  e_dict['sigma_corr_h'][450] = 0.85
  e_dict['sigma_corr_v'][450] = 0.87
  e_dict['sigma_corr_h'][6500] = {1:0.37, 2:0.336}
  e_dict['sigma_corr_v'][6500] = {1:0.3, 2:0.36} 

  return e_dict

---------------------------------------------------
Fill 4038

'''


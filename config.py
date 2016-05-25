import os
class cf:
  def __init__(self):
    self.t1 = '2016-05-17 13:08:00.000'
    self.t2 = '2016-05-17 13:20:00.000'

    self.filln = 4937
    self.tag = ''
    self.output_path = os.path.join('/afs/cern.ch/work/l/lcarver/public/Instability_Data','{:d}{:s}'.format(self.filln, self.tag))

    #For SUSSIX
    self.q1 = 0.27
    self.q2 = 0.295
    #
